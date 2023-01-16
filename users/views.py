from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.db.models import Q
from django.contrib.auth.models import User
# from django.contrib.auth.models import Permission
from users.serializers import *
from users.filters import *
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password, make_password
from pic.serializers import beauty_address_only_serializer, beauty_local_path_only_serializer

class users(viewsets.ModelViewSet):
    queryset =  User.objects.filter(~Q(is_superuser = 1)).all()
    filter_class = user_filter
    permission_classes = (permissions.IsAdminUser,)
    tags = ['用户管理']
    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return user_serializer_update
        elif self.action == 'create':
            return user_serializer_create
        else:
            return user_serializer

@method_decorator(name = "retrieve", decorator=swagger_auto_schema(auto_schema=None,),) # 隐藏详细信息接口
@method_decorator(name = "list", decorator=swagger_auto_schema(auto_schema=None,),)
@method_decorator(name = "destroy", decorator=swagger_auto_schema(auto_schema=None,),)
@method_decorator(name = "update", decorator=swagger_auto_schema(auto_schema=None,),)
@method_decorator(name = "partial_update", decorator=swagger_auto_schema(auto_schema=None,),)
@method_decorator(name = "create", decorator=swagger_auto_schema(operation_description="用户注册，无需权限",),)
class create_user(viewsets.ModelViewSet):
    serializer_class = user_serializer_create
    queryset = User.objects.filter(~Q(is_superuser = 1)).all()
    tags = ['新用户注册']
    def perform_create(self, serializer):
        serializer.save(is_active = False)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})

@method_decorator(name="retrieve", decorator=swagger_auto_schema(auto_schema=None,),) # 隐藏详细信息接口
@method_decorator(name = "list", decorator=swagger_auto_schema(operation_description="查看当前用户信息",),)
class current_user(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    tags = ['当前用户']
    def get_queryset(self):
        queryset =  User.objects.all().filter(id = self.request.user.id)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return user_serializer
        elif self.action == "had_liked":
            return user_serializer_had_liked
        else:
            return user_serializer_change_password
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})
    
    @action(methods=['post'], detail=False, url_path="change_password", permission_classes = (permissions.IsAuthenticated,))
    def change_password(self, request, *args, **kwargs):
        try:
            user_obj =  User.objects.get(id = self.request.user.id)
            serializer = user_serializer_change_password(data=request.data)
            serializer.is_valid(raise_exception=True)
            password = serializer.validated_data['password']
            new_password = serializer.validated_data['new_password']
            if check_password(password, user_obj.password):
                user_obj.password = make_password(new_password)
                user_obj.save()
                return Response(status=status.HTTP_201_CREATED, data={"detail": "密码修改成功"})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={"detail": "账号或密码错误"})
        # 未知错误，报服务器内部错误
        except Exception as error:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"detail": "服务器内部错误"})
    
    @action(methods=['get'], detail=False, url_path="had_liked", permission_classes = (permissions.IsAuthenticated,))
    def had_liked(self, request, *args, **kwargs):
        queryset = User.objects.filter(id = self.request.user.id)
        liked_pic = user_serializer_had_liked(instance=queryset ,many=True)
        return Response(liked_pic.data)


# class permission(viewsets.ReadOnlyModelViewSet):
#     queryset =  Permission.objects.all()
#     # permission_classes = (permissions.IsAdminUser,)
#     pagination_class = None
#     def get_serializer_class(self):
#         return permission_serializer



  
    