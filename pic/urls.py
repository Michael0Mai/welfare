from django.urls import path, include
from pic import views

app_name = 'beauties_list_app'
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'beauties', views.beauties, basename='beauties')
router.register(r'beauties_manager', views.beauties_manager, basename='beauties_manager')
router.register(r'beauties_local', views.beauties_local, basename='beauties_local')
router.register(r'beauties_manager_local', views.beauties_local_manager, basename='beauties_local_manager')

urlpatterns = [
    path('', include(router.urls)), # drf 自动注册路由
    path("beauties_list/", views.beauties_list, name = 'beauties_list_web'),
    path("beauties_local_list/", views.beauties_local_list, name = 'beauties_list_local'),
    path("add_like/", views.add_like),
]