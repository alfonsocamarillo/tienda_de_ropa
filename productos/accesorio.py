from .producto import Producto

class Accesorio(Producto):
    def __init__(self, codigo: str, material : str, precio: float | None = 0, stock: int | None = 0, descripcion: str | None = "") -> None:
        
        super().__init__(codigo, precio, stock, descripcion)
        
        self.__material = material
    
    def get_material(self):
        return self.__material

    def get_info(self):
        info = super().get_info()
        info["Material"] = self.__material
        return info