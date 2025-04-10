# home/strategies/composite_filter.py
from django.db.models.query import QuerySet
from typing import Dict
from home.strategies.filter_strategy import FilterStrategy
from home.models import Prenda

class CompositeFilterStrategy:
    """
    Estrategia compuesta que aplica múltiples filtros en secuencia.
    """
    def __init__(self, strategies: Dict[str, FilterStrategy]):
        """
        Inicializa la estrategia compuesta con un diccionario de estrategias.
        
        Args:
            strategies: Diccionario donde la clave es el nombre del parámetro
                       y el valor es la estrategia de filtrado a aplicar.
        """
        self.strategies = strategies
        
    def apply_filters(self, request) -> QuerySet:
        """
        Aplica todos los filtros a partir de los parámetros de la solicitud.
        
        Args:
            request: Objeto HttpRequest con los parámetros de filtrado
            
        Returns:
            QuerySet filtrado de prendas
        """
        # Comenzamos con todas las prendas
        prendas = Prenda.objects.all()
        
        # Aplicamos cada estrategia de filtrado
        for param_name, strategy in self.strategies.items():
            value = request.GET.get(param_name)
            prendas = strategy.filter(prendas, value)
            
        return prendas