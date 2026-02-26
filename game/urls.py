from django.urls import path
from .analytics import StatsCampanaView, aplicar_dano

app_name = 'game'

urlpatterns = [
    path('<int:pk>/stats/', StatsCampanaView.as_view(), name='stats_campana'),
    path('personaje/<int:pk>/aplicar_dano/', aplicar_dano, name='aplicar_dano'),
]