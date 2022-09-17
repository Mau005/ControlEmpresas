from entidades.registrousaurios import RegistroUsuarios

class Control_Network():

    def __init__(self) -> None:
        self.hilos_cliente = {}
        self.pendientes_desconexion = []

    def agregar_pendiente(self, key):
        if not key in self.pendientes_desconexion:
            self.pendientes_desconexion.append(key)

    def agregar_hilo(self, hilo):
        if self.hilos_cliente.get(hilo.usuario.correo) is None:
            self.hilos_cliente.update({hilo.usuario.correo: hilo})
            return True
        return False

    def eliminar(self, key):
        self.hilos_cliente[key].enfuncionamiento = False
        self.hilos_cliente.pop(key)
    def __agregar(self, key, valor):
        self.hilos_cliente.update({key: valor})

    def actualizar(self):
        for elementos in self.hilos_cliente.values():
            elementos.actualizar()

        for pendiente_eliminar in self.pendientes_desconexion:
            self.eliminar(pendiente_eliminar)
        self.pendientes_desconexion.clear()

    def solicitar_hilos(self):
        return self.hilos_cliente

    def eventos(self):
        pass

