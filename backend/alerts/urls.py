from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 创建路由器
router = DefaultRouter()
router.register(r'alerts', views.AlertViewSet, basename='alert')
router.register(r'export-tasks', views.ExportTaskViewSet, basename='export-task')

urlpatterns = [
    path('', include(router.urls)),
]