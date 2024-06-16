from django.apps import AppConfig


class StickynotesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stickynotes_app'

    def ready(self):
        import stickynotes_app.signals