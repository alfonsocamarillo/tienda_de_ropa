import csv
from productos.ropa import Ropa
from productos.accesorio import Accesorio

class Importador():
    @classmethod
    def importar(cls, ruta : str) -> list[object]:
        with open(ruta, newline="", encoding="utf-8") as archivo:
            info = csv.DictReader(archivo)
            lista = []
            for linea in info:
                codigo = linea.get("Codigo")
                precio = linea.get("Precio")
                stock = linea.get("Stock")
                descripcion = linea.get("Descripcion")
                if "Talle" in linea.keys():
                    talle = linea.get("Talle")
                    genero = linea.get("Genero")
                    lista.append( Ropa(codigo, talle, genero, precio, stock, descripcion) )
                elif "Material" in linea.keys():
                    material = linea.get("Material")
                    lista.append( Accesorio(codigo, material, precio, stock, descripcion) )
            return lista
    
    @classmethod
    def importar_usuarios(cls) -> list[list]:
        with open("./assets/csv/usuarios.csv",newline="",encoding="utf-8") as archivo:
            info = csv.DictReader(archivo)
            lista = [[linea.get("Usuario"), linea.get("Permiso"), linea.get("Contrasena")]  for linea in info]
            return lista
    
    @classmethod
    def __actualizar_csv_usuarios(cls, lista):
        ruta = "./assets/csv/usuarios.csv"
        with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
            titulos = ["Usuario", "Permiso", "Contrasena"]
            escribir = csv.DictWriter(archivo, titulos)
            escribir.writeheader()
            
            for linea in lista:
                nueva_lista = {}
                nueva_lista["Usuario"] = linea[0]
                nueva_lista["Permiso"] = linea[1]
                nueva_lista["Contrasena"] = linea[2]
                escribir.writerow(nueva_lista)
    
    @classmethod
    def agregar_usuario(cls, nombre, permiso, contrasena) -> bool:
        """Agrega un nuevo usuario si el nombre no esta en uso

        Args:
            nombre (str): nombre de usuario
            permiso (bool): permiso
            contrasena (str): contraseña del usuario

        Returns:
            bool: false si ya existe True si se agrega sin problema
        """
        usuarios = cls.importar_usuarios()
        for usuario, p, c in usuarios:
            if usuario == nombre:
                return False
        usuarios.append([nombre,permiso,contrasena])
        cls.__actualizar_csv_usuarios(usuarios)
        return True
    
    @classmethod
    def actualizar_usuario(cls, usuario, nombre_nuevo, permiso_nuevo, contrasena_nueva):
        """actualiza el usuario pasando el nombre de usuario

        Args:
            usuario (str): nombre de usuario a actualizar
            nombre_nuevo (_type_): nuevo nombre a cambiar
            permiso_nuevo (_type_): nuevo permiso
            contrasena_nueva (_type_): nueva contraseña
        """
        usuarios = cls.importar_usuarios()
        for x in range(len(usuarios)):
            if usuarios[x][0] == usuario:
                usuarios[x] = [nombre_nuevo, permiso_nuevo, contrasena_nueva]
    
        cls.__actualizar_csv_usuarios(usuarios)
    
    @classmethod
    def eliminar_usuario(cls, nombre):
        usuarios = cls.importar_usuarios()
        for usuario, permiso, contrasena in usuarios:
            if usuario == nombre:
                usuarios.remove([usuario,permiso,contrasena])
        cls.__actualizar_csv_usuarios(usuarios)
            
    @classmethod
    def exportar(
                    cls, nombre : str, stock : int, precio : float,
                    genero : str | None = False, talle : str | None = False, material : str | None = False, codigo = ""
                ):
        articulo = {}
        articulo["Codigo"] = cls.generar_codigo() if codigo == "" else codigo
        articulo["Descripcion"] = nombre
        articulo["Stock"] = stock
        articulo["Precio"] = precio
        if talle: 
            ruta = "./assets/csv/ropa.csv"
            articulo["Genero"] = genero
            articulo["Talle"] = talle
        else:
            ruta = "./assets/csv/accesorios.csv"
            articulo["Material"] = material
        with open(ruta, mode="a", newline="", encoding="utf-8") as archivo:
            titulos = ["Codigo","Precio","Stock","Descripcion"]
            if talle:
                titulos.insert(1,"Genero") 
                titulos.insert(1,"Talle") 
            else:
                titulos.insert(1,"Material")
                
            escribir = csv.DictWriter(archivo, titulos)
            
            escribir.writerow(articulo)
    
    @classmethod
    def agregar_ventas(
                    cls, codigo, cantidad, precio, descuento, usuario, fecha):
        articulo = {"codigo": codigo}
        articulo["cantidad"] = cantidad
        articulo["precio"] = precio
        articulo["descuento"] = descuento
        articulo["usuario"] = usuario
        articulo["fecha"] = fecha
        ruta = "./assets/csv/ventas.csv"

        with open(ruta, mode="a", newline="", encoding="utf-8") as archivo:
            titulos = ["codigo", "cantidad", "precio", "descuento", "usuario", "fecha"]
            escribir = csv.DictWriter(archivo, titulos)
            escribir.writerow(articulo)
        
    @classmethod
    def actualizar_stock(cls, lista : Ropa | Accesorio, tipo = "ropa"):
        """Actualiza el csv 

        Args:
            lista (Ropa | Accesorio): lista con los abojetos de ropa y accesorio
            tipo (str): "ropa" o "accesorio". Defaults to "ropa". indica tambien el csv a actualizar
        """
        ruta = f"./assets/csv/{tipo}.csv"
        with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
            titulos = ["Codigo", "Material", "Precio", "Stock", "Descripcion"]if tipo == "accesorios" else ["Codigo", "Talle", "Genero", "Precio", "Stock", "Descripcion"]
            escribir = csv.DictWriter(archivo, titulos)
            escribir.writeheader()
            
            for objeto in lista:
                nueva_lista = dict()
                nueva_lista["Codigo"] = objeto.get_codigo()
                if tipo == "ropa":
                    nueva_lista["Talle"] = objeto.get_talle()
                    nueva_lista["Genero"] = objeto.get_genero()
                else:
                    nueva_lista["Material"] = objeto.get_material()
                nueva_lista["Precio"] = objeto.get_precio()
                nueva_lista["Stock"] = objeto.get_stock()
                nueva_lista["Descripcion"] = objeto.get_descripcion()
                
                escribir.writerow(nueva_lista)
            
    
    @classmethod
    def generar_codigo(cls):
        lista_ropa = cls.importar("./assets/csv/ropa.csv")
        lista_accesorio = cls.importar("./assets/csv/accesorios.csv")
        if len(lista_ropa) != 0:
            codigo_de_ropa = lista_ropa[-1].get_info().get("Codigo")
        else:
            codigo_de_ropa = "000"
        if len(lista_accesorio) != 0:
            codigo_accesorios = lista_accesorio[-1].get_info().get("Codigo")
        else:
            codigo_accesorios = "000"
        if codigo_de_ropa > codigo_accesorios:
            return str(int(codigo_de_ropa) + 1)
        else:
            return str(int(codigo_accesorios) + 1)
    
    

if __name__ == "__main__":
    productos = Importador.importar("ropa.csv")
    productos.extend(Importador.importar("accesorios.csv"))
    for producto in productos:
        print(producto.get_info())