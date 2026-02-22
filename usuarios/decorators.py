from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def solo_roles(*roles_permitidos):
    def decorador(vista_func):
        @wraps(vista_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if request.user.rol not in roles_permitidos:
                return HttpResponseForbidden(
                    "No tienes permisos para acceder a esta sección"
                )

            return vista_func(request, *args, **kwargs)
        return _wrapped_view
    return decorador