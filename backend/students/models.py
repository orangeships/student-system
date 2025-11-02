from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    student_id = models.CharField('学号', max_length=20, unique=True)
    name = models.CharField('姓名', max_length=50)
    gender = models.CharField('性别', max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField('出生日期', null=True, blank=True)
    phone = models.CharField('联系电话', max_length=20, blank=True)
    email = models.EmailField('邮箱', blank=True)
    address = models.TextField('地址', blank=True)
    major = models.CharField('专业', max_length=100, blank=True)
    grade = models.CharField('年级', max_length=20, blank=True)
    class_name = models.CharField('班级', max_length=50, blank=True)
    enrollment_date = models.DateField('入学日期', null=True, blank=True)
    status = models.CharField('状态', max_length=20, default='active')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student_id} - {self.name}"
