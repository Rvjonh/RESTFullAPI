from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = "Creates a superuser."

    def handle(self, *args, **options):
        myUserModel = get_user_model()

        if not myUserModel.objects.filter(
            username=os.getenv("ADMIN_USERNAME")
        ).exists():
            myUserModel.objects.create_superuser(
                username=os.getenv("ADMIN_USERNAME"),
                password=os.getenv("ADMIN_PASSWORD"),
            )
        print("Superuser has been created.")
