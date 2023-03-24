from rest_framework import serializers
from tasks.models import TaskModel


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "title",
            "description",
            "user",
            "created_at",
            "updated_at",
        )
        model = TaskModel
        read_only_fields = ("user",)
        extra_kwargs = {
            "user": {"read_only": True},
        }
