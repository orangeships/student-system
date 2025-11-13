"""
预警信号处理器
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Alert
from transactions.models import Budget, Transaction


@receiver(post_save, sender=Transaction)
def create_budget_alert(sender, instance, created, **kwargs):
    """
    当创建新交易记录时，自动检查是否触发预算预警
    """
    if not created or instance.transaction_type != 'expense':
        return
    
    # 获取相关的预算
    budgets = Budget.objects.filter(
        user=instance.user,
        category=instance.category,
        is_active=True,
        start_date__lte=instance.date,
        end_date__gte=instance.date
    )
    
    for budget in budgets:
        # 计算当前已使用的预算
        spent_amount = Transaction.objects.filter(
            user=instance.user,
            category=instance.category,
            transaction_type='expense',
            date__gte=budget.start_date,
            date__lte=budget.end_date
        ).aggregate(total=sum('amount'))['total'] or 0
        
        percentage = (spent_amount / budget.amount) * 100
        
        # 检查是否需要创建预警
        if percentage >= 90 and percentage < 100:
            # 预算使用率超过90%，创建预警
            Alert.objects.get_or_create(
                user=instance.user,
                alert_type='budget',
                priority='high',
                title=f"预算预警 - {budget.category.name}",
                message=f"预算使用率已达到{percentage:.1f}%，剩余预算{budget.amount - spent_amount:.2f}元",
                related_id=budget.id,
                expires_at=timezone.now() + timedelta(days=7)
            )
        elif percentage >= 100:
            # 预算超支，创建紧急预警
            Alert.objects.get_or_create(
                user=instance.user,
                alert_type='budget',
                priority='urgent',
                title=f"预算超支 - {budget.category.name}",
                message=f"预算已超支{(spent_amount - budget.amount):.2f}元，请注意控制支出",
                related_id=budget.id,
                expires_at=timezone.now() + timedelta(days=3)
            )