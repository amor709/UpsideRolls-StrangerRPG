# views.py
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

    def form_valid(self, form):
        form.instance.dm = self.request.user
        return super().form_valid(form)

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
    template_name = 'game/personaje_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('game:personaje_list')

class PersonajeUpdateView(LoginRequiredMixin, SoloPropietarioMixin, UpdateView):
    model = Personaje
    form_class = PersonajeForm
    template_name = 'game/personaje_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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
        kwargs['campana'] = Campana.objects.first()
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

    jugadores = campana.jugadores.all()
    enemigos = campana.enemigos.all()

    if request.method == 'POST':
        accion_tipo = request.POST.get('tipo_accion')
        objetivo = request.POST.get('objetivo')
        tipo_dado = request.POST.get('tipo_dado')
        modificador = int(request.POST.get('modificador', 0))
        resultado = random.randint(1, int(tipo_dado[1:]))

        if accion_tipo == 'ataque':
            enemigo = get_object_or_404(Enemigo, id=objetivo)
            enemigo.vida -= (resultado + modificador)
            enemigo.vida = max(enemigo.vida, 0)
            enemigo.save()
            RegistroAccion.objects.create(
                campana=campana,
                usuario=request.user,
                tipo_accion='ataque',
                tipo_dado=tipo_dado,
                resultado_dado=resultado,
                modificador=modificador,
                total=resultado+modificador,
                exito=True,
                dano_curacion=resultado+modificador,
                enemigo=enemigo
            )
            messages.success(request, f"Ataque realizado a {enemigo.nombre} con {resultado+modificador} daño!")
        elif accion_tipo == 'curacion':
            personaje = get_object_or_404(Personaje, id=objetivo)
            personaje.vida_actual += (resultado + modificador)
            personaje.vida_actual = min(personaje.vida_actual, personaje.vida_maxima)
            personaje.save()
            RegistroAccion.objects.create(
                campana=campana,
                usuario=request.user,
                tipo_accion='curacion',
                tipo_dado=tipo_dado,
                resultado_dado=resultado,
                modificador=modificador,
                total=resultado+modificador,
                exito=True,
                dano_curacion=resultado+modificador,
                personaje=personaje
            )
            messages.success(request, f"Curación realizada a {personaje.nombre} con {resultado+modificador} puntos!")
        return redirect('game:batalla')

    return render(request, 'game/batalla.html', {
        'campana': campana,
        'jugadores': jugadores,
        'enemigos': enemigos
    })