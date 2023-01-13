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

class user_serializer(simple_user_serializer, serializers.HyperlinkedModelSerializer):
    user_permissions = permission_serializer(many=True, read_only=True)
    groups = group_serializer(many=True, read_only=True)
    class Meta(simple_user_serializer.Meta):
        fields = ("id", "url", "username", "first_name", "last_name", "user_permissions", "groups")
        # exclude = ('id',)

class user_serializer_change_password(simple_user_serializer):
    new_password = serializers.CharField()
    class Meta(simple_user_serializer.Meta):
        fields = ("id", "username", "new_password", "password", "is_active")
        write_only_fields = ("password", "new_password")
        read_only_fields = ("id", "username", "is_active")

class user_serializer_update(serializers.ModelSerializer):
    user_permissions = permission_serializer(many=True, read_only=True)
    groups = serializers.SlugRelatedField(queryset=Group.objects.all(), many=True, slug_field='name')
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ('password',)
        read_only_fields = ('date_joined', 'last_login', 'is_superuser')

class user_serializer_create(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ("username", "password", "is_active")
        write_only_fields = ("password", "is_active")
    
    def create(self, validated_data):
        user = super(user_serializer_create, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user