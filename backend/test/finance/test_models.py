from django.test import TestCase
from django.contrib.auth.models import User
from students.models import Student
from finance.models import FeeCategory, FeeRecord, Payment
from datetime import date, datetime


class FinanceModelTest(TestCase):
    """财务模型测试"""
    
    def setUp(self):
        """测试前准备"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.student = Student.objects.create(
            user=self.user,
            student_id='2024001',
            name='张三',
            gender='M'
        )
        
        self.fee_category = FeeCategory.objects.create(
            name='学费',
            description='2024年秋季学期学费',
            amount=5000.00,
            is_active=True
        )
    
    def test_create_fee_category(self):
        """测试创建费用类别"""
        self.assertEqual(self.fee_category.name, '学费')
        self.assertEqual(self.fee_category.amount, 5000.00)
        self.assertEqual(self.fee_category.description, '2024年秋季学期学费')
        self.assertTrue(self.fee_category.is_active)
        self.assertTrue(self.fee_category.created_at)
        self.assertTrue(self.fee_category.updated_at)
    
    def test_fee_category_str_method(self):
        """测试费用类别字符串表示"""
        expected_str = f"{self.fee_category.name}"
        self.assertEqual(str(self.fee_category), expected_str)
    
    def test_create_fee_record(self):
        """测试创建缴费记录"""
        fee_record = FeeRecord.objects.create(
            student=self.student,
            category=self.fee_category,
            amount=5000.00,
            status='pending',
            due_date=date(2024, 9, 1),
            created_by=self.user
        )
        
        self.assertEqual(fee_record.student, self.student)
        self.assertEqual(fee_record.category, self.fee_category)
        self.assertEqual(fee_record.amount, 5000.00)
        self.assertEqual(fee_record.status, 'pending')
        self.assertEqual(fee_record.paid_amount, 0.00)
        self.assertIsNone(fee_record.paid_date)
    
    def test_fee_record_str_method(self):
        """测试缴费记录字符串表示"""
        fee_record = FeeRecord.objects.create(
            student=self.student,
            category=self.fee_category,
            amount=5000.00,
            status='pending',
            due_date=date(2024, 9, 1),
            created_by=self.user
        )
        
        expected_str = f"{self.student.name} - {self.fee_category.name}"
        self.assertEqual(str(fee_record), expected_str)
    
    def test_fee_record_default_values(self):
        """测试缴费记录默认值"""
        fee_record = FeeRecord.objects.create(
            student=self.student,
            category=self.fee_category,
            amount=3000.00,
            due_date=date(2024, 9, 1)
        )
        
        self.assertEqual(fee_record.status, 'pending')
        self.assertEqual(fee_record.paid_amount, 0.00)
    
    def test_fee_record_status_choices(self):
        """测试缴费记录状态选择"""
        for status_choice, label in FeeRecord.STATUS_CHOICES:
            fee_record = FeeRecord.objects.create(
                student=self.student,
                category=self.fee_category,
                amount=1000.00,
                status=status_choice,
                due_date=date(2024, 9, 1),
                created_by=self.user
            )
            self.assertEqual(fee_record.status, status_choice)
    
    def test_create_payment(self):
        """测试创建支付记录"""
        fee_record = FeeRecord.objects.create(
            student=self.student,
            category=self.fee_category,
            amount=5000.00,
            status='pending',
            due_date=date(2024, 9, 1),
            created_by=self.user
        )
        
        payment = Payment.objects.create(
            fee_record=fee_record,
            amount=5000.00,
            payment_method='alipay',
            transaction_id='TXN123456',
            processed_by=self.user
        )
        
        self.assertEqual(payment.fee_record, fee_record)
        self.assertEqual(payment.amount, 5000.00)
        self.assertEqual(payment.payment_method, 'alipay')
        self.assertEqual(payment.transaction_id, 'TXN123456')
        self.assertEqual(payment.processed_by, self.user)
        self.assertTrue(payment.payment_date)
    
    def test_payment_str_method(self):
        """测试支付记录字符串表示"""
        fee_record = FeeRecord.objects.create(
            student=self.student,
            category=self.fee_category,
            amount=5000.00,
            due_date=date(2024, 9, 1),
            created_by=self.user
        )
        
        payment = Payment.objects.create(
            fee_record=fee_record,
            amount=2000.00,
            payment_method='wechat',
            transaction_id='WX123456789',
            processed_by=self.user
        )
        
        expected_str = f"{self.student.name} - {payment.amount}"
        self.assertEqual(str(payment), expected_str)
    
    def test_payment_default_values(self):
        """测试支付记录默认值"""
        fee_record = FeeRecord.objects.create(
            student=self.student,
            category=self.fee_category,
            amount=5000.00,
            due_date=date(2024, 9, 1),
            created_by=self.user
        )
        
        payment = Payment.objects.create(
            fee_record=fee_record,
            amount=1000.00,
            payment_method='alipay'
        )
        
        self.assertFalse(payment.transaction_id)
        self.assertFalse(payment.notes)
    
    def test_payment_method_choices(self):
        """测试支付方式选择"""
        fee_record = FeeRecord.objects.create(
            student=self.student,
            category=self.fee_category,
            amount=5000.00,
            due_date=date(2024, 9, 1),
            created_by=self.user
        )
        
        for method, label in Payment.PAYMENT_METHODS:
            payment = Payment.objects.create(
                fee_record=fee_record,
                amount=500.00,
                payment_method=method,
                processed_by=self.user
            )
            self.assertEqual(payment.payment_method, method)
    

    
    def test_fee_record_ordering(self):
        """测试缴费记录排序"""
        fee_record1 = FeeRecord.objects.create(
            student=self.student,
            category=self.fee_category,
            amount=1000.00,
            due_date=date(2024, 9, 1),
            created_by=self.user
        )
        
        # 等待一下确保时间差
        import time
        time.sleep(0.1)
        
        fee_record2 = FeeRecord.objects.create(
            student=self.student,
            category=self.fee_category,
            amount=2000.00,
            due_date=date(2024, 10, 1),
            created_by=self.user
        )
        
        fee_records = FeeRecord.objects.all()
        self.assertEqual(fee_records[0], fee_record2)  # 最新的在前
        self.assertEqual(fee_records[1], fee_record1)
    
    def test_payment_ordering(self):
        """测试支付记录排序"""
        fee_record = FeeRecord.objects.create(
            student=self.student,
            category=self.fee_category,
            amount=5000.00,
            due_date=date(2024, 9, 1),
            created_by=self.user
        )
        
        payment1 = Payment.objects.create(
            fee_record=fee_record,
            amount=1000.00,
            payment_method='cash',
            processed_by=self.user
        )
        
        # 等待一下确保时间差
        import time
        time.sleep(0.1)
        
        payment2 = Payment.objects.create(
            fee_record=fee_record,
            amount=2000.00,
            payment_method='wechat',
            processed_by=self.user
        )
        
        payments = Payment.objects.all()
        self.assertEqual(payments[0], payment2)  # 最新的在前
        self.assertEqual(payments[1], payment1)