from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set, Iterable


# ====== MODELOS ======
@dataclass(frozen=True)
class Libro:
    """Representa un libro en el sistema.

    Atributos:
        identidad: Tupla inmutable (titulo, autor). Requisito: no cambia tras crearse.
        categoria: Categoría/tema del libro (str mutable por si la biblioteca la re-clasifica).
        isbn: Identificador único del libro en la biblioteca (clave del diccionario de catálogo).

    Nota: Usamos dataclass con frozen=True para reforzar la inmutabilidad del objeto completo;
    sin embargo, la especificación solo exige inmutabilidad de (titulo, autor). Si se desea poder
    cambiar la categoría después, se podría quitar frozen=True y hacer "identidad" inmutable
    por contrato. Aquí preferimos inmutabilidad total de Libro para mayor seguridad.
    """
    identidad: Tuple[str, str]  # (titulo, autor)
    categoria: str
    isbn: str

    @property
    def titulo(self) -> str:
        return self.identidad[0]

    @property
    def autor(self) -> str:
        return self.identidad[1]


@dataclass
class Usuario:
    """Representa un usuario de la biblioteca.

    Atributos:
        nombre: Nombre del usuario
        user_id: ID único del usuario (se gestiona la unicidad con un conjunto en Biblioteca)
        prestados: Lista de ISBNs actualmente prestados por el usuario (estructura mutable)
    """
    nombre: str
    user_id: str
    prestados: List[str]

    def __post_init__(self):
        # Garantiza que prestados comience como lista vacía si no se pasa.
        if self.prestados is None:
            self.prestados = []


# ====== LÓGICA DE NEGOCIO ======
class Biblioteca:
    """Gestiona libros, usuarios y préstamos.

    Estructuras usadas (según requisitos):
        - Diccionario catalogo: {isbn: Libro} para accesos/búsquedas eficientes por clave.
        - Conjunto ids_usuarios: set con todos los IDs únicos (detección rápida de duplicados).
        - Diccionario usuarios: {user_id: Usuario} para obtener/gestionar usuarios.
        - Diccionario prestamos_activos: {isbn: user_id} para conocer rápidamente quién tiene un libro.
        - Historial de préstamos: lista de registros con timestamps para auditoría básica.

    Métodos cubren: añadir/quitar libros, registrar/baja usuarios, prestar/devolver,
    búsquedas y listado de libros prestados por usuario.
    """

    def __init__(self) -> None:
        self.catalogo: Dict[str, Libro] = {}
        self.usuarios: Dict[str, Usuario] = {}
        self.ids_usuarios: Set[str] = set()
        self.prestamos_activos: Dict[str, str] = {}  # isbn -> user_id
        self.historial: List[Dict[str, str]] = []  # registros simples legibles

    # --- Gestión de libros ---
    def anadir_libro(self, libro: Libro) -> None:
        if libro.isbn in self.catalogo:
            raise ValueError(f"Ya existe un libro con ISBN {libro.isbn} en el catálogo.")
        self.catalogo[libro.isbn] = libro

    def quitar_libro(self, isbn: str) -> None:
        if isbn not in self.catalogo:
            raise KeyError(f"ISBN {isbn} no existe en el catálogo.")
        if isbn in self.prestamos_activos:
            raise ValueError(f"No se puede quitar el libro {isbn} porque está prestado.")
        del self.catalogo[isbn]

    # --- Gestión de usuarios ---
    def registrar_usuario(self, usuario: Usuario) -> None:
        if usuario.user_id in self.ids_usuarios:
            raise ValueError(f"El ID de usuario {usuario.user_id} ya está registrado.")
        self.ids_usuarios.add(usuario.user_id)
        self.usuarios[usuario.user_id] = usuario

    def baja_usuario(self, user_id: str) -> None:
        if user_id not in self.usuarios:
            raise KeyError(f"Usuario {user_id} no existe.")
        usuario = self.usuarios[user_id]
        if usuario.prestados:
            raise ValueError(
                f"No se puede dar de baja al usuario {user_id}: tiene libros prestados ({len(usuario.prestados)})."
            )
        del self.usuarios[user_id]
        self.ids_usuarios.remove(user_id)

    # --- Préstamos ---
    def prestar_libro(self, isbn: str, user_id: str) -> None:
        if isbn not in self.catalogo:
            raise KeyError(f"ISBN {isbn} no existe en el catálogo.")
        if user_id not in self.usuarios:
            raise KeyError(f"Usuario {user_id} no existe.")
        if isbn in self.prestamos_activos:
            raise ValueError(f"El libro {isbn} ya está prestado al usuario {self.prestamos_activos[isbn]}.")

        usuario = self.usuarios[user_id]
        usuario.prestados.append(isbn)  # Lista: estructura pedida para libros prestados
        self.prestamos_activos[isbn] = user_id
        self.historial.append({
            "evento": "prestamo",
            "isbn": isbn,
            "user_id": user_id,
            "fecha": datetime.now().isoformat(timespec="seconds"),
        })

    def devolver_libro(self, isbn: str) -> None:
        if isbn not in self.prestamos_activos:
            raise ValueError(f"El libro {isbn} no figura como prestado.")
        user_id = self.prestamos_activos.pop(isbn)
        usuario = self.usuarios[user_id]
        try:
            usuario.prestados.remove(isbn)
        except ValueError:
            # Inconsistencia (no debería pasar), pero la manejamos con un aviso claro
            raise RuntimeError(
                f"Inconsistencia: el usuario {user_id} no tenía registrado el ISBN {isbn} en su lista de prestados"
            )
        self.historial.append({
            "evento": "devolucion",
            "isbn": isbn,
            "user_id": user_id,
            "fecha": datetime.now().isoformat(timespec="seconds"),
        })

    # --- Búsquedas ---
    def _filtrar(self, predicado) -> List[Libro]:
        return [lib for lib in self.catalogo.values() if predicado(lib)]

    @staticmethod
    def _normalizar(txt: str) -> str:
        return txt.strip().lower()

    def buscar_por_titulo(self, texto: str) -> List[Libro]:
        q = self._normalizar(texto)
        return self._filtrar(lambda l: q in self._normalizar(l.titulo))

    def buscar_por_autor(self, texto: str) -> List[Libro]:
        q = self._normalizar(texto)
        return self._filtrar(lambda l: q in self._normalizar(l.autor))

    def buscar_por_categoria(self, texto: str) -> List[Libro]:
        q = self._normalizar(texto)
        return self._filtrar(lambda l: q in self._normalizar(l.categoria))

    # --- Listados ---
    def listar_prestados_usuario(self, user_id: str) -> List[Libro]:
        if user_id not in self.usuarios:
            raise KeyError(f"Usuario {user_id} no existe.")
        isbns = self.usuarios[user_id].prestados
        return [self.catalogo[isbn] for isbn in isbns]

    def listar_disponibles(self) -> List[Libro]:
        """Devuelve libros no prestados actualmente."""
        return [lib for isbn, lib in self.catalogo.items() if isbn not in self.prestamos_activos]

    # --- Utilidades ---
    def mostrar_historial(self, ultimos: Optional[int] = None) -> List[Dict[str, str]]:
        if ultimos is None or ultimos >= len(self.historial):
            return list(self.historial)
        return self.historial[-ultimos:]

    def __len__(self) -> int:
        return len(self.catalogo)


# ====== DEMOSTRACIÓN / PRUEBAS BÁSICAS ======
if __name__ == "__main__":
    # Crear biblioteca
    biblio = Biblioteca()

    # Crear libros (tupla (titulo, autor))
    l1 = Libro(identidad=("Cien años de soledad", "Gabriel García Márquez"), categoria="Realismo mágico",
               isbn="9780307474728")
    l2 = Libro(identidad=("El amor en los tiempos del cólera", "Gabriel García Márquez"), categoria="Novela",
               isbn="9780307389732")
    l3 = Libro(identidad=("Python Crash Course", "Eric Matthes"), categoria="Programación", isbn="9781593276034")

    # Añadir libros
    biblio.anadir_libro(l1)
    biblio.anadir_libro(l2)
    biblio.anadir_libro(l3)

    # Registrar usuarios (IDs únicos con set)
    u1 = Usuario(nombre="Rubi Marilyn Noteno Dagua", user_id="U001", prestados=[])
    u2 = Usuario(nombre="Silvanna Ramirez", user_id="U002", prestados=[])
    biblio.registrar_usuario(u1)
    biblio.registrar_usuario(u2)

    # Prestar y devolver
    biblio.prestar_libro("9780307474728", "U001")  # Rubi toma "Cien años de soledad"
    biblio.prestar_libro("9781593276034", "U002")  # Silvanna toma "Python Crash Course"

    # Listar prestados de U001
    print("Prestados de U001:")
    for lib in biblio.listar_prestados_usuario("U001"):
        print(f"- {lib.titulo} — {lib.autor} (ISBN {lib.isbn})")

    # Búsquedas
    print("\nBuscar por autor 'garcía':")
    for lib in biblio.buscar_por_autor("garcía"):
        print(f"- {lib.titulo} ({lib.categoria})")

    # Devolver
    biblio.devolver_libro("9781593276034")  # Silvanna devuelve

    # Mostrar historial
    print("\nHistorial de eventos:")
    for ev in biblio.mostrar_historial():
        print(ev)

    # Baja usuario (fallará si tiene libros)
    try:
        biblio.baja_usuario("U001")
    except ValueError as e:
        print("\nNo se pudo dar de baja U001:", e)

    # Devolver y dar de baja
    biblio.devolver_libro("9780307474728")
    biblio.baja_usuario("U001")
    print("\nUsuario U001 dado de baja exitosamente.")
