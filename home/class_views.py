from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Prenda
from .forms import PrendaForm

class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin que verifica si el usuario es staff"""
    def test_func(self):
        return self.request.user.is_staff

class PrendaListView(ListView):
    model = Prenda
    template_name = 'prendas/prenda_list.html'
    context_object_name = 'prendas'
    paginate_by = 10
    
    def get_queryset(self):
        # Usamos el manager para aplicar los filtros
        filtros = {}
        
        searchPrenda = self.request.GET.get("searchPrenda")
        if searchPrenda:
            filtros['nombre'] = searchPrenda
            
        precio = self.request.GET.get("precio")
        if precio:
            try:
                filtros['precio_max'] = int(precio)
            except ValueError:
                pass
                
        estado = self.request.GET.get("estado")
        if estado:
            filtros['estado'] = estado
            
        talla = self.request.GET.get("talla")
        if talla:
            filtros['talla'] = talla
            
        return Prenda.objects.por_filtros(**filtros)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadimos los valores de los filtros al contexto
        context['searchPrenda'] = self.request.GET.get("searchPrenda", "")
        context['precio'] = self.request.GET.get("precio", "")
        context['estado'] = self.request.GET.get("estado", "")
        context['talla'] = self.request.GET.get("talla", "")
        return context

class PrendaDetailView(DetailView):
    model = Prenda
    template_name = 'prendas/prenda_detail.html'
    context_object_name = 'prenda'

class PrendaCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Prenda
    form_class = PrendaForm
    template_name = 'prendas/prenda_form.html'
    success_url = reverse_lazy('prenda-list')
    
    def form_valid(self, form):
        messages.success(self.request, "Prenda creada exitosamente")
        return super().form_valid(form)

class PrendaUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Prenda
    form_class = PrendaForm
    template_name = 'prendas/prenda_form.html'
    success_url = reverse_lazy('prenda-list')
    
    def form_valid(self, form):
        messages.success(self.request, "Prenda actualizada exitosamente")
        return super().form_valid(form)

class PrendaDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Prenda
    template_name = 'prendas/prenda_confirm_delete.html'
    success_url = reverse_lazy('prenda-list')
    context_object_name = 'prenda'
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Prenda eliminada exitosamente")
        return super().delete(request, *args, **kwargs)

class PrendasPopularesView(ListView):
    template_name = 'prendas/populares.html'
    context_object_name = 'prendas'
    
    def get_queryset(self):
        return Prenda.objects.populares(limit=10)