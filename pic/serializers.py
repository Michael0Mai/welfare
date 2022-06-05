from rest_framework import serializers
from pic.models import *
from users.serializers import simple_user_serializer
from django.contrib.auth.models import User

class beauty_serializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    liker = serializers.SlugRelatedField(queryset=User.objects.all(), many=True, slug_field='username')
    liker_count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    class Meta:
        model = beauty
        # exclude = ("liker",)
        fields = "__all__"
        read_only_fields = ('created_time',)

    def get_liker_count(self, obj):
        return obj.liker.count()
    def get_is_like(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user in obj.liker.all():
                return True
            else:
                return False

# 第二种写法
# class beauty_serializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#     liker = serializers.SlugRelatedField(queryset=User.objects.all(), many=True, slug_field='username')
#     class Meta:
#         model = beauty
#         # exclude = ("liker",)
#         fields = "__all__"

#     def to_representation(self, value):
#         data = super().to_representation(value) # 调用父类获取当前序列化数据，value代表每个对象实例ob
#         data['liker_count'] = value.liker.count() # 对序列化数据做修改，添加新的数据
#         user = None
#         request = self.context.get("request")
#         if request and hasattr(request, "user"):
#             user = request.user
#             if user in value.liker.all():
#                 data['is_like'] = True
#             else:
#                 data['is_like'] =False
#         return data

class create_beauty_serializer(serializers.ModelSerializer):
    class Meta:
        model = beauty
        # fields = "__all__"
        exclude = ("liker",)

# class liker_only_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = beauty
#         fields = ("id", "liker",)
