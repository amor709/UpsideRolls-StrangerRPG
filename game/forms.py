from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import PerfilJugador, Campana, Personaje, Enemigo, RegistroAccion
from .models import Campana

User = get_user_model()

class PerfilJugadorForm(forms.ModelForm):
    class Meta:
        model = PerfilJugador
        fields = ['biografia', 'preferencias_dados']
        widgets = {
            'biografia': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'preferencias_dados': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['usuario'].initial = self.user
            self.fields['usuario'].widget = forms.HiddenInput()

    def clean_usuario(self):
        if self.user:
            return self.user
        raise ValidationError("Usuario requerido para crear perfil.")


class CampanaForm(forms.ModelForm):
    class Meta:
        model = Campana
        fields = ['titulo', 'descripcion', 'estado', 'dm']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'dm': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dm'].queryset = User.objects.filter(is_active=True)
        if self.instance and self.instance.pk:
            self.fields['dm'].disabled = True

    def clean_dm(self):
        dm = self.cleaned_data.get('dm')
        if dm and Campana.objects.exclude(pk=self.instance.pk).filter(dm=dm).exists():
            raise ValidationError(f"{dm.username} ya es DM de otra campaña.")
        return dm

class PersonajeForm(forms.ModelForm):
    class Meta:
        model = Personaje
        fields = ['nombre', 'campana', 'vida_maxima', 'vida_actual', 'clase', 'nivel']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'campana': forms.Select(attrs={'class': 'form-control'}),
            'vida_maxima': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'vida_actual': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'clase': forms.TextInput(attrs={'class': 'form-control'}),
            'nivel': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['propietario'].initial = self.user
            self.fields['propietario'].widget = forms.HiddenInput()

    def clean_vida_actual(self):
        vida_actual = self.cleaned_data['vida_actual']
        vida_maxima = self.cleaned_data.get('vida_maxima')
        if vida_maxima and vida_actual > vida_maxima:
            raise ValidationError("Vida actual no puede superar la vida máxima.")
        return vida_actual

    def clean_nivel(self):
        nivel = self.cleaned_data['nivel']
        if nivel < 1 or nivel > 20:
            raise ValidationError("Nivel debe estar entre 1 y 20.")
        return nivel

    def clean(self):
        cleaned_data = super().clean()
        campana = cleaned_data.get('campana')
        propietario = self.user
        nombre = cleaned_data.get('nombre')

        if campana and propietario and not campana.jugadores.filter(id=propietario.id).exists():
            self.add_error('campana', "Debes participar en la campaña para crear un personaje.")

        if campana and nombre and Personaje.objects.filter(nombre=nombre, campana=campana).exists():
            self.add_error('nombre', "Ya existe un personaje con ese nombre en esta campaña.")

        return cleaned_data

class EnemigoForm(forms.ModelForm):
    class Meta:
        model = Enemigo
        fields = ['nombre', 'vida', 'dificultad', 'tipo', 'nota_narrativa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'vida': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'dificultad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'nota_narrativa': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.campana = kwargs.pop('campana', None)
        super().__init__(*args, **kwargs)
        if self.campana:
            self.fields['campana'].initial = self.campana
            self.fields['campana'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        campana = self.campana or cleaned_data.get('campana')
        nombre = cleaned_data.get('nombre')

        if campana and nombre and Enemigo.objects.filter(nombre=nombre, campana=campana).exists():
            self.add_error('nombre', "Ya existe un enemigo con ese nombre en esta campaña.")

        return cleaned_data

class RegistroAccionForm(forms.ModelForm):
    class Meta:
        model = RegistroAccion
        fields = ['tipo_accion', 'tipo_dado', 'resultado_dado', 'modificador', 'dano_curacion']
        widgets = {
            'tipo_accion': forms.Select(attrs={'class': 'form-control'}),
            'tipo_dado': forms.Select(attrs={'class': 'form-control'}),
            'resultado_dado': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'modificador': forms.NumberInput(attrs={'class': 'form-control'}),
            'dano_curacion': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.campana = kwargs.pop('campana', None)
        super().__init__(*args, **kwargs)

        if self.campana:
            self.fields['campana'].initial = self.campana
            self.fields['campana'].widget = forms.HiddenInput()

        if self.user and self.user.groups.filter(name='DM').exists():
            self.fields['enemigo'].widget = forms.Select(attrs={'class': 'form-control'})
        else:
            self.fields['personaje'].required = True
            self.fields['personaje'].widget.attrs['class'] = 'form-control'

    def clean_campana(self):
        campana = self.cleaned_data.get('campana')
        if self.campana:
            return self.campana
        if campana and self.user and not campana.jugadores.filter(id=self.user.id).exists() and not campana.dm == self.user:
            raise ValidationError("No puedes registrar acciones en campañas donde no participas.")
        return campana

    def clean(self):
        cleaned_data = super().clean()
        campana = cleaned_data.get('campana') or self.campana
        tipo_accion = cleaned_data.get('tipo_accion')

        if not campana:
            raise ValidationError("Campaña requerida.")

        if self.user and campana and not (campana.dm == self.user or campana.jugadores.filter(id=self.user.id).exists()):
            raise ValidationError("No autorizado para esta campaña.")

        personaje = cleaned_data.get('personaje')
        enemigo = cleaned_data.get('enemigo')
        if personaje and personaje.campana != campana:
            self.add_error('personaje', "El personaje no pertenece a esta campaña.")
        if enemigo and enemigo.campana != campana:
            self.add_error('enemigo', "El enemigo no pertenece a esta campaña.")

        tipo_dado = cleaned_data.get('tipo_dado')
        resultado = cleaned_data.get('resultado_dado')
        if tipo_dado and resultado:
            max_dado = int(tipo_dado[1:])
            if resultado < 1 or resultado > max_dado:
                self.add_error('resultado_dado', f"Resultado debe estar entre 1 y {max_dado} para {tipo_dado}.")

        return cleaned_data
