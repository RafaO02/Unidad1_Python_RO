from django.apps import AppConfig


class DispositivosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dispositivos'

    def ready(self):
        import dispositivos.signal  # Importa el archivo signals.py