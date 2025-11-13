from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q
from .models import Alert, ExportTask
from .serializers import (
    AlertSerializer, AlertListSerializer, 
    ExportTaskSerializer, CreateExportTaskSerializer, ExportResponseSerializer
)


class AlertViewSet(viewsets.ModelViewSet):
    """
    预警管理视图集
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """获取当前用户的预警列表"""
        return Alert.objects.filter(user=self.request.user, is_active=True)
    
    def get_serializer_class(self):
        """根据动作选择序列化器"""
        if self.action == 'list':
            return AlertListSerializer
        return AlertSerializer
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """获取未读预警列表"""
        queryset = self.get_queryset().filter(is_read=False)
        serializer = AlertListSerializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取未读预警成功',
            'data': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def read(self, request, pk=None):
        """标记预警已读"""
        alert = self.get_object()
        alert.is_read = True
        alert.save(update_fields=['is_read'])
        
        return Response({
            'code': 200,
            'message': '预警已标记为已读',
            'data': {
                'id': alert.id,
                'is_read': alert.is_read
            }
        })
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """标记所有预警为已读"""
        updated_count = self.get_queryset().filter(is_read=False).update(is_read=True)
        
        return Response({
            'code': 200,
            'message': f'已标记{updated_count}条预警为已读',
            'data': {
                'updated_count': updated_count
            }
        })
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """停用预警"""
        alert = self.get_object()
        alert.is_active = False
        alert.save(update_fields=['is_active'])
        
        return Response({
            'code': 200,
            'message': '预警已停用',
            'data': {
                'id': alert.id,
                'is_active': alert.is_active
            }
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取预警统计信息"""
        queryset = self.get_queryset()
        
        # 按类型统计
        type_stats = {}
        for choice in Alert.ALERT_TYPE_CHOICES:
            count = queryset.filter(alert_type=choice[0]).count()
            type_stats[choice[0]] = {
                'name': choice[1],
                'count': count
            }
        
        # 按优先级统计
        priority_stats = {}
        for choice in Alert.PRIORITY_CHOICES:
            count = queryset.filter(priority=choice[0]).count()
            priority_stats[choice[0]] = {
                'name': choice[1],
                'count': count
            }
        
        # 未读数量
        unread_count = queryset.filter(is_read=False).count()
        
        return Response({
            'code': 200,
            'message': '获取预警统计成功',
            'data': {
                'total_count': queryset.count(),
                'unread_count': unread_count,
                'type_stats': type_stats,
                'priority_stats': priority_stats
            }
        })


class ExportTaskViewSet(viewsets.ModelViewSet):
    """
    数据导出任务视图集
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """获取当前用户的导出任务列表"""
        return ExportTask.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """根据动作选择序列化器"""
        if self.action == 'create':
            return CreateExportTaskSerializer
        return ExportTaskSerializer
    
    def perform_create(self, serializer):
        """创建导出任务"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """下载导出文件"""
        task = self.get_object()
        
        if task.status != 'completed':
            return Response({
                'code': 400,
                'message': '导出任务尚未完成'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not task.file_url:
            return Response({
                'code': 400,
                'message': '文件链接不存在'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if task.expires_at and task.expires_at < timezone.now():
            return Response({
                'code': 400,
                'message': '文件下载链接已过期'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'code': 200,
            'message': '获取下载链接成功',
            'data': {
                'download_url': task.file_url,
                'file_name': task.file_name,
                'file_size': task.file_size
            }
        })
    
    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        """重试失败的导出任务"""
        task = self.get_object()
        
        if task.status != 'failed':
            return Response({
                'code': 400,
                'message': '只能重试失败的任务'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 重置任务状态
        task.status = 'pending'
        task.save(update_fields=['status'])
        
        # 这里应该触发实际的导出任务处理逻辑
        # 现在模拟任务处理
        return Response({
            'code': 200,
            'message': '导出任务已重新开始处理',
            'data': {
                'task_id': task.id,
                'status': task.status
            }
        })
    
    @action(detail=False, methods=['get'])
    def export_options(self, request):
        """获取导出选项"""
        # 获取用户的可用数据
        from transactions.models import Transaction, Budget, FinancialGoal
        
        # 交易记录统计
        transaction_count = Transaction.objects.filter(
            user=request.user
        ).count()
        
        # 预算统计
        budget_count = Budget.objects.filter(
            user=request.user
        ).count()
        
        # 目标统计
        goal_count = FinancialGoal.objects.filter(
            user=request.user
        ).count()
        
        # 预警统计
        alert_count = Alert.objects.filter(
            user=request.user, is_active=True
        ).count()
        
        return Response({
            'code': 200,
            'message': '获取导出选项成功',
            'data': {
                'export_types': [
                    {
                        'value': 'transactions',
                        'name': '交易记录',
                        'count': transaction_count,
                        'available': transaction_count > 0
                    },
                    {
                        'value': 'budgets',
                        'name': '预算数据',
                        'count': budget_count,
                        'available': budget_count > 0
                    },
                    {
                        'value': 'goals',
                        'name': '目标数据',
                        'count': goal_count,
                        'available': goal_count > 0
                    },
                    {
                        'value': 'alerts',
                        'name': '预警数据',
                        'count': alert_count,
                        'available': alert_count > 0
                    }
                ],
                'format_options': [
                    {'value': 'csv', 'name': 'CSV文件'},
                    {'value': 'excel', 'name': 'Excel文件'},
                    {'value': 'pdf', 'name': 'PDF文件'}
                ],
                'date_range_options': [
                    {'value': '7d', 'name': '最近7天'},
                    {'value': '30d', 'name': '最近30天'},
                    {'value': '90d', 'name': '最近90天'},
                    {'value': '1y', 'name': '最近1年'},
                    {'value': 'all', 'name': '全部'}
                ]
            }
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取导出任务统计信息"""
        queryset = self.get_queryset()
        
        # 按状态统计
        status_stats = {}
        for choice in ExportTask.STATUS_CHOICES:
            count = queryset.filter(status=choice[0]).count()
            status_stats[choice[0]] = {
                'name': choice[1],
                'count': count
            }
        
        # 按格式统计
        format_stats = {}
        for choice in ExportTask.FORMAT_CHOICES:
            count = queryset.filter(format=choice[0]).count()
            format_stats[choice[0]] = {
                'name': choice[1],
                'count': count
            }
        
        # 最近任务
        recent_tasks = queryset[:10]
        
        return Response({
            'code': 200,
            'message': '获取导出任务统计成功',
            'data': {
                'total_count': queryset.count(),
                'status_stats': status_stats,
                'format_stats': format_stats,
                'recent_tasks': ExportTaskSerializer(recent_tasks, many=True).data
            }
        })