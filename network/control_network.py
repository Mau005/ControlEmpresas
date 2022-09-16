
class Control_Network():
    
    def __init__(self) -> None:
        self.hilos_cliente = {}
        
        
    def __existe_hilo(self, correo):
        """Methodo puesto para comprobar si un hilo ha iniciado correctamente
        Args:
            correo (str): correo de usuario

        Returns:
            bool: si existe
        """
        if self.hilos_cliente.get(correo) !=None:
            return True
        return False

    def agregar_hilo(self, hilo):
        if self.__existe_hilo(hilo.usuario.correo):
            self.hilos_cliente.update({hilo.usuario.correo: hilo})
            return True
        return False
    
    def actualizar(self, dt):
        for elementos in self.hilos_cliente.values():
            elementos.actualiza(dt)
    
    def eventos(self):
        pass
    
    def actualizar(self):
        pass