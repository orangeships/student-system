from django.apps import AppConfig


class AlertsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alerts'
    verbose_name = '预警系统'
    
    def ready(self):
        """导入信号处理器"""
        import alerts.signals