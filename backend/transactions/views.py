from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q, Count, Avg
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404
from .models import Transaction, TransactionCategory, Budget, FinancialGoal, Alert, ExportTask
from .serializers import (
    TransactionSerializer, 
    TransactionCategorySerializer, 
    BudgetSerializer, 
    FinancialGoalSerializer,
    AlertSerializer,
    AlertListSerializer,
    ExportTaskSerializer,
    CreateExportTaskSerializer,
    ExportResponseSerializer
)


class TransactionCategoryViewSet(viewsets.ModelViewSet):
    queryset = TransactionCategory.objects.all()
    serializer_class = TransactionCategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TransactionCategory.objects.filter(created_by=self.request.user, is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['type'] = self.request.query_params.get('type')
        return context


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """获取交易记录列表 - 支持分页和筛选"""
        queryset = self.get_queryset()
        
        # 筛选参数
        transaction_type = request.query_params.get('type')
        category = request.query_params.get('category')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        if category:
            queryset = queryset.filter(category__name=category)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'data': {
                'transactions': serializer.data,
                'pagination': {
                    'total': queryset.count(),
                    'page': 1,
                    'page_size': 20,
                    'total_pages': 1
                }
            }
        })
    
    def create(self, request, *args, **kwargs):
        """创建交易记录"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'code': 201,
                'message': '交易记录创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': 400,
            'message': '创建失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """更新交易记录"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 200,
                'message': '交易记录更新成功',
                'data': serializer.data
            })
        return Response({
            'code': 400,
            'message': '更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """删除交易记录"""
        instance = self.get_object()
        instance.delete()
        return Response({
            'code': 200,
            'message': '交易记录删除成功'
        })
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """获取交易统计摘要"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = self.get_queryset()
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # 计算总收入和总支出
        income_total = queryset.filter(transaction_type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        expense_total = queryset.filter(transaction_type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # 计算交易数量
        transaction_count = queryset.count()
        income_count = queryset.filter(transaction_type='income').count()
        expense_count = queryset.filter(transaction_type='expense').count()
        
        summary_data = {
            'total_income': float(income_total),
            'total_expense': float(expense_total),
            'net_income': float(income_total - expense_total),
            'transaction_count': transaction_count,
            'income_count': income_count,
            'expense_count': expense_count,
            'start_date': start_date,
            'end_date': end_date
        }
        
        return Response({
            'code': 200,
            'data': summary_data
        })
    
    @action(detail=False, methods=['get'])
    def category_trends(self, request):
        """获取分类趋势数据"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        transaction_type = request.query_params.get('transaction_type', 'expense')
        
        queryset = self.get_queryset().filter(transaction_type=transaction_type)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # 按分类统计
        category_stats = queryset.values('category__name').annotate(
            total_amount=Sum('amount'),
            transaction_count=Count('id')
        ).order_by('-total_amount')
        
        trends_data = [
            {
                'category': item['category__name'] or '未分类',
                'total_amount': float(item['total_amount']),
                'transaction_count': item['transaction_count'],
                'percentage': 0  # 前端可以计算百分比
            }
            for item in category_stats
        ]
        
        return Response({
            'code': 200,
            'data': trends_data
        })
    
    @action(detail=False, methods=['get'])
    def monthly_trends(self, request):
        """获取月度趋势数据"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = self.get_queryset()
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # 按月份统计
        monthly_stats = queryset.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            income_total=Sum('amount', filter=Q(transaction_type='income')),
            expense_total=Sum('amount', filter=Q(transaction_type='expense')),
            transaction_count=Count('id')
        ).order_by('month')
        
        trends_data = []
        for item in monthly_stats:
            month_str = item['month'].strftime('%Y-%m')
            trends_data.append({
                'month': month_str,
                'income': float(item['income_total'] or 0),
                'expense': float(item['expense_total'] or 0),
                'transaction_count': item['transaction_count']
            })
        
        return Response({
            'code': 200,
            'data': trends_data
        })


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user, is_active=True)
    
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
        return Response({
            'code': 200,
            'data': serializer.data
        })


class FinancialGoalViewSet(viewsets.ModelViewSet):
    queryset = FinancialGoal.objects.all()
    serializer_class = FinancialGoalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user, is_active=True)
    
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
            return Response({
                'code': 200,
                'message': '进度更新成功',
                'data': serializer.data
            })
        except (ValueError, TypeError):
            return Response({
                'code': 400,
                'message': '无效金额'
            }, status=status.HTTP_400_BAD_REQUEST)


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user, is_active=True)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AlertListSerializer
        return AlertSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """标记预警为已读"""
        alert = self.get_object()
        alert.is_read = True
        alert.save()
        
        serializer = self.get_serializer(alert)
        return Response({
            'code': 200,
            'message': '预警已标记为已读',
            'data': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """获取未读预警"""
        alerts = Alert.objects.filter(user=request.user, is_read=False, is_active=True)
        serializer = self.get_serializer(alerts, many=True)
        return Response({
            'code': 200,
            'data': serializer.data
        })
    
    def list(self, request, *args, **kwargs):
        """获取预警列表"""
        alerts = self.get_queryset()
        
        # 筛选参数
        alert_type = request.query_params.get('type')
        priority = request.query_params.get('priority')
        is_read = request.query_params.get('is_read')
        
        if alert_type:
            alerts = alerts.filter(alert_type=alert_type)
        if priority:
            alerts = alerts.filter(priority=priority)
        if is_read is not None:
            is_read_bool = is_read.lower() in ('true', '1', 'yes')
            alerts = alerts.filter(is_read=is_read_bool)
        
        serializer = self.get_serializer(alerts, many=True)
        return Response({
            'code': 200,
            'data': serializer.data
        })


class ExportTaskViewSet(viewsets.ModelViewSet):
    queryset = ExportTask.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ExportTask.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateExportTaskSerializer
        elif self.action == 'create_export':
            return ExportResponseSerializer
        return ExportTaskSerializer
    
    @action(detail=False, methods=['post'])
    def create_export(self, request):
        """创建数据导出任务"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            export_task = serializer.save(user=request.user)
            
            # 模拟异步处理
            return Response({
                'code': 201,
                'message': '导出任务已创建',
                'data': {
                    'task_id': export_task.id,
                    'status': export_task.status,
                    'file_url': export_task.file_url if export_task.file_url else None
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': 400,
            'message': '创建失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """下载导出文件"""
        export_task = self.get_object()
        
        if export_task.status != 'completed':
            return Response({
                'code': 400,
                'message': '导出任务未完成，无法下载'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not export_task.file_url:
            return Response({
                'code': 404,
                'message': '文件不存在'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'code': 200,
            'message': '文件下载链接',
            'data': {
                'download_url': export_task.file_url,
                'expires_at': export_task.expires_at.isoformat() if export_task.expires_at else None
            }
        })
    
    def list(self, request, *args, **kwargs):
        """获取导出任务列表"""
        tasks = self.get_queryset()
        
        # 筛选参数
        status_filter = request.query_params.get('status')
        
        if status_filter:
            tasks = tasks.filter(status=status_filter)
        
        serializer = self.get_serializer(tasks, many=True)
        return Response({
            'code': 200,
            'data': serializer.data
        })