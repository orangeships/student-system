from django.contrib import admin
from .models import Alert, ExportTask


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    """预警管理界面"""
    list_display = [
        'id', 'user', 'alert_type', 'title', 'priority',
        'is_read', 'is_active', 'created_at'
    ]
    list_filter = [
        'alert_type', 'priority', 'is_read', 'is_active', 
        'created_at'
    ]
    search_fields = ['title', 'message', 'user__username']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'alert_type', 'title', 'message', 'priority')
        }),
        ('关联数据', {
            'fields': ('related_id', 'related_type'),
            'classes': ('collapse',)
        }),
        ('状态信息', {
            'fields': ('is_read', 'is_active')
        }),
        ('时间信息', {
            'fields': ('created_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """优化查询"""
        qs = super().get_queryset(request)
        return qs.select_related('user')


@admin.register(ExportTask)
class ExportTaskAdmin(admin.ModelAdmin):
    """导出任务管理界面"""
    list_display = [
        'id', 'user', 'export_type', 'format', 'status',
        'file_name', 'created_at', 'completed_at'
    ]
    list_filter = [
        'export_type', 'format', 'status', 
        'created_at', 'completed_at'
    ]
    search_fields = ['user__username', 'file_name']
    readonly_fields = [
        'id', 'created_at', 'completed_at', 'file_name', 
        'file_url', 'file_size'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'export_type', 'format')
        }),
        ('任务参数', {
            'fields': ('start_date', 'end_date', 'filters'),
            'classes': ('collapse',)
        }),
        ('任务状态', {
            'fields': ('status',)
        }),
        ('文件信息', {
            'fields': ('file_name', 'file_url', 'file_size'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'completed_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """优化查询"""
        qs = super().get_queryset(request)
        return qs.select_related('user')