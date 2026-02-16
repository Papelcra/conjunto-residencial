from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.views import CustomLogoutView



# Vista del dashboard dinámico por rol
@login_required
def dashboard(request):
    if request.user.es_admin:
        template = 'dashboard_admin.html'
    elif request.user.es_seguridad:
        template = 'dashboard_seguridad.html'
    else:
        template = 'dashboard_residente.html'
    return render(request, template, {'user': request.user})

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticación
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),

    # Ruta raíz
    path('', dashboard, name='home'),

    # Apps
    path('', include('core.urls')),
    path('apartamentos/', include('apartamentos.urls')),
]