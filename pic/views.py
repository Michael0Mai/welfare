from pic.models import *
from pic.serializers import *
from pic.filters import *
from rest_framework import viewsets, permissions, status
from pic.permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from pic.utils import img_proccess_save
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

# from django.views.decorators.csrf import csrf_exempt
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.models import TokenUser
# import json
# import uuid
# from pymysql import NULL

class beauties(viewsets.ModelViewSet):
    queryset =  beauty.objects.all().filter(is_delete=False)
    filter_class = beauty_filter
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly) # 只能修改自己的东西，superuser也不能改别人的东西
    tags = ['图片网址']

    def get_serializer_class(self):
        if self.action == "create":
            return create_beauty_serializer
        elif self.action == 'add_like':
            return beauty_serializer_add_like
        else:
            return beauty_serializer
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)
    
    @action(methods=['get'], detail=False, url_path="address_web")
    def address_web(self, request, *args, **kwargs): # 文件下载,访问 http://xx.xx.xx.xx:8000/....../[id]/download/ 链接，即可直接下载
        queryset = self.queryset
        serializer = beauty_address_only_serializer(instance=queryset, many=True)
        return Response(serializer.data)
    
    # @action(methods=['post'], detail=False, url_path="add_like", permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,))
    # def add_like(self, request, *args, **kwargs):      
    #     serializer = beauty_serializer_add_like(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     pic_id = serializer.validated_data['pic_id']
    #     had_liked = beauty.objects.values('liker').filter(Q(id=pic_id) & ~Q(liker__id__contains=self.request.user.id)).exists() # 同时检查图片存在和是否已经赞过
    #     if had_liked: 
    #         pic_obj = beauty.objects.get(id=pic_id)
    #         pic_obj.liker.add(self.request.user.id)
    #         pic_obj.save()
    #         return Response(status=status.HTTP_200_OK, data={"detail": "点赞成功。", "status_code": 200})
    #     else:
    #         return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "图片 ID 不正确 or 已经赞过了。"})

    @action(methods=['get'], detail=True, url_path="add_like", permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,))
    def add_like(self, request, pk, *args, **kwargs):      
        pic_obj = self.get_object()
        if self.request.user not in pic_obj.liker.all():         
            pic_obj.liker.add(self.request.user)
            pic_obj.save()
            return Response(status=status.HTTP_200_OK, data={"detail": "点赞成功。", "status_code": 200})
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "已经赞过了"})

    # @action(methods=['get', 'delete', 'patch'], detail=True, url_path="manager")
    # def manager(self, request, pk, *args, **kwargs):
    #     queryset =  beauty.objects.all().filter(id=pk)
    #     # permission_classes = (permissions.IsAdminUser,)
    #     serializer = beauty_serializer_manager(instance=queryset, many=True)
    #     return Response(serializer.data)


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

# @method_decorator(name = "retrieve", decorator=swagger_auto_schema(auto_schema=None,),) # 隐藏详细信息接口
@method_decorator(name = "list", decorator=swagger_auto_schema(auto_schema=None,),)
@method_decorator(name = "create", decorator=swagger_auto_schema(auto_schema=None,),)
@method_decorator(name = "update", decorator=swagger_auto_schema(auto_schema=None,),)
@method_decorator(name = "partial_update", decorator=swagger_auto_schema(auto_schema=None,),)
# @method_decorator(name = "destroy", decorator=swagger_auto_schema(operation_description="只有删除操作",),)
class beauties_manager(viewsets.ModelViewSet): # superuser 用来看和删除单张图片
    queryset =  beauty.objects.all()
    filter_class = beauty_filter
    permission_classes = (permissions.IsAdminUser,)
    tags = ['图片网址管理']

    def get_serializer_class(self):
        return beauty_serializer_manager
    
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})
    # def retrieve(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})

#-----------------------------------------------------------------------------------

class beauties_local(viewsets.ModelViewSet):
    queryset =  beauty_local.objects.all().filter(is_delete=False)
    filter_class = beauty_local_filter
    # permission_classes = (permissions.DjangoModelPermissions, IsOwnerOrReadOnly)
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
    tags = ['本地图片']

    def get_serializer_class(self):
        if self.action == "create":
            return create_beauty_local_serializer
        elif self.action == "add_like":
            return beauty_local_serializer_add_like
        else:
            return beauty_local_serializer
    def perform_create(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['file_path']
        img_file = str(self.request.user) # 图片存储的文件夹
        img_name, img_backend_relative_path = img_proccess_save(image, img_file)
        if serializer.validated_data['file_name'] == "":
            serializer.validated_data['file_name'] = img_name
        serializer.save(owner = self.request.user, file_path = img_backend_relative_path)

    @action(methods=['get'], detail=True, url_path="download")
    def download(self, request, *args, **kwargs): # 文件下载,访问 http://xx.xx.xx.xx:8000/....../[id]/download/ 链接，即可直接下载
        file_obj = self.get_object()
        response = FileResponse(open(file_obj.file_path.path, 'rb'))
        return response
    
    # @action(detail=False, methods=['post'], url_path="img_upload") # 用这个上传，可以存图片到服务器，但图片信息不会进入数据库
    # def img_upload(self, request, pk=None):
    #     try:
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
            
    #         image = serializer.validated_data['file_path']
    #         img_file = self.request.user # 图片存储的文件夹

    #         img_name, img_backend_relative_path = img_proccess_save(image, img_file)
            
    #         return Response(status=status.HTTP_201_CREATED, data=img_backend_relative_path)
    #     # 未知错误，报服务器内部错误
    #     except Exception as error:
    #         return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"detail": "服务器内部错误"})

    @action(methods=['post'], detail=False, url_path="add_like", permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,))
    def add_like(self, request, *args, **kwargs):      
        serializer = beauty_local_serializer_add_like(data=request.data)
        serializer.is_valid(raise_exception=True)
        pic_id = serializer.validated_data['pic_id']
        had_liked = beauty_local.objects.values('liker').filter(Q(id=pic_id) & ~Q(liker__id__contains=self.request.user.id)).exists() # 同时检查图片存在和是否已经赞过
        if had_liked:
            pic_obj = beauty_local.objects.get(id=pic_id)  
            pic_obj.liker.add(self.request.user)
            pic_obj.save()
            return Response(status=status.HTTP_200_OK, data={"detail": "点赞成功。", "status_code": 200})
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "图片不存在 or 已经赞过了。"})


# @method_decorator(name = "retrieve", decorator=swagger_auto_schema(auto_schema=None,),) # 隐藏详细信息接口
@method_decorator(name = "list", decorator=swagger_auto_schema(auto_schema=None,),)
@method_decorator(name = "create", decorator=swagger_auto_schema(auto_schema=None,),)
@method_decorator(name = "update", decorator=swagger_auto_schema(auto_schema=None,),)
@method_decorator(name = "partial_update", decorator=swagger_auto_schema(auto_schema=None,),)
# @method_decorator(name = "destroy", decorator=swagger_auto_schema(operation_description="只有删除操作",),)
class beauties_local_manager(viewsets.ModelViewSet):
    queryset =  beauty_local.objects.all()
    filter_class = beauty_local_filter
    permission_classes = (permissions.IsAdminUser,)
    tags = ['本地图片管理']

    def get_serializer_class(self):
        return beauty_local_serializer_manager
    
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})
    # def retrieve(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"detail": "不允许此操作"})



#-----------------------------------------------------------------------------------

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
    return render(request, 'beauty_pic_list.html', {"pic_list": pic_list, "is_local": False})

def beauties_local_list(request):
    list = beauty_local.objects.all().filter(is_delete=False)
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
    return render(request, 'beauty_pic_list.html', {"pic_list": pic_list, "is_local": True})




# @csrf_exempt
# def add_like(request):
#     if request.method != 'GET':
#         res = {"detail": "只允许 “GET” 方法。", "status_code": 405}
#     else:       
#         pic_id = request.GET.get('id')
#         if not check_uuid4(pic_id):
#             res = {'id':"输入不是有效的 UUID", "status_code": 400}
#         else:
#             JWT_authenticator = JWTAuthentication()
#             try: # 检查 token，只能合法注册用户点赞
#                 user, token = JWT_authenticator.authenticate(request) # 拿到 user 和 token
#                 had_liked = beauty.objects.values('liker').filter(Q(id=pic_id) & ~Q(liker__id__contains=TokenUser(token).id)).exists() # 同时检查图片存在和是否已经赞过
#                 if had_liked: # 未赞过
#                     like_pic = beauty.objects.filter(id=pic_id).first()
#                     like_pic.liker.add(user)
#                     res = {"detail": "点赞成功。", "status_code": 200}
#                 else:
#                     res = {"detail": "图片不存在 or 已经赞过了。", "status_code": 404}
#             except:
#                 res = {"detail": "未登录", "status_code": 401}
    
#     return HttpResponse(
#             json.dumps(res, ensure_ascii=False),
#             content_type="application/json,charset=utf-8"
#             )

# def check_uuid4(test_uuid):
#     try:
#         return uuid.UUID(test_uuid).version
#     except ValueError:
#         return False

# def check_uuid4_ok(test_uuid):
#     try:
#         return test_uuid.version
#     except ValueError:
#         return False