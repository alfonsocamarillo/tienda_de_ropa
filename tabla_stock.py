from tkinter import ttk, Tk
import db
from productos.ropa import Ropa
from productos.accesorio import Accesorio
from PIL import Image, ImageTk
import os

class TablaStock(ttk.Treeview):
    def __init__(self,master, tablas : list[str,str]):
        super().__init__(master,columns=["stock", "nombre", "precio", "material", "genero", "talle"])
        style = ttk.Style()
        style.configure("Treeview", rowheight=42)
        self.list_img = []
        self.img_accesorio = ImageTk.PhotoImage(image=Image.open("./assets/img/2.png").resize((40,40)))
        self.img_ropa = ImageTk.PhotoImage(image=Image.open("./assets/img/1.png").resize((40,40)))
        self.heading("#0", text="Codigo")
        self.heading("stock", text="Stock")
        self.heading("nombre", text="Nombre")
        self.heading("precio", text="Precio")
        self.heading("material", text="Material")
        self.heading("genero", text="Genero")
        self.heading("talle", text="Talle")

        self.column("#0", width=100, anchor="center")
        self.column("stock", width=50, anchor="center")
        self.column("precio", width=50, anchor="center")
        self.column("talle", width=50, anchor="center")
        self.column("genero", anchor="center")
        self.column("material", anchor="center")
        
        self.insertar_stock(tablas)

    def insertar_stock(self,tablas : list[str,str], es_tabla = True):
        """toma por defectios talbas y las tranforma a objetos luego los suma a el treeview, se le puede pasar objetos poniendo en false es tabla

        Args:
            tablas (list[str,str]): tablas a buscar
            treeview (_type_): treeview a cargar
            es_tabla (bool, optional): dependiendo si es una tabla o no . Defaults to True.
        """
        for id in self.get_children(""): self.delete(id)
        self.list_img = []
        for tabla in tablas:
            for info in db.datos(tabla) if es_tabla else tabla:
                if es_tabla:
                    item = Ropa(*info) if tabla == "ropa" else Accesorio(*info)
                else:
                    item = info
                path_img = f"./assets/img/{item.get_codigo()}.png"
                try:
                    genero = item.get_genero()
                    talle = item.get_talle()
                    material = ""
                    self.list_img.append(ImageTk.PhotoImage(Image.open(path_img))) if os.path.exists(path_img) else self.list_img.append(self.img_ropa)
                    
                except:
                    material = item.get_material()
                    genero = ""
                    talle = ""
                    self.list_img.append(ImageTk.PhotoImage(Image.open(path_img))) if os.path.exists(path_img) else self.list_img.append(self.img_accesorio)
                    
                self.insert("",
                    "end",
                    text=item.get_codigo(),
                    image=self.list_img[-1],
                    values=[
                        item.get_stock(),
                        item.get_descripcion(),
                        item.get_precio(),
                        material,
                        genero,
                        talle
                    ]
                    )

if __name__ == "__main__":
    ventana = Tk()
    tabla_stock = TablaStock(ventana,("ropa",))
    tabla_stock.pack()
    ventana.mainloop()