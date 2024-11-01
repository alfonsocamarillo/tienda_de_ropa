
from tkinter import Toplevel, ttk, messagebox
import tkinter as tk
from importador import Importador
from constantes import *

class VentanaUsuarios(Toplevel):
    def __init__(self):
        super().__init__()
        self.img_ojo = tk.PhotoImage(file="./assets/img/interfas/ojo.png")
        self.config(bg=COLOR_BARRA_IZQ)
        self.geometry("500x300")
        self.title("Administrador de Usuarios")
        btns = ["Agregar", "Actualizar", "Eliminar"]
        self.treeview = ttk.Treeview(self, columns=("admin","contrasena"))
        self.treeview.heading("#0", text="Usuario")
        self.treeview.heading("admin", text="Administrador")
        self.treeview.heading("contrasena", text="Contraseña")
        self.treeview.column("admin", width=90)
        self.treeview.column("contrasena", width=90)

        for usuario, permiso,contrasena in Importador.importar_usuarios():
            self.treeview.insert("", tk.END, text=usuario, values=[permiso, contrasena])
        
        self.treeview.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        frame = tk.Frame(self, bg=COLOR_BARRA_IZQ)
        
        btns = [tk.Button(frame,text=x, bg=COLOR_BUTTON, fg="white") for x in btns]
        for btn in btns: btn.pack(pady=10)
        
        btns[0].config(command=lambda : self.__agregar_actualizar_usuario())
        btns[1].config(command=lambda : self.__agregar_actualizar_usuario(
            self.treeview.item(self.treeview.focus())["text"],
            self.treeview.item(self.treeview.focus())["values"][0],
            self.treeview.item(self.treeview.focus())["values"][1]
        ))
        btns[-1].config(command=lambda: self.__eliminar_usuario(self.treeview))
        
        
        frame.pack(side="right", fill="y", ipadx=5)
    
    def __agregar_actualizar_usuario(self, nombre = "", admin=False, contrasena = ""):
        var_admin = tk.BooleanVar()
        var_admin.set(admin)
        text_btn = "Agregar" if not nombre else "Actualizar"
        ventana = Toplevel(self, bg=COLOR_BARRA_IZQ, padx=20,pady=20)
        tk.Label(ventana, text="Nombre:", bg=COLOR_BARRA_IZQ, fg="white").pack()
        _usuario = tk.Entry(ventana)
        _usuario.insert(0,nombre)
        _usuario.pack()
        tk.Label(ventana, text="Contraseña:", bg=COLOR_BARRA_IZQ, fg="white").pack()
        _contrasena = tk.Entry(ventana, show="*")
        _contrasena.insert(0, contrasena)
        _contrasena.pack()
        tk.Button(ventana, image=self.img_ojo, bg=COLOR_BARRA_IZQ, command=lambda : _contrasena.config(show="")).pack(ipadx=2,ipady=2)
        tk.Label(ventana, text="Administrador:", bg=COLOR_BARRA_IZQ, fg="white").pack()
        tk.Radiobutton(ventana, text="Si", value=True,
                        variable=var_admin, bg=COLOR_BARRA_IZQ, fg="white",
                selectcolor=COLOR_BARRA_IZQ, activebackground=COLOR_BARRA_IZQ, activeforeground="white", ).pack()
        tk.Radiobutton(ventana, text="No", value=False,
                        variable=var_admin, bg=COLOR_BARRA_IZQ, fg="white",
                selectcolor=COLOR_BARRA_IZQ, activebackground=COLOR_BARRA_IZQ, activeforeground="white",).pack()
        tk.Button(ventana, text="Cancelar", command=ventana.destroy).pack(side="left")
        tk.Button(ventana, text=text_btn,
                    command= lambda : self.__btn_agregar_actualizar(text_btn, nombre, _usuario.get(), var_admin.get(),_contrasena.get(), ventana)
                ).pack(side="right")
    
    def __btn_agregar_actualizar(self, text_btn, nombre, usuario, permiso, contrasena, ventana):
        if text_btn == "Agregar":
            if Importador.agregar_usuario(usuario, permiso, contrasena):
                self.treeview.insert("", "end", text=usuario, values=(permiso,contrasena))
                ventana.destroy()
            else:
                messagebox.showinfo("Cuidad", "Ese nombre de usuario ya esta en uso")
        else:
            Importador.actualizar_usuario(nombre, usuario, permiso, contrasena)
            item = self.treeview.focus()
            self.treeview.item(item, text=usuario, values=(permiso,contrasena))
            ventana.destroy()
        

    def __eliminar_usuario(self,treeview):
        id = treeview.focus()
        usuario = treeview.item(id)
        for user, permiso, contrasena in  Importador.importar_usuarios():
            if permiso == "True" and user != usuario["text"]:
                if messagebox.askokcancel("Eliminar", f"Decea eliminar al usuario {usuario['text']}", icon="warning"):
                    Importador.eliminar_usuario(usuario["text"])
                    treeview.delete(id)
                    return None
                else: return None
        messagebox.showinfo("Cuidado", "Es el unico administrador no se puede eliminar")

if __name__ == "__main__":
    ventana = tk.Tk()
    sub_ventana = VentanaUsuarios()
    ventana.mainloop()