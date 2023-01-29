from rest_framework import serializers
from video.models import *
from django.contrib.auth.models import User

#----------------------------------------------------------------------------------------

class video_local_serializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    liker_count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    file_path = serializers.ImageField()
    class Meta:
        model = video_local
        exclude = ("liker",)
        read_only_fields = ('created_time', 'owner', 'file_path')

    def get_liker_count(self, obj): # 加入字段  liker_count
        return obj.liker.count()
    def get_is_like(self, obj): # 加入字段  is_like
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user in obj.liker.all():
                return True
            else:
                return False

class video_local_serializer_add_like(serializers.ModelSerializer):
    video_id = serializers.UUIDField()
    class Meta:
        model = video_local
        fields =  ("video_id",)

class video_local_serializer_manager(video_local_serializer):
    class Meta(video_local_serializer.Meta):
        exclude = ("liker",)
        read_only_fields = ('created_time', 'owner', 'file_path', 'remark')


class create_video_local_serializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = video_local
        exclude = ("liker", "created_time", "is_delete")

class video_local_path_only_serializer(serializers.ModelSerializer):
     class Meta:
        model = video_local
        fields = ('file_path',)
        read_only_fields = ('file_path',)
