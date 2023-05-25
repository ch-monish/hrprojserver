from django.apps import AppConfig
from Scheduler import updatejob

class ManagerolesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manageroles'
    def ready(self):
        print("starting scheduler ................")
        updatejob.start()