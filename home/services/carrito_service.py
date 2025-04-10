from typing import List, Tuple
from django.contrib.auth.models import User
from home.models import Prenda, Carrito
from home.services.interfaces import CarritoServiceInterface

class CarritoService(CarritoServiceInterface):
    def get_or_create_carrito(self, usuario: User) -> Tuple[Carrito, bool]:
        return Carrito.objects.get_or_create(usuario=usuario)
    
    def add_prenda(self, usuario: User, prenda_id: int) -> str:
        prenda = Prenda.objects.get(id=prenda_id)
        carrito, _ = self.get_or_create_carrito(usuario)
        carrito.prendas.add(prenda)
        return f'"{prenda.nombre}" se ha agregado al carrito.'
    
    def get_prendas(self, usuario: User) -> List[Prenda]:
        carrito, _ = self.get_or_create_carrito(usuario)
        return carrito.prendas.all()
    
    def get_total(self, usuario: User) -> int:
        prendas = self.get_prendas(usuario)
        return sum(prenda.precio for prenda in prendas)
    
    def clear(self, usuario: User) -> None:
        carrito, _ = self.get_or_create_carrito(usuario)
        carrito.prendas.clear()