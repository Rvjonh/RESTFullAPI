from dj_rest_auth.serializers import PasswordResetSerializer


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        return {
            "email_template": "email/account/user_password_reset",
            "client_app": "hijos de puta",
            "current_site": "current_site.com",
        }
