# Definimos la clase Persona
class Persona:
    # Constructor: se ejecuta al crear un objeto
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
        print(f"Persona creada: {self.nombre}, Edad: {self.edad}")

    # Método que muestra información
    def mostrar_info(self):
        print(f"Nombre: {self.nombre}, Edad: {self.edad}")

    # Destructor: se ejecuta al eliminar el objeto
    def __del__(self):
        print(f"El objeto Persona con nombre {self.nombre} está siendo eliminado.")


# Código principal
if __name__ == "__main__":
    # Creamos un objeto de la clase Persona
    persona1 = Persona("Ana", 22)

    # Mostramos información del objeto
    persona1.mostrar_info()

    # El destructor se ejecuta automáticamente al terminar el programa
