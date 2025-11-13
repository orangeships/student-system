from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TransactionViewSet, 
    TransactionCategoryViewSet, 
    BudgetViewSet, 
    FinancialGoalViewSet,
    AlertViewSet,
    ExportTaskViewSet
)

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'categories', TransactionCategoryViewSet)
router.register(r'budgets', BudgetViewSet)
router.register(r'goals', FinancialGoalViewSet)
router.register(r'alerts', AlertViewSet)
router.register(r'exports', ExportTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]