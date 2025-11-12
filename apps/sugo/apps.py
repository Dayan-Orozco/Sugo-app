from django.apps import AppConfig


class SugoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sugo'
    
    def ready(self):
        import apps.sugo.signals  