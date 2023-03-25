from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
import copy

# Create your tests here.

MyUser = get_user_model()


class CustomUserSignUpTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_user(username="", email="", password=""):
        if username != "" and email != "" and password != "":
            MyUser.objects.create_user(
                username=username, email=email, password=password
            )

    def test_create_user_with_model(self):
        """
        Ensure we can create a new account object.
        """
        new_user = self.create_user(
            username="testuser1@gmail.com",
            email="testuser1@gmail.com",
            password="testuser123",
        )
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(MyUser.objects.get().email, "testuser1@gmail.com")

    def test_create_user_with_api(self):
        """Create a user with signup url"""
        url = reverse("signup")
        data = {"email": "testuser2@gmail.com", "password": "testpass2"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(MyUser.objects.get().username, data["email"])
        self.assertEqual(MyUser.objects.get().email, data["email"])

    def test_create_user_requires_fields(self):
        """signup will require email and password fields"""
        url = reverse("signup")
        data = {"email": "", "password": ""}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MyUser.objects.count(), 0)

    def test_create_user_requires_json(self):
        """signup will require and json with email and password fields"""
        url = reverse("signup")
        data = {}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MyUser.objects.count(), 0)


class CustomUserLoginTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_user(username="", email="", password=""):
        if username != "" and email != "" and password != "":
            return MyUser.objects.create_user(
                username=username, email=email, password=password
            )
        return None

    def setUp(self):
        self.user1 = self.create_user(
            username="test_user1@gmail.com",
            email="test_user1@gmail.com",
            password="testprof1",
        )

    def test_login_with_api(self):
        """Register user and check for their key"""
        url = reverse("rest_login")
        data = {"email": "test_user1@gmail.com", "password": "testprof1"}

        response = self.client.post(url, data, format="json")
        my_user_checker = MyUser.objects.get(email=data["email"])
        token_my_user_checker = Token.objects.get(user=my_user_checker)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_dict = {"token": token_my_user_checker.key}
        self.assertDictContainsSubset(expected_dict, response.data)

    def test_required_fields(self):
        """Can login without email and password fields"""
        url = reverse("rest_login")

        # and empty json is sent
        data = {}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # and password missing
        data = {"email": "test_user1@gmail.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # and email missing
        data = {"password": "testprof1"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # None data was sent
        data = None
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CustomUserLogoutTest(APITestCase):
    client = APIClient()

    def setUp(self) -> None:
        self.myUser = MyUser.objects.create_user(
            username="emailtest1@gmail.com",
            email="emailtest1@gmail.com",
            password="emailpassword",
        )
        self.myUserToken = Token.objects.create(user=self.myUser)

    def test_login_and_logout(self):
        url = reverse("rest_login")
        data = {"email": self.myUser.email, "password": "emailpassword"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_dict = {"token": self.myUserToken.key}
        self.assertDictContainsSubset(expected_dict, response.data)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.myUserToken.key)

        url = reverse("rest_logout")
        request = self.client.post(url)

        self.assertEqual(request.status_code, status.HTTP_200_OK)


class CustomUserChangePassword(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user_data = {"email": "emailtest1@gmail.com", "password": "emailpassword"}
        self.myUser = MyUser.objects.create_user(
            username=self.user_data["email"],
            email=self.user_data["email"],
            password=self.user_data["password"],
        )
        self.myUserToken = Token.objects.create(user=self.myUser)

    def test_user_password_change(self):
        """Change password with credencials 'token' succsessfully"""
        url = reverse("rest_password_change")
        data = {
            "old_password": self.user_data["password"],
            "new_password1": "mynewpassword",
            "new_password2": "mynewpassword",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.myUserToken.key)
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {"detail": "New password has been saved."})

    def test_user_password_change_without_AUTHORIZATION(self):
        """Change password without credencials 'token'"""
        url = reverse("rest_password_change")
        data = {
            "old_password": self.user_data["password"],
            "new_password1": "mynewpassword",
            "new_password2": "mynewpassword",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_password_change_with_wrong_old_password(self):
        """Change password with credencials 'token' succsessfully but old password incorrect"""
        url = reverse("rest_password_change")
        data = {
            "old_password": "fakepassword",
            "new_password1": "mynewpassword",
            "new_password2": "mynewpassword",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.myUserToken.key)
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_required_fields_password_change(self):
        """All fields are required"""
        url = reverse("rest_password_change")
        data = {}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.myUserToken.key)
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        erro_msj = {
            "old_password": ["This field is required."],
            "new_password1": ["This field is required."],
            "new_password2": ["This field is required."],
        }
        self.assertDictEqual(response.data, erro_msj)

    def test_required_fields_and_password_not_correct(self):
        """Password is not correct and new_password fields are required"""
        url = reverse("rest_password_change")
        data = {
            "old_password": self.user_data["password"],
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.myUserToken.key)
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CustomUserResetPassword(APITestCase):
    client = APIClient()

    def setUp(self) -> None:
        self.myUser = MyUser.objects.create_user(
            username="emailtest1@gmail.com",
            email="emailtest1@gmail.com",
            password="emailpassword",
        )

    def test_email_sent(self):
        """Test Email sent to change password"""
        url = "/api/v1/rest-auth/password/reset/"
        data = {"email": "emailtest1@gmail.com"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["detail"], "Password reset e-mail has been sent."
        )

    def test_email_sent_without_email(self):
        url = "/api/v1/rest-auth/password/reset/"

        data = {"email": ""}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = None
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
