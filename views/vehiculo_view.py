import tkinter as tk
from tkinter import ttk, StringVar
from views.base_view import BaseView
from controllers.vehiculo_controller import VehiculoController
from controllers.cliente_controller import ClienteController
from datetime import datetime
from utils.styles import AppStyles

class VehiculoView(BaseView):
    MARCAS_COMUNES = [
        'TOYOTA', 'CHEVROLET', 'FORD', 'HONDA', 'HYUNDAI', 
        'KIA', 'NISSAN', 'MAZDA', 'VOLKSWAGEN', 'RENAULT'
    ]

    def __init__(self, master=None):
        self.controller = VehiculoController()
        self.cliente_controller = ClienteController()
        # Generar lista de años desde 1990 hasta el año actual
        current_year = datetime.now().year
        self.años = [str(year) for year in range(1990, current_year + 1)]
        self.clientes_data = {}  # Inicializar diccionario de clientes
        super().__init__(master)

    def setup_ui(self):
        self.id_var = StringVar()
        self.placa_var = StringVar()
        self.marca_var = StringVar()
        self.modelo_var = StringVar()
        self.linea_var = StringVar()
        self.kilometraje_var = StringVar()
        self.cliente_id_var = StringVar()
        self.busqueda_var = StringVar()
        self.criterio_busqueda_var = StringVar(value="Placa")
        self.kpi_total_var = StringVar(value='0')
        self.kpi_operativos_var = StringVar(value='0')
        self.kpi_overdue_var = StringVar(value='0')
        self.kpi_promedio_km_var = StringVar(value='0')

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        container = ttk.Frame(self.frame, style='Main.TFrame')
        container.grid(row=0, column=0, sticky='nsew', padx=14, pady=12)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)

        hero = ttk.Frame(container, style='Main.TFrame')
        hero.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(hero, text='Fleet Inventory', style='HeroTitle.TLabel').pack(anchor='w')
        ttk.Label(
            hero,
            text='Monitorea el estado de la flota, kilometraje y proximos servicios.',
            style='Subtitle.TLabel'
        ).pack(anchor='w')

        kpi_row = ttk.Frame(container, style='Main.TFrame')
        kpi_row.grid(row=1, column=0, sticky='ew', pady=(2, 10))
        for col in range(4):
            kpi_row.grid_columnconfigure(col, weight=1)
        self._create_kpi_card(kpi_row, 0, 'TOTAL VEHICULOS', self.kpi_total_var, AppStyles.get_color('accent'))
        self._create_kpi_card(kpi_row, 1, 'OPERATIVOS', self.kpi_operativos_var, AppStyles.get_color('success'))
        self._create_kpi_card(kpi_row, 2, 'PROX. ALERTA', self.kpi_overdue_var, AppStyles.get_color('danger'))
        self._create_kpi_card(kpi_row, 3, 'PROM. KILOMETRAJE', self.kpi_promedio_km_var, AppStyles.get_color('info'))

        main_frame = ttk.Frame(container, style='Main.TFrame')
        main_frame.grid(row=2, column=0, sticky='nsew')
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(1, weight=1)

        data_frame = ttk.LabelFrame(main_frame, text="Registro de Vehiculo", padding=12)
        data_frame.grid(row=0, column=0, rowspan=2, padx=(0, 8), sticky='nsew')
        data_frame.columnconfigure(1, weight=1)
        data_frame.grid_rowconfigure(6, weight=1)

        ttk.Label(data_frame, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.cliente_var = StringVar()
        self.cliente_combo = ttk.Combobox(data_frame, textvariable=self.cliente_var, width=30, postcommand=self.actualizar_lista_clientes)
        self.cliente_combo.grid(row=0, column=1, columnspan=2, padx=5, pady=2)
        self.cliente_combo.bind('<KeyRelease>', self.filtrar_clientes)
        self.cargar_clientes()

        ttk.Label(data_frame, text="Placa:").grid(row=1, column=0, sticky="w")
        placa_entry = ttk.Entry(data_frame, textvariable=self.placa_var)
        placa_entry.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        placa_entry.bind('<KeyRelease>', lambda e: self.validar_placa(self.placa_var, e.widget))

        ttk.Label(data_frame, text="Marca:").grid(row=2, column=0, sticky="w")
        self.marca_combo = ttk.Combobox(data_frame, textvariable=self.marca_var, values=self.MARCAS_COMUNES)
        self.marca_combo.grid(row=2, column=1, padx=5, pady=2, sticky='ew')
        self.marca_combo.bind('<KeyRelease>', lambda e: self.validar_marca(self.marca_var, e.widget))

        ttk.Label(data_frame, text="Modelo:").grid(row=3, column=0, sticky="w")
        self.modelo_combo = ttk.Combobox(data_frame, textvariable=self.modelo_var, values=self.años)
        self.modelo_combo.grid(row=3, column=1, padx=5, pady=2, sticky='ew')
        self.modelo_combo.bind('<KeyRelease>', lambda e: self.validar_modelo(self.modelo_var, e.widget))

        ttk.Label(data_frame, text="Linea:").grid(row=4, column=0, sticky="w")
        linea_entry = ttk.Entry(data_frame, textvariable=self.linea_var)
        linea_entry.grid(row=4, column=1, padx=5, pady=2, sticky='ew')
        linea_entry.bind('<KeyRelease>', lambda e: self.validar_linea(self.linea_var, e.widget))

        ttk.Label(data_frame, text="Kilometraje:").grid(row=5, column=0, sticky="w")
        kilometraje_entry = ttk.Entry(data_frame, textvariable=self.kilometraje_var)
        kilometraje_entry.grid(row=5, column=1, padx=5, pady=2, sticky='ew')
        kilometraje_entry.bind('<KeyRelease>', lambda e: self.validar_solo_numeros(self.kilometraje_var, e.widget))

        btn_row = ttk.Frame(data_frame)
        btn_row.grid(row=7, column=0, columnspan=2, pady=(8, 4), sticky='ew')
        btn_row.columnconfigure(0, weight=1)
        btn_row.columnconfigure(1, weight=1)
        ttk.Button(btn_row, text="Guardar", command=self.save, style='Success.TButton').grid(row=0, column=0, padx=4, pady=3, sticky='ew')
        ttk.Button(btn_row, text="Modificar", command=self.update, style='Info.TButton').grid(row=0, column=1, padx=4, pady=3, sticky='ew')
        ttk.Button(btn_row, text="Eliminar", command=self.delete, style='Danger.TButton').grid(row=1, column=0, padx=4, pady=3, sticky='ew')
        ttk.Button(btn_row, text="Limpiar", command=self.clear_fields, style='Warning.TButton').grid(row=1, column=1, padx=4, pady=3, sticky='ew')

        search_frame = ttk.LabelFrame(main_frame, text="Filtros", padding=12)
        search_frame.grid(row=0, column=1, padx=(8, 0), pady=(0, 8), sticky='ew')
        
        ttk.Label(search_frame, text="Buscar por:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        criterio_combo = ttk.Combobox(search_frame, textvariable=self.criterio_busqueda_var, 
                                      values=["Placa", "Marca", "Cliente"], state="readonly", width=12)
        criterio_combo.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(search_frame, text="Texto:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        busqueda_entry = ttk.Entry(search_frame, textvariable=self.busqueda_var, width=25)
        busqueda_entry.grid(row=0, column=3, padx=5, pady=2)
        busqueda_entry.bind('<KeyRelease>', lambda e: self.buscar_vehiculos())
        
        ttk.Button(search_frame, text="Buscar", command=self.buscar_vehiculos, style='Primary.TButton').grid(row=0, column=4, padx=5, pady=2)
        ttk.Button(search_frame, text="Mostrar Todos", command=self.load_data, style='Secondary.TButton').grid(row=0, column=5, padx=5, pady=2)

        table_frame = ttk.LabelFrame(main_frame, text="Inventario de Vehiculos", padding=10)
        table_frame.grid(row=1, column=1, padx=(8, 0), sticky='nsew')
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(table_frame, columns=(
            "Placa", "Marca", "Modelo", "Línea", "Kilometraje", "Estado", "Cliente"
        ), show="headings", height=15)

        # Configurar columnas
        self.tree.heading("Placa", text="Placa", anchor="center")
        self.tree.heading("Marca", text="Marca", anchor="center")
        self.tree.heading("Modelo", text="Modelo", anchor="center")
        self.tree.heading("Línea", text="Línea", anchor="center")
        self.tree.heading("Kilometraje", text="Kilometraje", anchor="center")
        self.tree.heading("Estado", text="Estado Servicio", anchor="center")
        self.tree.heading("Cliente", text="Cliente", anchor="center")

        self.tree.column("Placa", width=100, anchor="center")
        self.tree.column("Marca", width=100, anchor="center")
        self.tree.column("Modelo", width=80, anchor="center")
        self.tree.column("Línea", width=100, anchor="center")
        self.tree.column("Kilometraje", width=100, anchor="center")
        self.tree.column("Estado", width=120, anchor="center")
        self.tree.column("Cliente", width=240, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

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

    def _update_kpis(self, vehiculos):
        self.kpi_total_var.set(str(len(vehiculos)))
        self.kpi_operativos_var.set(str(sum(1 for v in vehiculos if getattr(v, 'kilometraje', 0) < 200000)))
        self.kpi_overdue_var.set(str(sum(1 for v in vehiculos if getattr(v, 'kilometraje', 0) >= 200000)))

        if vehiculos:
            promedio = int(sum(getattr(v, 'kilometraje', 0) for v in vehiculos) / len(vehiculos))
            self.kpi_promedio_km_var.set(f"{promedio}")
        else:
            self.kpi_promedio_km_var.set('0')

    def cargar_clientes(self):
        clientes = self.cliente_controller.get_all()
        self.clientes_data = {f"{c.cedula} - {c.nombre}": c.id for c in clientes}
        self.cliente_combo['values'] = list(self.clientes_data.keys())

    def filtrar_clientes(self, event=None):
        """Filtrar clientes en el combobox mientras se escribe"""
        # Ignorar teclas especiales que no modifican el texto
        if event and event.keysym in ('Down', 'Up', 'Return', 'Tab', 'Escape'):
            return
        
        # Obtener el texto actual
        texto = self.cliente_var.get().upper()
        
        if not texto:
            # Si está vacío, mostrar todos
            self.cargar_clientes()
            return
        
        # Filtrar clientes que coincidan con el texto
        clientes = self.cliente_controller.get_all()
        clientes_filtrados = []
        
        # Reconstruir el diccionario para los filtrados
        self.clientes_data = {}
        
        for cliente in clientes:
            cliente_str = f"{cliente.cedula} - {cliente.nombre}"
            cliente_texto = cliente_str.upper()
            if texto in cliente_texto:
                clientes_filtrados.append(cliente_str)
                self.clientes_data[cliente_str] = cliente.id
        
        # Actualizar valores del combobox
        self.cliente_combo['values'] = clientes_filtrados

    def actualizar_lista_clientes(self):
        """Actualizar la lista cuando se abre el dropdown manualmente"""
        texto = self.cliente_var.get().upper()
        
        if not texto:
            self.cargar_clientes()
        else:
            # Ya está filtrado, no hacer nada
            pass

    def abrir_dropdown(self):
        """Abrir el dropdown del combobox manteniendo el foco"""
        try:
            # Simular clic en la flecha del combobox
            self.cliente_combo.tk.call('ttk::combobox::Post', self.cliente_combo)
        except:
            pass

    def on_cliente_selected(self, event=None):
        """Evento cuando se selecciona un cliente del dropdown"""
        # No hacer nada especial, solo mantener la selección
        pass



    def clear_fields(self):
        self.id_var.set("")
        self.placa_var.set("")
        self.marca_var.set("")
        self.modelo_var.set("")
        self.linea_var.set("")
        self.kilometraje_var.set("")
        self.cliente_combo.set("")
        self.busqueda_var.set("")
        # Restablecer valores originales de los comboboxes
        self.marca_combo['values'] = self.MARCAS_COMUNES
        self.modelo_combo['values'] = self.años
        self.cargar_clientes()  # Recargar la lista de clientes

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        vehiculos = self.controller.get_all()
        for vehiculo in vehiculos:
            cliente = vehiculo.cliente
            cliente_info = f"{cliente.cedula} - {cliente.nombre}" if cliente else "N/A"
            estado = self._estado_servicio(vehiculo)
            self.tree.insert("", "end", values=(
                vehiculo.placa,
                vehiculo.marca,
                vehiculo.modelo,
                vehiculo.linea or "",
                vehiculo.kilometraje,
                estado,
                cliente_info
            ), tags=(str(vehiculo.id),))  # Guardar ID en tags para uso interno
            self._update_kpis(vehiculos)

    def _estado_servicio(self, vehiculo):
        km = getattr(vehiculo, 'kilometraje', 0)
        if km >= 200000:
            return 'OVERDUE'
        if km >= 150000:
            return 'UPCOMING'
        return 'OK'

    def save(self):
        try:
            # Validaciones
            placa = self.placa_var.get().strip()
            marca = self.marca_var.get().strip()
            modelo = self.modelo_var.get().strip()
            linea = self.linea_var.get().strip()
            kilometraje = self.kilometraje_var.get().strip()
            
            if not placa:
                self.show_warning("La placa es obligatoria")
                return
            
            if len(placa) < 5:
                self.show_warning("La placa debe tener al menos 5 caracteres")
                return
            
            if not marca:
                self.show_warning("La marca es obligatoria")
                return
            
            if not modelo:
                self.show_warning("El modelo es obligatorio")
                return
            
            if not kilometraje:
                self.show_warning("El kilometraje es obligatorio")
                return
            
            cliente_seleccionado = self.cliente_combo.get()
            if not cliente_seleccionado:
                self.show_warning("Debe seleccionar un cliente")
                return

            cliente_id = self.clientes_data[cliente_seleccionado]
            self.controller.create(
                placa=placa,
                marca=marca,
                modelo=modelo,
                linea=linea,
                kilometraje=int(kilometraje),
                cliente_id=cliente_id
            )
            self.show_info("Vehículo guardado exitosamente")
            self.clear_fields()
            self.load_data()
        except ValueError as e:
            self.show_error(f"Error al guardar: {str(e)}")
        except Exception as e:
            self.show_error(f"Error inesperado: {str(e)}")

    def update(self):
        try:
            if not self.id_var.get():
                self.show_warning("Seleccione un vehículo para modificar")
                return

            # Validaciones
            placa = self.placa_var.get().strip()
            marca = self.marca_var.get().strip()
            modelo = self.modelo_var.get().strip()
            linea = self.linea_var.get().strip()
            kilometraje = self.kilometraje_var.get().strip()
            
            if not placa:
                self.show_warning("La placa es obligatoria")
                return
            
            if len(placa) < 5:
                self.show_warning("La placa debe tener al menos 5 caracteres")
                return
            
            if not marca:
                self.show_warning("La marca es obligatoria")
                return
            
            if not modelo:
                self.show_warning("El modelo es obligatorio")
                return
            
            if not kilometraje:
                self.show_warning("El kilometraje es obligatorio")
                return

            cliente_seleccionado = self.cliente_combo.get()
            if not cliente_seleccionado:
                self.show_warning("Debe seleccionar un cliente")
                return

            cliente_id = self.clientes_data[cliente_seleccionado]
            self.controller.update(
                id=self.id_var.get(),
                placa=placa,
                marca=marca,
                modelo=modelo,
                linea=linea,
                kilometraje=int(kilometraje),
                cliente_id=cliente_id
            )
            self.show_info("Vehículo actualizado exitosamente")
            self.clear_fields()
            self.load_data()
        except ValueError as e:
            self.show_error(f"Error al actualizar: {str(e)}")
        except Exception as e:
            self.show_error(f"Error inesperado: {str(e)}")

    def delete(self):
        try:
            if not self.id_var.get():
                self.show_warning("Seleccione un vehículo para eliminar")
                return

            if self.show_question("¿Está seguro de eliminar este vehículo?"):
                self.controller.delete(self.id_var.get())
                self.show_info("Vehículo eliminado exitosamente")
                self.clear_fields()
                self.load_data()
        except Exception as e:
            self.show_error(f"Error al eliminar: {str(e)}")

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
        # Obtener ID del tag
        item_id = self.tree.item(selected[0])["tags"][0]
        values = self.tree.item(selected[0])["values"]
        
        self.id_var.set(item_id)
        self.placa_var.set(values[0].upper())  # Asegurar que la placa esté en mayúsculas
        self.marca_var.set(values[1].upper())  # Asegurar que la marca esté en mayúsculas
        self.modelo_var.set(values[2])
        self.linea_var.set(values[3])
        self.kilometraje_var.set(values[4])
        self.cliente_combo.set(values[6])
        
        # Actualizar los comboboxes
        if values[1].upper() not in self.MARCAS_COMUNES:
            self.marca_combo['values'] = list(self.MARCAS_COMUNES) + [values[1].upper()]
        if values[2] not in self.años:
            self.modelo_combo['values'] = list(self.años) + [values[2]]

    def buscar_vehiculos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener criterio y texto de búsqueda
        criterio = self.criterio_busqueda_var.get()
        texto_busqueda = self.busqueda_var.get().strip().upper()

        if not texto_busqueda:
            self.load_data()
            return

        vehiculos = self.controller.get_all()
        vehiculos_filtrados = []

        for vehiculo in vehiculos:
            cliente = vehiculo.cliente
            cliente_info = f"{cliente.cedula} - {cliente.nombre}" if cliente else "N/A"
            
            if criterio == "Placa":
                if texto_busqueda in vehiculo.placa.upper():
                    vehiculos_filtrados.append((vehiculo, cliente_info))
            elif criterio == "Marca":
                if texto_busqueda in vehiculo.marca.upper():
                    vehiculos_filtrados.append((vehiculo, cliente_info))
            elif criterio == "Cliente":
                if cliente and texto_busqueda in cliente_info.upper():
                    vehiculos_filtrados.append((vehiculo, cliente_info))

        if vehiculos_filtrados:
            for vehiculo, cliente_info in vehiculos_filtrados:
                self.tree.insert("", "end", values=(
                    vehiculo.placa,
                    vehiculo.marca,
                    vehiculo.modelo,
                    vehiculo.linea or "",
                    vehiculo.kilometraje,
                    self._estado_servicio(vehiculo),
                    cliente_info
                ), tags=(str(vehiculo.id),))
            self._update_kpis([v for v, _ in vehiculos_filtrados])
        else:
            self._update_kpis([])
            self.show_info(f"No se encontraron vehículos con {criterio}: '{texto_busqueda}'")
    
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

    def validar_placa(self, variable, widget=None):
        valor = variable.get()
        valor_limpio = ''.join(c for c in valor if c.isalnum() or c in '-').upper()
        if valor != valor_limpio and widget:
            self._set_var_preserving_cursor(variable, valor_limpio, widget)

    def validar_marca(self, variable, widget=None):
        valor = variable.get()
        valor_limpio = ''.join(c for c in valor if c.isalnum() or c.isspace()).upper()
        if valor != valor_limpio and widget:
            self._set_var_preserving_cursor(variable, valor_limpio, widget)

    def validar_modelo(self, variable, widget=None):
        valor = variable.get()
        valor_limpio = ''.join(filter(str.isdigit, valor))[:4]
        if valor != valor_limpio and widget:
            self._set_var_preserving_cursor(variable, valor_limpio, widget)

    def validar_linea(self, variable, widget=None):
        valor = variable.get()
        valor_limpio = ''.join(c for c in valor if c.isalnum() or c.isspace() or c in '-').upper()
        if valor != valor_limpio and widget:
            self._set_var_preserving_cursor(variable, valor_limpio, widget)
