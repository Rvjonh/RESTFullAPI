from django.urls import path

from .views import SignUpUser

urlpatterns = [
    path("signup/", SignUpUser.as_view(), name="signup"),
]
