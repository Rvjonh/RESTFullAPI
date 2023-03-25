from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

myUserModel = get_user_model()


class Command(BaseCommand):
    help = "Creates a superuser."

    def handle(self, *args, **options):
        if not myUserModel.objects.filter(os.getenv("ADMIN_USERNAME")).exists():
            myUserModel.objects.create_superuser(
                username=os.getenv("ADMIN_USERNAME"),
                password=os.getenv("ADMIN_PASSWORD"),
            )
        print("Superuser has been created.")
