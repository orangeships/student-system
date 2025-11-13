from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Alert(models.Model):
    """
    财务预警模型
    """
    PRIORITY_CHOICES = [
        ('info', '信息'),
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('urgent', '紧急'),
    ]
    
    ALERT_TYPE_CHOICES = [
        ('budget', '预算预警'),
        ('goal', '目标预警'),
        ('saving', '储蓄预警'),
        ('expense', '支出异常'),
        ('income', '收入异常'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts_alert', verbose_name='用户')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES, verbose_name='预警类型')
    title = models.CharField(max_length=200, verbose_name='标题')
    message = models.TextField(verbose_name='消息内容')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name='优先级')
    
    # 关联数据
    related_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='关联ID')
    related_type = models.CharField(max_length=50, null=True, blank=True, verbose_name='关联类型')
    
    # 状态
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    
    # 时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='过期时间')
    
    class Meta:
        verbose_name = '预警'
        verbose_name_plural = '预警管理'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.user.username})"


class ExportTask(models.Model):
    """
    数据导出任务模型
    """
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]
    
    FORMAT_CHOICES = [
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
    ]
    
    EXPORT_TYPE_CHOICES = [
        ('transactions', '交易记录'),
        ('budgets', '预算数据'),
        ('goals', '目标数据'),
        ('alerts', '预警数据'),
        ('savings', '储蓄数据'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts_exporttask', verbose_name='用户')
    export_type = models.CharField(max_length=20, choices=EXPORT_TYPE_CHOICES, default='transactions', verbose_name='导出类型')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, verbose_name='文件格式')
    
    # 参数
    start_date = models.DateField(null=True, blank=True, verbose_name='开始日期')
    end_date = models.DateField(null=True, blank=True, verbose_name='结束日期')
    filters = models.JSONField(default=dict, blank=True, verbose_name='筛选参数')
    
    # 结果
    file_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='文件名')
    file_url = models.URLField(null=True, blank=True, verbose_name='文件链接')
    file_size = models.PositiveIntegerField(null=True, blank=True, verbose_name='文件大小(字节)')
    
    # 时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='过期时间')
    
    class Meta:
        verbose_name = '导出任务'
        verbose_name_plural = '导出任务管理'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"导出任务 {self.id} ({self.user.username})"