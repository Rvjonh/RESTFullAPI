from django.contrib.auth import get_user_model
from django.urls import reverse
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from tasks.models import TaskModel

from apiv1.serializers import TaskModelSerializer

MyUser = get_user_model()


class TaskModelTest(APITestCase):
    """Task model with user and credentials 'Token'"""

    def setUp(self) -> None:
        self.test_user_data = {
            "username": "jonh@gmail.com",
            "email": "jonh@gmail.com",
            "password": "jonhpassword",
        }

        self.test_user = MyUser.objects.create(
            username=self.test_user_data["username"],
            email=self.test_user_data["email"],
            password=self.test_user_data["password"],
        )

        self.test_user_token = Token.objects.create(user=self.test_user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.test_user_token.key)

    def test_api_create_task(self):
        """Create a task in the database with user"""
        url = reverse("tasks-list")
        data = {"title": "my task test", "description": "my task's description test"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskModel.objects.count(), 1)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["title"], "my task test")
        self.assertEqual(response.data["description"], "my task's description test")
        self.assertEqual(response.data["user"], 1)

    def test_api_create_task_required_fields(self):
        """Require title and description fields"""
        url = reverse("tasks-list")

        # data empty
        data = {}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "title": ["This field is required."],
                "description": ["This field is required."],
            },
        )

        # None fields entered
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "title": ["This field is required."],
                "description": ["This field is required."],
            },
        )

        # only title field entered
        data = {"title": "only title"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"description": ["This field is required."]})

        # description title field entered
        data = {"description": "only description"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"title": ["This field is required."]})

    def test_api_get_tasks(self):
        """Get user's tasks"""
        task1 = TaskModel.objects.create(
            user=self.test_user, title="first title", description="first description"
        )
        task2 = TaskModel.objects.create(
            user=self.test_user, title="second title", description="second description"
        )
        task3 = TaskModel.objects.create(
            user=self.test_user, title="third title", description="third description"
        )

        url = reverse("tasks-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # first task added
        self.assertEqual(response.data[0]["title"], task1.title)
        self.assertEqual(response.data[0]["description"], task1.description)
        self.assertEqual(response.data[0]["user"], task1.user.id)
        # Second task added
        self.assertEqual(response.data[1]["title"], task2.title)
        self.assertEqual(response.data[1]["description"], task2.description)
        self.assertEqual(response.data[1]["user"], task2.user.id)
        # Third task added
        self.assertEqual(response.data[2]["title"], task3.title)
        self.assertEqual(response.data[2]["description"], task3.description)
        self.assertEqual(response.data[2]["user"], task3.user.id)

    def test_api_get_task_individual(self):
        """Get an individual task from the user"""
        task_test = TaskModel.objects.create(
            user=self.test_user, title="my title", description="my description"
        )

        url = reverse("tasks-detail", args=[task_test.id])

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.test_user.id)
        self.assertEqual(response.data["title"], task_test.title)
        self.assertEqual(response.data["description"], task_test.description)

    def test_api_update_task(self):
        """Update task with of user"""
        task_test = TaskModel.objects.create(
            user=self.test_user, title="title", description="description"
        )

        url = reverse("tasks-detail", args=[task_test.id])

        data = {"title": "NEW TITLE", "description": "NEW DESCRIPTION"}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["description"], data["description"])

    def test_api_update_task_required_fields(self):
        """Required fields to update"""
        task_test = TaskModel.objects.create(
            user=self.test_user, title="title", description="description"
        )

        url = reverse("tasks-detail", args=[task_test.id])

        data = {}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "title": ["This field is required."],
                "description": ["This field is required."],
            },
        )

        data = None
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "title": ["This field is required."],
                "description": ["This field is required."],
            },
        )

        data = {"title": "This field is filled."}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"description": ["This field is required."]})

        data = {"description": "This field is filled."}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"title": ["This field is required."]})

    def test_api_delete_task(self):
        """Required fields to update"""
        task_test = TaskModel.objects.create(
            user=self.test_user, title="title", description="description"
        )

        url = reverse("tasks-detail", args=[task_test.id])

        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
