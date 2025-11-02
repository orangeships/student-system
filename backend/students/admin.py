from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'gender', 'grade', 'class_name', 'major', 'status', 'created_at']
    list_filter = ['gender', 'grade', 'class_name', 'major', 'status', 'created_at']
    search_fields = ['name', 'student_id', 'phone', 'email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'student_id', 'name', 'gender', 'birth_date')
        }),
        ('联系信息', {
            'fields': ('phone', 'email', 'address')
        }),
        ('学籍信息', {
            'fields': ('major', 'grade', 'class_name', 'enrollment_date', 'status')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
