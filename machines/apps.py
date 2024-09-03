from django.apps import AppConfig


class MachinesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'machines'

    def ready(self):
        # Import signal handlers
        import machines.signals
