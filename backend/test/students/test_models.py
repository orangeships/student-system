from django.test import TestCase
from django.contrib.auth.models import User
from students.models import Student
from datetime import date


class StudentModelTest(TestCase):
    """学生模型测试"""
    
    def setUp(self):
        """测试前准备"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_create_student(self):
        """测试创建学生"""
        student = Student.objects.create(
            user=self.user,
            student_id='2024001',
            name='张三',
            gender='M',
            birth_date=date(2000, 1, 1),
            phone='13800138000',
            email='zhangsan@example.com',
            major='计算机科学',
            grade='2024',
            class_name='计科1班',
            enrollment_date=date(2024, 9, 1),
            status='active'
        )
        
        self.assertEqual(student.student_id, '2024001')
        self.assertEqual(student.name, '张三')
        self.assertEqual(student.gender, 'M')
        self.assertEqual(student.major, '计算机科学')
        self.assertEqual(student.status, 'active')
        self.assertTrue(student.created_at)
        self.assertTrue(student.updated_at)
    
    def test_student_str_method(self):
        """测试学生字符串表示"""
        student = Student.objects.create(
            user=self.user,
            student_id='2024002',
            name='李四',
            gender='F'
        )
        
        self.assertEqual(str(student), '2024002 - 李四')
    
    def test_student_gender_choices(self):
        """测试性别选择"""
        # 测试有效性别
        for gender, label in Student.GENDER_CHOICES:
            student = Student.objects.create(
                user=User.objects.create_user(username=f'user_{gender}'),
                student_id=f'2024{gender}',
                name=f'学生{gender}',
                gender=gender
            )
            self.assertEqual(student.gender, gender)
    
    def test_student_default_status(self):
        """测试默认状态"""
        student = Student.objects.create(
            user=self.user,
            student_id='2024003',
            name='王五',
            gender='M'
        )
        
        self.assertEqual(student.status, 'active')
    
    def test_student_ordering(self):
        """测试学生排序"""
        student1 = Student.objects.create(
            user=self.user,
            student_id='2024001',
            name='张三',
            gender='M'
        )
        
        # 等待一下确保时间差
        import time
        time.sleep(0.1)
        
        user2 = User.objects.create_user(username='user2')
        student2 = Student.objects.create(
            user=user2,
            student_id='2024002',
            name='李四',
            gender='F'
        )
        
        students = Student.objects.all()
        self.assertEqual(students[0], student2)  # 最新的在前
        self.assertEqual(students[1], student1)
    
    def test_student_unique_student_id(self):
        """测试学号唯一性"""
        Student.objects.create(
            user=self.user,
            student_id='2024001',
            name='张三',
            gender='M'
        )
        
        user2 = User.objects.create_user(username='user2')
        with self.assertRaises(Exception):
            Student.objects.create(
                user=user2,
                student_id='2024001',  # 重复的学号
                name='李四',
                gender='F'
            )