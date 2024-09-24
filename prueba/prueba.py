import csv
from getpass import getpass

class Producto:
    def __init__(self, codigo, precio, stock):
        self.codigo = codigo
        self.precio = precio
        self.stock = stock

class Ropa(Producto):
    def __init__(self, codigo, talle, genero, precio, stock):
        super().__init__(codigo, precio, stock)
        self.talle = talle
        self.genero = genero

class Accesorio(Producto):
    def __init__(self, codigo, material, precio, stock):
        super().__init__(codigo, precio, stock)
        self.material = material

class Tienda:
    def __init__(self):
        self.ropa = []
        self.accesorios = []
        self.usuarios = {'admin': 'password'}  # Usuario predeterminado
        self.carrito = []

    def cargar_productos_csv(self, archivo, tipo_producto):
        with open(archivo, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if tipo_producto == 'ropa':
                    producto = Ropa(row['Codigo'], row['Talle'], row['Genero'], float(row['Precio']), int(row['Stock']))
                    self.ropa.append(producto)
                elif tipo_producto == 'accesorios':
                    producto = Accesorio(row['Codigo'], row['Material'], float(row['Precio']), int(row['Stock']))
                    self.accesorios.append(producto)

    def autenticar_usuario(self):
        usuario = input("Usuario: ")
        contraseña = getpass("Contraseña: ")
        if self.usuarios.get(usuario) == contraseña:
            print("Autenticación exitosa.")
            return True
        else:
            print("Usuario o contraseña incorrectos.")
            return False

    def agregar_al_carrito(self, producto):
        self.carrito.append(producto)

    def mostrar_carrito(self):
        if not self.carrito:
            print("El carrito está vacío.")
        else:
            for producto in self.carrito:
                print(f"{producto.codigo}: {producto.precio} - {producto.stock} unidades")

def main():
    tienda = Tienda()
    
    # Cargar productos desde archivos CSV
    tienda.cargar_productos_csv('ropa.csv', 'ropa')
    tienda.cargar_productos_csv('accesorios.csv', 'accesorios')
    
    if tienda.autenticar_usuario():
        while True:
            print("\n1. Ver Ropa\n2. Ver Accesorios\n3. Agregar al Carrito\n4. Ver Carrito\n5. Salir")
            opcion = input("Elija una opción: ")
            if opcion == '1':
                for ropa in tienda.ropa:
                    print(f"Código: {ropa.codigo}, Talle: {ropa.talle}, Género: {ropa.genero}, Precio: {ropa.precio}, Stock: {ropa.stock}")
            elif opcion == '2':
                for accesorio in tienda.accesorios:
                    print(f"Código: {accesorio.codigo}, Material: {accesorio.material}, Precio: {accesorio.precio}, Stock: {accesorio.stock}")
            elif opcion == '3':
                codigo = input("Ingrese el código del producto a agregar al carrito: ")
                producto = next((p for p in tienda.ropa + tienda.accesorios if p.codigo == codigo), None)
                if producto:
                    tienda.agregar_al_carrito(producto)
                    print("Producto agregado al carrito.")
                else:
                    print("Producto no encontrado.")
            elif opcion == '4':
                tienda.mostrar_carrito()
            elif opcion == '5':
                break
            else:
                print("Opción no válida.")

if __name__ == "__main__":
    main()
