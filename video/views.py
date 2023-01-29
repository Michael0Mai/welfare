from video.models import *
from video.serializers import *
from video.filters import *
from rest_framework import viewsets, permissions, status
from video.permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from pic.utils import img_proccess_save
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
import re
import os
import mimetypes
from wsgiref.util import FileWrapper

class videos_local(viewsets.ModelViewSet):
    queryset =  video_local.objects.all().filter(is_delete=False)
    filter_class = video_local_filter
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
    tags = ['本地视频']

    def get_serializer_class(self):
        if self.action == "create":
            return create_video_local_serializer
        elif self.action == "add_like":
            return video_local_serializer_add_like
        else:
            return video_local_serializer
    def perform_create(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        video = serializer.validated_data['file_path']
        video_file = str(self.request.user) # 图片存储的文件夹
        video_name, video_backend_relative_path = img_proccess_save(video, video_file)
        if serializer.validated_data['file_name'] == "":
            serializer.validated_data['file_name'] = video_name
        serializer.save(owner = self.request.user, file_path = video_backend_relative_path)

    @action(methods=['get'], detail=True, url_path="video_play", permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,))
    def video_play(self, request, *args, **kwargs):
        file_obj = self.get_object()
        
        range_header = request.META.get('HTTP_RANGE', '').strip()
        # print(range_header if range_header else '没有 range_header')
        range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
        range_match = range_re.match(range_header)
        
        path='media/' + str(file_obj.file_path)
        size = os.path.getsize(str(path))
        content_type, encoding = mimetypes.guess_type(path)
        content_type = content_type or 'application/octet-stream'
        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte) if first_byte else 0
            last_byte = first_byte + 1024 * 1024 * 10
            if last_byte >= size:
                last_byte = size - 1
            length = last_byte - first_byte + 1
            resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
            resp['Content-Length'] = str(length)
            resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        else:
            resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
            resp['Content-Length'] = str(size)
        resp['Accept-Ranges'] = 'bytes'
        return resp

# @method_decorator(name = "retrieve", decorator=swagger_auto_schema(auto_schema=None,),) # 隐藏详细信息接口
@method_decorator(name = "list", decorator=swagger_auto_schema(auto_schema=None,),)
@method_decorator(name = "create", decorator=swagger_auto_schema(auto_schema=None,),)
@method_decorator(name = "update", decorator=swagger_auto_schema(auto_schema=None,),)
@method_decorator(name = "partial_update", decorator=swagger_auto_schema(auto_schema=None,),)
# @method_decorator(name = "destroy", decorator=swagger_auto_schema(operation_description="只有删除操作",),)
class videos_local_manager(viewsets.ModelViewSet):
    queryset =  video_local.objects.all()
    filter_class = video_local_filter
    permission_classes = (permissions.IsAdminUser,)
    tags = ['本地视频管理']

    def get_serializer_class(self):
        return video_local_serializer_manager
    
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


def video_test(request):
    return render(request, 'vidoe_test.html')

def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length # 文件有多少 bytes
        while True: # 循环读文件
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length) # 读文件的一段
            if not data:
                break
            if remaining:
                remaining -= len(data) # 计算还有多少 bytes
            yield data