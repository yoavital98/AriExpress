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
        service.logIn("aaa", "asdf1233")
        service.createStore("aaa", "store123")
        service.createStore("aaa", "456store")
        service.addNewProductToStore("aaa", "store123", "apple", "fruit", "20", "3")
        service.addNewProductToStore("aaa", "store123", "banana", "fruit", "30", "8")
        service.addNewProductToStore("aaa", "store123", "headphones", "electronics", "10", "700")
        service.logOut("aaa")
        # from django.contrib.auth.models import User
        # users = User.objects.all()
        # for i in range(1, len(users)):
        #     User.objects.all()[i].delete()
