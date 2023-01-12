from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.auth.models import User
# from django.contrib.auth.models import Permission
from users.serializers import *
from rest_framework import viewsets, permissions
from users.filters import *
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

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
    tags = ['当前用户']
    def get_queryset(self):
        queryset =  User.objects.all().filter(id = self.request.user.id)
        return queryset
    pagination_class = None

    def get_serializer_class(self):
        return user_serializer
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})

# class permission(viewsets.ReadOnlyModelViewSet):
#     queryset =  Permission.objects.all()
#     # permission_classes = (permissions.IsAdminUser,)
#     pagination_class = None
#     def get_serializer_class(self):
#         return permission_serializer



  
    