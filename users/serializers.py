from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group

class permission_serializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("name", "codename")
        # exclude = ('id',)
        # fields = "__all__"

class group_serializer(serializers.ModelSerializer):
    permissions = permission_serializer(many=True)
    class Meta:
        model = Group
        # fields = ("name", "codename")
        exclude = ('id',)
        # fields = "__all__"

class simple_user_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)

class user_serializer(serializers.ModelSerializer):
    user_permissions = permission_serializer(many=True, read_only=True)
    groups = group_serializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "user_permissions", "groups")
        # exclude = ('id',)