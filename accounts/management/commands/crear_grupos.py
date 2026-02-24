from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        dm_group, _ = Group.objects.get_or_create(name='DM')
        player_group, _ = Group.objects.get_or_create(name='PLAYER')

        dm_perms = Permission.objects.filter(codename__in=[
            'add_campana', 'change_campana', 'view_campana',
            'add_enemigo', 'change_enemigo', 'delete_enemigo', 'view_enemigo',
            'view_registroaccion',
        ])
        dm_group.permissions.set(dm_perms)

        player_perms = Permission.objects.filter(codename__in=[
            'add_personaje', 'change_personaje', 'view_personaje',
            'add_registroaccion', 'view_registroaccion',
            'view_campana',
        ])
        player_group.permissions.set(player_perms)
