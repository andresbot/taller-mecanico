import tkinter as tk
from tkinter import ttk, StringVar, messagebox
from views.base_view import BaseView
from controllers.cliente_controller import ClienteController
from controllers.vehiculo_controller import VehiculoController
from utils.styles import AppStyles

class ClienteView(BaseView):
    def __init__(self, master=None):
        self.controller = ClienteController()
        self.vehiculo_controller = VehiculoController()
        super().__init__(master)

    def setup_ui(self):
        # Variables
        self.id_var = StringVar()
        self.cedula_var = StringVar()
        self.nombre_var = StringVar()
        self.telefono_var = StringVar()
        self.busqueda_var = StringVar()
        self.criterio_busqueda_var = StringVar(value="Cedula")
        self.kpi_total_var = StringVar(value="0")
        self.kpi_fleet_var = StringVar(value="0")
        self.kpi_nuevos_var = StringVar(value="0")
        self.kpi_alerta_var = StringVar(value="0")

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        container = ttk.Frame(self.frame, style='Main.TFrame')
        container.grid(row=0, column=0, sticky="nsew", padx=14, pady=12)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(3, weight=1)

        hero = ttk.Frame(container, style='Main.TFrame')
        hero.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(hero, text="Gestion de Clientes", style='HeroTitle.TLabel').pack(anchor='w')
        ttk.Label(
            hero,
            text="Administra el directorio de clientes y sus flotas asociadas.",
            style='Subtitle.TLabel'
        ).pack(anchor='w')

        kpi_row = ttk.Frame(container, style='Main.TFrame')
        kpi_row.grid(row=1, column=0, sticky='ew', pady=(2, 10))
        for col in range(4):
            kpi_row.grid_columnconfigure(col, weight=1)

        self._create_kpi_card(kpi_row, 0, "TOTAL CLIENTES", self.kpi_total_var, AppStyles.get_color('accent'))
        self._create_kpi_card(kpi_row, 1, "VEHICULOS ACTIVOS", self.kpi_fleet_var, AppStyles.get_color('info'))
        self._create_kpi_card(kpi_row, 2, "NUEVOS EN LISTA", self.kpi_nuevos_var, AppStyles.get_color('success'))
        self._create_kpi_card(kpi_row, 3, "POR CONTACTAR", self.kpi_alerta_var, AppStyles.get_color('danger'))

        top_actions = ttk.LabelFrame(container, text="Busqueda y Acciones", padding=10)
        top_actions.grid(row=2, column=0, sticky='ew', pady=(0, 10))
        top_actions.columnconfigure(3, weight=1)

        ttk.Label(top_actions, text="Buscar por:").grid(row=0, column=0, padx=5, pady=2, sticky='w')
        criterio_combo = ttk.Combobox(
            top_actions,
            textvariable=self.criterio_busqueda_var,
            values=["Cedula", "Nombre", "Telefono"],
            state="readonly",
            width=12
        )
        criterio_combo.grid(row=0, column=1, padx=5, pady=2, sticky='w')

        ttk.Entry(top_actions, textvariable=self.busqueda_var, width=36).grid(row=0, column=2, padx=5, pady=2, sticky='w')
        ttk.Button(top_actions, text="Buscar", command=self.buscar_clientes, style='Primary.TButton').grid(row=0, column=3, padx=5, pady=2, sticky='w')
        ttk.Button(top_actions, text="Limpiar", command=self.limpiar_busqueda, style='Secondary.TButton').grid(row=0, column=4, padx=5, pady=2, sticky='w')

        ttk.Button(top_actions, text="Nuevo Cliente", command=self.clear_fields, style='Success.TButton').grid(row=0, column=5, padx=5, pady=2, sticky='e')

        body = ttk.Frame(container, style='Main.TFrame')
        body.grid(row=3, column=0, sticky='nsew')
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        data_frame = ttk.LabelFrame(body, text="Datos del Cliente", padding=12)
        data_frame.grid(row=0, column=0, padx=(0, 8), sticky='nsew')
        data_frame.columnconfigure(1, weight=1)

        ttk.Label(data_frame, text="Cedula:").grid(row=0, column=0, sticky="w", pady=4)
        cedula_entry = ttk.Entry(data_frame, textvariable=self.cedula_var)
        cedula_entry.grid(row=0, column=1, padx=5, pady=4, sticky='ew')
        cedula_entry.bind('<KeyRelease>', lambda e: self.validar_solo_numeros(self.cedula_var, e.widget))

        ttk.Label(data_frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=4)
        nombre_entry = ttk.Entry(data_frame, textvariable=self.nombre_var)
        nombre_entry.grid(row=1, column=1, padx=5, pady=4, sticky='ew')
        nombre_entry.bind('<KeyRelease>', lambda e: self.validar_solo_letras(self.nombre_var, e.widget))

        ttk.Label(data_frame, text="Telefono:").grid(row=2, column=0, sticky="w", pady=4)
        telefono_entry = ttk.Entry(data_frame, textvariable=self.telefono_var)
        telefono_entry.grid(row=2, column=1, padx=5, pady=4, sticky='ew')
        telefono_entry.bind('<KeyRelease>', lambda e: self.validar_telefono(self.telefono_var, e.widget))

        buttons = ttk.Frame(data_frame)
        buttons.grid(row=3, column=0, columnspan=2, pady=(12, 0), sticky='ew')
        buttons.columnconfigure(0, weight=1)
        buttons.columnconfigure(1, weight=1)

        ttk.Button(buttons, text="Guardar", command=self.save, style='Success.TButton').grid(row=0, column=0, padx=4, pady=3, sticky='ew')
        ttk.Button(buttons, text="Modificar", command=self.update, style='Info.TButton').grid(row=0, column=1, padx=4, pady=3, sticky='ew')
        ttk.Button(buttons, text="Eliminar", command=self.delete, style='Danger.TButton').grid(row=1, column=0, padx=4, pady=3, sticky='ew')
        ttk.Button(buttons, text="Limpiar", command=self.clear_fields, style='Warning.TButton').grid(row=1, column=1, padx=4, pady=3, sticky='ew')

        table_frame = ttk.LabelFrame(body, text="Directorio de Clientes", padding=10)
        table_frame.grid(row=0, column=1, sticky='nsew')
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(table_frame, columns=("Cedula", "Nombre", "Telefono"), show="headings", height=14)
        self.tree.grid(row=0, column=0, sticky="nsew")
        sb = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        sb.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.heading("Cedula", text="Cedula", anchor="center")
        self.tree.heading("Nombre", text="Nombre", anchor="center")
        self.tree.heading("Telefono", text="Telefono", anchor="center")

        self.tree.column("Cedula", width=140, anchor="center")
        self.tree.column("Nombre", width=260, anchor="center")
        self.tree.column("Telefono", width=170, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.load_data()

    def _create_kpi_card(self, parent, column, title, value_var, accent_color):
        card = tk.Frame(parent, bg=AppStyles.get_color('white'), bd=1, relief='solid', highlightthickness=0)
        card.grid(row=0, column=column, padx=4, pady=4, sticky='nsew')

        bar = tk.Frame(card, bg=accent_color, width=5)
        bar.pack(side='left', fill='y')

        content = tk.Frame(card, bg=AppStyles.get_color('white'))
        content.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        tk.Label(
            content,
            text=title,
            bg=AppStyles.get_color('white'),
            fg=AppStyles.get_color('text_light'),
            font=('Segoe UI', 9, 'bold')
        ).pack(anchor='w')
        tk.Label(
            content,
            textvariable=value_var,
            bg=AppStyles.get_color('white'),
            fg=AppStyles.get_color('primary'),
            font=('Segoe UI', 22, 'bold')
        ).pack(anchor='w')

    def _update_kpis(self, clientes):
        self.kpi_total_var.set(str(len(clientes)))
        self.kpi_alerta_var.set(str(sum(1 for c in clientes if not getattr(c, 'telefono', '').strip())))

        vehiculos = self.vehiculo_controller.get_all()
        self.kpi_fleet_var.set(str(len(vehiculos)))

        recientes = clientes[:45] if len(clientes) > 45 else clientes
        self.kpi_nuevos_var.set(str(len(recientes)))

    def clear_fields(self):
        self.id_var.set("")
        self.cedula_var.set("")
        self.nombre_var.set("")
        self.telefono_var.set("")

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            clientes = self.controller.get_all()
            for cliente in clientes:
                self.tree.insert("", "end", values=(
                    cliente.cedula,
                    cliente.nombre,
                    cliente.telefono
                ), tags=(str(cliente.id),))  # Guardar ID en tags para uso interno
            self._update_kpis(clientes)
        except Exception as e:
            self.show_error(f"Error al cargar datos: {str(e)}")

    def save(self):
        try:
            # Validaciones
            cedula = self.cedula_var.get().strip()
            nombre = self.nombre_var.get().strip()
            telefono = self.telefono_var.get().strip()
            
            if not cedula:
                self.show_warning("La cédula es obligatoria")
                return
            
            if not nombre:
                self.show_warning("El nombre es obligatorio")
                return
            
            if not telefono:
                self.show_warning("El teléfono es obligatorio")
                return
            
            if len(cedula) < 6:
                self.show_warning("La cédula debe tener al menos 6 dígitos")
                return
            
            if len(nombre) < 3:
                self.show_warning("El nombre debe tener al menos 3 caracteres")
                return
            
            if len(telefono) < 7:
                self.show_warning("El teléfono debe tener al menos 7 dígitos")
                return
            
            self.controller.create(
                cedula=cedula,
                nombre=nombre,
                telefono=telefono
            )
            self.show_info("Cliente guardado exitosamente")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            self.show_error(f"Error al guardar: {str(e)}")

    def update(self):
        try:
            if not self.id_var.get():
                self.show_warning("Seleccione un cliente para modificar")
                return

            # Validaciones
            cedula = self.cedula_var.get().strip()
            nombre = self.nombre_var.get().strip()
            telefono = self.telefono_var.get().strip()
            
            if not cedula:
                self.show_warning("La cédula es obligatoria")
                return
            
            if not nombre:
                self.show_warning("El nombre es obligatorio")
                return
            
            if not telefono:
                self.show_warning("El teléfono es obligatorio")
                return
            
            if len(cedula) < 6:
                self.show_warning("La cédula debe tener al menos 6 dígitos")
                return
            
            if len(nombre) < 3:
                self.show_warning("El nombre debe tener al menos 3 caracteres")
                return
            
            if len(telefono) < 7:
                self.show_warning("El teléfono debe tener al menos 7 dígitos")
                return

            self.controller.update(
                id=self.id_var.get(),
                cedula=cedula,
                nombre=nombre,
                telefono=telefono
            )
            self.show_info("Cliente actualizado exitosamente")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            self.show_error(f"Error al actualizar: {str(e)}")

    def delete(self):
        try:
            if not self.id_var.get():
                self.show_warning("Seleccione un cliente para eliminar")
                return

            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
                self.controller.delete(self.id_var.get())
                self.show_info("Cliente eliminado exitosamente")
                self.clear_fields()
                self.load_data()
        except Exception as e:
            self.show_error(f"Error al eliminar: {str(e)}")

    def buscar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            clientes = self.controller.get_all()
            busqueda = self.busqueda_var.get().upper()
            criterio = self.criterio_busqueda_var.get()
            filtrados = []

            for cliente in clientes:
                mostrar = False
                
                if criterio == "Cedula" and busqueda in cliente.cedula:
                    mostrar = True
                elif criterio == "Nombre" and busqueda in cliente.nombre.upper():
                    mostrar = True
                elif criterio == "Telefono" and busqueda in cliente.telefono:
                    mostrar = True

                if mostrar:
                    self.tree.insert("", "end", values=(
                        cliente.cedula,
                        cliente.nombre,
                        cliente.telefono
                    ), tags=(str(cliente.id),))
                    filtrados.append(cliente)
            self._update_kpis(filtrados if busqueda else clientes)
        except Exception as e:
            self.show_error(f"Error al buscar: {str(e)}")

    def limpiar_busqueda(self):
        """Limpiar búsqueda y mostrar todos los clientes"""
        self.busqueda_var.set("")
        self.load_data()

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
        # Obtener ID del tag
        item_id = self.tree.item(selected[0])["tags"][0]
        values = self.tree.item(selected[0])["values"]
        
        self.id_var.set(item_id)
        self.cedula_var.set(values[0])
        self.nombre_var.set(values[1])
        self.telefono_var.set(values[2])
    
    def _set_var_preserving_cursor(self, variable, nuevo_valor, widget):
        pos = widget.index("insert")
        diff = len(variable.get()) - len(nuevo_valor)
        variable.set(nuevo_valor)
        widget.icursor(max(0, pos - diff))

    def validar_solo_numeros(self, variable, widget=None):
        valor = variable.get()
        valor_limpio = ''.join(filter(str.isdigit, valor))
        if valor != valor_limpio and widget:
            self._set_var_preserving_cursor(variable, valor_limpio, widget)

    def validar_solo_letras(self, variable, widget=None):
        valor = variable.get()
        valor_limpio = ''.join(c for c in valor if c.isalpha() or c.isspace()).upper()
        if valor != valor_limpio and widget:
            self._set_var_preserving_cursor(variable, valor_limpio, widget)

    def validar_telefono(self, variable, widget=None):
        valor = variable.get()
        valor_limpio = ''.join(c for c in valor if c.isdigit() or c in '-()+ ')
        if valor != valor_limpio and widget:
            self._set_var_preserving_cursor(variable, valor_limpio, widget)
