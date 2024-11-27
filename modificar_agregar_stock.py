from tkinter import Toplevel, Tk, filedialog, ttk
import tkinter as tk
from PIL import Image, ImageTk
from constantes import *
import db

class ModificarAgregar(Toplevel):
    def __init__(self,master,codigo = "", nombre = "", stock = "",
                        precio = "", genero="", talle="", material = "", agregar = True):
        super().__init__(master)
        
        ANCHO_ROOT   = master.winfo_screenwidth()  - 101
        ALTO_ROOT    = master.winfo_screenheight() - 150
    
        var_producto =  tk.StringVar()
        var_producto.set("accesorio") if genero == "" else var_producto.set("ropa")
        var_genero = tk.StringVar(value=genero)
        var_talle = tk.StringVar(value=talle)
        var_material = tk.StringVar(value=material)
        self.config(bg=COLOR_BARRA_IZQ)
        self.geometry(f"300x600+{ANCHO_ROOT//2-150}+{ALTO_ROOT//2-250}")
        tk.Label(self, text="Imagen:", bg=COLOR_BARRA_IZQ, fg="white").pack()
        imagen = tk.Button(self, text="Selecione Imagen", command= lambda: self.seleccionar_imagen(imagen))
        imagen.pack(pady=15)
        tk.Label(self, text="Codigo", bg=COLOR_BARRA_IZQ, fg="white").pack()
        _codigo = tk.Entry(self)
        _codigo.insert(0, db.generar_codigo()) if codigo == "" else  _codigo.insert(0, codigo)
        _codigo.config(state=tk.DISABLED)
        _codigo.pack(pady=15)
        tk.Label(self, text="Nombre", bg=COLOR_BARRA_IZQ, fg="white").pack()
        _nombre = tk.Entry(self)
        if nombre != "": _nombre.insert(0, nombre)
        _nombre.pack(pady=15)
        tk.Label(self, text="Stock", bg=COLOR_BARRA_IZQ, fg="white").pack()
        _stock = tk.Entry(self)
        if stock != "": _stock.insert(0, stock)
        _stock.pack(pady=15)
        tk.Label(self, text="Precio", bg=COLOR_BARRA_IZQ, fg="white").pack()
        _precio = tk.Entry(self)
        if precio != "": _precio.insert(0, precio)
        _precio.pack(pady=15)
        frame_rbtn = tk.Frame(self, bg=COLOR_BARRA_IZQ)
        rbtn_accesorio = tk.Radiobutton(
            frame_rbtn,
            text="Accesorio",
            value="accesorio",
            variable=var_producto,
            state="disabled" if  nombre else "active",
            bg=COLOR_BARRA_IZQ,
            fg="white",
            selectcolor=COLOR_BARRA_IZQ, activebackground=COLOR_BARRA_IZQ, activeforeground="white"
            )
        rbtn_ropa = tk.Radiobutton(
            frame_rbtn,
            text="Ropa",
            value="ropa",
            variable=var_producto,
            state="disabled" if  nombre else "active",
            bg=COLOR_BARRA_IZQ, fg="white",
            selectcolor=COLOR_BARRA_IZQ, activebackground=COLOR_BARRA_IZQ, activeforeground="white"
            )
        rbtn_accesorio.pack(side="left")
        rbtn_ropa.pack(side="left")
        frame_rbtn.pack()
        frame_info = tk.Frame(self, bg=COLOR_BARRA_IZQ)
        self.__cambio_area_info(frame_info,var_genero, var_talle, var_material, var_producto.get())

        frame_info.pack()
        var_producto.trace_add("write", lambda a,b,c: self.__cambio_area_info(frame_info, var_genero, var_talle, var_material, var_producto.get()))
        
        btn_agregar = tk.Button(
            self,
            text="Agregar" if agregar else "Actualizar",
            bg=COLOR_BUTTON,
            fg="white",
            command= lambda:
                self.agregar_stock(
                    imagen.cget("text"),
                    _codigo.get(),
                    _nombre.get(),
                    _stock.get(),
                    _precio.get(),
                    var_material.get(),
                    var_talle.get(),
                    var_genero.get(),
                    var_producto.get()
                    ) if agregar else
                self.modificar_stock(
                    imagen.cget("text"),
                    _codigo.get(),
                    _nombre.get(),
                    _stock.get(),
                    _precio.get(),
                    var_material.get(),
                    var_talle.get(),
                    var_genero.get(),
                    var_producto.get()
                    )
            )
        btn_cancelar = tk.Button(self, text="Cancelar", bg=COLOR_BUTTON, fg="white", command=self.destroy)

        btn_cancelar.pack(side="left", padx=15)
        btn_agregar.pack(side="right", padx=15)


    def modificar_stock(self, path, codigo, nombre, stock, precio, material, talle, genero, producto):
        try:
            with Image.open(path) as img:
                img = img.resize((35,35))
                img.save(f"./assets/img/{codigo}.png")
        except:
            pass
        if producto == "ropa":
            db.actualizar_ropa(codigo, talle, genero, precio, stock, nombre )
        else:
            db.actualizar_accesorios(codigo, material, precio, stock, nombre)
        self.destroy()
        
    def agregar_stock(self, path, codigo, nombre, stock, precio, material, talle, genero, producto):
        try:
            with Image.open(path) as img:
                img = img.resize((35,35))
                img.save(f"./assets/img/{codigo}.png")
        except:
            pass
        if producto == "ropa":
            db.agregar_stock_ropa(codigo, talle, genero, precio, stock, nombre)
        else:
            db.agregar_stock_accesorio(codigo, material, precio, stock, nombre)
        self.destroy()

    def seleccionar_imagen(self, button):
        path = filedialog.askopenfilename(
                title="Selecione Imagen",
                filetypes=(("image", ("*.jpg", "*.jpeg", "*.png", "*.gif")),)
                )
        self.img = Image.open(path).resize((40,40))
        self.img = ImageTk.PhotoImage(self.img)
        button.config( image=self.img, text=path)
    
    def __cambio_area_info(self, frame_info, var_genero, var_talle, var_material, producto_seleccionado):
        for x in frame_info.winfo_children(): x.destroy()
        if producto_seleccionado == "accesorio":
            tk.Label(frame_info, text="Material", bg=COLOR_BARRA_IZQ, fg="white").pack()
            material = ttk.Combobox(frame_info, textvariable=var_material, values=["Plástico", "Metal", "Cuero"], state="readonly")
            material.pack(pady=15)
        else:
            tk.Label(frame_info, text="Talle", bg=COLOR_BARRA_IZQ, fg="white").pack()
            talle = ttk.Combobox(frame_info, textvariable=var_talle, values=["S", "M", "L", "XL"], state="readonly")
            talle.pack(pady=15)
            rbtn_masculino = tk.Radiobutton(
                frame_info, text="Hombre", value="Hombre", variable=var_genero,  bg=COLOR_BARRA_IZQ, fg="white",
                selectcolor=COLOR_BARRA_IZQ, activebackground=COLOR_BARRA_IZQ, activeforeground="white",
                )
            rbtn_femenino = tk.Radiobutton(
                frame_info, text="Mujer", value="Mujer", variable=var_genero,  bg=COLOR_BARRA_IZQ, fg="white",
                selectcolor=COLOR_BARRA_IZQ, activebackground=COLOR_BARRA_IZQ, activeforeground="white",
                )
            rbtn_unisex = tk.Radiobutton(
                frame_info, text="Unisex", value="Unisex", variable=var_genero,  bg=COLOR_BARRA_IZQ, fg="white",
                selectcolor=COLOR_BARRA_IZQ, activebackground=COLOR_BARRA_IZQ, activeforeground="white",
                )
            
            rbtn_masculino.pack(side="left")
            rbtn_unisex.pack(side="left")
            rbtn_femenino.pack()

if __name__ == "__main__":
    root = Tk()
    self = ModificarAgregar(root, "123","remera",51,15000,"Masculino", "XL")
    root.mainloop()