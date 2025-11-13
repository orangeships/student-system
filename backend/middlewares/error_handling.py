"""
统一的错误处理中间件
"""
import logging
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.db import DatabaseError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied as DRFPermissionDenied,
    NotFound,
    MethodNotAllowed
)
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class APIErrorHandlerMiddleware:
    """
    API统一错误处理中间件
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        """
        处理异常并返回统一的错误响应
        """
        error_code = 500
        message = "内部服务器错误"
        errors = {}
        
        # 处理不同类型的异常
        if isinstance(exception, (AuthenticationFailed, NotAuthenticated)):
            error_code = 401
            message = "身份认证失败"
            logger.warning(f"Authentication failed for {request.user}")
            
        elif isinstance(exception, (PermissionDenied, DRFPermissionDenied)):
            error_code = 403
            message = "权限不足"
            logger.warning(f"Permission denied for {request.user} on {request.path}")
            
        elif isinstance(exception, NotFound):
            error_code = 404
            message = "资源不存在"
            logger.info(f"Resource not found: {request.path}")
            
        elif isinstance(exception, MethodNotAllowed):
            error_code = 405
            message = "方法不允许"
            errors = {"method": [f"HTTP方法 {exception.args[0] if exception.args else '未知'} 不被允许"]}
            
        elif isinstance(exception, ValidationError):
            error_code = 400
            message = "请求参数错误"
            errors = exception.detail if hasattr(exception, 'detail') else {"detail": [str(exception)]}
            logger.warning(f"Validation error: {exception}")
            
        elif isinstance(exception, DjangoValidationError):
            error_code = 400
            message = "数据验证错误"
            errors = {"validation": exception.messages}
            
        elif isinstance(exception, DatabaseError):
            error_code = 500
            message = "数据库操作错误"
            logger.error(f"Database error: {exception}", exc_info=True)
            
        elif isinstance(exception, ValueError):
            error_code = 400
            message = "参数值错误"
            errors = {"value": [str(exception)]}
            logger.warning(f"Value error: {exception}")
            
        else:
            # 未预期的异常
            logger.error(f"Unexpected error: {exception}", exc_info=True)
            message = "发生了未知错误"
            errors = {"detail": [str(exception)]}
        
        # 构建错误响应
        error_response = {
            "code": error_code,
            "message": message,
            "errors": errors if errors else None,
            "path": request.path,
            "method": request.method,
            "timestamp": request.META.get('HTTP_X_TIMESTAMP', 'N/A')
        }
        
        return JsonResponse(error_response, status=error_code)


class APILoggingMiddleware:
    """
    API请求日志中间件
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 记录请求
        if request.path.startswith('/api/'):
            logger.info(f"API Request: {request.method} {request.path} - User: {getattr(request, 'user', 'Anonymous')}")
        
        response = self.get_response(request)
        
        # 记录响应
        if request.path.startswith('/api/'):
            logger.info(f"API Response: {response.status_code} {request.method} {request.path}")
        
        return response