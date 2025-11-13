from rest_framework import serializers
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from transactions.models import Transaction, TransactionCategory


class SummarySerializer(serializers.Serializer):
    """交易统计摘要序列化器"""
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    transaction_count = serializers.IntegerField()
    avg_transaction = serializers.DecimalField(max_digits=12, decimal_places=2)
    date_range = serializers.DictField()


class CategoryStatsSerializer(serializers.Serializer):
    """分类统计序列化器"""
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    type = serializers.CharField()
    categories = serializers.ListField(
        child=serializers.DictField()
    )
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class TrendDataSerializer(serializers.Serializer):
    """趋势数据项序列化器"""
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    income = serializers.DecimalField(max_digits=12, decimal_places=2)
    expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)


class TrendSerializer(serializers.Serializer):
    """收支趋势序列化器"""
    range = serializers.CharField()
    periods = TrendDataSerializer(many=True)


class PredictionSerializer(serializers.Serializer):
    """财务预测序列化器"""
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    predicted_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    predicted_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    predicted_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    confidence = serializers.FloatField()


class PredictionListSerializer(serializers.Serializer):
    """财务预测列表序列化器"""
    predictions = PredictionSerializer(many=True)
    based_on_months = serializers.IntegerField()


class BudgetRecommendationSerializer(serializers.Serializer):
    """预算建议序列化器"""
    category = serializers.CharField()
    current_avg = serializers.DecimalField(max_digits=12, decimal_places=2)
    recommended = serializers.DecimalField(max_digits=12, decimal_places=2)
    reason = serializers.CharField()


class SavingsAdviceItemSerializer(serializers.Serializer):
    """储蓄建议项序列化器"""
    advice = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)


class FinancialHealthSerializer(serializers.Serializer):
    """财务健康度序列化器"""
    score = serializers.IntegerField()
    level = serializers.CharField()
    improvement_suggestions = serializers.ListField(
        child=serializers.CharField()
    )


class RecommendationSerializer(serializers.Serializer):
    """建议数据序列化器"""
    budget_recommendations = BudgetRecommendationSerializer(many=True)
    savings_advice = SavingsAdviceItemSerializer(many=True)
    financial_health = FinancialHealthSerializer()