from django.db import models

class Member(models.Model):
    username = models.CharField()
    email = models.CharField()
    isLoggedIn = models.BooleanField()