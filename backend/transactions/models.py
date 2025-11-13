from django.db import models
from django.contrib.auth.models import User

class TransactionCategory(models.Model):
    CATEGORY_TYPES = [
        ('expense', '支出'),
        ('income', '收入'),
    ]
    
    name = models.CharField('分类名称', max_length=100)
    type = models.CharField('类型', max_length=10, choices=CATEGORY_TYPES, default='expense')
    icon = models.CharField('图标', max_length=50, blank=True)
    color = models.CharField('颜色', max_length=7, default='#1890ff')
    is_active = models.BooleanField('是否启用', default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '交易分类'
        verbose_name_plural = '交易分类'
        ordering = ['name']

    def __str__(self):
        return f"{self.get_type_display()} - {self.name}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('expense', '支出'),
        ('income', '收入'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE, verbose_name='分类')
    amount = models.DecimalField('金额', max_digits=10, decimal_places=2)
    transaction_type = models.CharField('交易类型', max_length=10, choices=TRANSACTION_TYPES, default='expense')
    date = models.DateField('交易日期')
    description = models.TextField('备注', blank=True)
    tags = models.CharField('标签', max_length=200, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '交易记录'
        verbose_name_plural = '交易记录'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.date} - {self.category.name} - ¥{self.amount}"

class Budget(models.Model):
    BUDGET_PERIODS = [
        ('monthly', '月度'),
        ('yearly', '年度'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE, verbose_name='分类')
    amount = models.DecimalField('预算金额', max_digits=10, decimal_places=2)
    period = models.CharField('预算周期', max_length=10, choices=BUDGET_PERIODS, default='monthly')
    start_date = models.DateField('开始日期')
    end_date = models.DateField('结束日期')
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '预算设置'
        verbose_name_plural = '预算设置'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - ¥{self.amount}"

class FinancialGoal(models.Model):
    GOAL_TYPES = [
        ('savings', '储蓄目标'),
        ('expense_limit', '支出限制'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    name = models.CharField('目标名称', max_length=100)
    goal_type = models.CharField('目标类型', max_length=20, choices=GOAL_TYPES)
    target_amount = models.DecimalField('目标金额', max_digits=10, decimal_places=2)
    current_amount = models.DecimalField('当前金额', max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField('截止日期', null=True, blank=True)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '财务目标'
        verbose_name_plural = '财务目标'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    @property
    def progress_percentage(self):
        if self.target_amount == 0:
            return 0
        return min(100, (self.current_amount / self.target_amount) * 100)


class Alert(models.Model):
    """财务预警"""
    TYPE_CHOICES = (
        ('budget', '预算预警'),
        ('goal', '目标预警'),
        ('spending', '支出预警'),
        ('income', '收入预警'),
        ('system', '系统预警'),
    )
    
    LEVEL_CHOICES = (
        ('info', '信息'),
        ('warning', '警告'),
        ('danger', '危险'),
        ('success', '成功'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_alert', verbose_name='用户')
    alert_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='预警类型')
    title = models.CharField(max_length=200, verbose_name='预警标题')
    message = models.TextField(verbose_name='预警消息')
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='info', verbose_name='预警级别')
    related_data = models.JSONField(null=True, blank=True, verbose_name='相关数据')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '财务预警'
        verbose_name_plural = '财务预警'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ExportTask(models.Model):
    """数据导出任务"""
    FORMAT_CHOICES = (
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
    )
    
    STATUS_CHOICES = (
        ('pending', '等待中'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_exporttask', verbose_name='用户')
    task_id = models.CharField(max_length=50, unique=True, verbose_name='任务ID')
    file_name = models.CharField(max_length=200, verbose_name='文件名')
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, verbose_name='文件格式')
    export_type = models.CharField(max_length=20, default='transactions', verbose_name='导出类型')
    file_path = models.CharField(max_length=500, null=True, blank=True, verbose_name='文件路径')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='任务状态')
    start_date = models.DateField(null=True, blank=True, verbose_name='开始日期')
    end_date = models.DateField(null=True, blank=True, verbose_name='结束日期')
    include_categories = models.JSONField(null=True, blank=True, verbose_name='包含的分类')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    error_message = models.TextField(null=True, blank=True, verbose_name='错误信息')
    
    class Meta:
        verbose_name = '数据导出任务'
        verbose_name_plural = '数据导出任务'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.file_name} ({self.get_status_display()})"