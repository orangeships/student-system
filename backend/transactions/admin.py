from django.contrib import admin
from .models import Transaction, TransactionCategory, Budget, FinancialGoal


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'is_active', 'created_by', 'created_at']
    list_filter = ['type', 'is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'transaction_type', 'date', 'created_at']
    list_filter = ['transaction_type', 'category', 'date', 'created_at']
    search_fields = ['description', 'tags']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'period', 'start_date', 'end_date', 'is_active']
    list_filter = ['period', 'is_active', 'created_at']
    search_fields = ['user__username', 'category__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FinancialGoal)
class FinancialGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'goal_type', 'target_amount', 'current_amount', 'progress_percentage', 'deadline', 'is_active']
    list_filter = ['goal_type', 'is_active', 'created_at']
    search_fields = ['user__username', 'name']
    readonly_fields = ['created_at', 'updated_at', 'progress_percentage']