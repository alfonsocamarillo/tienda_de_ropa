from .producto import Producto

class Ropa(Producto):
    def __init__(
                self, codigo: str,
                talle : str,
                genero : str,
                precio: float | None = 0,
                stock: int | None = 0,
                descripcion: str | None = "",
                ) -> None:
        super().__init__(codigo, precio, stock, descripcion)
        self.__talle = talle
        self.__genero = genero
        self.__lista_talles = ["S", "M", "L", "XL"]
        self.__lista_generos = ["Masculino", "Femenino", "Unisex"]
    
    def get_talle(self):
        return self.__talle
    
    def get_genero(self):
        return self.__genero

    def set_talle(self, nuevo_talle : str):
        """
        Args:
            nuevo_talle (str): [ S , M , L , XL ]
        """
        if nuevo_talle.upper() in self.__lista_talles:
            self.__talle = self.__lista_talles
        else:
            print(f"El Talle que se paso no es valido \nLos valores validos son {self.__lista_talles}")
    
    def set_genero(self, nuev_genero : str):
        """
        Args:
            nuev_genero (str): [ Masculino , Femenino , Unisex]
        """
        if nuev_genero.capitalize() in self.__lista_generos:
            self.__genero = nuev_genero
        else:
            print(f"No es valido el valor pasado\nLos valores validos son {self.__lista_generos}")
    
    def get_info(self):
        info = super().get_info()
        info.update({
                        "Talle" : self.__talle,
                        "Genero" : self.__genero
                    })
        return info
            
if __name__ == "__main__":
    ropa = Ropa("23","XL","Masculino")