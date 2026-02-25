from django.contrib import admin
from .models import PerfilJugador, Campana, Personaje, Enemigo, RegistroAccion

@admin.register(PerfilJugador)
class PerfilJugadorAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'biografia']
    search_fields = ['usuario__username', 'biografia']

@admin.register(Campana)
class CampanaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'dm', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion', 'dm']
    search_fields = ['titulo', 'descripcion']
    filter_horizontal = ['jugadores']
    readonly_fields = ['fecha_creacion']

@admin.register(Personaje)
class PersonajeAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'propietario', 'campana', 'vida_actual', 'nivel']
    list_filter = ['campana', 'clase', 'nivel']
    search_fields = ['nombre', 'propietario__username']
    list_editable = ['vida_actual']

@admin.register(Enemigo)
class EnemigoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'campana', 'vida', 'dificultad']
    list_filter = ['campana', 'tipo', 'dificultad']
    search_fields = ['nombre', 'tipo']

class RegistroAccionInline(admin.TabularInline):
    model = RegistroAccion
    fields = ['tipo_accion', 'total', 'exito', 'dano_curacion']
    readonly_fields = ['fecha']
    extra = 0
    ordering = ['-fecha']

@admin.register(RegistroAccion)
class RegistroAccionAdmin(admin.ModelAdmin):
    list_display = ['tipo_accion', 'campana', 'usuario', 'total', 'exito', 'fecha']
    list_filter = ['tipo_accion', 'campana', 'exito', 'fecha']
    search_fields = ['campana__titulo', 'usuario__username']
    date_hierarchy = 'fecha'
    inlines = [RegistroAccionInline]
