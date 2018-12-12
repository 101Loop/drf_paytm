from django.apps import AppConfig


class DrfPaytmConfig(AppConfig):
    name = 'drf_paytm'
    verbose_name = "PayTM | Django REST Framework"

    def ready(self):
        from .signals.handlers import transaction_response_handler
