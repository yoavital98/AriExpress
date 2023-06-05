from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Clean all users in the database'

    def handle(self, *args, **options):
        # Delete all users
        User.objects.filter(username__startswith='GuestUser').delete()
        print("Guests have been deleted")