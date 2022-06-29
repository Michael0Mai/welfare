from django.urls import path, include
from users import views

#app_name = 'equipment_manage_app'
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.users)
router.register(r'create_user', views.create_user, 'create_user')
router.register(r'current_user', views.current_user, 'current_user_detail')
# router.register(r'permissions', views.permission)

urlpatterns = [
    path('', include(router.urls)), # drf 自动注册路由
]