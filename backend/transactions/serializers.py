from rest_framework import serializers
from .models import Transaction, TransactionCategory, Budget, FinancialGoal


class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ['id', 'name', 'type', 'icon', 'color', 'is_active']
        read_only_fields = ['id']


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'category', 'category_name', 'category_icon', 'category_color',
            'amount', 'transaction_type', 'date', 'description', 'tags', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

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
    spent_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = [
            'id', 'user', 'category', 'category_name', 'amount', 'period',
            'start_date', 'end_date', 'spent_amount', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_spent_amount(self, obj):
        # 计算预算周期内已花费金额
        from django.db.models import Sum
        spent = Transaction.objects.filter(
            user=obj.user,
            category=obj.category,
            transaction_type='expense',
            date__range=[obj.start_date, obj.end_date]
        ).aggregate(total=Sum('amount'))['total']
        return spent or 0


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