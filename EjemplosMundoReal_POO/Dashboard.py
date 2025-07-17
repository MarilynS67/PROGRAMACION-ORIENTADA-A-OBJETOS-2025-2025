import os

# Función que muestra el contenido de un archivo .py seleccionado
def mostrar_codigo(ruta_script):
    """
    Muestra el contenido del archivo .py seleccionado.
    """
    ruta_script_absoluta = os.path.abspath(ruta_script)  # Convierte la ruta relativa en absoluta

    try:
        # Intenta abrir el archivo en modo lectura con codificación UTF-8
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
            print(f"\n📄 --- Código de {ruta_script} ---\n")
            print(archivo.read())  # Muestra el contenido del archivo
    except FileNotFoundError:
        print("❌ El archivo no se encontró.")  # Si no se encuentra el archivo
    except Exception as e:
        print(f"⚠️ Ocurrió un error al intentar leer el archivo: {e}")  # Otros errores

# Función que muestra el menú principal de opciones
def mostrar_menu():
    """
    Muestra el menú principal con los temas disponibles.
    """
    opciones = {
        '1': 'Programacion tradicional.py',
        '2': 'Programacion orientada a objetos.py',
        '3': 'Técnicas de Programación (POO).py',
        '4': 'Tipos de datos, identificadores.py',
        '5': 'Clases, objetos, herencia, encapsulamiento y polimorfismo.py',
        '6': 'Implementación de Constructores y Destructores en Python.py'
    }

    # Bucle para mostrar el menú hasta que el usuario elija salir
    while True:
        print("\n📘 MENÚ DE OPCIONES:")
        print("1. Programación Tradicional")
        print("2. Programación Orientada a Objetos")
        print("3. Técnicas de Programación (POO)")
        print("4. Tipos de Datos e Identificadores")
        print("5. Clases, Objetos, Herencia, Encapsulamiento y Polimorfismo")
        print("6. Constructores y Destructores en Python")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '0':
            print("👋 Saliendo del programa...")
            break  # Sale del bucle y finaliza el programa
        elif opcion in opciones:
            mostrar_codigo(opciones[opcion])  # Llama a la función para mostrar el código seleccionado
        else:
            print("⚠️ Opción inválida. Intenta nuevamente.")  # Mensaje de error si se escribe una opción inválida

# Punto de entrada principal del programa
if __name__ == '__main__':
    mostrar_menu()
