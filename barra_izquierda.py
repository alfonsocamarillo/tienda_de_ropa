import tkinter as tk
from constantes import *
from modificar_agregar_stock import ModificarAgregar
from ventana_usuarios import VentanaUsuarios

lista_btn_izquierda = ["Ver Prendas", "Ver Accesorios", "Realizar Ventas", "Agregar Articulos", "Modificar Articulos", "Cambiar Usuario" ,"Cambiar Permisos", "Salir"]

class FrameIzquierdo(tk.Frame):
    def __init__(self,master):
        super().__init__(
            master,
            width=int( (master.winfo_screenwidth()  - 101) / 5),
            height= master.winfo_screenheight() - 150,
            bg=COLOR_BARRA_IZQ,
            border=2
            )
        self.master = master
        self.usuario = None
        btn_lista_izquierda = [tk.Button(
            self,
            text=f"{lista_btn_izquierda[x]}",
            bg=COLOR_BUTTON,
            fg="white",
            height=1,
            width=ANCHO_BUTTON,
            font=(LETRA,TAMANIO,ESTILO),
            border=5
            ) for x in range(len(lista_btn_izquierda))]
        for x in range(len(btn_lista_izquierda)):
            btn_lista_izquierda[x].place(x=10, y=60*(x+1))
        
        self.text_usuario = tk.Label(self, text=f"Usuario: {self.usuario}", bg=COLOR_BARRA_IZQ, fg="white" ,font=(LETRA,TAMANIO,ESTILO))

        btn_lista_izquierda[0].config(command=self.btn_ver_prendas)
        btn_lista_izquierda[1].config(command=self.btn_ver_accesorios)
        btn_lista_izquierda[2].config(command=self.btn_realizar_venta)
        btn_lista_izquierda[3].config(command= lambda : ModificarAgregar(self) if self.master.login["permisos"] else tk.messagebox.showinfo("Permisos", "No tienes los persmisos requeridos") )
        btn_lista_izquierda[4].config(command= lambda : self.btn_modificar_articulo() if self.master.login["permisos"] else tk.messagebox.showinfo("Permisos", "No tienes los persmisos requeridos"))
        btn_lista_izquierda[-3].config(command=lambda : self.master.ventana_verificar_usuario(None, False))
        btn_lista_izquierda[-2].config(command=lambda :self.btn_cambiar_permisos() if self.master.login["permisos"] else tk.messagebox.showinfo("Permisos", "No tienes los persmisos requeridos"))
        btn_lista_izquierda[-1].config(command=self.quit)
        
        self.text_usuario.pack(side="bottom", pady=10)
        self.pack(side="left")
        self.pack_propagate(False)
    
    def btn_realizar_venta(self):
        self.master.limpiar_area_trabajo()
        self.master.area_venta()
        self.master.barra_abajo()
        self.master.frame_barra_abajo.pack_propagate(False)
        self.master.frame_barra_abajo.pack(side="bottom", fill="x")
    
    def btn_ver_prendas(self):
        self.master.limpiar_area_trabajo()
        self.master.ver_productos(("ropa",))
    
    def btn_ver_accesorios(self):
        self.master.limpiar_area_trabajo()
        self.master.ver_productos(("accesorios",))
    
    def btn_modificar_articulo(self):
        try: 
            id = self.master.treeview.focus()
            if id == "": raise 
        except:
            tk.messagebox.showinfo("Cuidado", "No a seleccionado ningun articulo de alguna lista")
            return 0
        item = self.master.treeview.item(id)
        ventana = ModificarAgregar(
            self,
            item["text"],
            item["values"][1],
            item["values"][0],
            item["values"][2],
            item["values"][4],
            item["values"][5],
            item["values"][3],
            False)
    
    def btn_cambiar_permisos(self):
        ventana = VentanaUsuarios()

if __name__ == "__main__":
    ventan = tk.Tk()
    frame = FrameIzquierdo(ventan)
    ventan.mainloop()