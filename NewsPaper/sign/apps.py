from django.apps import AppConfig

class signConfig(AppConfig):
    name = 'sign'

    def ready(self):
        import sign.signals