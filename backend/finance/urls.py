from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeeCategoryViewSet, FeeRecordViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'categories', FeeCategoryViewSet, basename='feecategory')
router.register(r'records', FeeRecordViewSet, basename='feerecord')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]