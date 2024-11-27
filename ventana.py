import tkinter as tk
from tkinter import ttk, messagebox
from constantes import *
from PIL import Image, ImageTk
from productos.ropa import Ropa
from productos.accesorio import Accesorio
from datetime import datetime
import db
from tabla_stock import TablaStock
from barra_izquierda import FrameIzquierdo
from peewee import SqliteDatabase, Model, CharField, BooleanField, FloatField, IntegerField, Check, DateTimeField, ForeignKeyField


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
    
        self.login = dict()
        self.login["validacion"] = False 
        self.login["permisos"] =  False
        self.login["id"] = None

        self.img = None
        self.ropa = [Ropa(*x) for x in db.datos("ropa")]   
        
        self.frame_izquierdo = FrameIzquierdo(self)
        self.ventana_verificar_usuario(self.imprimir, False)
    
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
        usuarios = db.datos("usuarios")
        for u , p , c in usuarios:
            if usuario == u and contrasena == c:
                self.frame_izquierdo.usuario = u
                self.frame_izquierdo.text_usuario.config(text=f"Usuario: {u}")
                self.login["validacion"] =  True 
                self.login["permisos"] =  bool(p)
                self.login["id"] = u
                try:
                    if not administrador or self.login["permisos"]:
                        funcion()
                except:
                    print("no se ejecuta funcion en login")
                messagebox.showinfo("Usuario", f"El usuario que esta usando es: \n{u.upper()}")
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
        ventana.attributes('-topmost', True)
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
                
                self.treeview.insertar_stock(("ropa", "accesorios"))
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
        self.treeview.insertar_stock(("ropa", "accesorios"))
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
        self.treeview_barra_abajo.delete((item_seleccionado))
    
    def realizar_venta(self, treeview):
        id = self.treeview_barra_abajo.get_children("")
        fecha = datetime.now()
        for x in id:
            codigo = self.treeview_barra_abajo.item(x)["text"]
            cantidad = int(self.treeview_barra_abajo.item(x)["values"][0])

            db.agregar_ventas(
                codigo,
                self.treeview_barra_abajo.item(x)["values"][1],
                cantidad,
                self.treeview_barra_abajo.item(x)["values"][3],
                self.treeview_barra_abajo.item(x)["values"][2],
                fecha,
                self.login["id"]
            )
            info  = db.busqueda_id("ropa", codigo)
            if info:
                db.actualizar_ropa(codigo, stock=(int(info[4]) - cantidad))
            else:
                info = db.busqueda_id("accesorios", codigo)
                db.actualizar_accesorios(codigo, stock=(int(info[3]) - cantidad))

        for x in id: self.treeview_barra_abajo.delete(x)
        self.var_texto_total.set(0.0)
        self.treeview.insertar_stock(("ropa", "accesorios"))
    
    def busqueda(self, tablas : list[str,str], treeview : ttk.Treeview, palabra : str):
        nueva_lista = []
        for tabla in tablas:
            if tabla == "ropa":
                for datos in db.busqueda_texto(tabla, palabra): nueva_lista.append(Ropa(*datos))
            elif tabla == "accesorios":
                for datos in db.busqueda_texto(tabla, palabra): nueva_lista.append(Accesorio(*datos))
            
        self.treeview.insertar_stock((nueva_lista,), False)
        
    
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
        
        self.treeview = TablaStock(frame_izq, ("ropa","accesorios"))
        
        var_buscador.trace_add("write",lambda a,b,c: self.busqueda(
                ("ropa", "accesorios"),
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
        
        self.treeview.pack(padx=15, expand=True, fill="both")
        btn_agregar.pack(padx=15, pady=15)
        btn_quitar.pack()
        btn_vender.pack(side="bottom", pady=15)
        buscador.pack(pady=15, ipadx=5)
        
        frame_arriba.pack( fill="x")
        frame_izq.pack(side="left", fill="both",expand=True)
        frame_der.pack(side="right", fill="both")
    
    def ver_productos(self, tabla : list[str,str]):
        var_busqueda = tk.StringVar()
        frame_arriba = tk.Frame(self.frame_area_trabajo, bg="#fff")
        frame_izq = tk.Frame(self.frame_area_trabajo, bg="#fff")

        buscador = tk.Entry(frame_arriba, width=50, textvariable=var_busqueda)
        buscador.insert(0,"Buscar...")
        
        
        self.treeview = TablaStock(frame_izq, tabla)
        
        var_busqueda.trace_add("write", lambda a,b,c: self.busqueda(
                tabla,
                self.treeview,
                var_busqueda.get()
            )
        )
        
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
        self.frame_area_trabajo.pack(side="top", fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()