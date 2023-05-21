from django.apps import AppConfig
from ProjectCode.Service.Service import Service






class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainApp'
    def ready(self):
        service = Service()
        service.register("aaa", "asdf1233", "a@a.com") # for debug only
        service.register("bbb", "asdf1233", "a@a.com") # for debug only
        service.register("rubin_krief", "h9reynWq", "roobink@post.bgu.ac.il") # for debug only

        # from django.contrib.auth.models import User
        # users = User.objects.all()
        # for i in range(1, len(users)):
        #     User.objects.all()[i].delete()
