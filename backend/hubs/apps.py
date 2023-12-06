from django.apps import AppConfig


class HubsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hubs'
    verbose_name = 'Хабр'

    def ready(self):
        import hubs.signals
