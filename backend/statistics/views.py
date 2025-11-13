from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta, date
from decimal import Decimal
from transactions.models import Transaction, TransactionCategory
from .serializers import (
    SummarySerializer,
    CategoryStatsSerializer,
    TrendSerializer,
    PredictionListSerializer,
    RecommendationSerializer
)


class StatisticsSummaryView(APIView):
    """交易统计摘要API"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取交易统计摘要"""
        # 获取查询参数
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # 默认查询最近30天
        if not start_date:
            start_date = timezone.now().date() - timedelta(days=30)
        if not end_date:
            end_date = timezone.now().date()
        
        # 构建查询条件
        filters = {
            'user': request.user,
            'date__gte': start_date,
            'date__lte': end_date
        }
        
        # 获取总收入
        total_income = Transaction.objects.filter(
            **filters,
            transaction_type='income'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        # 获取总支出
        total_expense = Transaction.objects.filter(
            **filters,
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        # 计算净结余
        net_balance = total_income - total_expense
        
        # 获取交易总数
        transaction_count = Transaction.objects.filter(
            **filters
        ).count()
        
        # 计算平均交易金额
        if transaction_count > 0:
            avg_transaction = (total_income + total_expense) / transaction_count
        else:
            avg_transaction = Decimal('0')
        
        data = {
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': net_balance,
            'transaction_count': transaction_count,
            'avg_transaction': avg_transaction,
            'date_range': {
                'start_date': start_date,
                'end_date': end_date
            }
        }
        
        serializer = SummarySerializer(data)
        return Response({
            'code': 200,
            'data': serializer.data
        })


class StatisticsCategoriesView(APIView):
    """分类统计分析API"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取分类统计"""
        # 获取查询参数
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))
        trans_type = request.query_params.get('type', 'expense')
        
        # 构建时间范围
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        # 获取该月指定类型的交易
        transactions = Transaction.objects.filter(
            user=request.user,
            transaction_type=trans_type,
            date__gte=start_date,
            date__lte=end_date
        )
        
        # 按分类统计
        category_stats = transactions.values(
            'category__name',
            'category__color'
        ).annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        # 计算总金额
        total_amount = sum(stat['total_amount'] for stat in category_stats)
        
        # 构建响应数据
        categories_data = []
        for stat in category_stats:
            if total_amount > 0:
                percentage = round((stat['total_amount'] / total_amount) * 100, 1)
            else:
                percentage = 0.0
            
            categories_data.append({
                'name': stat['category__name'],
                'amount': stat['total_amount'],
                'percentage': percentage,
                'color': stat['category__color'] or '#808080',
                'count': stat['count']
            })
        
        data = {
            'year': year,
            'month': month,
            'type': trans_type,
            'categories': categories_data,
            'total_amount': total_amount
        }
        
        serializer = CategoryStatsSerializer(data)
        return Response({
            'code': 200,
            'data': serializer.data
        })


class StatisticsTrendView(APIView):
    """收支趋势分析API"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取收支趋势"""
        # 获取时间范围
        range_param = request.query_params.get('range', '3m')
        
        range_map = {
            '1m': 1,
            '3m': 3,
            '6m': 6,
            '1y': 12
        }
        
        months_back = range_map.get(range_param, 3)
        end_date = timezone.now().date()
        start_date = end_date.replace(day=1) - timedelta(days=30 * months_back)
        
        periods_data = []
        current_date = start_date.replace(day=1)
        end_month = end_date.replace(day=1)
        
        while current_date <= end_month:
            # 计算该月的结束日期
            if current_date.month == 12:
                month_end = date(current_date.year + 1, 1, 1) - timedelta(days=1)
            else:
                month_end = date(current_date.year, current_date.month + 1, 1) - timedelta(days=1)
            
            # 获取该月的收支数据
            month_transactions = Transaction.objects.filter(
                user=request.user,
                date__gte=current_date,
                date__lte=month_end
            )
            
            income = month_transactions.filter(
                transaction_type='income'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
            
            expense = month_transactions.filter(
                transaction_type='expense'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
            
            balance = income - expense
            
            periods_data.append({
                'year': current_date.year,
                'month': current_date.month,
                'income': income,
                'expense': expense,
                'balance': balance
            })
            
            # 移动到下个月
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        data = {
            'range': range_param,
            'periods': periods_data
        }
        
        serializer = TrendSerializer(data)
        return Response({
            'code': 200,
            'data': serializer.data
        })


class PlanningPredictionView(APIView):
    """财务预测API"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取财务预测"""
        months = int(request.query_params.get('months', 3))
        
        # 获取最近6个月的历史数据作为预测基础
        end_date = timezone.now().date()
        start_date = end_date.replace(day=1) - timedelta(days=30 * 6)
        
        # 获取历史数据
        historical_data = []
        current_date = start_date.replace(day=1)
        end_month = end_date.replace(day=1)
        
        while current_date <= end_month:
            if current_date.month == 12:
                month_end = date(current_date.year + 1, 1, 1) - timedelta(days=1)
            else:
                month_end = date(current_date.year, current_date.month + 1, 1) - timedelta(days=1)
            
            month_transactions = Transaction.objects.filter(
                user=request.user,
                date__gte=current_date,
                date__lte=month_end
            )
            
            income = month_transactions.filter(
                transaction_type='income'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
            
            expense = month_transactions.filter(
                transaction_type='expense'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
            
            historical_data.append({
                'year': current_date.year,
                'month': current_date.month,
                'income': float(income),
                'expense': float(expense)
            })
            
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        # 简单的线性回归预测
        if len(historical_data) >= 3:
            # 计算平均增长率
            income_values = [d['income'] for d in historical_data]
            expense_values = [d['expense'] for d in historical_data]
            
            avg_income = sum(income_values) / len(income_values)
            avg_expense = sum(expense_values) / len(expense_values)
            
            # 简单的趋势计算
            income_trend = (income_values[-1] - income_values[0]) / len(income_values) if len(income_values) > 1 else 0
            expense_trend = (expense_values[-1] - expense_values[0]) / len(expense_values) if len(expense_values) > 1 else 0
            
            predictions = []
            current_date = end_date.replace(day=1)
            
            for i in range(months):
                # 预测下个月
                if current_date.month == 12:
                    pred_date = current_date.replace(year=current_date.year + 1, month=1)
                else:
                    pred_date = current_date.replace(month=current_date.month + 1)
                
                predicted_income = max(0, avg_income + income_trend * (i + 1))
                predicted_expense = max(0, avg_expense + expense_trend * (i + 1))
                predicted_balance = predicted_income - predicted_expense
                
                # 置信度随时间递减
                confidence = max(0.5, 0.9 - (i * 0.1))
                
                predictions.append({
                    'year': pred_date.year,
                    'month': pred_date.month,
                    'predicted_income': Decimal(str(round(predicted_income, 2))),
                    'predicted_expense': Decimal(str(round(predicted_expense, 2))),
                    'predicted_balance': Decimal(str(round(predicted_balance, 2))),
                    'confidence': confidence
                })
                
                current_date = pred_date
        else:
            # 数据不足，使用默认值
            predictions = []
            current_date = end_date.replace(day=1)
            
            for i in range(months):
                if current_date.month == 12:
                    pred_date = current_date.replace(year=current_date.year + 1, month=1)
                else:
                    pred_date = current_date.replace(month=current_date.month + 1)
                
                predictions.append({
                    'year': pred_date.year,
                    'month': pred_date.month,
                    'predicted_income': Decimal('0'),
                    'predicted_expense': Decimal('0'),
                    'predicted_balance': Decimal('0'),
                    'confidence': 0.5
                })
                
                current_date = pred_date
        
        data = {
            'predictions': predictions,
            'based_on_months': len(historical_data)
        }
        
        serializer = PredictionListSerializer(data)
        return Response({
            'code': 200,
            'data': serializer.data
        })


class PlanningRecommendationsView(APIView):
    """获取预算建议API"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取预算和储蓄建议"""
        # 获取最近3个月的数据
        end_date = timezone.now().date()
        start_date = end_date.replace(day=1) - timedelta(days=90)
        
        # 获取历史交易数据
        transactions = Transaction.objects.filter(
            user=request.user,
            date__gte=start_date,
            date__lte=end_date
        )
        
        # 计算各类别的平均支出
        expense_categories = transactions.filter(
            transaction_type='expense'
        ).values(
            'category__name'
        ).annotate(
            total_amount=Sum('amount'),
            count=Count('id'),
            avg_amount=Avg('amount')
        ).order_by('-total_amount')
        
        # 预算建议
        budget_recommendations = []
        for category in expense_categories[:5]:  # 取前5个主要支出类别
            category_name = category['category__name']
            avg_amount = category['avg_amount']
            
            # 基于数据给出建议
            if avg_amount > 1000:
                recommended = avg_amount * Decimal('0.9')
                reason = "支出较高，建议适当控制"
            elif avg_amount > 500:
                recommended = avg_amount * Decimal('0.95')
                reason = "支出中等，建议小幅优化"
            else:
                recommended = avg_amount
                reason = "支出合理，建议保持"
            
            budget_recommendations.append({
                'category': category_name,
                'current_avg': avg_amount,
                'recommended': recommended,
                'reason': reason
            })
        
        # 计算总收支
        total_income = transactions.filter(
            transaction_type='income'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        total_expense = transactions.filter(
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        net_balance = total_income - total_expense
        
        # 储蓄建议
        savings_advice = []
        if net_balance > 0:
            savings_advice.append({
                'advice': f"本月可储蓄金额预计为{net_balance:.2f}元",
                'amount': net_balance
            })
            savings_advice.append({
                'advice': "建议将30%的结余用于紧急备用金",
                'amount': net_balance * Decimal('0.3')
            })
        else:
            savings_advice.append({
                'advice': "当前支出超过收入，建议控制支出",
                'amount': Decimal('0')
            })
        
        # 财务健康度评分
        if total_income > 0:
            savings_rate = float(net_balance / total_income) * 100
            if savings_rate >= 30:
                health_score = 90
                health_level = "优秀"
            elif savings_rate >= 20:
                health_score = 80
                health_level = "良好"
            elif savings_rate >= 10:
                health_score = 70
                health_level = "一般"
            else:
                health_score = 50
                health_level = "需改善"
        else:
            health_score = 0
            health_level = "无收入数据"
        
        # 改进建议
        improvement_suggestions = []
        if total_expense > total_income and total_income > 0:
            improvement_suggestions.append("支出超过收入，需要开源节流")
        elif savings_rate < 10 and savings_rate > 0:
            improvement_suggestions.append("储蓄率偏低，建议增加收入或控制支出")
        
        if len(expense_categories) > 0:
            top_category = expense_categories[0]
            top_category_ratio = float(top_category['total_amount'] / total_expense) * 100
            if top_category_ratio > 40:
                improvement_suggestions.append(f"{top_category['category__name']}支出占比偏高({top_category_ratio:.1f}%)")
        
        data = {
            'budget_recommendations': budget_recommendations,
            'savings_advice': savings_advice,
            'financial_health': {
                'score': health_score,
                'level': health_level,
                'improvement_suggestions': improvement_suggestions
            }
        }
        
        serializer = RecommendationSerializer(data)
        return Response({
            'code': 200,
            'data': serializer.data
        })