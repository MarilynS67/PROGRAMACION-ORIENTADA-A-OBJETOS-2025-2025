import tkinter as tk
from tkinter import messagebox

# --- Clase principal de la aplicación ---
class GestorDatosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Datos")
        self.root.geometry("400x300")  # Tamaño de la ventana

        # --- Etiqueta ---
        self.label = tk.Label(root, text="Ingrese un dato:")
        self.label.pack(pady=5)

        # --- Campo de texto ---
        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=5)

        # --- Botón Agregar ---
        self.btn_agregar = tk.Button(root, text="Agregar", command=self.agregar_dato)
        self.btn_agregar.pack(pady=5)

        # --- Lista para mostrar los datos ---
        self.lista = tk.Listbox(root, width=40, height=8)
        self.lista.pack(pady=5)

        # --- Botón Limpiar ---
        self.btn_limpiar = tk.Button(root, text="Limpiar", command=self.limpiar_lista)
        self.btn_limpiar.pack(pady=5)

    # --- Función para agregar dato ---
    def agregar_dato(self):
        dato = self.entry.get().strip()
        if dato:
            self.lista.insert(tk.END, dato)  # Agrega al final de la lista
            self.entry.delete(0, tk.END)     # Limpia el campo de texto
        else:
            messagebox.showwarning("Atención", "Debe ingresar un dato antes de agregar.")

    # --- Función para limpiar lista o selección ---
    def limpiar_lista(self):
        seleccion = self.lista.curselection()
        if seleccion:  # Si el usuario seleccionó un elemento
            self.lista.delete(seleccion)
        else:  # Si no hay selección, limpiar toda la lista
            self.lista.delete(0, tk.END)

# --- Programa principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = GestorDatosApp(root)
    root.mainloop()
