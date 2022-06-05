from django.urls import path, include
from pic import views

#app_name = 'equipment_manage_app'
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'beauties', views.beauties, basename='beauties')

urlpatterns = [
    path('', include(router.urls)), # drf 自动注册路由
    path("beauties_list/", views.beauties_list),
    path("add_like/", views.add_like),
]