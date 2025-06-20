from django.apps import AppConfig


class TeamsAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "teams_app"

    def ready(self):
        import teams_app.signals

        teams_app.signals.signals_imported()
        pass
