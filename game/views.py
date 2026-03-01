from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Campana, Personaje, Enemigo, RegistroAccion
from .forms import CampanaForm, PersonajeForm, EnemigoForm
from .mixins import SoloPropietarioMixin, SoloDMMixin
import random
from django.contrib.auth.decorators import login_required

class CampanaView(LoginRequiredMixin, TemplateView):
    template_name = 'game/campana.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campana'] = Campana.objects.first()
        return context

class CampanaCreateView(LoginRequiredMixin, CreateView):
    model = Campana
    form_class = CampanaForm
    template_name = 'game/campana_form.html'

    def dispatch(self, request, *args, **kwargs):
        if Campana.objects.exists():
            messages.warning(request, "Ya existe una campaña, no puedes crear otra.")
            return redirect('game:campana')
        return super().dispatch(request, *args, **kwargs)


    def get_success_url(self):
        return reverse_lazy('game:campana')

class CampanaUpdateView(LoginRequiredMixin, SoloDMMixin, UpdateView):
    model = Campana
    form_class = CampanaForm
    template_name = 'game/campana_form.html'

    def get_object(self, queryset=None):
        return Campana.objects.first()

    def get_success_url(self):
        return reverse_lazy('game:campana')

class CampanaDeleteView(LoginRequiredMixin, SoloDMMixin, DeleteView):
    model = Campana
    template_name = 'game/campana_confirm_delete.html'

    def get_object(self, queryset=None):
        return Campana.objects.first()

    def get_success_url(self):
        return reverse_lazy('game:campana')

class PersonajeListView(LoginRequiredMixin, ListView):
    model = Personaje
    template_name = 'game/personaje_list.html'

    def get_queryset(self):
        campana = Campana.objects.first()
        return campana.personajes_campana.all() if campana else Personaje.objects.none()

class PersonajeCreateView(LoginRequiredMixin, CreateView):
    model = Personaje
    form_class = PersonajeForm
    template_name = "game/crear_personaje.html"

    def dispatch(self, request, *args, **kwargs):
        self.campana = Campana.objects.first()
        if not self.campana:
            messages.warning(request, "No hay ninguna campaña activa. Crea una campaña primero.")
            return redirect('game:campana')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        personaje = form.save(commit=False)
        personaje.propietario = self.request.user
        personaje.campana = self.campana
        personaje.save()
        if self.request.user not in self.campana.jugadores.all():
            self.campana.jugadores.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('game:personaje_list')

class PersonajeUpdateView(LoginRequiredMixin, SoloPropietarioMixin, UpdateView):
    model = Personaje
    form_class = PersonajeForm
    template_name = 'game/personaje_form.html'

    def get_success_url(self):
        return reverse_lazy('game:personaje_list')

class PersonajeDeleteView(LoginRequiredMixin, SoloPropietarioMixin, DeleteView):
    model = Personaje
    template_name = 'game/personaje_confirm_delete.html'
    success_url = reverse_lazy('game:personaje_list')

class EnemigoListView(LoginRequiredMixin, SoloDMMixin, ListView):
    model = Enemigo
    template_name = 'game/enemigo_list.html'

    def get_queryset(self):
        campana = Campana.objects.first()
        return campana.enemigos.all() if campana else Enemigo.objects.none()

class EnemigoCreateView(LoginRequiredMixin, SoloDMMixin, CreateView):
    model = Enemigo
    form_class = EnemigoForm
    template_name = 'game/enemigo_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        campana = Campana.objects.first()
        if not campana:
            raise ValueError("No hay ninguna campaña activa.")
        kwargs['campana'] = campana
        return kwargs

    def get_success_url(self):
        return reverse_lazy('game:enemigo_list')

class EnemigoUpdateView(LoginRequiredMixin, SoloDMMixin, UpdateView):
    model = Enemigo
    form_class = EnemigoForm
    template_name = 'game/enemigo_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['campana'] = Campana.objects.first()
        return kwargs

    def get_success_url(self):
        return reverse_lazy('game:enemigo_list')

class EnemigoDeleteView(LoginRequiredMixin, SoloDMMixin, DeleteView):
    model = Enemigo
    template_name = 'game/enemigo_confirm_delete.html'
    success_url = reverse_lazy('game:enemigo_list')

@login_required
def batalla_view(request):
    campana = Campana.objects.first()
    if not campana:
        messages.warning(request, "No hay campaña activa.")
        return redirect('game:campana')

    if not campana.batalla_activa:
        return render(request, 'game/victoria.html')

    todos_enemigos = campana.enemigos.all()
    enemigos_vivos = todos_enemigos.filter(vida__gt=0)
    personajes_vivos = campana.personajes_campana.filter(vida_actual__gt=0)

    if not todos_enemigos.exists():
        return render(request, 'game/batalla.html', {
            'campana': campana,
            'personajes': personajes_vivos,
            'enemigos': [],
            'turno_usuario': None,
            'historial': []
        })

    if todos_enemigos.exists() and not enemigos_vivos.exists():
        campana.batalla_activa = False
        campana.save()
        return render(request, 'game/victoria.html')

    if not personajes_vivos.exists():
        campana.batalla_activa = False
        campana.save()
        return render(request, 'game/derrota.html')

    historial = campana.registros_acciones.order_by('-fecha')[:50]

    if campana.turno_actual == 'enemigos':
        enemigo_turno = enemigos_vivos[campana.indice_turno % enemigos_vivos.count()]
        objetivo = random.choice(list(personajes_vivos))

        dano = random.randint(1, 8)

        objetivo.vida_actual -= dano
        objetivo.vida_actual = max(objetivo.vida_actual, 0)
        objetivo.save()

        RegistroAccion.objects.create(
            campana=campana,
            usuario=None,
            enemigo=enemigo_turno,
            tipo_accion='ataque',
            tipo_dado='d8',
            resultado_dado=dano,
            modificador=0,
            total=dano,
            exito=True,
            dano_curacion=dano,
            personaje=objetivo
        )

        campana.indice_turno += 1

        if campana.indice_turno >= enemigos_vivos.count():
            campana.turno_actual = 'personajes'
            campana.indice_turno = 0

        campana.save()
        return redirect('game:batalla')

    if request.method == 'POST':
        personaje_turno = personajes_vivos[campana.indice_turno % personajes_vivos.count()]

        if personaje_turno.propietario != request.user:
            messages.error(request, "No es tu turno.")
            return redirect('game:batalla')

        accion_tipo = request.POST.get('accion')
        tipo_dado = request.POST.get('tipo_dado')
        modificador = int(request.POST.get('modificador', 0))
        resultado = random.randint(1, int(tipo_dado[1:]))
        total = resultado + modificador

        if accion_tipo == 'ataque':
            enemigo_id = request.POST.get('enemigo')
            enemigo = get_object_or_404(Enemigo, id=enemigo_id)
            enemigo.vida -= total
            enemigo.vida = max(enemigo.vida, 0)
            enemigo.save()

            RegistroAccion.objects.create(
                campana=campana,
                usuario=request.user,
                tipo_accion='ataque',
                tipo_dado=tipo_dado,
                resultado_dado=resultado,
                modificador=modificador,
                total=total,
                exito=True,
                dano_curacion=total,
                enemigo=enemigo
            )

        elif accion_tipo == 'curacion':
            personaje_turno.vida_actual += total
            personaje_turno.vida_actual = min(personaje_turno.vida_actual, personaje_turno.vida_maxima)
            personaje_turno.save()

            RegistroAccion.objects.create(
                campana=campana,
                usuario=request.user,
                tipo_accion='curacion',
                tipo_dado=tipo_dado,
                resultado_dado=resultado,
                modificador=modificador,
                total=total,
                exito=True,
                dano_curacion=total,
                personaje=personaje_turno
            )

        campana.indice_turno += 1
        if campana.indice_turno >= personajes_vivos.count():
            campana.turno_actual = 'enemigos'
            campana.indice_turno = 0

        campana.save()
        return redirect('game:batalla')

    turno_usuario = None
    if campana.turno_actual == 'personajes':
        turno_usuario = personajes_vivos[campana.indice_turno % personajes_vivos.count()]

    return render(request, 'game/batalla.html', {
        'campana': campana,
        'personajes': personajes_vivos,
        'enemigos': enemigos_vivos,
        'turno_usuario': turno_usuario,
        'historial': historial
    })