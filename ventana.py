import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from constantes import *
from PIL import Image, ImageTk
from importador import Importador
from productos.ropa import Ropa
from productos.accesorio import Accesorio
import os
from ventana_usuarios import VentanaUsuarios
from datetime import datetime

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.ANCHO_ROOT   = self.winfo_screenwidth()  - 101
        self.ALTO_ROOT    = self.winfo_screenheight() - 150

        self.title("Mi Tiendita de Ropa y Accesorios")
        self.geometry(f"{self.ANCHO_ROOT}x{self.ALTO_ROOT}+{POS_X}+{POS_Y}")
        self.resizable(0,0)
        self.configure(bg=COLOR_BACKGROUND) 
        style = ttk.Style()
        style.configure("Treeview", rowheight=42)
        
        self.usuario = None
    
        self.login = dict()
        self.login["validacion"] = False
        self.login["permisos"] =  False

        self.img = None
        self.list_img = []
        self.accesorios = Importador.importar("./assets/csv/accesorios.csv")
        self.ropa = Importador.importar("./assets/csv/ropa.csv")
        self.img_accesorio = ImageTk.PhotoImage(image=Image.open("./assets/img/2.png").resize((40,40)))
        self.img_ropa = ImageTk.PhotoImage(image=Image.open("./assets/img/1.png").resize((40,40)))

        self.ANCHO_BARRA = int(self.ANCHO_ROOT / 5)

        self.lista_btn_izquierda = ["Ver Prendas", "Ver Accesorios", "Realizar Ventas", "Agregar Articulos", "Modificar Articulos", "Cambiar Permisos", "Salir"]
        
        
        
        self.barra_izquierda()
        self.ventana_verificar_usuario(self.imprimir, False)
    
    
    def insertar_treeview(self,datos : list[list,list], treeview):
        for id in treeview.get_children(""): treeview.delete(id)
        self.list_img = []
        for lista in datos:
            for item in lista:
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
                    
                treeview.insert("",
                    tk.END,
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
    
    def barra_izquierda(self):
        self.frame_barra_izquierda = tk.Frame(self, width=f"{self.ANCHO_BARRA}", height=f"{self.ALTO_ROOT}", bg=COLOR_BARRA_IZQ, border=2)

        btn_lista_izquierda = [tk.Button(
            self,
            text=f"{self.lista_btn_izquierda[x]}",
            bg=COLOR_BUTTON,
            fg="white",
            height=1,
            width=ANCHO_BUTTON,
            font=(LETRA,TAMANIO,ESTILO),
            border=5
            ) for x in range(len(self.lista_btn_izquierda))]
        for x in range(len(btn_lista_izquierda)):
            btn_lista_izquierda[x].place(x=10, y=60*(x+1))
        
        self.text_usuario = tk.Label(self.frame_barra_izquierda, text=f"Usuario: {self.usuario}", bg=COLOR_BARRA_IZQ, fg="white" ,font=(LETRA,TAMANIO,ESTILO))
        
        btn_lista_izquierda[0].config(command=self.btn_ver_prendas)
        btn_lista_izquierda[1].config(command=self.btn_ver_accesorios)
        btn_lista_izquierda[2].config(command=self.btn_realizar_venta)
        btn_lista_izquierda[3].config(command= lambda : self.ventana_verificar_usuario(self.btn_agregar_articulo, True))
        btn_lista_izquierda[4].config(command= lambda : self.ventana_verificar_usuario(self.btn_modificar_articulo, True))
        btn_lista_izquierda[-2].config(command=lambda : self.ventana_verificar_usuario(self.btn_cambiar_permisos, True))
        btn_lista_izquierda[-1].config(command=self.quit)
    
    def limpiar_area_trabajo(self):
        for x in self.frame_area_trabajo.winfo_children(): x.destroy()
        try:
            self.frame_barra_abajo.destroy()
        except:
            pass
    
    def verificar_usuario(self, usuario, contrasena, ventana, funcion, administrador):
        """verifica y ejecuta la funcion dependiendo si tiene que ser administrador o no 

        Args:
            usuario (str): usuario ingresado
            contrasena (str): contraseña ingresada
            ventana (toplevel): ventana a cerrar al finalizar
            funcion (funtion): funcion a ejecutar
            administrador (bool): True si se ejecuta si es administrador False si no es nesesario serlo
        """
        usuarios = Importador.importar_usuarios()
        for u , p , c in usuarios:
            if usuario == u and contrasena == c:
                self.usuario = u
                self.text_usuario.config(text=f"Usuario: {u}")
                self.login["validacion"] =  True 
                self.login["permisos"] =  True if p == "True" else False
                if not administrador or self.login["permisos"]: funcion()
                ventana.destroy()
                return None
        messagebox.showinfo("daton incorrectos", "El usuario o la contraseña no se encuentran")
    
    def ventana_verificar_usuario(self, funcion, administrador):
        """genera una ventana para verificar el usuario y validarlo

        Args:
            funcion (funtion): funcion a ejecutar
            administrador (bool): True se ejecuta la funcion unque no sea administrador False si no lo es no se ejecuta
        """
        ventana = tk.Toplevel(self, bg=COLOR_BARRA_IZQ)
        ventana.geometry("300x200")
        ventana.title("Login")
        tk.Label(ventana, text="Usuario", bg=COLOR_BARRA_IZQ, fg="white", font=(LETRA,TAMANIO,ESTILO)).pack(pady=5)
        usuario = tk.Entry(ventana)
        usuario.pack()
        tk.Label(ventana, text="Contraseña", bg=COLOR_BARRA_IZQ, fg="white", font=(LETRA,TAMANIO,ESTILO)).pack(pady=5)
        contrasena = tk.Entry(ventana, show="*")
        contrasena.pack()
        btn_ingresar = tk.Button(ventana, text="Ingresar", command= lambda: self.verificar_usuario(usuario.get(), contrasena.get(), ventana, funcion, administrador))
        btn_ingresar.pack(side="right", padx=10)
        btn_cancelar = tk.Button(ventana, text="cancelar", command = lambda : ventana.destroy())
        btn_cancelar.pack(side="left", padx=10)
        
    
    def btn_realizar_venta(self):
        self.limpiar_area_trabajo()
        self.area_venta()
        self.barra_abajo()
        self.frame_barra_abajo.pack_propagate(False)
        self.frame_barra_abajo.pack(side="bottom", fill="x")
    
    def btn_ver_prendas(self):
        self.limpiar_area_trabajo()
        self.ver_productos(self.ropa)
    
    def btn_ver_accesorios(self):
        self.limpiar_area_trabajo()
        self.ver_productos(self.accesorios)
    
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
    
    def modificar_stock(self, path, codigo, nombre, stock, precio, material, talle, genero, producto, ventana):
        try:
            with Image.open(path) as img:
                img = img.resize((35,35))
                img.save(f"./assets/img/{codigo}.png")
        except:
            pass
        if producto == "ropa":
            Importador.exportar(nombre, stock, precio, genero, talle, "", codigo)
            for ropa in self.ropa:
                if ropa.get_codigo() == codigo:
                    index = self.ropa.index(ropa)
                    self.ropa[index].set_talle(talle)
                    self.ropa[index].set_genero(genero)
                    self.ropa[index].set_precio(precio)
                    self.ropa[index].set_stock(stock)
                    self.ropa[index].set_descripcion(nombre)
        else:
            Importador.exportar(nombre, stock, precio, "", "", material, codigo)
            for accesorio in self.accesorios:
                if accesorio.get_codigo() == codigo:
                    index = self.accesorios.index[ropa]
                    self.accesorios[index].set_materila(material)
                    self.accesorios[index].set_precio(precio)
                    self.accesorios[index].set_stock(stock)
                    self.accesorios[index].set_descripcion(nombre)
        ventana.destroy()
        
    
    def agregar_stock(self, path, codigo, nombre, stock, precio, material, talle, genero, producto, ventana):
        try:
            with Image.open(path) as img:
                img.show()
                img = img.resize((35,35))
                img.save(f"./assets/img/{codigo}.png")
        except:
            pass
        if producto == "ropa":
            Importador.exportar(nombre, stock, precio, genero, talle, "", codigo)
            self.ropa.append( Ropa(codigo, talle, genero, precio, stock, nombre))
        else:
            Importador.exportar(nombre, stock, precio, "", "", material, codigo)
            self.accesorios.append( Accesorio(codigo, material, precio, stock, nombre))
        self.login["permisos"] = False 
        ventana.destroy()
    
    def seleccionar_imagen(self, button):
        path = filedialog.askopenfilename(
                title="Selecione Imagen",
                filetypes=(("image", ("*.jpg", "*.jpeg", "*.png", "*.gif")),)
                )
        self.img = Image.open(path).resize((40,40))
        self.img = ImageTk.PhotoImage(self.img)
        button.config( image=self.img, text=path)

    def ventana_modificar_articulo(self, codigo = "", nombre = "", stock = "",
                                precio = "", genero="", talle="", material = ""):
        var_producto = tk.StringVar()
        var_producto.set("accesorio") if genero == "" else var_producto.set("ropa")
        var_genero = tk.StringVar(value=genero)
        var_talle = tk.StringVar(value=talle)
        var_material = tk.StringVar(value=material)
        ventana = tk.Toplevel(self, bg=COLOR_BARRA_IZQ)
        ventana.geometry(f"300x600+{self.ANCHO_ROOT//2-150}+{self.ALTO_ROOT//2-250}")
        tk.Label(ventana, text="Imagen:", bg=COLOR_BARRA_IZQ, fg="white").pack()
        imagen = tk.Button(ventana, text="Selecione Imagen", command= lambda: self.seleccionar_imagen(imagen))
        imagen.pack(pady=15)
        tk.Label(ventana, text="Codigo", bg=COLOR_BARRA_IZQ, fg="white").pack()
        _codigo = tk.Entry(ventana)
        _codigo.insert(0,Importador.generar_codigo()) if codigo == "" else  _codigo.insert(0, codigo)
        _codigo.config(state=tk.DISABLED)
        _codigo.pack(pady=15)
        tk.Label(ventana, text="Nombre", bg=COLOR_BARRA_IZQ, fg="white").pack()
        _nombre = tk.Entry(ventana)
        if nombre != "": _nombre.insert(0, nombre)
        _nombre.pack(pady=15)
        tk.Label(ventana, text="Stock", bg=COLOR_BARRA_IZQ, fg="white").pack()
        _stock = tk.Entry(ventana)
        if stock != "": _stock.insert(0, stock)
        _stock.pack(pady=15)
        tk.Label(ventana, text="Precio", bg=COLOR_BARRA_IZQ, fg="white").pack()
        _precio = tk.Entry(ventana)
        if precio != "": _precio.insert(0, precio)
        _precio.pack(pady=15)
        frame_rbtn = tk.Frame(ventana, bg=COLOR_BARRA_IZQ)
        rbtn_accesorio = tk.Radiobutton(
            frame_rbtn, text="Accesorio", value="accesorio", variable=var_producto, state="disabled",  bg=COLOR_BARRA_IZQ, fg="white",
            selectcolor=COLOR_BARRA_IZQ, activebackground=COLOR_BARRA_IZQ, activeforeground="white"
            )
        rbtn_ropa = tk.Radiobutton(
            frame_rbtn, text="Ropa", value="ropa", variable=var_producto, state="disabled", bg=COLOR_BARRA_IZQ, fg="white",
            selectcolor=COLOR_BARRA_IZQ, activebackground=COLOR_BARRA_IZQ, activeforeground="white"
            )
        rbtn_accesorio.pack(side="left")
        rbtn_ropa.pack(side="left")
        frame_rbtn.pack()
        frame_info = tk.Frame(ventana, bg=COLOR_BARRA_IZQ)
        self.__cambio_area_info(frame_info,var_genero, var_talle, var_material, var_producto.get())

        frame_info.pack()
        var_producto.trace_add("write", lambda a,b,c: self.__cambio_area_info(frame_info, var_genero, var_talle, var_material, var_producto.get()))
        
        btn_agregar = tk.Button(ventana, text="Agregar", bg=COLOR_BUTTON, fg="white",
                command=lambda: self.modificar_stock(
                    imagen.cget("text"), _codigo.get(), _nombre.get(), _stock.get(), _precio.get(), var_material.get(), var_talle.get(), var_genero.get(), var_producto.get(), ventana)
            )
        btn_cancelar = tk.Button(ventana, text="Cancelar", bg=COLOR_BUTTON, fg="white", command=ventana.destroy)

        btn_cancelar.pack(side="left", padx=15)
        btn_agregar.pack(side="right", padx=15)

    def btn_modificar_articulo(self):
        try: 
            id = self.treeview.focus()
            if id == "": raise 
        except:
            messagebox.showinfo("Cuidado", "No a seleccionado ningun articulo de alguna lista")
            return 0
        item = self.treeview.item(id)
        self.ventana_modificar_articulo(
            item["text"],
            item["values"][1],
            item["values"][0],
            item["values"][2],
            item["values"][4],
            item["values"][5],
            item["values"][3],
            
        )
        

    def btn_agregar_articulo(self):
        var_producto = tk.StringVar()
        var_producto.set("accesorio")
        var_genero = tk.StringVar()
        var_talle = tk.StringVar()
        var_material = tk.StringVar()
        ventana = tk.Toplevel(self, bg=COLOR_BARRA_IZQ)
        ventana.geometry(f"300x600+{self.ANCHO_ROOT//2-150}+{self.ALTO_ROOT//2-250}")
        tk.Label(ventana, text="Imagen:", bg=COLOR_BARRA_IZQ, fg="white").pack()
        imagen = tk.Button(ventana, text="Selecione Imagen", command= lambda: self.seleccionar_imagen(imagen))
        imagen.pack(pady=15)
        tk.Label(ventana, text="Codigo", bg=COLOR_BARRA_IZQ, fg="white").pack()
        codigo = tk.Entry(ventana)
        codigo.insert(0,Importador.generar_codigo())
        codigo.config(state=tk.DISABLED)
        codigo.pack(pady=15)
        tk.Label(ventana, text="Nombre", bg=COLOR_BARRA_IZQ, fg="white").pack()
        nombre = tk.Entry(ventana)
        nombre.pack(pady=15)
        tk.Label(ventana, text="Stock", bg=COLOR_BARRA_IZQ, fg="white").pack()
        stock = tk.Entry(ventana)
        stock.pack(pady=15)
        tk.Label(ventana, text="Precio", bg=COLOR_BARRA_IZQ, fg="white").pack()
        precio = tk.Entry(ventana)
        precio.pack(pady=15)
        frame_rbtn = tk.Frame(ventana, bg=COLOR_BARRA_IZQ)
        rbtn_accesorio = tk.Radiobutton(
            frame_rbtn, text="Accesorio", value="accesorio", variable=var_producto,  bg=COLOR_BARRA_IZQ, fg="white",
            selectcolor=COLOR_BARRA_IZQ, activebackground=COLOR_BARRA_IZQ, activeforeground="white"
            )
        rbtn_ropa = tk.Radiobutton(
            frame_rbtn, text="Ropa", value="ropa", variable=var_producto,  bg=COLOR_BARRA_IZQ, fg="white",
            selectcolor=COLOR_BARRA_IZQ, activebackground=COLOR_BARRA_IZQ, activeforeground="white"
            )
        rbtn_accesorio.pack(side="left")
        rbtn_ropa.pack(side="left")
        frame_rbtn.pack()
        frame_info = tk.Frame(ventana, bg=COLOR_BARRA_IZQ)
        

        frame_info.pack()
        var_producto.trace_add("write", lambda a,b,c: self.__cambio_area_info(frame_info, var_genero, var_talle, var_material, var_producto.get()))
        
        btn_agregar = tk.Button(ventana, text="Agregar", bg=COLOR_BUTTON, fg="white",
                command=lambda: self.agregar_stock(
                    imagen.cget("text"), codigo.get(), nombre.get(), stock.get(), precio.get(), var_material.get(), var_talle.get(), var_genero.get(), var_producto.get(), ventana)
            )
        btn_cancelar = tk.Button(ventana, text="Cancelar", bg=COLOR_BUTTON, fg="white", command=ventana.destroy)

        btn_cancelar.pack(side="left", padx=15)
        btn_agregar.pack(side="right", padx=15)
    
    def btn_cambiar_permisos(self):
        ventana = VentanaUsuarios()
    
    def verificador_Agregar(self, info, cantidad, descuento, precio, ventana) -> int:
        if not cantidad.get().isdecimal() or int(cantidad.get()) <= 0:
            messagebox.showwarning("Cantidad no valida", "La cantidad tiene que ser mayor que 0")
            return 0
        if int(cantidad.get()) > int(info["values"][0]):
            messagebox.showwarning("Cantidad no valida", "No tienes tanto stock")
            return 0
        try:
            float(precio.get())
        except:
            messagebox.showwarning("precio no valida", "el precio tiene que ser un numero ejemplo: 12.5")
            return 0

        # Verifica si no supera el stock
        stock_carrito = 0
        for id in self.treeview_barra_abajo.get_children(""):
            if self.treeview_barra_abajo.item(id)["text"] == info["text"]:
                stock_carrito += int(self.treeview_barra_abajo.item(id)["values"][0])
            
        if stock_carrito >= info["values"][0]:
            messagebox.showwarning("cantidad no valida", "No tienes tanto stock")
            return 0

        subtotal = lambda c : float(precio.get()) * int(c) * ( ( 100 - int(descuento) ) / 100)
        
        for producto in self.ropa:
            if producto.get_codigo() == info["text"]:
                index = self.ropa.index(producto)
                self.ropa[index].set_stock(int(self.ropa[index].get_stock()) - int(cantidad.get()))
            
        
        # Verifica si existe y se esta se lo agrega
        for id in self.treeview_barra_abajo.get_children(""):
            if self.treeview_barra_abajo.item(id)["text"] == info["text"] and int(self.treeview_barra_abajo.item(id)["values"][2]) == descuento:
                cantidad_total = int(cantidad.get()) + int(self.treeview_barra_abajo.item(id)["values"][0])
                anterior_valor = float(self.treeview_barra_abajo.item(id)["values"][4])
                self.treeview_barra_abajo.item(id, values=(
                    cantidad_total,
                    info["values"][1],
                    descuento,
                    precio.get(),
                    subtotal(cantidad_total),
                    ))
                self.var_texto_total.set( subtotal(cantidad_total) + self.var_texto_total.get() - anterior_valor )
                
                self.insertar_treeview((self.ropa,self.accesorios), self.treeview)
                ventana.destroy()
                return 1

        # Inserta uno nuevo
        self.treeview_barra_abajo.insert(
            "", 
            tk.END,
            text=info["text"],
            image=info["image"],
            values=(cantidad.get(),
                    info["values"][1],
                    descuento,
                    precio.get(),
                    subtotal(cantidad.get())
                    )
        )
        self.var_texto_total.set( subtotal(cantidad.get()) + self.var_texto_total.get() )
        self.insertar_treeview((self.ropa,self.accesorios), self.treeview)
        ventana.destroy()
        return 1
    
    def ventana_agregar_carrito(self,info):
        var_descuento = tk.IntVar()
        ventana = tk.Toplevel(self, bg=COLOR_BARRA_IZQ)
        ventana.geometry(f"300x500+{self.ANCHO_ROOT//2-150}+{self.ALTO_ROOT//2-200}")
        ventana.title("Agregar al Carrito")
        tk.Label(ventana, text=info["values"][1], bg=COLOR_BARRA_IZQ, fg="white").pack(pady=10)
        tk.Label(ventana, text=f"Codigo: {info["text"]}", bg=COLOR_BARRA_IZQ, fg="white").pack(pady=10)
        tk.Label(ventana, text="Cantidad:", bg=COLOR_BARRA_IZQ, fg="white").pack()
        cantidad = tk.Entry(ventana)
        cantidad.insert(0,"1")
        cantidad.pack(pady=10)
        tk.Label(ventana, text="Precio:", bg=COLOR_BARRA_IZQ, fg="white").pack()
        precio = tk.Entry(ventana)
        precio.insert(0,info["values"][2])
        precio.config(state="disabled")
        precio.pack(pady=10)
        tk.Label(ventana, text="Descuento:", bg=COLOR_BARRA_IZQ, fg="white").pack()
        rbtn_descuentos = [
            tk.Radiobutton(ventana, text=f"{x}%", value=x, variable=var_descuento, bg=COLOR_BARRA_IZQ, fg="white",
                selectcolor=COLOR_BARRA_IZQ, activebackground=COLOR_BARRA_IZQ, activeforeground="white"
                ) 
            for x in range(0,100,25)
            ]
        for rbtn in rbtn_descuentos:
            rbtn.pack()

        if info["values"][3]: tk.Label(ventana, text=f"Material: {info["values"][3]}", bg=COLOR_BARRA_IZQ, fg="white").pack(pady=10)
        if info["values"][4]:
            tk.Label(ventana, text=f"Genero: {info["values"][4]}", bg=COLOR_BARRA_IZQ, fg="white").pack(pady=10)
            tk.Label(ventana, text=f"Talle: {info["values"][5]}", bg=COLOR_BARRA_IZQ, fg="white").pack(pady=10)
        tk.Button(ventana,
            text="Agregar",
            bg=COLOR_BUTTON,
            fg="white",
            command=lambda: self.verificador_Agregar(info, cantidad, var_descuento.get(), precio, ventana)
            ).pack(side="right", padx=40, ipadx=5, ipady=5)
        tk.Button(ventana, text="Salir", bg=COLOR_BUTTON, fg="white", command=ventana.destroy).pack(side="left", padx=40, ipadx=5, ipady=5)

    def quitar_carrito(self):
        item_seleccionado = self.treeview_barra_abajo.focus()
        for articulo in self.ropa:
            if articulo.get_codigo() == self.treeview_barra_abajo.item(item_seleccionado)["text"]:
                index = self.ropa.index(articulo)
                self.ropa[index].set_stock(int(articulo.get_stock()) + self.treeview_barra_abajo.item(item_seleccionado)["values"][0])
        self.var_texto_total.set(
            self.var_texto_total.get() - float(self.treeview_barra_abajo.item(item_seleccionado)["values"][4])
            )
        self.treeview_barra_abajo.delete((item_seleccionado))
        self.insertar_treeview((self.ropa,self.accesorios), self.treeview)
    
    def realizar_venta(self, treeview):
        id = self.treeview_barra_abajo.get_children("")
        fecha = datetime.now()
        for x in id: Importador.agregar_ventas(
            self.treeview_barra_abajo.item(x)["text"],
            self.treeview_barra_abajo.item(x)["values"][0],
            self.treeview_barra_abajo.item(x)["values"][3],
            self.treeview_barra_abajo.item(x)["values"][2],
            self.usuario,fecha
            
        )
        for x in id: self.treeview_barra_abajo.delete(x)
        for x in treeview.get_children(""): treeview.delete(x)
        self.var_texto_total.set(0.0)
        self.insertar_treeview((self.ropa,self.accesorios), self.treeview)
        Importador.actualizar_stock(self.ropa, "ropa")
        Importador.actualizar_stock(self.accesorios, "accesorios")
    
    def busqueda(self, datos : list[list,list], treeview : ttk.Treeview, palabra : str):
        nueva_lista = []
        vocales = [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u")]
        for lista in datos:
            for producto in lista:
                nombre = producto.get_descripcion().lower()
                for acento, vocal in vocales:
                    if acento in nombre:
                        cantidad = producto.get_descripcion().count(acento)
                        for y in range(cantidad):
                            index = producto.get_descripcion().index(acento)
                            nombre = producto.get_descripcion()[:index] + vocal + producto.get_descripcion()[index:]
                if palabra.lower() in  nombre:
                    nueva_lista.append(producto)
        
        for id in treeview.get_children(""): treeview.delete(id)
            
        self.insertar_treeview((nueva_lista,), treeview)
        
    
    def area_venta(self):
        var_buscador = tk.StringVar()
        frame_arriba = tk.Frame(self.frame_area_trabajo, bg="#fff")
        frame_izq = tk.Frame(self.frame_area_trabajo, bg="#fff")
        frame_der = tk.Frame(self.frame_area_trabajo, bg="#fff")

        buscador = tk.Entry(frame_arriba, width=50, textvariable=var_buscador)
        buscador.insert(0,"Buscar...")
        
        btn_agregar = tk.Button(
            frame_der,
            text="Agregar Articulo",
            bg=COLOR_BUTTON,
            fg="white",
            command=lambda: self.ventana_agregar_carrito(self.treeview.item(self.treeview.focus()))
            )
        btn_quitar = tk.Button(
            frame_der,
            text="Quitar Articulo",
            bg=COLOR_BUTTON,
            fg="white",
            command=self.quitar_carrito
            )
        
        self.treeview = ttk.Treeview(frame_izq, columns=["stock", "nombre", "precio", "material", "genero", "talle"])
        
        var_buscador.trace_add("write",lambda a,b,c: self.busqueda(
                (self.ropa, self.accesorios,),
                self.treeview,
                var_buscador.get()
                )
            )
        
        btn_vender = tk.Button(
            frame_der,
            text="Vender",
            bg=COLOR_BUTTON,
            fg="white",
            command=lambda: self.realizar_venta(self.treeview)
            )
        
        self.treeview.heading("#0", text="Codigo")
        self.treeview.heading("stock", text="Stock")
        self.treeview.heading("nombre", text="Nombre")
        self.treeview.heading("precio", text="Precio")
        self.treeview.heading("material", text="Material")
        self.treeview.heading("genero", text="Genero")
        self.treeview.heading("talle", text="Talle")

        self.treeview.column("#0", width=100, anchor="center")
        self.treeview.column("stock", width=50, anchor="center")
        self.treeview.column("precio", width=50, anchor="center")
        self.treeview.column("talle", width=50, anchor="center")
        self.treeview.column("genero", anchor="center")
        self.treeview.column("material", anchor="center")
        
        self.insertar_treeview((self.ropa, self.accesorios), self.treeview)
        
        self.treeview.pack(padx=15, expand=True, fill="both")
        btn_agregar.pack(padx=15, pady=15)
        btn_quitar.pack()
        btn_vender.pack(side="bottom", pady=15)
        buscador.pack(pady=15, ipadx=5)
        
        frame_arriba.pack( fill="x")
        frame_izq.pack(side="left", fill="both",expand=True)
        frame_der.pack(side="right", fill="both")
    
    def ver_productos(self, lista_productos):
        var_busqueda = tk.StringVar()
        frame_arriba = tk.Frame(self.frame_area_trabajo, bg="#fff")
        frame_izq = tk.Frame(self.frame_area_trabajo, bg="#fff")

        buscador = tk.Entry(frame_arriba, width=50, textvariable=var_busqueda)
        buscador.insert(0,"Buscar...")
        
        
        self.treeview = ttk.Treeview(frame_izq, columns=["stock", "nombre", "precio", "material", "genero", "talle"])
        
        var_busqueda.trace_add("write", lambda a,b,c: self.busqueda(
                (lista_productos,),
                self.treeview,
                var_busqueda.get()
            )
        )
        
        self.treeview.heading("#0", text="Codigo")
        self.treeview.heading("stock", text="Stock")
        self.treeview.heading("nombre", text="Nombre")
        self.treeview.heading("precio", text="Precio")
        self.treeview.heading("material", text="Material")
        self.treeview.heading("genero", text="Genero")
        self.treeview.heading("talle", text="Talle")

        self.treeview.column("#0", width=100, anchor="center")
        self.treeview.column("stock", width=50, anchor="center")
        self.treeview.column("precio", width=50, anchor="center")
        self.treeview.column("talle", width=50, anchor="center")
        self.treeview.column("genero", anchor="center")
        self.treeview.column("material", anchor="center")
        
        self.insertar_treeview((lista_productos,), self.treeview)
        
        self.treeview.pack(padx=15, expand=True, fill="both", pady=5)
        buscador.pack(pady=15, ipadx=5)
        
        frame_arriba.pack( fill="x")
        frame_izq.pack(side="left", fill="both",expand=True)
    
    def barra_abajo(self):
        self.frame_barra_abajo = tk.Frame(self, height=self.ALTO_ROOT//4, bg=COLOR_BARRA_ABAJO, border=2  )
        frame_izq = tk.Frame(self.frame_barra_abajo, bg=COLOR_BARRA_ABAJO)
        frame_der = tk.Frame(self.frame_barra_abajo)

        self.treeview_barra_abajo = ttk.Treeview(frame_izq, columns=["cantidad","nombre", "descuento", "precio","subtotal"])
        self.treeview_barra_abajo.heading("#0", text="Codigo")
        self.treeview_barra_abajo.heading("nombre", text="Nombre")
        self.treeview_barra_abajo.heading("cantidad", text="Cantidad")
        self.treeview_barra_abajo.heading("descuento", text=" % ")
        self.treeview_barra_abajo.heading("precio", text="Precio")
        self.treeview_barra_abajo.heading("subtotal", text="Subtotal")
        self.treeview_barra_abajo.column("#0", width=30, anchor="center")
        self.treeview_barra_abajo.column("cantidad", width=30, anchor="center")
        self.treeview_barra_abajo.column("precio", width=30, anchor="center")
        self.treeview_barra_abajo.column("descuento", width=30, anchor="center")
        self.treeview_barra_abajo.column("subtotal", width=30, anchor="center")
        self.treeview_barra_abajo.pack(expand=True, fill="both")

        self.var_texto_total = tk.DoubleVar()
        texto_total = tk.Label(frame_der, textvariable=self.var_texto_total, bg=COLOR_BARRA_ABAJO, font=(LETRA,TAMANIO,ESTILO))
        texto_total.pack()
        
        frame_izq.pack(side="left",fill="both",expand=True)
        frame_der.pack(side="bottom",padx=20,pady=20)
    
    def area_trabajo(self):
        self.img = Image.open("./assets/img/background.jpg")
        self.img = self.img.resize((680,480))
        self.img = ImageTk.PhotoImage(self.img)
        self.frame_area_trabajo = tk.Frame(self, border=2, background="#000")
        label_imagen = tk.Label(self.frame_area_trabajo, image=self.img)
        label_imagen.pack()

    def imprimir(self):
        self.area_trabajo()
        self.frame_barra_izquierda.pack(side="left")
        self.frame_barra_izquierda.pack_propagate(False)
        self.frame_area_trabajo.pack(side="top", fill="both", expand=True)
        self.text_usuario.pack(side="bottom", pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()