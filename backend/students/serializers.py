from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
    def validate_student_id(self, value):
        # 如果是更新操作，需要排除当前实例
        if self.instance:
            if Student.objects.filter(student_id=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("该学号已存在")
        else:
            # 创建操作
            if Student.objects.filter(student_id=value).exists():
                raise serializers.ValidationError("该学号已存在")
        return value