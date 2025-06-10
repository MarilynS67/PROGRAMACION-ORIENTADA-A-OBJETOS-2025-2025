from abc import ABC, abstractmethod

class Vehiculo(ABC):
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    @abstractmethod
    def encender(self):
        pass
#abstraccion
class Auto(Vehiculo):
    def encender(self):
        print(f"El auto {self.marca} {self.modelo} está encendido.")

class Moto(Vehiculo):
    def encender(self):
        print(f"La moto {self.marca} {self.modelo} está encendida.")

vehiculo1 = Auto("Toyota", "Corolla")
vehiculo2 = Moto("Yamaha", "MT-07")

vehiculo1.encender()
vehiculo2.encender()


#encapsulacion
class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.__password = "1234"  # atributo privado

    def cambiar_password(self, nueva_password):
        if len(nueva_password) >= 4:
            self.__password = nueva_password
            print("Contraseña cambiada correctamente.")
        else:
            print("La contraseña debe tener al menos 4 caracteres.")

    def mostrar_password(self):
        print(f"La contraseña de {self.nombre} es privada.")

usuario = Usuario("Luis")
usuario.mostrar_password()
usuario.cambiar_password("abc")
usuario.cambiar_password("abcd")

#herencia
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def presentarse(self):
        print(f"Hola, soy {self.nombre} y tengo {self.edad} años.")

class Estudiante(Persona):
    def estudiar(self):
        print(f"{self.nombre} está estudiando.")

class Profesor(Persona):
    def enseñar(self):
        print(f"{self.nombre} está enseñando.")

alumno = Estudiante("Carlos", 20)
docente = Profesor("Ana", 35)

alumno.presentarse()
alumno.estudiar()
docente.presentarse()
docente.enseñar()


#polimorfismo
class Animal:
    def sonar(self):
        print("El animal hace un sonido.")

class Gato(Animal):
    def sonar(self):
        print("El gato dice: Miau.")

class Perro(Animal):
    def sonar(self):
        print("El perro dice: Guau.")

def hacer_sonar(animal):
    animal.sonar()

gato = Gato()
perro = Perro()
hacer_sonar(gato)
hacer_sonar(perro)


