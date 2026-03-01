from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from game.models import Campana, Enemigo, Personaje, RegistroAccion


class Command(BaseCommand):
    help = 'Configura grupos DM y PLAYER con permisos del sistema'

    def handle(self, *args, **kwargs):

        dm_group, _ = Group.objects.get_or_create(name='DM')
        player_group, _ = Group.objects.get_or_create(name='PLAYER')

        # Permisos DM
        dm_models = [Campana, Enemigo, RegistroAccion]
        dm_perms = Permission.objects.filter(
            content_type__in=[
                ContentType.objects.get_for_model(m)
                for m in dm_models
            ]
        )
        dm_group.permissions.set(dm_perms)

        # Permisos PLAYER
        player_models = [Personaje, RegistroAccion, Campana]
        player_perms = Permission.objects.filter(
            content_type__in=[
                ContentType.objects.get_for_model(m)
                for m in player_models
            ]
        )
        player_group.permissions.set(player_perms)

        self.stdout.write(
            self.style.SUCCESS('Grupos DM y PLAYER configurados correctamente.')
        )