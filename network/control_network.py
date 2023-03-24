class Control_Network():

    def __init__(self) -> None:
        self.hilos_cliente = {}
        self.pendientes_desconexion = []
        self.pendientes_recuperacion = []
        self.control_recuperacion = {}

    def agregar_control_recuperacion(self, nombre_cuenta, valor):
        if self.control_recuperacion.get(nombre_cuenta) is None:
            self.control_recuperacion.update({nombre_cuenta: valor})
            return True
        return False

    def buscar_control_recuperacion(self, nombre_cuenta):

        if nombre_cuenta in self.control_recuperacion.keys():
            return True
        return False

    def comprobar_control_recuperacion(self, nombre_cuenta, valor):

        if self.control_recuperacion[nombre_cuenta] == valor:
            self.pendientes_recuperacion.append(nombre_cuenta)
            return True
        return False

    def comprobar_control_hilos(self, nombre_cuenta):
        """
        Methodo especifico para encontrar si el hilo se encuentra activo
        :str nombre_cuenta: nombre_cuenta str
        :return: bool si existe el hilo
        """
        if nombre_cuenta in self.hilos_cliente.keys():
            return True
        return False
    def perdida_tiempo_recuperacion(self, nombre_cuenta):
        self.control_recuperacion.pop(nombre_cuenta)

    def agregar_pendiente_hilos(self, key):
        if not key in self.pendientes_desconexion:
            self.pendientes_desconexion.append(key)

    def agregar_hilo(self, hilo):
        if self.hilos_cliente.get(hilo.control_usuarios.cuenta.nombre_cuenta) is None:
            self.hilos_cliente.update({hilo.control_usuarios.cuenta.nombre_cuenta: hilo})
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
