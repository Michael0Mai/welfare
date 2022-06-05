from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from . import views
from pic import views as pic_views
from django.contrib.auth.decorators import login_required

from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
# from welfare.utils import MyTokenObtainPairView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')), #DRF 的登录视图，为你的可视化接口页面生成一个用户登录的入口
    
    # 令牌获取和刷新
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), # 自定义token 信息
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include('django.contrib.auth.urls')),

    # 接口描述
    url('^swagger(?P<format>\.json|\.yaml)$', login_required(views.schema_view.without_ui(cache_timeout=0)), name='schema-json'),
    url('swagger', login_required(views.schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    url('redoc/', login_required(views.schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),

    #登陆后台管理
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')), # 假的后台地址
    path('secret_manager/', admin.site.urls), # 真的后台地址
    
    path('pic/', include("pic.urls")),
    path('users/', include("users.urls")),
    url(r'^$', pic_views.beauties_list),
    url('status_codes/', views.status_codes), 
]
