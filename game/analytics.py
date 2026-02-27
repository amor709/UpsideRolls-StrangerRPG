from django.db.models import Q, F, Count, Avg, Sum, Max
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db import transaction
from .models import Campana, Personaje, RegistroAccion


class StatsCampanaView(LoginRequiredMixin, TemplateView):
    template_name = 'game/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']

        campana = Campana.objects.select_related(
            'dm'
        ).prefetch_related(
            'jugadores',
            'personajes_campana',
            'registros_acciones'
        ).get(pk=pk)

        personajes = campana.personajes_campana.annotate(
            total_acciones=Count('acciones_personaje'),
            dano_total=Sum(
                'acciones_personaje__dano_curacion',
                filter=Q(acciones_personaje__tipo_accion='ataque')
            ),
            curacion_total=Sum(
                'acciones_personaje__dano_curacion',
                filter=Q(acciones_personaje__tipo_accion='curacion')
            )
        )

        stats = RegistroAccion.objects.filter(
            campana=campana
        ).aggregate(
            total_acciones=Count('id'),
            media_tirada=Avg('total'),
            max_dano=Max('dano_curacion'),
            total_dano=Sum(
                'dano_curacion',
                filter=Q(tipo_accion='ataque')
            ),
            total_curacion=Sum(
                'dano_curacion',
                filter=Q(tipo_accion='curacion')
            )
        )

        texto = self.request.GET.get('q')

        logs_filtrados = RegistroAccion.objects.select_related(
            'usuario',
            'personaje',
            'enemigo'
        ).filter(
            campana=campana
        ).filter(
            Q(tipo_accion='ataque') | Q(tipo_accion='curacion')
        ).filter(
            Q(exito=True)
        )

        if texto:
            logs_filtrados = logs_filtrados.filter(
                Q(personaje__nombre__icontains=texto) |
                Q(enemigo__nombre__icontains=texto)
            )

        context.update({
            'campana': campana,
            'personajes': personajes,
            'stats': stats,
            'logs_exito': logs_filtrados.count(),
        })

        return context


@transaction.atomic
def aplicar_dano(request, pk):
    dano = int(request.POST.get('dano', 0))

    Personaje.objects.filter(
        pk=pk,
        propietario=request.user
    ).update(
        vida_actual=F('vida_actual') - dano
    )

    return redirect('personaje_detail', pk=pk)