class Control_Network:

    def __init__(self) -> None:
        self.hilos_cliente = {}

    def agregar_hilo(self, hilo):
        print("Entro a agregar hilo")
        print(f"COntenido de los hilos: {self.hilos_cliente}")
        if self.hilos_cliente.get(hilo.usuario.correo) is None:
            print("se ha agregado el hilo correctamente")
            self.hilos_cliente.update({hilo.usuario.correo: hilo})
            return True
        return False

    def __agregar(self, key, valor):
        self.hilos_cliente.update({key:valor})

    def actualizar(self, dt):
        for elementos in self.hilos_cliente.values():
            elementos.actualiza(dt)

    def eventos(self):
        pass

    def actualizar(self):
        pass
