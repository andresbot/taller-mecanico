import tkinter as tk
from tkinter import ttk
from views.cliente_view import ClienteView
from views.vehiculo_view import VehiculoView
from views.mantenimiento_view import (
    CambioAceiteView,
    MantenimientoFrenosView,
    MantenimientoGeneralView,
    MantenimientoCorrectivoView
)
from views.reporte_view import ReporteView
from views.precio_view import PrecioView
from models.mantenimiento_varios_model import TipoMantenimientoVarios
from tkinter import messagebox
from utils.styles import AppStyles

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Mantenimiento Vehicular")
        # Tamaño base de la app
        self.root.geometry("1200x800")
        # Aplicar estilos personalizados
        self.style = AppStyles.configure_styles(self.root)
        # Configurar color de fondo de la ventana principal
        self.root.configure(bg=AppStyles.get_color('bg_main'))
        # Centrar ventana principal
        self._center_window(self.root)
        self.setup_ui()

    def setup_ui(self):
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)

        # Pestaña de Clientes
        clientes_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(clientes_frame, text='Clientes')
        cliente_view = ClienteView(clientes_frame)
        cliente_view.frame.pack(expand=True, fill='both')

        # Pestaña de Vehículos
        vehiculos_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(vehiculos_frame, text='Vehículos')
        vehiculo_view = VehiculoView(vehiculos_frame)
        vehiculo_view.frame.pack(expand=True, fill='both')

        # Pestaña de Mantenimientos
        self.setup_mantenimientos_tab()

        # Pestaña de Reportes
        reportes_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(reportes_frame, text='Reportes')
        self.reporte_view = ReporteView(reportes_frame)
        self.reporte_view.frame.pack(expand=True, fill='both')

        # Pestaña de Precios
        precios_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(precios_frame, text='Precios')
        self.precio_view = PrecioView(precios_frame)
        self.precio_view.frame.pack(expand=True, fill='both')

        # Refrescar historial automáticamente al cambiar a la pestaña de Reportes
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)

    def setup_mantenimientos_tab(self):
        mant_frame = ttk.Frame(self.notebook)
        self.notebook.add(mant_frame, text='Mantenimientos')

        # Contenedor centrado dentro de la pestaña
        mant_frame.grid_columnconfigure(0, weight=1)
        container = ttk.Frame(mant_frame)
        container.grid(row=0, column=0, padx=10, pady=10)

        # Frame para selección de tipo de mantenimiento
        select_frame = ttk.LabelFrame(container, text="Nuevo Mantenimiento", padding=10)
        select_frame.pack(fill='x', padx=10, pady=5)

        # Hacer que el grid dentro del frame se distribuya mejor
        select_frame.columnconfigure(0, weight=0)
        select_frame.columnconfigure(1, weight=1)
        select_frame.columnconfigure(2, weight=0)

        # Combobox para tipo de mantenimiento
        ttk.Label(select_frame, text="Tipo de mantenimiento:").grid(row=0, column=0, padx=5)
        tipos_mant = [
            "Cambio de Aceite",
            "Mantenimiento de Frenos",
            "Mantenimiento General",
            "Mantenimiento Correctivo"
        ]
        self.tipo_mant_var = tk.StringVar()
        tipo_combo = ttk.Combobox(select_frame, textvariable=self.tipo_mant_var,
                                 values=tipos_mant, state="readonly")
        tipo_combo.grid(row=0, column=1, padx=5)

        # Botón para crear nuevo mantenimiento
        ttk.Button(select_frame, text="Crear Nuevo",
                  command=self.crear_mantenimiento).grid(row=0, column=2, padx=5)

        # Sección para gestionar "Mantenimientos Varios" debajo de Nuevo Mantenimiento
        varios_frame = ttk.LabelFrame(container, text="Mantenimientos Varios", padding=10)
        varios_frame.pack(fill='both', expand=False, padx=10, pady=5)

        # Para que la tabla crezca con el contenedor
        varios_frame.columnconfigure(0, weight=1)
        varios_frame.columnconfigure(1, weight=1)
        varios_frame.columnconfigure(2, weight=0)
        varios_frame.columnconfigure(3, weight=0)
        varios_frame.rowconfigure(1, weight=1)

        # Entrada y botón para agregar nuevo tipo
        ttk.Label(varios_frame, text="Nuevo tipo:").grid(row=0, column=0, sticky='w', padx=5)
        self.nuevo_tipo_var = tk.StringVar()
        nuevo_entry = ttk.Entry(varios_frame, textvariable=self.nuevo_tipo_var)
        nuevo_entry.grid(row=0, column=1, padx=5)
        nuevo_entry.bind('<KeyRelease>', lambda e: self.nuevo_tipo_var.set(self.nuevo_tipo_var.get().upper()))
        ttk.Button(varios_frame, text="Agregar", command=self.agregar_tipo_varios).grid(row=0, column=2, padx=5)

        # Lista de tipos existentes
        self.tipos_tree = ttk.Treeview(varios_frame, columns=("Nombre",), show='headings', height=5)
        self.tipos_tree.heading("Nombre", text="Tipos de Mantenimiento")
        self.tipos_tree.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)

        # Scrollbar
        sb = ttk.Scrollbar(varios_frame, orient='vertical', command=self.tipos_tree.yview)
        self.tipos_tree.configure(yscrollcommand=sb.set)
        sb.grid(row=1, column=3, sticky='ns')

        # Botón eliminar
        ttk.Button(varios_frame, text="Eliminar seleccionado", command=self.eliminar_tipo_vario).grid(row=2, column=0, pady=5, padx=5)

        # Cargar tipos existentes
        self.cargar_tipos_varios()

    def crear_mantenimiento(self):
        tipo = self.tipo_mant_var.get()
        if not tipo:
            return

        # Crear nueva ventana para el formulario
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Nuevo {tipo}")
        ventana.geometry("700x500")
        ventana.transient(self.root)
        ventana.grab_set()

        # Seleccionar la vista apropiada
        if tipo == "Cambio de Aceite":
            view = CambioAceiteView(ventana)
        elif tipo == "Mantenimiento de Frenos":
            view = MantenimientoFrenosView(ventana)
        elif tipo == "Mantenimiento General":
            view = MantenimientoGeneralView(ventana)
        elif tipo == "Mantenimiento Correctivo":
            view = MantenimientoCorrectivoView(ventana)

        view.frame.pack(expand=True, fill='both', padx=15, pady=10)
        # Centrar el formulario una vez construido
        self._center_window(ventana)

    def _on_tab_changed(self, event):
        try:
            tab_text = self.notebook.tab(self.notebook.select(), 'text')
            if tab_text == 'Reportes' and hasattr(self, 'reporte_view'):
                self.reporte_view.refresh()
            elif tab_text == 'Precios' and hasattr(self, 'precio_view'):
                self.precio_view.refresh()
        except Exception:
            pass

    # Métodos para gestionar tipos de mantenimientos varios
    def cargar_tipos_varios(self):
        # limpiar tree
        for it in self.tipos_tree.get_children():
            self.tipos_tree.delete(it)
        try:
            tipos = TipoMantenimientoVarios.get_all()
            for t in tipos:
                self.tipos_tree.insert('', 'end', values=(t.nombre,))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los tipos: {e}")

    def agregar_tipo_varios(self):
        nombre = self.nuevo_tipo_var.get().strip().upper()
        if not nombre:
            messagebox.showwarning("Aviso", "Ingrese un nombre para el tipo de mantenimiento")
            return
        try:
            tipo = TipoMantenimientoVarios(nombre=nombre)
            tipo.save()
            messagebox.showinfo("Éxito", "Tipo agregado correctamente")
            self.nuevo_tipo_var.set("")
            self.cargar_tipos_varios()
        except ValueError as ve:
            messagebox.showwarning("Aviso", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el tipo: {e}")

    def eliminar_tipo_vario(self):
        sel = self.tipos_tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un tipo para eliminar")
            return
        nombre = self.tipos_tree.item(sel[0])['values'][0]
        # Buscar el registro en la base
        try:
            tipo = TipoMantenimientoVarios.get_by_nombre(nombre)
            if not tipo:
                messagebox.showerror("Error", "Tipo no encontrado en la base de datos")
                return
            if messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre}'?"):
                tipo.delete()
                self.cargar_tipos_varios()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def run(self):
        self.root.mainloop()

    # Utilidades de UI
    def _center_window(self, win):
        """Centra una ventana en la pantalla actual."""
        win.update_idletasks()
        w = win.winfo_width()
        h = win.winfo_height()
        # Si aún no se ha dibujado, tomar del geometry
        if w == 1 and h == 1:
            try:
                geo = win.geometry()
                size = geo.split('+')[0]
                w, h = map(int, size.split('x'))
            except Exception:
                w, h = 800, 600
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = int((sw - w) / 2)
        y = int((sh - h) / 2)
        win.geometry(f"{w}x{h}+{x}+{y}")

    def _apply_style(self):
        """Aplica un tema agradable y padding por defecto a los widgets."""
        style = ttk.Style(self.root)
        # Elegir un tema moderno disponible en Windows
        themes = style.theme_names()
        if 'vista' in themes:
            style.theme_use('vista')
        elif 'clam' in themes:
            style.theme_use('clam')
        # Fuente y espaciado por defecto (evitar strings con espacios que rompen Tk)
        default_font = ("Segoe UI", 10)
        style.configure('.', font=default_font)
        style.configure("TLabel", padding=(4, 2), font=default_font)
        style.configure("TButton", padding=(10, 6), font=default_font)
        style.configure("TEntry", padding=(4, 4), font=default_font)
        style.configure("TCombobox", padding=(4, 4), font=default_font)