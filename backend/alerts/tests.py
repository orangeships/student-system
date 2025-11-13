from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Alert, ExportTask

User = get_user_model()


class AlertModelTest(TestCase):
    """预警模型测试"""
    
    def setUp(self):
        """测试设置"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_alert_creation(self):
        """测试预警创建"""
        alert = Alert.objects.create(
            user=self.user,
            alert_type='budget',
            title='测试预警',
            message='这是一个测试预警消息',
            priority='medium'
        )
        
        self.assertEqual(alert.user, self.user)
        self.assertEqual(alert.alert_type, 'budget')
        self.assertEqual(alert.title, '测试预警')
        self.assertEqual(alert.message, '这是一个测试预警消息')
        self.assertEqual(alert.priority, 'medium')
        self.assertFalse(alert.is_read)
        self.assertTrue(alert.is_active)
    
    def test_alert_str_representation(self):
        """测试预警字符串表示"""
        alert = Alert.objects.create(
            user=self.user,
            alert_type='budget',
            title='测试预警',
            message='测试消息',
            priority='medium'
        )
        
        self.assertEqual(str(alert), f"测试预警 ({self.user.username})")


class ExportTaskModelTest(TestCase):
    """导出任务模型测试"""
    
    def setUp(self):
        """测试设置"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_export_task_creation(self):
        """测试导出任务创建"""
        task = ExportTask.objects.create(
            user=self.user,
            export_type='transactions',
            format='csv'
        )
        
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.export_type, 'transactions')
        self.assertEqual(task.format, 'csv')
        self.assertEqual(task.status, 'pending')
        self.assertFalse(task.file_name)
        self.assertFalse(task.file_url)
    
    def test_export_task_str_representation(self):
        """测试导出任务字符串表示"""
        task = ExportTask.objects.create(
            user=self.user,
            export_type='transactions',
            format='csv'
        )
        
        self.assertEqual(str(task), f"导出任务 {task.id} ({self.user.username})")


class AlertAPITest(APITestCase):
    """预警API测试"""
    
    def setUp(self):
        """测试设置"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_alert_list(self):
        """测试获取预警列表"""
        Alert.objects.create(
            user=self.user,
            alert_type='budget',
            title='测试预警',
            message='测试消息',
            priority='medium'
        )
        
        url = reverse('alert-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200)
        self.assertEqual(len(response.data['data']), 1)
    
    def test_mark_alert_as_read(self):
        """测试标记预警已读"""
        alert = Alert.objects.create(
            user=self.user,
            alert_type='budget',
            title='测试预警',
            message='测试消息',
            priority='medium',
            is_read=False
        )
        
        url = reverse('alert-read', kwargs={'pk': alert.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200)
        
        alert.refresh_from_db()
        self.assertTrue(alert.is_read)
    
    def test_get_unread_alerts(self):
        """测试获取未读预警"""
        # 创建一个已读预警
        Alert.objects.create(
            user=self.user,
            alert_type='budget',
            title='已读预警',
            message='测试消息',
            priority='medium',
            is_read=True
        )
        
        # 创建一个未读预警
        Alert.objects.create(
            user=self.user,
            alert_type='budget',
            title='未读预警',
            message='测试消息',
            priority='medium',
            is_read=False
        )
        
        url = reverse('alert-unread')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['title'], '未读预警')


class ExportTaskAPITest(APITestCase):
    """导出任务API测试"""
    
    def setUp(self):
        """测试设置"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_export_task(self):
        """测试创建导出任务"""
        url = reverse('export-task-list')
        data = {
            'export_type': 'transactions',
            'format': 'csv',
            'filters': {}
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['code'], 200)
        self.assertEqual(response.data['data']['export_type'], 'transactions')
        self.assertEqual(response.data['data']['format'], 'csv')
    
    def test_get_export_task_list(self):
        """测试获取导出任务列表"""
        ExportTask.objects.create(
            user=self.user,
            export_type='transactions',
            format='csv'
        )
        
        url = reverse('export-task-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200)
        self.assertEqual(len(response.data['data']), 1)
    
    def test_export_options(self):
        """测试获取导出选项"""
        url = reverse('export-task-export-options')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 200)
        self.assertIn('export_types', response.data['data'])
        self.assertIn('format_options', response.data['data'])
        self.assertIn('date_range_options', response.data['data'])