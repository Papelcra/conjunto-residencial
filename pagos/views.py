from django.shortcuts import render

# Create your views here.
def estado_cuenta(request):
    return render(request, 'estado_cuenta.html')