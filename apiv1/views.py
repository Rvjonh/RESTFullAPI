from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets

from tasks.models import TaskModel

from .serializers import TaskModelSerializer
from .permissions import IsAuthor
from rest_framework import permissions


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
