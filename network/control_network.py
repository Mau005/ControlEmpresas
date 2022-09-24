class Control_Network():

    def __init__(self) -> None:
        self.hilos_cliente = {}
        self.pendientes_desconexion = []
        self.pendientes_recuperacion = []
        self.control_recuperacion = {}

    def agregar_control_recuperacion(self, correo, valor):
        if self.control_recuperacion.get(correo) is None:
            self.control_recuperacion.update({correo: valor})
            return True
        return False

    def buscar_control_recuperacion(self, correo):

        if correo in self.control_recuperacion.keys():
            return True
        return False

    def comprobar_control_recuperacion(self, correo, valor):

        if self.control_recuperacion[correo] == valor:
            self.pendientes_recuperacion.append(correo)
            return True
        return False

    def comprobar_control_hilos(self, correo):
        """
        Methodo especifico para encontrar si el hilo se encuentra activo
        :str correo: correo str
        :return: bool si existe el hilo
        """
        if correo in self.hilos_cliente.keys():
            return True
        return False
    def perdida_tiempo_recuperacion(self, correo):
        self.control_recuperacion.pop(correo)

    def agregar_pendiente_hilos(self, key):
        if not key in self.pendientes_desconexion:
            self.pendientes_desconexion.append(key)

    def agregar_hilo(self, hilo):
        if self.hilos_cliente.get(hilo.usuario.correo) is None:
            self.hilos_cliente.update({hilo.usuario.correo: hilo})
            return True
        return False

    def eliminar_hilos(self, key):
        if self.hilos_cliente.get(key) is not None:
            self.hilos_cliente[key].enfuncionamiento = False
            self.hilos_cliente.pop(key)

    def eliminar_recuperacion(self, key):
        self.control_recuperacion.pop(key)

    def __agregar_hilos(self, key, valor):
        self.hilos_cliente.update({key: valor})

    def actualizar(self):
        """
        Methodo que actualiza cada 1 segundo, espera listas para poder eliminar
        contenido en tiempo real de los diccionarios
        :return:
        """
        for elementos in self.hilos_cliente.values():
            elementos.actualizar()

        for pendiente_eliminar in self.pendientes_desconexion:
            self.eliminar_hilos(pendiente_eliminar)

        for pendientes_eliminar in self.pendientes_recuperacion:
            self.eliminar_recuperacion(pendientes_eliminar)

        self.pendientes_desconexion.clear()
        self.pendientes_recuperacion.clear()

    def solicitar_hilos(self):
        return self.hilos_cliente

    def eventos(self):
        pass
