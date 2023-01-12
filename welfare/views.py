from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from django.contrib.auth.decorators import login_required
from django.shortcuts import render

schema_view = get_schema_view(
    openapi.Info(
        title="福利管理系统 API",
        default_version='V1',
        #description="设备管理系统 API description",
        #terms_of_service="",
        contact=openapi.Contact(email = "micheal.chao@hotmail.com"),
        #license=openapi.License(name=""),
    ),
    public = False, # public 表示文档完全公开, 无需针对用户鉴权
    permission_classes=(permissions.AllowAny,),
    # permission_classes=(permissions.IsAuthenticatedOrReadOnly,), # 可以传递 drf 的 BasePermission
)

def status_codes(request):
    return render(request, 'status_codes.html')

def index_read(request):
    return render(request, 'index_read.html')