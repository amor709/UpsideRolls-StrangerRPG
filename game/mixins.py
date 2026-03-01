from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .models import Campana

class SoloPropietarioMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.propietario == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied("No tienes permiso para modificar este objeto.")

class SoloDMMixin(UserPassesTestMixin):
    def test_func(self):
        campana = Campana.objects.first()
        return campana and self.request.user == campana.dm