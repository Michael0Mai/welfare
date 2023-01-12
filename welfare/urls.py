from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.static import serve
from django.contrib import admin
from . import views
from pic import views as pic_views
from django.contrib.auth.decorators import login_required
# from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from welfare.utils_token import MyTokenObtainPairView, MyTokenRefreshView, MyTokenVerifyView
from welfare import settings

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')), #DRF 的登录视图，为你的可视化接口页面生成一个用户登录的入口
    
    # 令牌获取和刷新
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), # 自定义 token 信息
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'), # 自定义刷新 token 信息
    path('token/verify', MyTokenVerifyView.as_view(), name='token_verify'), # 自定义验证 token 信息
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

    # url('web', pic_views.beauties_list, name='web_pic'),
    # url('local', pic_views.beauties_local_list, name='local_pic'),
    url('status_codes/', views.status_codes), 
    url(r'^$', views.index_read, name='index_read'), 

    re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    
]
