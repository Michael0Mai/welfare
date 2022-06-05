from django.contrib.auth.models import User
# from django.contrib.auth.models import Permission
from users.serializers import *
from rest_framework import viewsets, permissions
from users.filters import *

class users(viewsets.ReadOnlyModelViewSet):
    queryset =  User.objects.all()
    filter_class = user_filter
    permission_classes = (permissions.IsAdminUser,)
    def get_serializer_class(self):
        return user_serializer


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

# class permission(viewsets.ReadOnlyModelViewSet):
#     queryset =  Permission.objects.all()
#     # permission_classes = (permissions.IsAdminUser,)
#     pagination_class = None
#     def get_serializer_class(self):
#         return permission_serializer



  
    