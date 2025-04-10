from abc import ABC, abstractmethod
from typing import List, Tuple
from django.contrib.auth.models import User
from home.models import Prenda

class CarritoServiceInterface(ABC):
    @abstractmethod
    def get_or_create_carrito(self, usuario: User) -> Tuple[object, bool]:
        """Obtiene o crea un carrito para el usuario."""
        pass
    
    @abstractmethod
    def add_prenda(self, usuario: User, prenda_id: int) -> str:
        """Añade una prenda al carrito del usuario."""
        pass
    
    @abstractmethod
    def get_prendas(self, usuario: User) -> List[Prenda]:
        """Obtiene todas las prendas en el carrito del usuario."""
        pass
    
    @abstractmethod
    def get_total(self, usuario: User) -> int:
        """Calcula el total del carrito del usuario."""
        pass
    
    @abstractmethod
    def clear(self, usuario: User) -> None:
        """Limpia el carrito del usuario."""
        pass