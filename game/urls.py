from django.urls import path
from . import views
app_name = 'game'

urlpatterns = [
    path('', views.CampanaView.as_view(), name='campana'),
    path('crear/', views.CampanaCreateView.as_view(), name='campana_create'),
    path('editar/', views.CampanaUpdateView.as_view(), name='campana_update'),
    path('borrar/', views.CampanaDeleteView.as_view(), name='campana_delete'),
    path('personajes/', views.PersonajeListView.as_view(), name='personaje_list'),
    path('personaje/crear/', views.PersonajeCreateView.as_view(), name='personaje_create'),
    path('personaje/<int:pk>/editar/', views.PersonajeUpdateView.as_view(), name='personaje_update'),
    path('personaje/<int:pk>/borrar/', views.PersonajeDeleteView.as_view(), name='personaje_delete'),
    path('enemigos/', views.EnemigoListView.as_view(), name='enemigo_list'),
    path('enemigo/crear/', views.EnemigoCreateView.as_view(), name='enemigo_create'),
    path('enemigo/<int:pk>/editar/', views.EnemigoUpdateView.as_view(), name='enemigo_update'),
    path('enemigo/<int:pk>/borrar/', views.EnemigoDeleteView.as_view(), name='enemigo_delete'),
    path('batalla/', views.batalla_view, name='batalla'),
    path('tema/', views.cambiar_tema, name='cambiar_tema'),
]