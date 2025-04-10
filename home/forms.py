from django import forms
from .models import Prenda

class PrendaForm(forms.ModelForm):
    class Meta:
        model = Prenda
        fields = ['imagen', 'nombre', 'precio', 'estado', 'talla']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'talla': forms.TextInput(attrs={'class': 'form-control'}),
        }