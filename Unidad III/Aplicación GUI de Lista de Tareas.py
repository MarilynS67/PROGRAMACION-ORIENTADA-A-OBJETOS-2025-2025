import tkinter as tk
from tkinter import messagebox


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("400x400")

        # Lista interna para guardar las tareas
        self.tasks = []

        # ====== Entrada de texto ======
        self.entry_task = tk.Entry(root, width=35)
        self.entry_task.pack(pady=10)
        # Permitir presionar Enter para añadir tarea
        self.entry_task.bind("<Return>", lambda event: self.add_task())

        # ====== Botones ======
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=5)

        btn_add = tk.Button(frame_buttons, text="Añadir Tarea", width=15, command=self.add_task)
        btn_add.grid(row=0, column=0, padx=5)

        btn_complete = tk.Button(frame_buttons, text="Marcar Completada", width=15, command=self.mark_completed)
        btn_complete.grid(row=0, column=1, padx=5)

        btn_delete = tk.Button(frame_buttons, text="Eliminar Tarea", width=15, command=self.delete_task)
        btn_delete.grid(row=0, column=2, padx=5)

        # ====== Listbox para mostrar las tareas ======
        self.listbox_tasks = tk.Listbox(root, width=50, height=15, selectmode=tk.SINGLE)
        self.listbox_tasks.pack(pady=10)
        # Evento opcional: doble clic para marcar completada
        self.listbox_tasks.bind("<Double-Button-1>", lambda event: self.mark_completed())

    def add_task(self):
        """Añade una nueva tarea a la lista."""
        task = self.entry_task.get().strip()
        if task:
            self.tasks.append(task)
            self.listbox_tasks.insert(tk.END, task)
            self.entry_task.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "No puedes añadir una tarea vacía.")

    def mark_completed(self):
        """Marca la tarea seleccionada como completada (cambia su estilo)."""
        selection = self.listbox_tasks.curselection()
        if not selection:
            messagebox.showinfo("Info", "Selecciona una tarea para marcarla como completada.")
            return
        index = selection[0]
        task_text = self.listbox_tasks.get(index)

        # Si ya está marcada, no la marcamos otra vez
        if task_text.startswith("✔ "):
            messagebox.showinfo("Info", "Esta tarea ya está completada.")
            return

        # Actualizar texto con una marca
        self.listbox_tasks.delete(index)
        self.listbox_tasks.insert(index, "✔ " + task_text)
        # Mantener selección
        self.listbox_tasks.itemconfig(index, fg="gray")

    def delete_task(self):
        """Elimina la tarea seleccionada de la lista."""
        selection = self.listbox_tasks.curselection()
        if not selection:
            messagebox.showinfo("Info", "Selecciona una tarea para eliminarla.")
            return
        index = selection[0]
        self.listbox_tasks.delete(index)
        # Eliminar también de la lista interna
        del self.tasks[index]


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
