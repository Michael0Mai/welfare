from django_filters import rest_framework as filters
from django.contrib.auth.models import User

class user_filter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            "id": ['exact'],
            "username": ['icontains'],
        }