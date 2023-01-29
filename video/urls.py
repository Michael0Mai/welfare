from django.urls import path, include
from video import views

app_name = 'video_app'
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'beauties', views.beauties, basename='beauties')
# router.register(r'beauties_manager', views.beauties_manager, basename='beauties_manager')
router.register(r'videos_local', views.videos_local, basename='videos_local')
router.register(r'videos_manager_local', views.videos_local_manager, basename='videos_local_manager')

urlpatterns = [
    path('', include(router.urls)), # drf 自动注册路由
    path("video_test/", views.video_test),
]