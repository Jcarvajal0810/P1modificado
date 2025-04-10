from django.db.models.query import QuerySet
from home.strategies.filter_strategy import FilterStrategy

class PrecioFilterStrategy(FilterStrategy):
    """
    Estrategia para filtrar prendas por precio máximo.
    """
    def filter(self, prendas: QuerySet, value) -> QuerySet:
        if not value:
            return prendas
        try:
            precio = int(value)
            return prendas.filter(precio__lte=precio)
        except ValueError:
            return prendas.none()