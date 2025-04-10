# home/strategies/filter_strategy.py
from abc import ABC, abstractmethod
from django.db.models.query import QuerySet
from home.models import Prenda

class FilterStrategy(ABC):
    """
    Interfaz para las estrategias de filtrado de prendas.
    """
    @abstractmethod
    def filter(self, prendas: QuerySet, value) -> QuerySet:
        """
        Aplica el filtro a un conjunto de prendas.
        
        Args:
            prendas: QuerySet de prendas a filtrar
            value: Valor del filtro a aplicar
            
        Returns:
            QuerySet filtrado
        """
        pass