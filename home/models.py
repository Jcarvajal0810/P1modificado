from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q

class PrendaManager(models.Manager):
    def por_talla(self, talla):
        """Retorna prendas de una talla específica"""
        return self.filter(talla=talla)
    
    def por_estado(self, estado):
        """Retorna prendas de un estado específico"""
        return self.filter(estado__icontains=estado)
    
    def por_rango_precio(self, min_precio=0, max_precio=None):
        """Retorna prendas dentro de un rango de precios"""
        queryset = self.filter(precio__gte=min_precio)
        if max_precio is not None:
            queryset = queryset.filter(precio__lte=max_precio)
        return queryset
    
    def buscar(self, termino):
        """Busca prendas por nombre"""
        if not termino:
            return self.all()
        return self.filter(nombre__icontains=termino)
    
    def populares(self, limit=5):
        """
        Retorna las prendas más populares (las que más aparecen en carritos)
        """
        return self.annotate(
            carrito_count=Count('carrito')
        ).order_by('-carrito_count')[:limit]
    
    def por_filtros(self, **filtros):
        """
        Método flexible para aplicar múltiples filtros a la vez
        
        Ejemplo de uso:
        Prenda.objects.por_filtros(
            nombre='camisa', 
            talla='M', 
            precio_min=1000, 
            precio_max=5000
        )
        """
        queryset = self.all()
        
        # Filtro por nombre
        if 'nombre' in filtros and filtros['nombre']:
            queryset = queryset.filter(nombre__icontains=filtros['nombre'])
        
        # Filtro por talla
        if 'talla' in filtros and filtros['talla']:
            queryset = queryset.filter(talla=filtros['talla'])
        
        # Filtro por estado
        if 'estado' in filtros and filtros['estado']:
            queryset = queryset.filter(estado__icontains=filtros['estado'])
        
        # Filtro por rango de precio
        precio_min = filtros.get('precio_min', 0)
        precio_max = filtros.get('precio_max', None)
        
        queryset = queryset.filter(precio__gte=precio_min)
        if precio_max is not None:
            queryset = queryset.filter(precio__lte=precio_max)
        
        return queryset
    
    def estadisticas(self):
        """
        Retorna estadísticas generales sobre las prendas
        """
        return {
            'total': self.count(),
            'precio_promedio': self.aggregate(Avg('precio'))['precio__avg'],
            'por_talla': {
                talla: self.filter(talla=talla).count()
                for talla in self.values_list('talla', flat=True).distinct()
            },
            'por_estado': {
                estado: self.filter(estado=estado).count()
                for estado in self.values_list('estado', flat=True).distinct()
            }
        }

class Prenda(models.Model):
    imagen = models.ImageField(upload_to='img/')
    nombre = models.CharField(max_length=200)
    precio = models.IntegerField()
    estado = models.CharField(max_length=200)
    talla = models.CharField(max_length=200)
    
    # Añadimos el manager personalizado
    objects = PrendaManager()
    
    def __str__(self):
        return self.nombre
    
    @property
    def en_carritos(self):
        """Retorna el número de carritos que contienen esta prenda"""
        return self.carrito_set.count()

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    prendas = models.ManyToManyField(Prenda)
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    
    @property
    def total(self):
        """Calcula el total del carrito"""
        return sum(prenda.precio for prenda in self.prendas.all())
    
    @property
    def cantidad_prendas(self):
        """Retorna la cantidad de prendas en el carrito"""
        return self.prendas.count()