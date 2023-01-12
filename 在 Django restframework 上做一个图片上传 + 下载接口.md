# 在 Django REST framework 上自定义图片上传 + 下载接口

## 0

DRF 框架本身的图片上传功能有很多限制，网上的文章要么做出来功能单一，要么互相抄袭，几乎没有完善可用的方案。

## 需求

1. 找一个位置放图片，按照上传的用户名和时间建立文件夹放好
2. 上传的图片应该在数据库中记录相应的信息：路径、上传用户、上传时间等
3. 接口应该做成 API，在 API 文档中可以显示和测试

## 准备工作

1. 先建立一个测试项目 $welfare$
2. 在项目里建立 APP $pic$
3. 把项目运行起来

## 确定存放位置

一般来讲，图片会选择集中存放在项目根目录中的 $media$ 文件夹。那么我们应该告诉 Django 这个 $media$ 文件夹的位置在哪里，这个设置应该在根目录的 $setting.py$ 文件里，在文件里加入

``` python
MEDIA_ROOT = os.path.join(BASE_DIR, "media") # 告诉 Django 图片应该放在哪里
```
接着在根目录里找到与你项目同名的文件夹，我这里就是 $welfare$ 文件夹，打开文件夹里的 $urls.py$，增加一条 url 链接，别忘了导入 $setting.py$ 文件

``` python
from django.urls import path, include, re_path
from welfare import settings
from django.views.static import serve

urlpatterns = [
    re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}), # 增加这条
]
```

到这里，往$media$ 文件夹里复制一张图片，并在浏览器中打开链接：

> http://127.0.0.1:8000/media/你的图片.jpg/

你应该可以看到刚刚复制进去的图片了

## 在模板中打开

现在，虽然可以在浏览器中看到单独的一张图片，但图片是不能放入模板中，要在网页里显示的，我们应该在 $setting.py$ 文件里下面加入

``` python
MEDIA_URL = '/media/' # 告诉 Django 图片应该这样生成 url

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.media', # 加入这句
            ],
        },
    },
]
```

在模板里这样使用：

```html
<!--如果你的图片路径是 "media/你的图片.jpg"-->
<img class="pic" src="{{MEDIA_URL}}你的图片.jpg" />
<!--如果你的图片路径是 "media/用户名/你的图片.jpg"-->
<img class="pic" src="{{MEDIA_URL}}用户名/你的图片.jpg" />
```

至此，你已经可以利用服务器里已有的图片了，但还和 DRF 接口还没有关系，也不能上传图片

## DRF 接口

### 建立模型

在 根目录 里的 APP 文件夹 $pic$ 有一个 $model.py$ 文件，建立模型，记录上传的图片信息

``` python
from django.db import models
import uuid
import os
from django.utils import timezone

class beauty_local(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID') # 32位的设备ID
    file_path = models.ImageField(upload_to = 'uploads', verbose_name='路径') 
    file_name = models.TextField(blank=True, null=True, verbose_name='文件名')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='生成时间')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    owner = models.ForeignKey('auth.User', on_delete=models.SET("已删除"), related_name = "local_own_by")
    liker = models.ManyToManyField('auth.User', blank=True, null=True, related_name = "local_like_by") # 谁给图片点了赞
    is_delete = models.BooleanField(default=False)
    def delete(self):
        self.is_delete=True
        self.save()
    def __str__(self): 
        return str(self.file_path)
    class Meta:
        ordering = ['-created_time']
        verbose_name_plural = "本地图片"
        verbose_name = verbose_name_plural
        unique_together = (('file_path'), )
```
解析：
``file_path = models.ImageField(upload_to = 'uploads', verbose_name='路径')`` 这里的 upload_to = 'uploads' 指定了默认的图片保存位置是 $media$ 里的 $uploads$ 文件夹

### 序列化器

2 个序列化器，一个用于上传，另一个用于上传以外的功能，并没有什么高深的东西

``` python
from rest_framework import serializers
from pic.models import *

class beauty_local_serializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    liker_count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    file_path = serializers.ImageField()
    class Meta:
        model = beauty_local
        exclude = ("liker",)
        read_only_fields = ('created_time', 'owner', 'file_path')

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

class create_beauty_local_serializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = beauty_local
        exclude = ("liker", "created_time", "is_delete")
```

### 视图集---简单

先把简单的做出来

``` python
from pic.models import *
from pic.serializers import *
from pic.filters import *
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class beauties_local(viewsets.ModelViewSet):
    queryset =  beauty_local.objects.all().filter(is_delete=False)
    filter_class = beauty_local_filter
    def get_serializer_class(self): # 根据不同请求调用序列化器
        if self.action == "create":
            return create_beauty_local_serializer
        else:
            return beauty_local_serializer
    def perform_create(self, serializer): # 保存上传的用户信息
        serializer.save(owner = self.request.user)

    @action(methods=['get'], detail=True, url_path="download")
    def download(self, request, pk=None, *args, **kwargs): # 下载,访问 http://xx.xx.xx.xx:8000/....../[id]/download/ 链接，即可直接下载图片
        file_obj = self.get_object()
        response = FileResponse(open(file_obj.file_path.path, 'rb'))
        return response
```

### urls

根目录里找到与你项目同名的文件夹，我这里就是 $welfare$ 文件夹，打开文件夹里的 $urls.py$，补充完整

```python
from django.urls import path, include, re_path
from django.views.static import serve
from welfare import settings

urlpatterns = [
    path('pic/', include("pic.urls")),
    re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),   
]
```
在 APP 的文件夹里找到 $urls.py$，补充完整

```python
from django.urls import path, include
from pic import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'beauties_local', views.beauties_local, basename='beauties_local')

urlpatterns = [
    path('', include(router.urls)), # drf 自动注册路由
]
```

到这里，应该可以看到上传的页面了

![ 视图集---简单--上传](https://pic3.zhimg.com/v2-5add244e483a87a6c4eb4c20d19826fe_r.jpg)

上传图片后，可以看到上传后的记录

![ 视图集---简单--查看](https://i0.hdslb.com/bfs/new_dyn/8a6c1b7b2ed75bce8798a45662f2cd3713871723.jpg)

### 视图集---完整

经过上面的一番操作，基本的功能已经有了，但只能上传到模型里设定的文件夹，而且文件名也不能自动填写。为了完善功能，我们还需要一些新的函数

#### 新的函数

在 APP 的文件夹里新建 $utils.py$ 文件，写个函数

```python
import random
import os
import datetime, time
from pathlib import Path
from rest_framework.response import Response
from django.conf import settings

def img_proccess_save(image, file):
    # 防重名
    name = Path(image.name)
    img_pure_name = name.stem + '_' + str(int(time.time())) # name.stem：提取无后缀的文件名
    img_extend_name = name.suffix # 提取后缀名
    img_name = img_pure_name + img_extend_name # 新的文件名

    # 创建存储路径
    img_dir = os.path.join(settings.MEDIA_ROOT, file) # 想要保存的文件夹 
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    img_file_year = os.path.join(img_dir, datetime.datetime.now().strftime("%Y")) # 按年保存的文件夹
    if not os.path.exists(img_file_year):
        os.mkdir(img_file_year)
    img_file_month = os.path.join(img_file_year, datetime.datetime.now().strftime("%m")) # 按月保存的文件夹
    if not os.path.exists(img_file_month):
        os.mkdir(img_file_month)

    # 存储图片
    destination = open(os.path.join(img_file_month, img_name), 'wb+')
    for chunk in image.chunks(): # 对图片切片
        destination.write(chunk) # 把切片写入
    destination.close()

    # 传回给后端ImageField要存储的图片路径
    backend_relative_path = file + '/' + datetime.datetime.now().strftime("%Y") + '/' + datetime.datetime.now().strftime("%m") + '/' + img_name 

    return img_name, backend_relative_path
```

解析：
1. 输入图片和保存图片的文件夹名，返回图片名和在 $media$ 文件夹的相对路径
2. 图片文件名后面加入时间戳防止重名
3. 在将要保存的文件夹里按年月建子文件夹

#### 修改 视图集

修改前面的视图集，把功能加进去

```python
from pic.utils import img_proccess_save

class beauties_local(viewsets.ModelViewSet):
    queryset =  beauty_local.objects.all().filter(is_delete=False)
    filter_class = beauty_local_filter
    # permission_classes = (permissions.DjangoModelPermissions, IsOwnerOrReadOnly)
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
    def get_serializer_class(self):
        if self.action == "create":
            return create_beauty_local_serializer
        else:
            return beauty_local_serializer
    def perform_create(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        image = serializer.validated_data['file_path'] # 从序列化器获得图片
        img_file = str(self.request.user) # 图片存储的文件夹
        img_name, img_backend_relative_path = img_proccess_save(image, img_file)
        if serializer.validated_data['file_name'] == "": # 如果没有填文件名，就自动填
            serializer.validated_data['file_name'] = img_name
        serializer.save(owner = self.request.user, file_path = img_backend_relative_path)

    @action(methods=['get'], detail=True, url_path="download")
    def download(self, request, pk=None, *args, **kwargs): # 文件下载,访问 http://xx.xx.xx.xx:8000/....../[id]/download/ 链接，即可直接下载
        file_obj = self.get_object()
        response = FileResponse(open(file_obj.file_path.path, 'rb'))
        return response
```

至此，功能应该完整了

![视图集---完整--上传](https://i0.hdslb.com/bfs/new_dyn/501b6c23297b41cf94374624ac69e4cd13871723.jpg)

上传后的一个 bug 是不能返回图片的 url，但上传已经成功，没有任何不良影响

![视图集---完整--查看](https://i0.hdslb.com/bfs/new_dyn/897cd85cd52256328a0e4e87ac4dff0613871723.jpg)

## 参考文献

[Django restframework 自定义图片上传接口](https://blog.csdn.net/ZeroChia/article/details/123793999)