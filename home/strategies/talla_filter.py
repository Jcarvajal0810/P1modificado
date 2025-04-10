from django.db.models.query import QuerySet
from home.strategies.filter_strategy import FilterStrategy

class TallaFilterStrategy(FilterStrategy):
    """
    Estrategia para filtrar prendas por talla.
    """
    def filter(self, prendas: QuerySet, value) -> QuerySet:
        if not value:
            return prendas
        return prendas.filter(talla=value)