from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.views import CustomLogoutView, dashboard
from core.views import dashboard_residente
from django.conf import settings
from django.conf.urls.static import static


# =============================
# DASHBOARD DINÁMICO POR ROL
# =============================
@login_required
def dashboard(request):
    request.user.refresh_from_db()

    if request.user.rol == 'admin':
        template = 'dashboard_admin.html'
    elif request.user.rol == 'seguridad':
        template = 'dashboard_seguridad.html'
    else:
        template = 'dashboard_residente.html'

    return render(request, template, {'user': request.user})


# =============================
# URLS PRINCIPALES
# =============================
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import dashboard, CustomLogoutView, dashboard_residente  # Asegúrate de importar dashboard_residente

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticación
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),

    # Dashboard principal
    path('', dashboard, name='home'),

    # Apps principales
    path('arrendatarios/', include('arrendatarios.urls')),
    path('core/', include('core.urls')),
    path('apartamentos/', include('apartamentos.urls')),
    path('pagos/', include('pagos.urls')),
    path('usuarios/', include('usuarios.urls')),

    # Módulos nuevos de develop (mantenimientos y anuncios)
    path('mantenimientos/', include('mantenimientos.urls')),
    path('anuncios/', include('anuncios.urls')),

    # Módulos existentes
    path('reservas/', include('reservas.urls')),
    path('pqrs/', include('pqrs.urls')),

    # Ruta nueva del panel residente con carrusel (de develop)
    path('dashboard/residente/', dashboard_residente, name='dashboard_residente'),
]

# =============================
# MEDIA FILES
# =============================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)