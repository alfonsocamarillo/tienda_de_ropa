
class ProductoCarrito():
    def __init__(
                    self, codigo : str , descripcion : str,
                    precio : float, cantidad : int, tipo_producto : bool, talle = "" ,
                    genero = "", material = "",
                    descuento = 0
                ) -> None:
        """
        Args:
            descuento (int, optional): descuento es de 0 a 100 indica el %
            tipo_producto (bool): True = Ropa, False = Accesorio
        """
        self.codigo = codigo
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad = cantidad
        self.talle = talle
        self.genero = genero
        self.material = material
        self.tipo_producto = "Ropa" if tipo_producto else "Accesorio"
        self.descuento = descuento
    
    def modificar_cantidad(self, cantidad : int):
        self.cantidad += cantidad
    
    def cambiar_precio(self, nuevo_precio : float):
        self.cambiar_precio = nuevo_precio
    
    def mostrar_total(self) -> float:
        resultado = float(self.precio)*int(self.cantidad)
        descuento = resultado * float(self.descuento) / 100
        return resultado - descuento