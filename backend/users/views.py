from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """用户注册"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # 验证密码强度
            validate_password(serializer.validated_data['password'])
            
            # 创建用户
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            
            # 生成JWT token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'code': 201,
                'message': '注册成功',
                'data': {
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    },
                    'token': str(refresh.access_token)
                }
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({
                'code': 400,
                'message': '密码不符合安全要求',
                'errors': {'password': e.messages}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except IntegrityError:
            return Response({
                'code': 400,
                'message': '用户名或邮箱已存在',
                'errors': {
                    'username': ['该用户名已存在'],
                    'email': ['该邮箱已被注册']
                }
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'code': 400,
        'message': '请求参数错误',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """用户登录"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # 生成JWT token
        refresh = RefreshToken.for_user(user)
        
        # 获取用户月预算（如果有学生档案）
        monthly_budget = None
        try:
            from students.models import Student
            student = Student.objects.get(user=user)
            monthly_budget = getattr(student, 'monthly_budget', None)
        except Student.DoesNotExist:
            pass
        
        return Response({
            'code': 200,
            'message': '登录成功',
            'data': {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'monthly_budget': monthly_budget
                },
                'token': str(refresh.access_token)
            }
        })
    
    return Response({
        'code': 400,
        'message': '登录失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_profile(request):
    """获取当前用户信息"""
    if not request.user.is_authenticated:
        return Response({
            'code': 401,
            'message': '未认证用户'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = UserProfileSerializer(request.user)
    
    # 获取学生扩展信息
    monthly_budget = None
    try:
        from students.models import Student
        student = Student.objects.get(user=request.user)
        monthly_budget = getattr(student, 'monthly_budget', None)
    except Student.DoesNotExist:
        pass
    
    data = serializer.data
    data['monthly_budget'] = monthly_budget
    
    return Response({
        'code': 200,
        'data': data
    })


@api_view(['PUT'])
def update_profile(request):
    """更新用户个人信息"""
    if not request.user.is_authenticated:
        return Response({
            'code': 401,
            'message': '未认证用户'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        
        # 如果提供了月度预算，同时更新学生档案
        monthly_budget = request.data.get('monthly_budget')
        if monthly_budget is not None:
            try:
                from students.models import Student
                student, created = Student.objects.get_or_create(user=request.user)
                student.monthly_budget = monthly_budget
                student.save()
            except Exception:
                pass  # 忽略更新学生档案的错误
        
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': serializer.data
        })
    
    return Response({
        'code': 400,
        'message': '更新失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)