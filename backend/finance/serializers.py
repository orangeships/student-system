from rest_framework import serializers
from .models import FeeCategory, FeeRecord, Payment

class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeCategory
        fields = '__all__'

class FeeRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = FeeRecord
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='fee_record.student.name', read_only=True)
    fee_category = serializers.CharField(source='fee_record.category.name', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'