from django.contrib import admin
from .models import FeeCategory, FeeRecord, Payment

@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

@admin.register(FeeRecord)
class FeeRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'category', 'amount', 'paid_amount', 'due_date', 'status', 'created_at']
    list_filter = ['status', 'category', 'due_date', 'created_at']
    search_fields = ['student__name', 'student__student_id', 'description']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'due_date'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['fee_record', 'amount', 'payment_method', 'payment_date', 'processed_by']
    list_filter = ['payment_method', 'payment_date']
    search_fields = ['fee_record__student__name', 'transaction_id']
    readonly_fields = ['payment_date']
    date_hierarchy = 'payment_date'
