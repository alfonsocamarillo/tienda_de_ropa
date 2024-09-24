from usuario import Usuario

class Admin(Usuario):
    def __init__(self, nombre, contrasena) -> None:
        super().__init__(nombre, contrasena)
        self.__permisos = True
    
    def set_permisos(self):
        print("No se puede modificar los permisos")


if __name__ == "__main__":
    admin = Admin("juan", "123")
    admin.set_permisos()
    