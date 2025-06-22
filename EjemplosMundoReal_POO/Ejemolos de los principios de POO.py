# sistema_reservas.py

# Clase que representa una habitación de hotel
class Habitacion:
    def __init__(self, numero, tipo, precio):
        self.numero = numero
        self.tipo = tipo
        self.precio = precio
        self.disponible = True

    def reservar(self):
        if self.disponible:
            self.disponible = False
            print(f"Habitación {self.numero} reservada con éxito.")
        else:
            print(f"La habitación {self.numero} no está disponible.")

    def liberar(self):
        self.disponible = True
        print(f"Habitación {self.numero} ahora está disponible.")

# Clase que representa un cliente
class Cliente:
    def __init__(self, nombre, identificacion):
        self.nombre = nombre
        self.identificacion = identificacion

# Clase que gestiona el sistema de reservas
class SistemaReservas:
    def __init__(self):
        self.habitaciones = []
        self.reservas = {}

    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)

    def mostrar_disponibles(self):
        print("Habitaciones disponibles:")
        for h in self.habitaciones:
            if h.disponible:
                print(f"  - Habitación {h.numero} ({h.tipo}) - ${h.precio}")

    def hacer_reserva(self, cliente, numero_habitacion):
        for h in self.habitaciones:
            if h.numero == numero_habitacion and h.disponible:
                h.reservar()
                self.reservas[cliente.identificacion] = h.numero
                return
        print("No se pudo hacer la reserva. Verifica si la habitación está disponible.")

# --- Ejemplo de uso del sistema ---

# Crear el sistema
sistema = SistemaReservas()

# Agregar habitaciones
sistema.agregar_habitacion(Habitacion(101, "Individual", 50))
sistema.agregar_habitacion(Habitacion(102, "Doble", 80))
sistema.agregar_habitacion(Habitacion(103, "Suite", 150))

# Mostrar habitaciones disponibles
sistema.mostrar_disponibles()

# Crear cliente y hacer una reserva
cliente1 = Cliente("María Pérez", "172839")
sistema.hacer_reserva(cliente1, 102)

# Mostrar habitaciones nuevamente
sistema.mostrar_disponibles()
