from django.apps import AppConfig


class ViewerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'viewer'


class ViewerConfig(AppConfig):
    name = 'viewer'

    def ready(self):
        import viewer.signals

