from rest_framework import serializers
from .models import Alert, ExportTask


class AlertSerializer(serializers.ModelSerializer):
    """预警序列化器"""
    
    class Meta:
        model = Alert
        fields = [
            'id', 'alert_type', 'title', 'message', 'priority',
            'related_id', 'related_type', 'is_read', 'is_active',
            'created_at', 'expires_at'
        ]
        read_only_fields = ['id', 'created_at', 'is_active']


class AlertListSerializer(serializers.ModelSerializer):
    """预警列表序列化器"""
    
    class Meta:
        model = Alert
        fields = [
            'id', 'alert_type', 'title', 'message', 'priority',
            'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ExportTaskSerializer(serializers.ModelSerializer):
    """导出任务序列化器"""
    
    class Meta:
        model = ExportTask
        fields = [
            'id', 'export_type', 'status', 'format',
            'start_date', 'end_date', 'filters',
            'file_name', 'file_url', 'file_size',
            'created_at', 'completed_at', 'expires_at'
        ]
        read_only_fields = [
            'id', 'status', 'file_name', 'file_url', 
            'file_size', 'created_at', 'completed_at'
        ]


class CreateExportTaskSerializer(serializers.ModelSerializer):
    """创建导出任务序列化器"""
    
    class Meta:
        model = ExportTask
        fields = [
            'export_type', 'format', 'start_date', 
            'end_date', 'filters'
        ]
    
    def validate(self, data):
        """验证导出任务参数"""
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError({
                    'start_date': '开始日期不能晚于结束日期'
                })
        return data


class ExportResponseSerializer(serializers.Serializer):
    """导出响应序列化器"""
    task_id = serializers.IntegerField()
    status = serializers.CharField()
    message = serializers.CharField(required=False)
    
    class Meta:
        fields = ['task_id', 'status', 'message']