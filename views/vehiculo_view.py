from tkinter import ttk, StringVar
from views.base_view import BaseView
from controllers.vehiculo_controller import VehiculoController
from controllers.cliente_controller import ClienteController
from datetime import datetime

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
        # Variables
        self.id_var = StringVar()
        self.placa_var = StringVar()
        self.marca_var = StringVar()
        self.modelo_var = StringVar()
        self.linea_var = StringVar()
        self.kilometraje_var = StringVar()
        self.cliente_id_var = StringVar()
        self.busqueda_var = StringVar()
        self.criterio_busqueda_var = StringVar(value="Placa")

        # Centrar contenido: crear un contenedor centrado
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        container = ttk.Frame(self.frame)
        container.grid(row=0, column=0, columnspan=2, pady=10)

        # Frame principal dentro del contenedor
        main_frame = ttk.Frame(container)
        main_frame.grid(row=0, column=0)

        # Frame de datos del vehículo
        data_frame = ttk.LabelFrame(main_frame, text="Datos del Vehículo", padding=12)
        data_frame.grid(row=0, column=0, padx=10, pady=5)
        # Hacer que la columna de inputs sea más ancha
        data_frame.columnconfigure(0, weight=0)
        data_frame.columnconfigure(1, weight=1)

        # Selector de cliente con autocompletado
        ttk.Label(data_frame, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.cliente_var = StringVar()
        self.cliente_combo = ttk.Combobox(data_frame, textvariable=self.cliente_var, width=30, postcommand=self.actualizar_lista_clientes)
        self.cliente_combo.grid(row=0, column=1, columnspan=2, padx=5, pady=2)
        # Bind para autocompletar mientras se escribe
        self.cliente_combo.bind('<KeyRelease>', self.filtrar_clientes)
        self.cargar_clientes()

        # Campos
        # Campo de Placa
        ttk.Label(data_frame, text="Placa:").grid(row=1, column=0, sticky="w")
        placa_entry = ttk.Entry(data_frame, textvariable=self.placa_var)
        placa_entry.grid(row=1, column=1, padx=5, pady=2)
        placa_entry.bind('<KeyRelease>', lambda e: self.validar_placa(self.placa_var))

        # Campo de Marca con Combobox editable
        ttk.Label(data_frame, text="Marca:").grid(row=2, column=0, sticky="w")
        self.marca_combo = ttk.Combobox(data_frame, textvariable=self.marca_var, values=self.MARCAS_COMUNES)
        self.marca_combo.grid(row=2, column=1, padx=5, pady=2)
        self.marca_combo.bind('<KeyRelease>', lambda e: self.validar_marca(self.marca_var))

        # Campo de Modelo (Año) con Combobox editable
        ttk.Label(data_frame, text="Modelo:").grid(row=3, column=0, sticky="w")
        self.modelo_combo = ttk.Combobox(data_frame, textvariable=self.modelo_var, values=self.años)
        self.modelo_combo.grid(row=3, column=1, padx=5, pady=2)
        self.modelo_combo.bind('<KeyRelease>', lambda e: self.validar_modelo(self.modelo_var))

        # Campo de Línea
        ttk.Label(data_frame, text="Línea:").grid(row=4, column=0, sticky="w")
        linea_entry = ttk.Entry(data_frame, textvariable=self.linea_var)
        linea_entry.grid(row=4, column=1, padx=5, pady=2)
        linea_entry.bind('<KeyRelease>', lambda e: self.validar_linea(self.linea_var))

        ttk.Label(data_frame, text="Kilometraje:").grid(row=5, column=0, sticky="w")
        kilometraje_entry = ttk.Entry(data_frame, textvariable=self.kilometraje_var)
        kilometraje_entry.grid(row=5, column=1, padx=5, pady=2)
        kilometraje_entry.bind('<KeyRelease>', lambda e: self.validar_solo_numeros(self.kilometraje_var))

        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10)

        ttk.Button(button_frame, text="Guardar", command=self.save, style='Success.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Modificar", command=self.update, style='Info.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.delete, style='Danger.TButton').grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_fields, style='Warning.TButton').grid(row=0, column=3, padx=5)

        # Frame de búsqueda/consulta
        search_frame = ttk.LabelFrame(main_frame, text="Consultar Vehículos", padding=12)
        search_frame.grid(row=2, column=0, padx=10, pady=5)
        
        ttk.Label(search_frame, text="Buscar por:").grid(row=0, column=0, sticky="w", padx=5)
        criterio_combo = ttk.Combobox(search_frame, textvariable=self.criterio_busqueda_var, 
                                      values=["Placa", "Marca", "Cliente"], state="readonly", width=12)
        criterio_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(search_frame, text="Texto:").grid(row=0, column=2, sticky="w", padx=5)
        busqueda_entry = ttk.Entry(search_frame, textvariable=self.busqueda_var, width=25)
        busqueda_entry.grid(row=0, column=3, padx=5)
        busqueda_entry.bind('<KeyRelease>', lambda e: self.buscar_vehiculos())
        
        ttk.Button(search_frame, text="Buscar", command=self.buscar_vehiculos, style='Primary.TButton').grid(row=0, column=4, padx=5)
        ttk.Button(search_frame, text="Mostrar Todos", command=self.load_data, style='Secondary.TButton').grid(row=0, column=5, padx=5)

        # Tabla
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=3, column=0, pady=10)

        # Treeview
        self.tree = ttk.Treeview(table_frame, columns=(
            "Placa", "Marca", "Modelo", "Línea", "Kilometraje", "Cliente"
        ), show="headings", height=8)

        # Configurar columnas
        self.tree.heading("Placa", text="Placa", anchor="center")
        self.tree.heading("Marca", text="Marca", anchor="center")
        self.tree.heading("Modelo", text="Modelo", anchor="center")
        self.tree.heading("Línea", text="Línea", anchor="center")
        self.tree.heading("Kilometraje", text="Kilometraje", anchor="center")
        self.tree.heading("Cliente", text="Cliente", anchor="center")

        self.tree.column("Placa", width=100, anchor="center")
        self.tree.column("Marca", width=100, anchor="center")
        self.tree.column("Modelo", width=80, anchor="center")
        self.tree.column("Línea", width=100, anchor="center")
        self.tree.column("Kilometraje", width=100, anchor="center")
        self.tree.column("Cliente", width=220, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Bind para selección
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Cargar datos
        self.load_data()

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
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Cargar datos
        vehiculos = self.controller.get_all()
        for vehiculo in vehiculos:
            cliente = vehiculo.cliente
            cliente_info = f"{cliente.cedula} - {cliente.nombre}" if cliente else "N/A"
            self.tree.insert("", "end", values=(
                vehiculo.placa,
                vehiculo.marca,
                vehiculo.modelo,
                vehiculo.linea or "",
                vehiculo.kilometraje,
                cliente_info
            ), tags=(str(vehiculo.id),))  # Guardar ID en tags para uso interno

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
        self.cliente_combo.set(values[5])
        
        # Actualizar los comboboxes
        if values[1].upper() not in self.MARCAS_COMUNES:
            self.marca_combo['values'] = list(self.MARCAS_COMUNES) + [values[1].upper()]
        if values[2] not in self.años:
            self.modelo_combo['values'] = list(self.años) + [values[2]]

    def buscar_vehiculos(self):
        """Busca vehículos según el criterio seleccionado"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener criterio y texto de búsqueda
        criterio = self.criterio_busqueda_var.get()
        texto_busqueda = self.busqueda_var.get().strip().upper()

        # Si no hay texto de búsqueda, mostrar todos
        if not texto_busqueda:
            self.load_data()
            return

        # Obtener todos los vehículos y filtrar
        vehiculos = self.controller.get_all()
        vehiculos_filtrados = []

        for vehiculo in vehiculos:
            cliente = vehiculo.cliente
            cliente_info = f"{cliente.cedula} - {cliente.nombre}" if cliente else "N/A"
            
            # Aplicar filtro según criterio
            if criterio == "Placa":
                if texto_busqueda in vehiculo.placa.upper():
                    vehiculos_filtrados.append((vehiculo, cliente_info))
            elif criterio == "Marca":
                if texto_busqueda in vehiculo.marca.upper():
                    vehiculos_filtrados.append((vehiculo, cliente_info))
            elif criterio == "Cliente":
                if cliente and texto_busqueda in cliente_info.upper():
                    vehiculos_filtrados.append((vehiculo, cliente_info))

        # Mostrar resultados
        if vehiculos_filtrados:
            for vehiculo, cliente_info in vehiculos_filtrados:
                self.tree.insert("", "end", values=(
                    vehiculo.placa,
                    vehiculo.marca,
                    vehiculo.modelo,
                    vehiculo.linea or "",
                    vehiculo.kilometraje,
                    cliente_info
                ), tags=(str(vehiculo.id),))
        else:
            # Mostrar mensaje si no hay resultados
            self.show_info(f"No se encontraron vehículos con {criterio}: '{texto_busqueda}'")
    
    def validar_solo_numeros(self, variable):
        """Permite solo numeros en un campo"""
        valor = variable.get()
        valor_limpio = ''.join(filter(str.isdigit, valor))
        if valor != valor_limpio:
            variable.set(valor_limpio)
    
    def validar_placa(self, variable):
        """Permite alfanumericos y convierte a mayusculas"""
        valor = variable.get()
        valor_limpio = ''.join(c for c in valor if c.isalnum() or c in '-')
        valor_limpio = valor_limpio.upper()
        if valor != valor_limpio:
            variable.set(valor_limpio)
    
    def validar_marca(self, variable):
        """Permite letras, numeros, espacios y convierte a mayusculas"""
        valor = variable.get()
        valor_limpio = ''.join(c for c in valor if c.isalnum() or c.isspace())
        valor_limpio = valor_limpio.upper()
        if valor != valor_limpio:
            variable.set(valor_limpio)
    
    def validar_modelo(self, variable):
        """Permite solo numeros para el modelo (ano)"""
        valor = variable.get()
        valor_limpio = ''.join(filter(str.isdigit, valor))
        if len(valor_limpio) > 4:
            valor_limpio = valor_limpio[:4]
        if valor != valor_limpio:
            variable.set(valor_limpio)
    
    def validar_linea(self, variable):
        """Permite letras, numeros, espacios y convierte a mayusculas"""
        valor = variable.get()
        valor_limpio = ''.join(c for c in valor if c.isalnum() or c.isspace() or c in '-')
        valor_limpio = valor_limpio.upper()
        if valor != valor_limpio:
            variable.set(valor_limpio)
