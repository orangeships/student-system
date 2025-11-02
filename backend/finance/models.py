from django.db import models
from django.contrib.auth.models import User
from students.models import Student

class FeeCategory(models.Model):
    name = models.CharField('费用名称', max_length=100)
    description = models.TextField('描述', blank=True)
    amount = models.DecimalField('标准金额', max_digits=10, decimal_places=2)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '费用类别'
        verbose_name_plural = '费用类别'
        ordering = ['name']

    def __str__(self):
        return self.name

class FeeRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', '待缴费'),
        ('paid', '已缴费'),
        ('overdue', '逾期'),
        ('cancelled', '已取消'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学生')
    category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE, verbose_name='费用类别')
    amount = models.DecimalField('应缴金额', max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField('实缴金额', max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField('截止日期')
    paid_date = models.DateTimeField('缴费时间', null=True, blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField('备注', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '缴费记录'
        verbose_name_plural = '缴费记录'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.name} - {self.category.name}"

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', '现金'),
        ('card', '银行卡'),
        ('alipay', '支付宝'),
        ('wechat', '微信'),
        ('bank_transfer', '银行转账'),
    ]
    
    fee_record = models.ForeignKey(FeeRecord, on_delete=models.CASCADE, verbose_name='缴费记录')
    amount = models.DecimalField('支付金额', max_digits=10, decimal_places=2)
    payment_method = models.CharField('支付方式', max_length=20, choices=PAYMENT_METHODS)
    payment_date = models.DateTimeField('支付时间', auto_now_add=True)
    transaction_id = models.CharField('交易号', max_length=100, blank=True)
    notes = models.TextField('备注', blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='处理人')

    class Meta:
        verbose_name = '支付记录'
        verbose_name_plural = '支付记录'
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.fee_record.student.name} - {self.amount}"
