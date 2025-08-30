import json  # Para guardar y cargar el inventario en archivos

# -----------------------------
# Clase Producto
# -----------------------------
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Métodos getter y setter
    def get_id(self):
        return self.id_producto

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_cantidad(self):
        return self.cantidad

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def get_precio(self):
        return self.precio

    def set_precio(self, precio):
        self.precio = precio

    def __str__(self):
        return f"ID: {self.id_producto}, Nombre: {self.nombre}, Cantidad: {self.cantidad}, Precio: ${self.precio:.2f}"

# -----------------------------
# Clase Inventario
# -----------------------------
class Inventario:
    def __init__(self):
        # Diccionario con ID como clave para acceso rápido
        self.productos = {}

    # Añadir producto
    def agregar_producto(self, producto):
        if producto.get_id() in self.productos:
            print("El producto ya existe. Actualiza la cantidad o el precio.")
        else:
            self.productos[producto.get_id()] = producto
            print(f"Producto '{producto.get_nombre()}' agregado correctamente.")

    # Eliminar producto por ID
    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
            print(f"Producto con ID {id_producto} eliminado.")
        else:
            print("Producto no encontrado.")

    # Actualizar cantidad o precio
    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        if id_producto in self.productos:
            if cantidad is not None:
                self.productos[id_producto].set_cantidad(cantidad)
            if precio is not None:
                self.productos[id_producto].set_precio(precio)
            print(f"Producto con ID {id_producto} actualizado.")
        else:
            print("Producto no encontrado.")

    # Buscar productos por nombre
    def buscar_producto(self, nombre):
        encontrados = [p for p in self.productos.values() if nombre.lower() in p.get_nombre().lower()]
        if encontrados:
            for p in encontrados:
                print(p)
        else:
            print("No se encontraron productos con ese nombre.")

    # Mostrar todos los productos
    def mostrar_todos(self):
        if self.productos:
            for p in self.productos.values():
                print(p)
        else:
            print("El inventario está vacío.")

    # Guardar inventario en archivo JSON
    def guardar_en_archivo(self, archivo):
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump({id: vars(p) for id, p in self.productos.items()}, f, ensure_ascii=False, indent=4)
        print("Inventario guardado en archivo.")

    # Cargar inventario desde archivo JSON
    def cargar_desde_archivo(self, archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                for id_producto, info in datos.items():
                    p = Producto(info['id_producto'], info['nombre'], info['cantidad'], info['precio'])
                    self.productos[id_producto] = p
            print("Inventario cargado desde archivo.")
        except FileNotFoundError:
            print("Archivo no encontrado. Se iniciará un inventario vacío.")

# -----------------------------
# Interfaz de Usuario
# -----------------------------
def menu():
    inventario = Inventario()
    inventario.cargar_desde_archivo("inventario.json")

    while True:
        print("\n--- SISTEMA DE INVENTARIO ---")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Mostrar todos los productos")
        print("6. Guardar inventario")
        print("7. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            id_producto = input("ID del producto: ")
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))
            producto = Producto(id_producto, nombre, cantidad, precio)
            inventario.agregar_producto(producto)
        elif opcion == "2":
            id_producto = input("ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)
        elif opcion == "3":
            id_producto = input("ID del producto a actualizar: ")
            cantidad = input("Nueva cantidad (deja en blanco si no cambia): ")
            precio = input("Nuevo precio (deja en blanco si no cambia): ")
            cantidad = int(cantidad) if cantidad else None
            precio = float(precio) if precio else None
            inventario.actualizar_producto(id_producto, cantidad, precio)
        elif opcion == "4":
            nombre = input("Nombre del producto a buscar: ")
            inventario.buscar_producto(nombre)
        elif opcion == "5":
            inventario.mostrar_todos()
        elif opcion == "6":
            inventario.guardar_en_archivo("inventario.json")
        elif opcion == "7":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

# -----------------------------
# Ejecutar el programa
# -----------------------------
if __name__ == "__main__":
    menu()
