from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from tasks.models import TaskModel

from .serializers import TaskModelSerializer, UserSerializer
from .permissions import IsAuthor

# Create your views here.

MyUser = get_user_model()  # CustomUser model to make references


class SignUpUser(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response(
            {"token": token.key}, status=status.HTTP_201_CREATED, headers=headers
        )


# Create your views here.
class EmailSenderView(TemplateView):
    template_name = "password_reset_confirm.html"


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthor,)
    serializer_class = TaskModelSerializer

    def get_queryset(self):
        item = TaskModel.objects.filter(user=self.request.user)
        return item

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
