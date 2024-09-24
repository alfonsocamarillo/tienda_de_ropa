import csv

# Rutas de los archivos CSV
archivo_ropa = 'ropa.csv'
archivo_accesorios = 'accesorios.csv'

# Función para cargar y mostrar el contenido de un archivo CSV
def mostrar_contenido_csv(archivo):
    with open(archivo) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)

# Mostrar el contenido de ropa.csv
print("Contenido de ropa.csv:")
mostrar_contenido_csv(archivo_ropa)

# Mostrar el contenido de accesorios.csv
print("Contenido de accesorios.csv:")
mostrar_contenido_csv(archivo_accesorios)
