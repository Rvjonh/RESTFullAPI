from django.shortcuts import render
from django.views.generic import TemplateView
from dj_rest_auth.views import PasswordResetView


# Create your views here.
class EmailSenderView(TemplateView):
    template_name = "password_reset_confirm.html"
