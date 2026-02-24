from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

# Importa vistas necesarias
from core.views import dashboard, CustomLogoutView  # dashboard principal y logout personalizado (si lo usas)
from usuarios.views import panel_residente  # ← CORRECTO: usa el nombre real  # ← CORRECCIÓN: importa desde usuarios, NO desde core

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticación
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),  # Usa tu logout personalizado

    # Dashboard principal (dinámico por rol)
    path('', dashboard, name='home'),

    # Ruta específica del panel residente (con carrusel de anuncios)
    path('dashboard/residente/', panel_residente, name='dashboard_residente'),

    # Apps principales
    path('arrendatarios/', include('arrendatarios.urls')),
    path('core/', include('core.urls')),
    path('apartamentos/', include('apartamentos.urls')),
    path('pagos/', include('pagos.urls')),
    path('usuarios/', include('usuarios.urls')),

    # Módulos nuevos (de develop)
    path('mantenimientos/', include('mantenimientos.urls')),
    path('anuncios/', include('anuncios.urls')),

    # Módulos existentes
    path('reservas/', include('reservas.urls')),
    path('pqrs/', include('pqrs.urls')),
]

# Servir media en desarrollo (DEBUG = True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)