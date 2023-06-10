from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Notification

class Command(BaseCommand):
    help = 'Clean all users in the database'

    def handle(self, *args, **options):
        # Delete all users
        Notification.objects.all().delete()
        print("Notifications have been deleted")