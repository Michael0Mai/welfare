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

class beauties(viewsets.ModelViewSet):
    queryset =  beauty.objects.all()
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
        page = request.GET.get('page') # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        try:
            pic_list = paginator.page(page)
        except PageNotAnInteger: # 如果请求的页数不是整数, 返回第一页。
            pic_list = paginator.page(1)
        except InvalidPage: # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage: # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            pic_list = paginator.page(paginator.num_pages)
    return render(request, 'beauty_pic_list.html', {"pic_list": pic_list})


@csrf_exempt
def add_like(request):
    if request.method != 'GET':
        res = {"detail": "只允许 “GET” 方法。", "status_code": 405}
    else:       
        pic_id = request.GET.get('id')
        if not check_uuid4(pic_id):
            res = {'id':"输入不是有效的 UUID", "status_code": 400}
        else:
            JWT_authenticator = JWTAuthentication()
            try: # 检查 token，只能合法注册用户点赞
                user, token = JWT_authenticator.authenticate(request) # 拿到 user 和 token
                had_liked = beauty.objects.values('liker').filter(Q(id=pic_id) & ~Q(liker__id__contains=TokenUser(token).id)).exists() # 同时检查图片存在和是否已经赞过
                if had_liked: # 未赞过
                    like_pic = beauty.objects.filter(id=pic_id).first()
                    like_pic.liker.add(user)
                    res = {"detail": "点赞成功。", "status_code": 200}
                else:
                    res = {"detail": "图片不存在 or 已经赞过了。", "status_code": 404}
            except:
                res = {"detail": "未登录", "status_code": 401}
    
    return HttpResponse(
            json.dumps(res, ensure_ascii=False),
            content_type="application/json,charset=utf-8"
            )

def check_uuid4(test_uuid):
    try:
        return uuid.UUID(test_uuid).version
    except ValueError:
        return False