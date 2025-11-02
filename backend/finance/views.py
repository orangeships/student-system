from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from .models import FeeCategory, FeeRecord, Payment
from .serializers import FeeCategorySerializer, FeeRecordSerializer, PaymentSerializer

class FeeCategoryViewSet(viewsets.ModelViewSet):
    queryset = FeeCategory.objects.filter(is_active=True)
    serializer_class = FeeCategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'amount', 'created_at']
    ordering = ['name']

class FeeRecordViewSet(viewsets.ModelViewSet):
    queryset = FeeRecord.objects.all()
    serializer_class = FeeRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'student']
    search_fields = ['student__name', 'student__student_id', 'description']
    ordering_fields = ['created_at', 'due_date', 'amount']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total_records = FeeRecord.objects.count()
        pending_records = FeeRecord.objects.filter(status='pending').count()
        paid_records = FeeRecord.objects.filter(status='paid').count()
        
        total_amount = FeeRecord.objects.aggregate(total=Sum('amount'))['total'] or 0
        paid_amount = FeeRecord.objects.filter(status='paid').aggregate(total=Sum('paid_amount'))['total'] or 0
        pending_amount = FeeRecord.objects.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            'total_records': total_records,
            'pending_records': pending_records,
            'paid_records': paid_records,
            'total_amount': total_amount,
            'paid_amount': paid_amount,
            'pending_amount': pending_amount,
            'collection_rate': (paid_amount / total_amount * 100) if total_amount > 0 else 0
        })

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_method', 'fee_record__student']
    search_fields = ['fee_record__student__name', 'transaction_id']
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']
