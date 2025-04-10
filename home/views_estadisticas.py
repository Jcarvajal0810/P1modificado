from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Prenda

def is_staff(user):
    return user.is_staff

@login_required
def prendas_populares(request):
    """Vista que muestra las prendas más populares usando el manager"""
    prendas = Prenda.objects.populares(limit=10)
    return render(request, 'prendas/populares.html', {'prendas': prendas})

@login_required
@user_passes_test(is_staff)
def estadisticas_prendas(request):
    """Vista que muestra estadísticas de prendas (solo para staff)"""
    estadisticas = Prenda.objects.estadisticas()
    return render(request, 'prendas/estadisticas.html', {'estadisticas': estadisticas})