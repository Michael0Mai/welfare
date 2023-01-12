from django_filters import rest_framework as filters
from pic.models import *

class beauty_filter(filters.FilterSet):
    class Meta:
        model = beauty
        fields = {
            "is_delete": ['exact'],
            "address_web": ['exact'],
            "owner": ['exact'],
        }

class beauty_local_filter(filters.FilterSet):
    class Meta:
        model = beauty_local
        fields = {
            "is_delete": ['exact'],
            "owner": ['exact'],
        }