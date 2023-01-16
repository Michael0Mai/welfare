from rest_framework import serializers
from pic.models import *
# from users.serializers import simple_user_serializer
from django.contrib.auth.models import User

class beauty_serializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # liker = serializers.SlugRelatedField(queryset=User.objects.all(), many=True, slug_field='username')
    liker_count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    class Meta:
        model = beauty
        exclude = ("liker",)
        # fields = "__all__"
        read_only_fields = ('created_time', 'owner', 'address_web')
        # read_only_fields = ('created_time', 'owner', 'liker', 'address_web')

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

class beauty_address_only_serializer(serializers.ModelSerializer):
     class Meta:
        model = beauty
        fields = ('address_web',)
        read_only_fields = ('address_web',)

class beauty_serializer_add_like(serializers.ModelSerializer):
    pic_id = serializers.UUIDField()
    class Meta:
        model = beauty
        fields =  ("pic_id",)

class beauty_serializer_manager(beauty_serializer):
    class Meta(beauty_serializer.Meta):
        exclude = ("liker",)
        read_only_fields = ('created_time', 'owner', 'address_web', 'remark')

# class beauty_serializer_manager(serializers.ModelSerializer):
#     class Meta:
#         model = beauty
#         # exclude = ("liker",)
#         # read_only_fields = ('created_time', 'owner', 'address_web', 'remark')
#         fields = "__all__"

class create_beauty_serializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = beauty
        # fields = "__all__"
        exclude = ("liker", "created_time", "is_delete")

#----------------------------------------------------------------------------------------

class beauty_local_serializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # liker = serializers.SlugRelatedField(queryset=User.objects.all(), many=True, slug_field='username')
    liker_count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    file_path = serializers.ImageField()
    class Meta:
        model = beauty_local
        exclude = ("liker",)
        # fields = "__all__"
        read_only_fields = ('created_time', 'owner', 'file_path')
        # read_only_fields = ('created_time', 'owner', 'liker', 'address_web')

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

class beauty_local_serializer_add_like(serializers.ModelSerializer):
    pic_id = serializers.UUIDField()
    class Meta:
        model = beauty_local
        fields =  ("pic_id",)

class beauty_local_serializer_manager(beauty_local_serializer):
    class Meta(beauty_local_serializer.Meta):
        exclude = ("liker",)
        read_only_fields = ('created_time', 'owner', 'file_path', 'remark')


class create_beauty_local_serializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = beauty_local
        # fields = "__all__"
        exclude = ("liker", "created_time", "is_delete")

class beauty_local_path_only_serializer(serializers.ModelSerializer):
     class Meta:
        model = beauty_local
        fields = ('file_path',)
        read_only_fields = ('file_path',)

# class liker_only_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = beauty
#         fields = ("id", "liker",)
