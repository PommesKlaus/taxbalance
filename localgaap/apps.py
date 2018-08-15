from django.apps import AppConfig


class LocalgaapConfig(AppConfig):
    name = 'localgaap'

    def ready(self):
        import localgaap.signals
