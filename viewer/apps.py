from django.apps import AppConfig


class ViewerConfig(AppConfig):
    # Nastavení automatického generování primárních klíčů pro modely
    default_auto_field = 'django.db.models.BigAutoField'

    # Název aplikace, jak bude odkazována v projektu
    name = 'viewer'
