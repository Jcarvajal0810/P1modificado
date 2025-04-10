from django.db.models.query import QuerySet
from home.strategies.filter_strategy import FilterStrategy

class NombreFilterStrategy(FilterStrategy):
    """
    Estrategia para filtrar prendas por nombre.
    """
    def filter(self, prendas: QuerySet, value) -> QuerySet:
        if not value:
            return prendas
        return prendas.filter(nombre__icontains=value)