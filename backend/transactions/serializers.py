from rest_framework import serializers
from .models import Transaction, TransactionCategory, Budget, FinancialGoal, Alert, ExportTask


class TransactionCategorySerializer(serializers.ModelSerializer):
    category_type = serializers.CharField(source='type')
    
    class Meta:
        model = TransactionCategory
        fields = ['id', 'name', 'category_type', 'icon', 'color', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    description = serializers.CharField(allow_blank=True, required=False)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'category', 'category_name', 'category_color',
            'amount', 'transaction_type', 'date', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("金额必须大于0")
        return value

    def validate_date(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("交易日期不能是未来日期")
        return value


class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    current_spent = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = [
            'id', 'user', 'category', 'category_name', 'amount', 'period',
            'start_date', 'end_date', 'current_spent', 'remaining', 
            'progress_percentage', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_current_spent(self, obj):
        # 计算预算周期内已花费金额
        from django.db.models import Sum
        spent = Transaction.objects.filter(
            user=obj.user,
            category=obj.category,
            transaction_type='expense',
            date__range=[obj.start_date, obj.end_date]
        ).aggregate(total=Sum('amount'))['total']
        return float(spent or 0)
    
    def get_remaining(self, obj):
        current_spent = self.get_current_spent(obj)
        return max(0, float(obj.amount) - current_spent)
    
    def get_progress_percentage(self, obj):
        current_spent = self.get_current_spent(obj)
        if obj.amount == 0:
            return 0
        return min(100, (current_spent / float(obj.amount)) * 100)


class FinancialGoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = FinancialGoal
        fields = [
            'id', 'user', 'name', 'goal_type', 'target_amount', 
            'current_amount', 'progress_percentage', 'deadline', 
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_target_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("目标金额必须大于0")
        return value


class AlertSerializer(serializers.ModelSerializer):
    """预警序列化器"""
    
    class Meta:
        model = Alert
        fields = ['id', 'alert_type', 'title', 'message', 'level', 'related_data', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']


class AlertListSerializer(serializers.Serializer):
    """预警列表序列化器"""
    alerts = AlertSerializer(many=True)


class ExportTaskSerializer(serializers.ModelSerializer):
    """导出任务序列化器"""
    
    class Meta:
        model = ExportTask
        fields = ['id', 'task_id', 'file_name', 'file_format', 'export_type', 'status', 'start_date', 'end_date', 'created_at', 'completed_at']
        read_only_fields = ['id', 'task_id', 'status', 'created_at', 'completed_at']


class CreateExportTaskSerializer(serializers.Serializer):
    """创建导出任务序列化器"""
    format = serializers.ChoiceField(choices=['csv', 'excel'])
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)
    include_categories = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )
    
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("开始日期不能晚于结束日期")
        
        return data


class ExportResponseSerializer(serializers.Serializer):
    """导出响应序列化器"""
    export_id = serializers.CharField()
    download_url = serializers.CharField()
    estimated_time = serializers.CharField()


# 统一响应序列化器
class StandardResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    message = serializers.CharField(allow_blank=True)
    data = serializers.JSONField(allow_null=True)
    errors = serializers.JSONField(allow_null=True)