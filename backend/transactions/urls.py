from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TransactionViewSet, 
    TransactionCategoryViewSet, 
    BudgetViewSet, 
    FinancialGoalViewSet
)

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'categories', TransactionCategoryViewSet)
router.register(r'budgets', BudgetViewSet)
router.register(r'goals', FinancialGoalViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]