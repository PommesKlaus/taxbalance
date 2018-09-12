from django.apps import AppConfig


class LocalgaapConfig(AppConfig):
    name = 'ifrs'

    def ready(self):
        import ifrs.signals
