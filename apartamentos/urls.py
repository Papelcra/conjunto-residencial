from django.urls import path
from . import views

app_name = 'apartamentos'

urlpatterns = [
    path('crear/', views.apartamento_create, name='create'),
    path('<int:pk>/editar/', views.apartamento_update, name='update'),
]