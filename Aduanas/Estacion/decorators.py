from django.shortcuts import redirect
from functools import wraps

def require_role(role):
    """
    Decorador para restringir acceso según el rol del usuario.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if 'usuario_id' not in request.session:
                return redirect('/Estacion/iniciar_sesion/')  # Redirigir si no está autenticado
            if request.session.get('usuario_rol') != role:
                return redirect('/Estacion/desautorizado/')  # Página de acceso denegado
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator