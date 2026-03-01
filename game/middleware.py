import time
from django.urls import resolve
from .models import Campana


class RegistroAccesoCampanaMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        try:
            if request.user.is_authenticated:
                ruta_actual = resolve(request.path_info).url_name
                campana = None

                if request.resolver_match and 'pk' in request.resolver_match.kwargs:
                    campana = Campana.objects.filter(
                        pk=request.resolver_match.kwargs['pk']
                    ).first()

                tiempo_respuesta = round((time.time() - start_time) * 1000, 2)

                print(
                    f"[AccesoCampana] Usuario: {request.user.username}, "
                    f"Ruta: {ruta_actual}, "
                    f"Campaña: {campana}, "
                    f"Tiempo: {tiempo_respuesta}ms"
                )

        except Exception as e:
            print(f"[MiddlewareError] {e}")

        return response