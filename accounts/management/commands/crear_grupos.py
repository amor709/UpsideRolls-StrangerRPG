from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        dm, created_dm = Group.objects.get_or_create(name='DM')
        player, created_player = Group.objects.get_or_create(name='PLAYER')