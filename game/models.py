from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

User = get_user_model()

class PerfilJugador(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_jugador',
        related_query_name='perfil'
    )
    biografia = models.TextField(blank=True, max_length=500)
    preferencias_dados = models.CharField(max_length=100, blank=True, help_text="Ej: 'prefiero d20'")

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

class Campana(models.Model):
    ESTADOS = [
        ('activa', 'Activa'),
        ('pausada', 'Pausada'),
        ('finalizada', 'Finalizada'),
    ]
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    dm = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='campanas_dirigidas',
        related_query_name='dm_campana'
    )
    jugadores = models.ManyToManyField(
        User,
        related_name='campanas_participadas',
        related_query_name='jugador_campana',
        blank=True
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activa')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Personaje(models.Model):
    nombre = models.CharField(max_length=100)
    propietario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='personajes'
    )
    campana = models.ForeignKey(
        Campana,
        on_delete=models.CASCADE,
        related_name='personajes_campana',
        related_query_name='personaje_campana'
    )
    vida_maxima = models.PositiveIntegerField(default=100)
    vida_actual = models.PositiveIntegerField(default=100)
    clase = models.CharField(max_length=50, default='Guerrero')
    nivel = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('nombre', 'campana')

    def clean(self):
        if self.vida_actual > self.vida_maxima:
            raise ValidationError("Vida actual no puede superar máxima.") [web:17]

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.clase} lvl {self.nivel})"

class Enemigo(models.Model):
    nombre = models.CharField(max_length=100)
    campana = models.ForeignKey(
        Campana,
        on_delete=models.CASCADE,
        related_name='enemigos',
        related_query_name='enemigo_campana'
    )
    vida = models.PositiveIntegerField(default=50)
    dificultad = models.PositiveIntegerField(default=1)
    tipo = models.CharField(max_length=50, default='Monstruo')
    nota_narrativa = models.TextField(blank=True)

    class Meta:
        unique_together = ('nombre', 'campana')

    def __str__(self):
        return f"{self.nombre} (Dificultad {self.dificultad})"

class RegistroAccion(models.Model):
    TIPOS_ACCION = [('ataque', 'Ataque'), ('curacion', 'Curación'), ('otros', 'Otros')]
    TIPO_DADO_CHOICES = [('d20', 'D20'), ('d6', 'D6'), ('d8', 'D8'), ('d10', 'D10'), ('d12', 'D12')]
    campana = models.ForeignKey(
        Campana,
        on_delete=models.CASCADE,
        related_name='registros_acciones'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='acciones_realizadas'
    )
    personaje = models.ForeignKey(
        Personaje,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='acciones_personaje'
    )
    enemigo = models.ForeignKey(
        Enemigo,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='acciones_enemigo'
    )
    tipo_accion = models.CharField(max_length=20, choices=TIPOS_ACCION)
    tipo_dado = models.CharField(max_length=10, choices=TIPO_DADO_CHOICES)
    resultado_dado = models.PositiveIntegerField()
    modificador = models.IntegerField(default=0)
    total = models.IntegerField()
    exito = models.BooleanField()
    dano_curacion = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total = self.resultado_dado + self.modificador
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo_accion}: {self.total}"
