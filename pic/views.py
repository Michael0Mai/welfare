from pymysql import NULL
import json
from pic.models import *
from pic.serializers import *
from pic.filters import *
from rest_framework import viewsets, permissions
from pic.permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.models import TokenUser
from django.db.models import Q
import uuid
from rest_framework.response import Response
from rest_framework import status

class beauties(viewsets.ModelViewSet):
    queryset =  beauty.objects.all().filter(is_delete=False)
    filter_class = beauty_filter
    # permission_classes = (permissions.DjangoModelPermissions, IsOwnerOrReadOnly)
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
    def get_serializer_class(self):
        if self.action == "create":
            return create_beauty_serializer
        else:
            return beauty_serializer
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

class beauties_manager(viewsets.ModelViewSet):
    queryset =  beauty.objects.all()
    filter_class = beauty_filter
    permission_classes = (permissions.IsAdminUser,)
    def get_serializer_class(self):
        return beauty_serializer_manager
    
    # def list(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    # def retrieve(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# class beauties(viewsets.ModelViewSet):
#     filter_class = beauty_filter
#     # permission_classes = (permissions.DjangoModelPermissions, IsOwnerOrReadOnly)
#     permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
#     def get_queryset(self):
#         queryset =  beauty.objects.all()
#         # for i in queryset:
#         #     i.liker_count = 3
#             # print(i.liker)
#         return queryset
#     def get_serializer_class(self):
#         # print(self.request.user.id)
#         # if self.action == "create" or self.action == "update":
#         if self.action == "create":
#             return create_beauty_serializer
#         else:
#             return beauty_serializer
#     def perform_create(self, serializer):
#         serializer.save(owner = self.request.user)

def beauties_list(request):
    list = beauty.objects.all().filter(is_delete=False)
    paginator = Paginator(list, 10)
    if request.method == "GET": 
        page = request.GET.get('page') # ?????? url ????????? page ????????????, ??????????????? page ??????, ???????????? 1
        try:
            pic_list = paginator.page(page)
        except PageNotAnInteger: # ?????????????????????????????????, ??????????????????
            pic_list = paginator.page(1)
        except InvalidPage: # ??????????????????????????????, ???????????????
            return HttpResponse('????????????????????????')
        except EmptyPage: # ????????????????????????????????????????????????????????????????????????????????????
            pic_list = paginator.page(paginator.num_pages)
    return render(request, 'beauty_pic_list.html', {"pic_list": pic_list})


@csrf_exempt
def add_like(request):
    if request.method != 'GET':
        res = {"detail": "????????? ???GET??? ?????????", "status_code": 405}
    else:       
        pic_id = request.GET.get('id')
        if not check_uuid4(pic_id):
            res = {'id':"????????????????????? UUID", "status_code": 400}
        else:
            JWT_authenticator = JWTAuthentication()
            try: # ?????? token?????????????????????????????????
                user, token = JWT_authenticator.authenticate(request) # ?????? user ??? token
                had_liked = beauty.objects.values('liker').filter(Q(id=pic_id) & ~Q(liker__id__contains=TokenUser(token).id)).exists() # ?????????????????????????????????????????????
                if had_liked: # ?????????
                    like_pic = beauty.objects.filter(id=pic_id).first()
                    like_pic.liker.add(user)
                    res = {"detail": "???????????????", "status_code": 200}
                else:
                    res = {"detail": "??????????????? or ??????????????????", "status_code": 404}
            except:
                res = {"detail": "?????????", "status_code": 401}
    
    return HttpResponse(
            json.dumps(res, ensure_ascii=False),
            content_type="application/json,charset=utf-8"
            )

def check_uuid4(test_uuid):
    try:
        return uuid.UUID(test_uuid).version
    except ValueError:
        return False