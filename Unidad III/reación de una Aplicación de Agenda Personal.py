"""
agenda_tkinter.py
Aplicación de Agenda Personal usando Tkinter.

Requisitos:
- Python 3.x
- (Opcional) tkcalendar para DatePicker: pip install tkcalendar

Funcionalidades:
- Mostrar eventos en un TreeView (fecha, hora, descripción)
- Añadir eventos mediante campos de entrada
- Eliminar evento seleccionado con confirmación
- Organización por Frames
- Comentarios explicativos en el código
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Intentamos importar DateEntry de tkcalendar para el DatePicker opcional.
# Si no está instalado, usamos un campo Entry con validación de formato.
try:
    from tkcalendar import DateEntry
    TKCALENDAR_AVAILABLE = True
except Exception:
    TKCALENDAR_AVAILABLE = False


class AgendaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda Personal")
        self.geometry("700x450")
        self.resizable(False, False)

        # Contenedor principal: top (lista) y bottom (entradas y botones)
        self.create_widgets()

    def create_widgets(self):
        # ---------- Frame: Lista de eventos ----------
        frame_list = ttk.Frame(self, padding=(10, 8))
        frame_list.pack(fill=tk.BOTH, expand=False)

        lbl_title = ttk.Label(frame_list, text="Eventos programados", font=("Segoe UI", 12, "bold"))
        lbl_title.pack(anchor=tk.W, pady=(0, 6))

        # Definición del Treeview
        columns = ("fecha", "hora", "descripcion")
        self.tree = ttk.Treeview(frame_list, columns=columns, show="headings", height=10)
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.column("fecha", width=120, anchor=tk.CENTER)
        self.tree.column("hora", width=80, anchor=tk.CENTER)
        self.tree.column("descripcion", width=440, anchor=tk.W)

        # Scrollbar vertical para el Treeview
        vsb = ttk.Scrollbar(frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # ---------- Frame: Entradas (Date, Time, Description) ----------
        frame_inputs = ttk.Frame(self, padding=(10, 8))
        frame_inputs.pack(fill=tk.X, expand=False)

        # Labels y campos organizados en grid
        lbl_fecha = ttk.Label(frame_inputs, text="Fecha (día/mes/año):")
        lbl_fecha.grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
        if TKCALENDAR_AVAILABLE:
            # Si tkcalendar está instalado, usamos DateEntry (selector visual de fecha)
            self.entry_fecha = DateEntry(frame_inputs, date_pattern="dd/mm/yyyy")
        else:
            # Fallback: Entry de texto con placeholder sobre formato dd/mm/yyyy
            self.entry_fecha = ttk.Entry(frame_inputs)
            self.entry_fecha.insert(0, "dd/mm/yyyy")  # ayuda visual; se validará
            # borrar placeholder al hacer foco
            self.entry_fecha.bind("<FocusIn>", lambda e: self._clear_placeholder(e, "dd/mm/yyyy"))
            self.entry_fecha.bind("<FocusOut>", lambda e: self._restore_placeholder(e, "dd/mm/yyyy"))
        self.entry_fecha.grid(row=0, column=1, padx=4, pady=4)

        lbl_hora = ttk.Label(frame_inputs, text="Hora (HH:MM):")
        lbl_hora.grid(row=0, column=2, sticky=tk.W, padx=12, pady=4)
        self.entry_hora = ttk.Entry(frame_inputs, width=10)
        self.entry_hora.insert(0, "12:00")
        self.entry_hora.grid(row=0, column=3, padx=4, pady=4)

        lbl_desc = ttk.Label(frame_inputs, text="Descripción:")
        lbl_desc.grid(row=1, column=0, sticky=tk.W, padx=4, pady=4)
        self.entry_desc = ttk.Entry(frame_inputs, width=70)
        self.entry_desc.grid(row=1, column=1, columnspan=3, padx=4, pady=4, sticky=tk.W)

        # ---------- Frame: Botones ----------
        frame_buttons = ttk.Frame(self, padding=(10, 8))
        frame_buttons.pack(fill=tk.X, expand=False)

        btn_add = ttk.Button(frame_buttons, text="Agregar Evento", command=self.add_event)
        btn_add.pack(side=tk.LEFT, padx=(0, 6))

        btn_delete = ttk.Button(frame_buttons, text="Eliminar Evento Seleccionado", command=self.delete_selected)
        btn_delete.pack(side=tk.LEFT, padx=(0, 6))

        btn_exit = ttk.Button(frame_buttons, text="Salir", command=self.on_exit)
        btn_exit.pack(side=tk.RIGHT)

        # Mensaje de ayuda / estado (opcional)
        self.status_var = tk.StringVar(value="Lista vacía")
        lbl_status = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        lbl_status.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)

    # ---------- Helpers para placeholder ----------
    def _clear_placeholder(self, event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)

    def _restore_placeholder(self, event, placeholder):
        if not event.widget.get().strip():
            event.widget.insert(0, placeholder)

    # ---------- Validaciones ----------
    def validate_date(self, date_text):
        """
        Valida la fecha en formato dd/mm/yyyy.
        Devuelve True si es válida, False en caso contrario.
        """
        try:
            datetime.strptime(date_text, "%d/%m/%Y")
            return True
        except Exception:
            return False

    def validate_time(self, time_text):
        """
        Valida la hora en formato HH:MM (24 horas).
        """
        try:
            datetime.strptime(time_text, "%H:%M")
            return True
        except Exception:
            return False

    # ---------- Acciones de botones ----------
    def add_event(self):
        """
        Toma los valores de los campos, valida y agrega un nuevo evento al Treeview.
        """
        fecha = self.entry_fecha.get().strip()
        hora = self.entry_hora.get().strip()
        desc = self.entry_desc.get().strip()

        # Validaciones
        if TKCALENDAR_AVAILABLE:
            # DateEntry devuelve un datetime.date o cadena según versión; convertimos a dd/mm/yyyy
            if hasattr(fecha, "strftime"):
                fecha = fecha.strftime("%d/%m/%Y")

        if not fecha or fecha == "dd/mm/yyyy":
            messagebox.showwarning("Fecha inválida", "Ingrese una fecha válida.")
            return
        if not self.validate_date(fecha):
            messagebox.showwarning("Fecha inválida", "Formato de fecha requerido: dd/mm/yyyy (ej. 31/12/2025).")
            return

        if not hora:
            messagebox.showwarning("Hora inválida", "Ingrese una hora.")
            return
        if not self.validate_time(hora):
            messagebox.showwarning("Hora inválida", "Formato de hora requerido: HH:MM (24 horas).")
            return

        if not desc:
            messagebox.showwarning("Descripción vacía", "Ingrese una breve descripción para el evento.")
            return

        # Agregamos el evento al Treeview
        self.tree.insert("", tk.END, values=(fecha, hora, desc))
        self.status_var.set(f"Evento agregado: {fecha} {hora} - {desc}")
        # Limpiar campos (excepto fecha si usamos DateEntry)
        if not TKCALENDAR_AVAILABLE:
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, "dd/mm/yyyy")
        self.entry_hora.delete(0, tk.END)
        self.entry_hora.insert(0, "12:00")
        self.entry_desc.delete(0, tk.END)

    def delete_selected(self):
        """
        Elimina el evento seleccionado en el Treeview, con diálogo de confirmación.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Eliminar", "No hay ningún evento seleccionado.")
            return

        # Si se seleccionan múltiples, preguntamos confirmación general
        count = len(selected)
        if count == 1:
            item = selected[0]
            values = self.tree.item(item, "values")
            fecha, hora, desc = values
            msg = f"¿Deseas eliminar el evento?\n\n{fecha} {hora} - {desc}"
        else:
            msg = f"¿Deseas eliminar los {count} eventos seleccionados?"

        if messagebox.askyesno("Confirmar eliminación", msg):
            for item in selected:
                self.tree.delete(item)
            self.status_var.set(f"{count} evento(s) eliminado(s).")

    def on_exit(self):
        """
        Cierra la aplicación (pregunta de confirmación opcional).
        """
        if messagebox.askokcancel("Salir", "¿Estás seguro que deseas salir?"):
            self.destroy()


if __name__ == "__main__":
    # Si no tenemos tkcalendar, avisamos al usuario sobre la opción de instalarlo
    if not TKCALENDAR_AVAILABLE:
        print("Nota: 'tkcalendar' no está instalado. El selector de fecha será un campo de texto.")
        print("Para instalarlo ejecuta: pip install tkcalendar")
    app = AgendaApp()
    app.mainloop()
