from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['grade', 'class_name', 'major', 'status']
    search_fields = ['name', 'student_id', 'phone', 'email']
    ordering_fields = ['created_at', 'name', 'student_id']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total_students = Student.objects.count()
        active_students = Student.objects.filter(status='active').count()
        
        return Response({
            'total_students': total_students,
            'active_students': active_students,
            'inactive_students': total_students - active_students
        })
