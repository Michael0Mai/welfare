from django_filters import rest_framework as filters
from video.models import *

class video_local_filter(filters.FilterSet):
    class Meta:
        model = video_local
        fields = {
            "is_delete": ['exact'],
            "owner": ['exact'],
        }