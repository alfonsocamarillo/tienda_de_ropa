from peewee import SqliteDatabase, Model, CharField, BooleanField, FloatField, IntegerField, Check, DateTimeField, ForeignKeyField
import csv

TALLES = [('s','S'), ('m','M'), ('l','L'), ('xl', 'XL')]
GENEROS = [('hombre','Hombre'), ('mujer', 'Mujer'), ('unisex', 'Unisex')]
MATERIALES = [('plástico','Plástico'), ('metal','Metal'), ('cuero', 'Cuero')]

db = SqliteDatabase('./assets/db/datos.db')

class Usuario(Model):
    nombre = CharField(max_length=40, null=False, unique=True)
    permiso = BooleanField(default=False)
    contrasena = CharField(max_length=70, null=False)
    class Meta:
        database = db

class Ropa(Model):
    talle = CharField(max_length=5, choise=TALLES)
    genero = CharField(max_length=10, choise=GENEROS)
    precio = FloatField()
    stock =  IntegerField(constraints=Check('stock >= 0'), default=0)
    descripcion = CharField(max_length=50)
    class Meta:
        database = db

class Accesorio(Model):
    material =  CharField(max_length=10, choise=MATERIALES)
    precio = FloatField()
    stock = IntegerField(constraints=Check('stock >= 0'), default=0)
    descripcion =  CharField(max_length=50)
    class Meta:
        database = db

class Ventas(Model):
    codigo = CharField()
    descripcion = CharField(max_length=50)
    cantidad = IntegerField()
    precio = FloatField()
    descuento = IntegerField()
    fecha = DateTimeField()
    id_usuario = ForeignKeyField(Usuario)
    
    class Meta:
        database = db

models = [Usuario, Ropa, Accesorio, Ventas]

db.create_tables(models, safe=True)


def agregar_stock_ropa(codigo, talle, genero, precio, stock, descripcion):
    Ropa.create(
        id = codigo,
        talle = talle,
        genero = genero,
        precio = precio,
        stock = stock,
        descripcion = descripcion
        ).save()

def agregar_stock_accesorio(codigo, material, precio, stock, descripcion):
    Accesorio.create(
        id = codigo,
        material = material,
        precio = precio,
        stock = stock,
        descripcion = descripcion
        ).save()

def agregar_ventas(codigo, descripcion, cantidad, precio, descuento, fecha, id_usuario):
    Ventas.create(
        codigo = codigo,
        descripcion = descripcion,
        cantidad = cantidad,
        precio = precio,
        descuento = descuento,
        fecha = fecha,
        id_usuario = id_usuario
        ).save()

def agregar_usuario(nombre, contrasena, permiso):
    Usuario.create(
        nombre = nombre,
        contrasena = contrasena,
        permiso = permiso
        ).save()
    return True

def eliminar(codigo, tabla : str):
    """
        Elimina con referencia de id
    """
    if tabla.capitalize == "Usuario":
        tabla = Usuario
    elif tabla.capitalize == "Accesorio":
        tabla = Accesorio
    elif tabla.capitalize == "Ropa":
        tabla = Ropa
    tabla.get( tabla.id == codigo ).delete_instance()

def actualizar_usuario(codigo, permiso, contrasena):
    usuario = Usuario.get( Usuario.id == codigo)
    usuario.permiso = permiso
    usuario.contrasena = contrasena
    usuario.save()

def actualizar_ropa(codigo, talle = "", genero = "", precio = "", stock = "", descripcion = ""):
    ropa = Ropa.get( Ropa.id == codigo)
    
    if talle != "" :
        ropa.talle = talle
    if genero != "" :
        ropa.genero = genero
    if precio != "":
        ropa.precio = precio
    if stock != "":
        ropa.stock = stock
    if descripcion != "":
        ropa.descripcion = descripcion
    
    ropa.save()

def actualizar_accesorios(codigo, material = "", precio = "", stock = "", descripcion = ""):
    accesorio = Accesorio.get( Accesorio.id == codigo)
    if material != "" :
        accesorio.material = material
    if precio != "":
        accesorio.precio = precio
    if stock != "":
        accesorio.stock = stock
    if descripcion != "":
        accesorio.descripcion = descripcion
    
    accesorio.save()

def importar_datos_csv(ruta):
    with open(ruta, newline="", encoding="utf-8") as archivo:
            info = csv.DictReader(archivo)
            for linea in info:
                codigo = linea.get("Codigo")
                precio = linea.get("Precio")
                stock = linea.get("Stock")
                descripcion = linea.get("Descripcion")
                if "Talle" in linea.keys():
                    talle = linea.get("Talle")
                    genero = linea.get("Genero")
                    agregar_stock_ropa(codigo, talle, genero, precio, stock, descripcion)
                elif "Material" in linea.keys():
                    material = linea.get("Material")
                    agregar_stock_accesorio(codigo, material, precio, stock, descripcion)

def datos(tabla : object) -> list:
    return tabla.select()

def busqueda_id(tabla,id) -> tuple:
    return tabla.get( tabla.id == id )

def busqueda_texto(tabla, texto):
    return tabla.select().where(
        tabla.descripcion.contains(texto)
    )

def exportar_ventas_csv(ruta):
    ventas = Ventas.select()
    info = []
    for venta in ventas:
        info.append([
            venta.codigo,
            venta.descripcion,
            venta.cantidad,
            venta.precio,
            venta.descuento,
            venta.fecha,
            venta.id_usuario
            ])
            
    with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
        titulos = ["Codigo", "Descripcion","Cantidad", "Precio", "Descuento", "Fecha", "Vendedor"]
        escribir = csv.DictWriter(archivo, titulos)
        escribir.writeheader()
        
        for linea in info:
            nueva_lista = dict()
            nueva_lista["Codigo"] = linea[1]
            nueva_lista["Descripcion"] = linea[2]
            nueva_lista["Cantidad"] = linea[3]
            nueva_lista["Precio"] = linea[4]
            nueva_lista["Descuento"] = linea[5]
            nueva_lista["Fecha"] = linea[6]
            nueva_lista["Vendedor"] = linea[7]

            escribir.writerow(nueva_lista)


def generar_codigo():
    ropa = datos("ropa")
    accesorios = datos("accesorios")
    codigo = "000"
    if int(ropa[-1][0]) > int(accesorios[-1][0]):
        codigo += str(int(ropa[-1][0]) + 1)
    else:
        codigo += str(int(accesorios[-1][0]) + 1)
    
    return codigo[-3:]

if __name__ == "__main__":
    print(busqueda_id("usuarios","Ana"))