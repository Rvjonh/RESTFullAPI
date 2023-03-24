from rest_framework import serializers
from tasks.models import TaskModel
from django.contrib.auth import get_user_model

MyUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("email", "password")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def validate(self, data):
        if MyUser.objects.filter(username=data["email"]).exists():
            raise serializers.ValidationError(
                {"Error": f'{data["email"]} already registered'}
            )
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = MyUser(**validated_data)
        user.username = validated_data.pop("email")
        user.set_password(password)
        user.save()
        return user


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
