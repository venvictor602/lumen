from django.apps import AppConfig


class AdmissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admissions'

    def ready(self):
        import admissions.signals  # Import the signals

