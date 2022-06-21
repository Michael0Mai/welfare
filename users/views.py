from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.auth.models import User
# from django.contrib.auth.models import Permission
from users.serializers import *
from rest_framework import viewsets, permissions
from users.filters import *

class users(viewsets.ModelViewSet):
    queryset =  User.objects.filter(~Q(is_superuser = 1)).all()
    filter_class = user_filter
    permission_classes = (permissions.IsAdminUser,)
    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return user_serializer_update
        elif self.action == 'create':
            return user_serializer_create
        else:
            return user_serializer

class create_user(viewsets.ModelViewSet):
    serializer_class = user_serializer_create
    queryset = User.objects.filter(~Q(is_superuser = 1)).all()
    def perform_create(self, serializer):
        serializer.save(is_active = False)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



class current_user(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        queryset =  User.objects.all().filter(id = self.request.user.id)
        # queryset =  self.request.user.id
        return queryset
    # filter_class = user_filter
    pagination_class = None
    # permission_classes = permissions.IsAuthenticated
    def get_serializer_class(self):
        return user_serializer
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

# class permission(viewsets.ReadOnlyModelViewSet):
#     queryset =  Permission.objects.all()
#     # permission_classes = (permissions.IsAdminUser,)
#     pagination_class = None
#     def get_serializer_class(self):
#         return permission_serializer



  
    