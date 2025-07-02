# Clase base: Mascota
class Mascota:
    def __init__(self, nombre, edad):
        self.nombre = nombre         # Atributo público
        self._edad = edad            # Atributo protegido (encapsulación)

    def hacer_sonido(self):
        return "Esta mascota hace un sonido"

    def mostrar_info(self):
        print(f"Nombre: {self.nombre}")
        print(f"Edad: {self._edad} años")

    # Método getter para acceder a la edad (encapsulación)
    def get_edad(self):
        return self._edad

    # Método setter para modificar la edad (encapsulación)
    def set_edad(self, nueva_edad):
        if nueva_edad > 0:
            self._edad = nueva_edad
        else:
            print("La edad debe ser mayor que 0")


# Clase derivada: Perro (hereda de Mascota)
class Perro(Mascota):
    def __init__(self, nombre, edad, raza):
        super().__init__(nombre, edad)  # Llama al constructor de la clase base
        self.raza = raza

    # Polimorfismo: sobrescribimos el método hacer_sonido()
    def hacer_sonido(self):
        return "¡Guau!"

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Raza: {self.raza}")


# Otra clase derivada: Gato (también hereda de Mascota)
class Gato(Mascota):
    def __init__(self, nombre, edad, color):
        super().__init__(nombre, edad)
        self.color = color

    # Polimorfismo: otro sobrescrito del mismo método
    def hacer_sonido(self):
        return "¡Miau!"

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Color: {self.color}")


# Crear objetos (instancias)
perro1 = Perro("Max", 4, "Labrador")
gato1 = Gato("Michi", 2, "Gris")

# Demostrar uso de métodos y atributos
print("--- Información del Perro ---")
perro1.mostrar_info()
print("Sonido:", perro1.hacer_sonido())

print("\n--- Información del Gato ---")
gato1.mostrar_info()
print("Sonido:", gato1.hacer_sonido())

# Encapsulación: acceder y modificar edad con métodos
print("\nEdad actual del gato:", gato1.get_edad())
gato1.set_edad(3)
print("Edad modificada del gato:", gato1.get_edad())

# Polimorfismo: iterar con una misma interfaz
print("\n--- Sonidos con polimorfismo ---")
mascotas = [perro1, gato1]
for mascota in mascotas:
    print(f"{mascota.nombre} dice: {mascota.hacer_sonido()}")
