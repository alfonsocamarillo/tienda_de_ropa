
class Usuario():
    def __init__(self, nombre, contrasena, permisos = False) -> None:
        self.__nombre = nombre
        self.__contrasena = contrasena
        self.__permisos = permisos
    
    def set_permisos(self, permisos : bool):
        self.__permisos = permisos

    def incio_secion(self, nombre, contrasena):
        return nombre == self.__nombre and contrasena == self.__contrasena