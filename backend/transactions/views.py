from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Transaction, TransactionCategory, Budget, FinancialGoal
from .serializers import (
    TransactionSerializer, 
    TransactionCategorySerializer, 
    BudgetSerializer, 
    FinancialGoalSerializer
)


class TransactionCategoryViewSet(viewsets.ModelViewSet):
    queryset = TransactionCategory.objects.all()
    serializer_class = TransactionCategorySerializer
    
    def get_queryset(self):
        return TransactionCategory.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """获取交易统计摘要"""
        today = timezone.now().date()
        this_month = today.replace(day=1)
        
        # 本月收入
        monthly_income = Transaction.objects.filter(
            user=request.user,
            transaction_type='income',
            date__gte=this_month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # 本月支出
        monthly_expense = Transaction.objects.filter(
            user=request.user,
            transaction_type='expense',
            date__gte=this_month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # 净结余
        net_balance = monthly_income - monthly_expense
        
        # 交易总数
        total_transactions = Transaction.objects.filter(user=request.user).count()
        
        return Response({
            'monthly_income': monthly_income,
            'monthly_expense': monthly_expense,
            'net_balance': net_balance,
            'total_transactions': total_transactions
        })
    
    @action(detail=False, methods=['get'])
    def category_stats(self, request):
        """获取分类统计"""
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        queryset = Transaction.objects.filter(user=request.user)
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        stats = queryset.values('category__name', 'transaction_type').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """获取收支趋势"""
        days = int(request.query_params.get('days', 30))
        date_from = timezone.now().date() - timedelta(days=days)
        
        trends = Transaction.objects.filter(
            user=request.user,
            date__gte=date_from
        ).extra(
            select={'day': 'date(date)'}
        ).values('day', 'transaction_type').annotate(
            total=Sum('amount')
        ).order_by('day')
        
        return Response(trends)


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """获取当前生效的预算"""
        today = timezone.now().date()
        budgets = Budget.objects.filter(
            user=request.user,
            is_active=True,
            start_date__lte=today,
            end_date__gte=today
        )
        serializer = self.get_serializer(budgets, many=True)
        return Response(serializer.data)


class FinancialGoalViewSet(viewsets.ModelViewSet):
    queryset = FinancialGoal.objects.all()
    serializer_class = FinancialGoalSerializer
    
    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """更新目标进度"""
        goal = self.get_object()
        amount = request.data.get('amount', 0)
        
        try:
            amount = float(amount)
            goal.current_amount += amount
            goal.save()
            
            serializer = self.get_serializer(goal)
            return Response(serializer.data)
        except (ValueError, TypeError):
            return Response(
                {'error': '无效金额'}, 
                status=status.HTTP_400_BAD_REQUEST
            )