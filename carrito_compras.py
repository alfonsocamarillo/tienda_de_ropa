from productos.accesorio import Accesorio
from productos.ropa import Ropa
from producto_carrito import ProductoCarrito

class CarritoCompras():
    def __init__(self) -> None:
        self.carrito = []
    
    def agregar(self, producto : object, cantidad : int, descuento : int | None = 0):
        info = producto.get_info() 
        codigo = info.get("Codigo")
        descripcion = info.get("Descripcion")
        precio = info.get("Precio")
        nuevo_producto = ProductoCarrito(codigo, descripcion, precio, cantidad, True)
        nuevo_producto.descuento = descuento
        
        if type(producto) == type(Ropa("","","")):
            talle = info.get("Talle")
            genero = info.get("Genero")
            nuevo_producto.talle = talle
            nuevo_producto.genero = genero 
        elif type(producto) == type(Accesorio("","")):
            material = info.get("Material")
            nuevo_producto.tipo_producto = "Accesorio"
            nuevo_producto.material = material

        for articulo in self.carrito:
            if nuevo_producto.codigo == articulo.codigo:
                indice = self.carrito.index(articulo)
                self.carrito[indice].cantidad += nuevo_producto.cantidad
                return None
        
        self.carrito.append(nuevo_producto)
        

    def mostrar(self):
        for producto in self.carrito:
            print(f"\n\nCodigo: {producto.codigo}")
            print(f"Nombre: {producto.descripcion}")
            print(f"Cantiad: {producto.cantidad}")
            print(f"Descuento: {producto.descuento}%")
            if producto.tipo_producto == "Ropa":
                print(f"Talle: {producto.talle}")
                print(f"Genero: {producto.genero}")
            elif producto.tipo_producto == "Accesorio":
                print(f"Material: {producto.material}")
    
    def remover(self, codigo : str) -> bool:
        for producto in self.carrito:
            if producto.codigo == codigo:
                self.carrito.remove(producto)
                return True
        return False
        
    def cantidad(self):
        return len(self.carrito)
    
    def mostrar_total(self) -> float:
        total = 0
        for articulo in self.carrito:
            total += articulo.mostrar_total()
        return total


if __name__ == "__main__":
    carrito = CarritoCompras()
    carrito.agregar(Ropa("001","XL","Masculino",stock=5, descripcion="Remera"),5)
    carrito.agregar(Ropa("001","XL","Masculino",stock=3),3)
    carrito.agregar(Accesorio("002", material="Oro", descripcion="reloj"),1)
    print(carrito.cantidad())
    carrito.mostrar()
    #print(carrito.cantidad())
    #carrito.mostrar()
