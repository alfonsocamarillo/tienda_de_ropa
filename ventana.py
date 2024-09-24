import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from constantes import *
from PIL import Image, ImageTk
from importador import Importador

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.ANCHO_ROOT   = self.winfo_screenwidth()  - 100
        self.ALTO_ROOT    = self.winfo_screenheight() - 150

        self.title("Mi Tiendita de Ropa y Accesorios")
        self.geometry(f"{self.ANCHO_ROOT}x{self.ALTO_ROOT}+{POS_X}+{POS_Y}")
        self.resizable(0,0)
        self.configure(bg=COLOR_BACKGROUND) 
        style = ttk.Style()
        style.configure("Treeview", rowheight=42)

        self.img = None
        self.accesorios = Importador.importar("./assets/csv/accesorios.csv")
        self.ropa = Importador.importar("./assets/csv/ropa.csv")
        self.img_accesorio = ImageTk.PhotoImage(image=Image.open("./assets/img/2.png").resize((40,40)))
        self.img_ropa = ImageTk.PhotoImage(image=Image.open("./assets/img/1.png").resize((40,40)))

        self.ANCHO_BARRA = int(self.ANCHO_ROOT / 5)

        self.lista_btn_izquierda = ["Ver Prendas", "Ver Accesorios", "Realizar Ventas", "Agregar Articulos", "Modificar Articulos", "Cambiar Permisos", "Salir"]
        
        self.barra_izquierda()
        self.area_trabajo()
        
        self.imprimir()
    
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
        
        btn_lista_izquierda[2].config(command=self.btn_realizar_venta)
    
    def agregar_producto(self, widget, img, cantidad, descripcion, descuento, precio ) -> tk.Frame:
        frame = tk.Frame(widget, bg=COLOR_BARRA_ABAJO)
        img = tk.Label(frame, image=img)
        cantidad = tk.Label(frame, text=cantidad, font=(LETRA,TAMANIO,ESTILO), bg=COLOR_BARRA_ABAJO)
        descripcion = tk.Label(frame, text=descripcion, font=(LETRA,TAMANIO,ESTILO), bg=COLOR_BARRA_ABAJO)
        descuento = tk.Label(frame, text=descuento, font=(LETRA,TAMANIO,ESTILO), bg=COLOR_BARRA_ABAJO)
        precio = tk.Label(frame, text=precio, font=(LETRA,TAMANIO,ESTILO), bg=COLOR_BARRA_ABAJO)
        img.pack(side="left", padx=20)
        cantidad.pack(side="left")
        descripcion.pack(side="left")
        descuento.pack(side="left")
        precio.pack(side="left")
        return frame
        
    def btn_realizar_venta(self):
        for x in self.frame_area_trabajo.winfo_children(): x.destroy()
        try:
            self.frame_barra_abajo.destroy()
        except:
            print("")
        self.area_venta()
        self.barra_abajo()
        self.frame_barra_abajo.pack_propagate(False)
        self.frame_barra_abajo.pack(side="bottom", fill="x")
    
    def verificador_Agregar(self, info, cantidad, descuento, precio, ventana) -> int:
        if not cantidad.get().isdecimal() or int(cantidad.get()) <= 0:
            messagebox.showwarning("Cantidad no valida", "La cantidad tiene que ser mayor que 0")
            return 0
        if int(cantidad.get()) > int(info["values"][0]):
            messagebox.showwarning("Cantidad no valida", "No tienes tanto stock")
            return 0
        """
        if not descuento.get().isdecimal() or int(descuento.get()) < 0 or int(descuento.get()) > 100 :
            messagebox.showwarning("descuento no valida", "el descuento tiene que ser un numero entre 0 y 100")
            return 0
        """
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
        self.var_texto_total.set(
            self.var_texto_total.get() - float(self.treeview_barra_abajo.item(item_seleccionado)["values"][4])
            )
        self.treeview_barra_abajo.delete((item_seleccionado))
    
    def realizar_venta(self, treeview):
        id = self.treeview_barra_abajo.get_children("")
        codigo = [self.treeview_barra_abajo.item(x)["text"] for x in id]
        for ropa in self.ropa:
            if ropa.get_codigo() in codigo:
                ropa.set_stock(
                    int(ropa.get_stock()) - int(self.treeview_barra_abajo.item(
                        id[codigo.index(ropa.get_codigo()) ]
                        )["values"][0])
                    )
        for x in id: self.treeview_barra_abajo.delete(x)
        for x in treeview.get_children(""): treeview.delete(x)
        for item in self.ropa[:5]:
            treeview.insert("",
                tk.END,
                text=item.get_codigo(),
                image=self.img_ropa, 
                values=[
                    item.get_stock(),
                    item.get_descripcion(),
                    item.get_precio(),
                    "",
                    item.get_genero(),
                    item.get_talle()
                ]
                )
    
    def area_venta(self):
        frame_arriba = tk.Frame(self.frame_area_trabajo, bg="#fff")
        frame_izq = tk.Frame(self.frame_area_trabajo, bg="#fff")
        frame_der = tk.Frame(self.frame_area_trabajo, bg="#fff")

        buscador = tk.Entry(frame_arriba, width=50)
        buscador.insert(0,"Buscar...")
        btn_agregar = tk.Button(
            frame_der,
            text="Agregar Articulo",
            bg=COLOR_BUTTON,
            fg="white",
            command=lambda: self.ventana_agregar_carrito(treeview.item(treeview.focus()))
            )
        btn_quitar = tk.Button(
            frame_der,
            text="Quitar Articulo",
            bg=COLOR_BUTTON,
            fg="white",
            command=self.quitar_carrito
            )
        
        treeview = ttk.Treeview(frame_izq, columns=["stock", "nombre", "precio", "material", "genero", "talle"])
        
        btn_vender = tk.Button(
            frame_der,
            text="Vender",
            bg=COLOR_BUTTON,
            fg="white",
            command=lambda: self.realizar_venta(treeview)
            )
        
        treeview.heading("#0", text="Codigo")
        treeview.heading("stock", text="Stock")
        treeview.heading("nombre", text="Nombre")
        treeview.heading("precio", text="Precio")
        treeview.heading("material", text="Material")
        treeview.heading("genero", text="Genero")
        treeview.heading("talle", text="Talle")

        treeview.column("#0", width=100, anchor="center")
        treeview.column("stock", width=50, anchor="center")
        treeview.column("precio", width=50, anchor="center")
        treeview.column("talle", width=50, anchor="center")
        treeview.column("genero", anchor="center")
        treeview.column("material", anchor="center")
        for item in self.accesorios[:5]:
            treeview.insert("",
                tk.END,
                text=item.get_codigo(),
                image=self.img_accesorio,
                values=[
                    item.get_stock(),
                    item.get_descripcion(),
                    item.get_precio(),
                    item.get_material(),
                    "",
                    ""
                ]
                )
        for item in self.ropa[:5]:
            treeview.insert("",
                tk.END,
                text=item.get_codigo(),
                image=self.img_ropa, 
                values=[
                    item.get_stock(),
                    item.get_descripcion(),
                    item.get_precio(),
                    "",
                    item.get_genero(),
                    item.get_talle()
                ]
                )
        
        treeview.pack(padx=15, expand=True, fill="both")
        btn_agregar.pack(padx=15, pady=15)
        btn_quitar.pack()
        btn_vender.pack(side="bottom", pady=15)
        buscador.pack(pady=15, ipadx=5)
        
        frame_arriba.pack( fill="x")
        frame_izq.pack(side="left", fill="both",expand=True)
        frame_der.pack(side="right", fill="both")
    
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
        self.frame_barra_izquierda.pack(side="left")
        self.frame_area_trabajo.pack(side="top", fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()