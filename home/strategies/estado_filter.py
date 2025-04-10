from django.db.models.query import QuerySet
from home.strategies.filter_strategy import FilterStrategy

class EstadoFilterStrategy(FilterStrategy):
    """
    Estrategia para filtrar prendas por estado.
    """
    def filter(self, prendas: QuerySet, value) -> QuerySet:
        if not value:
            return prendas
        return prendas.filter(estado__icontains=value)
    