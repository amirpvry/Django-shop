from django.apps import AppConfig


class Cart2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart_2'

    def ready(self):
        import cart_2.signals  # سیگنال‌ها را اینجا ایمپورت کنید

