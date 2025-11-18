import tkinter as tk
from tkinter import ttk, StringVar, Frame
from views.base_view import BaseView
from controllers.mantenimiento_controller import MantenimientoController
from controllers.vehiculo_controller import VehiculoController
from models.mantenimiento_varios_model import TipoMantenimientoVarios
from datetime import datetime

class MantenimientoBaseView(BaseView):
    MECANICOS = [
        'ANDRES BOTERO',
        'SANTIAGO CASTAÑEDA',
        'JADER CASTAÑEDA'
    ]

    def __init__(self, master=None, vehiculo_id=None, mantenimiento_id=None):
        self.controller = MantenimientoController()
        self.vehiculo_controller = VehiculoController()
        self.vehiculo_id = vehiculo_id
        self.mantenimiento_id = mantenimiento_id
        self.modo_edicion = mantenimiento_id is not None
        super().__init__(master)
        
        # Configurar el tamaño de la ventana
        if master:
            # Obtener el tamaño de la pantalla
            screen_width = master.winfo_screenwidth()
            screen_height = master.winfo_screenheight()
            
            # Definir el tamaño de la ventana - un poco más grande que el formulario
            window_width = 750
            window_height = 650
            
            # Calcular la posición para centrar la ventana
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            # Establecer geometría
            master.geometry(f"{window_width}x{window_height}+{x}+{y}")
            master.minsize(700, 600)  # Tamaño mínimo
    
    def crear_frame_con_scroll(self, parent, titulo, padding=15):
        """Crea un frame con scrollbar vertical para el contenido"""
        # Configurar el grid del parent
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # LabelFrame principal
        main_container = ttk.LabelFrame(parent, text=titulo, padding=5)
        main_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Canvas para el scroll
        canvas = tk.Canvas(main_container, highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Frame scrollable dentro del canvas
        scrollable_frame = ttk.Frame(canvas, padding=padding)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar el scroll con la rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind solo al canvas específico, no a toda la ventana
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
        return scrollable_frame

    def clear_fields(self):
        if hasattr(self, 'kilometraje_entry'):
            self.kilometraje_entry.delete(0, 'end')
        if hasattr(self, 'mecanico_combo'):
            self.mecanico_combo.set('')
        if hasattr(self, 'observaciones_text'):
            self.observaciones_text.delete(0, 'end')
        if hasattr(self, 'vehiculo_combo'):
            self.vehiculo_combo.set('')
        if hasattr(self, 'fecha_entry'):
            self.fecha_entry.delete(0, 'end')
            self.fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        

    def setup_common_fields(self, frame):
        # Campos comunes para todos los tipos de mantenimiento
        # Configurar el grid para mejor alineación
        frame.columnconfigure(0, weight=0, minsize=120)  # Columna de labels con ancho fijo
        frame.columnconfigure(1, weight=1, minsize=300)  # Columna de campos
        frame.columnconfigure(2, weight=0)  # Columna para hints
        
        # Ancho estándar para todos los campos
        campo_ancho = 35
        
        # Fecha
        ttk.Label(frame, text="Fecha:", font=("Arial", 9, "bold")).grid(
            row=0, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.fecha_entry = ttk.Entry(frame, width=15, font=("Arial", 9))
        self.fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.fecha_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(frame, text="(AAAA-MM-DD)", font=("Arial", 8), foreground="gray").grid(
            row=0, column=2, sticky="w", pady=5
        )
        
        # Kilometraje
        ttk.Label(frame, text="Kilometraje:", font=("Arial", 9, "bold")).grid(
            row=1, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.kilometraje_entry = ttk.Entry(frame, width=campo_ancho, font=("Arial", 9))
        self.kilometraje_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.kilometraje_entry.bind('<KeyRelease>', lambda e: self.validar_solo_numeros(self.kilometraje_entry))
        
        # Mecánico
        ttk.Label(frame, text="Mecánico:", font=("Arial", 9, "bold")).grid(
            row=2, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.mecanico_combo = ttk.Combobox(frame, values=self.MECANICOS, width=campo_ancho-2, font=("Arial", 9))
        self.mecanico_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        self.mecanico_combo.bind('<KeyRelease>', lambda e: self.validar_mecanico())
        
        # Observaciones
        ttk.Label(frame, text="Observaciones:", font=("Arial", 9, "bold")).grid(
            row=3, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.observaciones_text = ttk.Entry(frame, width=campo_ancho, font=("Arial", 9))
        self.observaciones_text.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # Si no se proporciona un vehículo_id, mostrar selector de vehículo
        if not self.vehiculo_id:
            ttk.Label(frame, text="Vehículo:", font=("Arial", 9, "bold")).grid(
                row=4, column=0, sticky="e", padx=(10, 5), pady=5
            )
            
            # Frame para agrupar el combo de vehículo y el buscador
            vehiculo_frame = ttk.Frame(frame)
            vehiculo_frame.grid(row=4, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
            
            # Combobox de vehículos
            self.vehiculo_combo = ttk.Combobox(vehiculo_frame, state="readonly", width=32, font=("Arial", 9))
            self.vehiculo_combo.grid(row=0, column=0, sticky="w")
            
            # Separador visual
            ttk.Separator(vehiculo_frame, orient="vertical").grid(row=0, column=1, sticky="ns", padx=8)
            
            # Label y campo de búsqueda por placa
            buscar_label = ttk.Label(vehiculo_frame, text="🔍", font=("Segoe UI Emoji", 10))
            buscar_label.grid(row=0, column=2, sticky="w", padx=(0, 3))
            
            self.buscar_placa_entry = ttk.Entry(vehiculo_frame, width=15, font=("Arial", 9))
            self.buscar_placa_entry.grid(row=0, column=3, sticky="w")
            self.buscar_placa_entry.insert(0, "Buscar placa...")
            self.buscar_placa_entry.config(foreground="gray")
            
            # Eventos para el placeholder
            self.buscar_placa_entry.bind("<FocusIn>", self.on_buscar_focus_in)
            self.buscar_placa_entry.bind("<FocusOut>", self.on_buscar_focus_out)
            self.buscar_placa_entry.bind("<KeyRelease>", self.buscar_vehiculo_por_placa)
            
            self.cargar_vehiculos()

    def cargar_vehiculos(self):
        vehiculos = self.vehiculo_controller.get_all()
        self.vehiculos_data = {
            f"{v.placa} - {v.marca} {v.modelo}": v.id for v in vehiculos
        }
        self.vehiculo_combo['values'] = list(self.vehiculos_data.keys())
    
    def on_buscar_focus_in(self, event):
        """Elimina el placeholder cuando el campo recibe foco"""
        if self.buscar_placa_entry.get() == "Buscar placa...":
            self.buscar_placa_entry.delete(0, 'end')
            self.buscar_placa_entry.config(foreground="black")
    
    def on_buscar_focus_out(self, event):
        """Restaura el placeholder si el campo está vacío"""
        if not self.buscar_placa_entry.get():
            self.buscar_placa_entry.insert(0, "Buscar placa...")
            self.buscar_placa_entry.config(foreground="gray")
    
    def buscar_vehiculo_por_placa(self, event=None):
        """Busca y selecciona un vehículo por placa en tiempo real"""
        texto_busqueda = self.buscar_placa_entry.get().upper().strip()
        
        # No buscar si es el placeholder
        if texto_busqueda == "BUSCAR PLACA..." or not texto_busqueda:
            return
        
        # Buscar en el diccionario de vehículos
        for vehiculo_texto, vehiculo_id in self.vehiculos_data.items():
            placa = vehiculo_texto.split(" - ")[0]
            if placa.startswith(texto_busqueda):
                self.vehiculo_combo.set(vehiculo_texto)
                return
        
        # Si no encuentra ninguna coincidencia, limpiar la selección
        if texto_busqueda and not any(v.split(" - ")[0].startswith(texto_busqueda) for v in self.vehiculos_data.keys()):
            self.vehiculo_combo.set('')

    def get_vehiculo_id(self):
        if self.vehiculo_id:
            return self.vehiculo_id
        vehiculo_seleccionado = self.vehiculo_combo.get()
        if not vehiculo_seleccionado:
            raise ValueError("Debe seleccionar un vehículo")
        return self.vehiculos_data[vehiculo_seleccionado]

    def get_common_data(self):
        # Validaciones
        fecha_str = self.fecha_entry.get().strip()
        kilometraje_str = self.kilometraje_entry.get().strip()
        mecanico = self.mecanico_combo.get().strip()
        
        if not fecha_str:
            raise ValueError("La fecha es obligatoria")
        
        if not kilometraje_str:
            raise ValueError("El kilometraje es obligatorio")
        
        if not mecanico:
            raise ValueError("El mecánico es obligatorio")
        
        try:
            # Intentar parsear la fecha en formato AAAA-MM-DD
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Fecha inválida. Use formato AAAA-MM-DD")
        
        return {
            'vehiculo_id': self.get_vehiculo_id(),
            'fecha_mantenimiento': fecha,
            'kilometraje': int(kilometraje_str),
            'mecanico': mecanico,
            'observaciones': self.observaciones_text.get()
        }

    def validar_solo_numeros(self, entry_widget):
        """Permite solo números en un campo Entry"""
        valor = entry_widget.get()
        valor_limpio = ''.join(filter(str.isdigit, valor))
        if valor != valor_limpio:
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, valor_limpio)
    
    def validar_mecanico(self):
        """Permite solo letras y espacios en el mecánico, convierte a mayúsculas"""
        valor = self.mecanico_combo.get()
        valor_limpio = ''.join(c for c in valor if c.isalpha() or c.isspace())
        valor_limpio = valor_limpio.upper()
        if valor != valor_limpio:
            self.mecanico_combo.set(valor_limpio)
    
    def crear_boton_estilizado(self, parent, text, command, tipo="primary"):
        """Crea un botón con estilo personalizado"""
        if tipo == "primary":
            # Botón principal (Guardar/Actualizar) - Verde
            style_name = "Primary.TButton"
            if not hasattr(self, '_primary_style_created'):
                style = ttk.Style()
                style.configure("Primary.TButton",
                    foreground="white",
                    background="#28a745",
                    font=("Arial", 9, "bold"),
                    padding=(10, 5))
                style.map("Primary.TButton",
                    background=[('active', '#218838'), ('pressed', '#1e7e34')])
                self._primary_style_created = True
        else:
            # Botón secundario (Cancelar) - Gris
            style_name = "Secondary.TButton"
            if not hasattr(self, '_secondary_style_created'):
                style = ttk.Style()
                style.configure("Secondary.TButton",
                    foreground="white",
                    background="#6c757d",
                    font=("Arial", 9),
                    padding=(10, 5))
                style.map("Secondary.TButton",
                    background=[('active', '#5a6268'), ('pressed', '#545b62')])
                self._secondary_style_created = True
        
        btn = ttk.Button(parent, text=text, command=command, style=style_name, width=14)
        return btn

    # Se eliminan métodos de gestión de 'Mantenimientos Varios' de las ventanas individuales

class CambioAceiteView(MantenimientoBaseView):
    def clear_fields(self):
        super().clear_fields()  # Limpia los campos comunes
        self.filtro_aceite_entry.delete(0, 'end')
        self.filtro_aire_entry.delete(0, 'end')
        self.tipo_aceite_entry.delete(0, 'end')

    def setup_ui(self):
        # Frame principal con scroll
        titulo = "Editar Cambio de Aceite" if self.modo_edicion else "Cambio de Aceite"
        main_frame = self.crear_frame_con_scroll(self.frame, titulo)

        # Campos comunes
        self.setup_common_fields(main_frame)

        # Campos específicos
        row = 5 if not self.vehiculo_id else 4
        campo_ancho = 35
        
        ttk.Label(main_frame, text="Filtro de Aceite:", font=("Arial", 9, "bold")).grid(
            row=row, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.filtro_aceite_entry = ttk.Entry(main_frame, width=campo_ancho, font=("Arial", 9))
        self.filtro_aceite_entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, text="Filtro de Aire:", font=("Arial", 9, "bold")).grid(
            row=row+1, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.filtro_aire_entry = ttk.Entry(main_frame, width=campo_ancho, font=("Arial", 9))
        self.filtro_aire_entry.grid(row=row+1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, text="Tipo de Aceite:", font=("Arial", 9, "bold")).grid(
            row=row+2, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.tipo_aceite_entry = ttk.Entry(main_frame, width=campo_ancho, font=("Arial", 9))
        self.tipo_aceite_entry.grid(row=row+2, column=1, sticky="ew", padx=5, pady=5)

        # Frame para botones centrado
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row+3, column=0, columnspan=3, pady=20)
        
        btn_text = "Actualizar" if self.modo_edicion else "Guardar"
        self.crear_boton_estilizado(btn_frame, btn_text, self.save, "primary").pack(side="left", padx=8)
        self.crear_boton_estilizado(btn_frame, "Cancelar", self.frame.master.destroy, "secondary").pack(side="left", padx=8)

        # Cargar datos si es edición
        if self.modo_edicion:
            self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos del mantenimiento para edición"""
        from models.mantenimiento_model import CambioAceite
        mantenimiento = CambioAceite.get_by_id(self.mantenimiento_id)
        if mantenimiento:
            self.fecha_entry.delete(0, 'end')
            self.fecha_entry.insert(0, mantenimiento.fecha_mantenimiento.strftime("%Y-%m-%d"))
            self.kilometraje_entry.delete(0, 'end')
            self.kilometraje_entry.insert(0, str(mantenimiento.kilometraje))
            self.mecanico_combo.set(mantenimiento.mecanico)
            self.observaciones_text.delete(0, 'end')
            self.observaciones_text.insert(0, mantenimiento.observaciones or '')
            
            self.filtro_aceite_entry.delete(0, 'end')
            self.filtro_aceite_entry.insert(0, mantenimiento.filtro_aceite or '')
            self.filtro_aire_entry.delete(0, 'end')
            self.filtro_aire_entry.insert(0, mantenimiento.filtro_aire or '')
            self.tipo_aceite_entry.delete(0, 'end')
            self.tipo_aceite_entry.insert(0, mantenimiento.tipo_aceite or '')

    def save(self):
        try:
            data = self.get_common_data()
            
            if self.modo_edicion:
                self.controller.update_cambio_aceite(
                    id=self.mantenimiento_id,
                    **data,
                    filtro_aceite=self.filtro_aceite_entry.get(),
                    filtro_aire=self.filtro_aire_entry.get(),
                    tipo_aceite=self.tipo_aceite_entry.get()
                )
                self.show_info("Cambio de aceite actualizado exitosamente")
            else:
                mantenimiento_id = self.controller.create_cambio_aceite(
                    **data,
                    filtro_aceite=self.filtro_aceite_entry.get(),
                    filtro_aire=self.filtro_aire_entry.get(),
                    tipo_aceite=self.tipo_aceite_entry.get()
                )
                self.show_info("Cambio de aceite registrado exitosamente")
            
            # Notificar a la app que el historial cambió
            try:
                self.frame.winfo_toplevel().event_generate('<<HistorialActualizado>>', when='tail')
            except Exception:
                pass
            self.frame.master.destroy()
        except Exception as e:
            self.show_error(f"Error al guardar: {str(e)}")

class MantenimientoFrenosView(MantenimientoBaseView):
    def clear_fields(self):
        super().clear_fields()  # Limpia los campos comunes
        self.estado_pastillas_entry.delete(0, 'end')
        self.estado_discos_entry.delete(0, 'end')
        self.estado_liquido_entry.delete(0, 'end')
        self.estado_campanas_entry.delete(0, 'end')

    def setup_ui(self):
        # Frame principal con scroll
        titulo = "Editar Mantenimiento de Frenos" if self.modo_edicion else "Mantenimiento de Frenos"
        main_frame = self.crear_frame_con_scroll(self.frame, titulo)

        # Campos comunes
        self.setup_common_fields(main_frame)

        # Campos específicos
        row = 5 if not self.vehiculo_id else 4
        campo_ancho = 35

        ttk.Label(main_frame, text="Estado Pastillas:", font=("Arial", 9, "bold")).grid(
            row=row, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.estado_pastillas_entry = ttk.Entry(main_frame, width=campo_ancho, font=("Arial", 9))
        self.estado_pastillas_entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, text="Estado Discos:", font=("Arial", 9, "bold")).grid(
            row=row+1, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.estado_discos_entry = ttk.Entry(main_frame, width=campo_ancho, font=("Arial", 9))
        self.estado_discos_entry.grid(row=row+1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, text="Estado Líquido:", font=("Arial", 9, "bold")).grid(
            row=row+2, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.estado_liquido_entry = ttk.Entry(main_frame, width=campo_ancho, font=("Arial", 9))
        self.estado_liquido_entry.grid(row=row+2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, text="Estado Campanas:", font=("Arial", 9, "bold")).grid(
            row=row+3, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.estado_campanas_entry = ttk.Entry(main_frame, width=campo_ancho, font=("Arial", 9))
        self.estado_campanas_entry.grid(row=row+3, column=1, sticky="ew", padx=5, pady=5)

        # Frame para botones centrado
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row+4, column=0, columnspan=3, pady=20)
        
        btn_text = "Actualizar" if self.modo_edicion else "Guardar"
        self.crear_boton_estilizado(btn_frame, btn_text, self.save, "primary").pack(side="left", padx=8)
        self.crear_boton_estilizado(btn_frame, "Cancelar", self.frame.master.destroy, "secondary").pack(side="left", padx=8)

        # Cargar datos si es edición
        if self.modo_edicion:
            self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos del mantenimiento para edición"""
        from models.mantenimiento_model import MantenimientoFrenos
        mantenimiento = MantenimientoFrenos.get_by_id(self.mantenimiento_id)
        if mantenimiento:
            self.fecha_entry.delete(0, 'end')
            self.fecha_entry.insert(0, mantenimiento.fecha_mantenimiento.strftime("%Y-%m-%d"))
            self.kilometraje_entry.delete(0, 'end')
            self.kilometraje_entry.insert(0, str(mantenimiento.kilometraje))
            self.mecanico_combo.set(mantenimiento.mecanico)
            self.observaciones_text.delete(0, 'end')
            self.observaciones_text.insert(0, mantenimiento.observaciones or '')
            
            self.estado_pastillas_entry.delete(0, 'end')
            self.estado_pastillas_entry.insert(0, mantenimiento.estado_pastillas or '')
            self.estado_discos_entry.delete(0, 'end')
            self.estado_discos_entry.insert(0, mantenimiento.estado_discos or '')
            self.estado_liquido_entry.delete(0, 'end')
            self.estado_liquido_entry.insert(0, mantenimiento.estado_liquido or '')
            self.estado_campanas_entry.delete(0, 'end')
            self.estado_campanas_entry.insert(0, mantenimiento.estado_campanas or '')

    def save(self):
        try:
            data = self.get_common_data()
            
            if self.modo_edicion:
                self.controller.update_mantenimiento_frenos(
                    id=self.mantenimiento_id,
                    **data,
                    estado_pastillas=self.estado_pastillas_entry.get(),
                    estado_discos=self.estado_discos_entry.get(),
                    estado_liquido=self.estado_liquido_entry.get(),
                    estado_campanas=self.estado_campanas_entry.get()
                )
                self.show_info("Mantenimiento de frenos actualizado exitosamente")
            else:
                mantenimiento_id = self.controller.create_mantenimiento_frenos(
                    **data,
                    estado_pastillas=self.estado_pastillas_entry.get(),
                    estado_discos=self.estado_discos_entry.get(),
                    estado_liquido=self.estado_liquido_entry.get(),
                    estado_campanas=self.estado_campanas_entry.get()
                )
                self.show_info("Mantenimiento de frenos registrado exitosamente")
            
            try:
                self.frame.winfo_toplevel().event_generate('<<HistorialActualizado>>', when='tail')
            except Exception:
                pass
            self.frame.master.destroy()
        except Exception as e:
            self.show_error(f"Error al guardar: {str(e)}")

class MantenimientoGeneralView(MantenimientoBaseView):
    def clear_fields(self):
        super().clear_fields()  # Limpia los campos comunes
        self.estado_luces_entry.delete(0, 'end')
        self.estado_frenos_entry.delete(0, 'end')
        self.estado_correa_entry.delete(0, 'end')

    def setup_ui(self):
        # Frame principal con scroll
        titulo = "Editar Mantenimiento General" if self.modo_edicion else "Mantenimiento General"
        main_frame = self.crear_frame_con_scroll(self.frame, titulo)

        # Campos comunes
        self.setup_common_fields(main_frame)

        # Campos específicos
        row = 5 if not self.vehiculo_id else 4
        campo_ancho = 35

        ttk.Label(main_frame, text="Estado Luces:", font=("Arial", 9, "bold")).grid(
            row=row, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.estado_luces_entry = ttk.Entry(main_frame, width=campo_ancho, font=("Arial", 9))
        self.estado_luces_entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, text="Estado Frenos:", font=("Arial", 9, "bold")).grid(
            row=row+1, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.estado_frenos_entry = ttk.Entry(main_frame, width=campo_ancho, font=("Arial", 9))
        self.estado_frenos_entry.grid(row=row+1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, text="Estado Correa:", font=("Arial", 9, "bold")).grid(
            row=row+2, column=0, sticky="e", padx=(10, 5), pady=5
        )
        self.estado_correa_entry = ttk.Entry(main_frame, width=campo_ancho, font=("Arial", 9))
        self.estado_correa_entry.grid(row=row+2, column=1, sticky="ew", padx=5, pady=5)

        # Frame para botones centrado
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row+3, column=0, columnspan=3, pady=20)
        
        btn_text = "Actualizar" if self.modo_edicion else "Guardar"
        self.crear_boton_estilizado(btn_frame, btn_text, self.save, "primary").pack(side="left", padx=8)
        self.crear_boton_estilizado(btn_frame, "Cancelar", self.frame.master.destroy, "secondary").pack(side="left", padx=8)

        # Cargar datos si es edición
        if self.modo_edicion:
            self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos del mantenimiento para edición"""
        from models.mantenimiento_model import MantenimientoGeneral

    def cargar_datos(self):
        """Carga los datos del mantenimiento para edición"""
        from models.mantenimiento_model import MantenimientoGeneral
        mantenimiento = MantenimientoGeneral.get_by_id(self.mantenimiento_id)
        if mantenimiento:
            self.fecha_entry.delete(0, 'end')
            self.fecha_entry.insert(0, mantenimiento.fecha_mantenimiento.strftime("%Y-%m-%d"))
            self.kilometraje_entry.delete(0, 'end')
            self.kilometraje_entry.insert(0, str(mantenimiento.kilometraje))
            self.mecanico_combo.set(mantenimiento.mecanico)
            self.observaciones_text.delete(0, 'end')
            self.observaciones_text.insert(0, mantenimiento.observaciones or '')
            
            self.estado_luces_entry.delete(0, 'end')
            self.estado_luces_entry.insert(0, mantenimiento.estado_luces or '')
            self.estado_frenos_entry.delete(0, 'end')
            self.estado_frenos_entry.insert(0, mantenimiento.estado_frenos or '')
            self.estado_correa_entry.delete(0, 'end')
            self.estado_correa_entry.insert(0, mantenimiento.estado_correa_accesorios or '')

    def save(self):
        try:
            data = self.get_common_data()
            
            if self.modo_edicion:
                self.controller.update_mantenimiento_general(
                    id=self.mantenimiento_id,
                    **data,
                    estado_luces=self.estado_luces_entry.get(),
                    estado_frenos=self.estado_frenos_entry.get(),
                    estado_correa_accesorios=self.estado_correa_entry.get(),
                    fecha_ultima_correa=datetime.now().date()
                )
                self.show_info("Mantenimiento general actualizado exitosamente")
            else:
                mantenimiento_id = self.controller.create_mantenimiento_general(
                    **data,
                    estado_luces=self.estado_luces_entry.get(),
                    estado_frenos=self.estado_frenos_entry.get(),
                    estado_correa_accesorios=self.estado_correa_entry.get(),
                    fecha_ultima_correa=datetime.now().date()
                )
                self.show_info("Mantenimiento general registrado exitosamente")
            
            try:
                self.frame.winfo_toplevel().event_generate('<<HistorialActualizado>>', when='tail')
            except Exception:
                pass
            self.frame.master.destroy()
        except Exception as e:
            self.show_error(f"Error al guardar: {str(e)}")

class MantenimientoCorrectivoView(MantenimientoBaseView):
    def __init__(self, master=None, vehiculo_id=None, mantenimiento_id=None):
        self.trabajos_vars = {}  # Dict para guardar las variables de los checkboxes
        super().__init__(master, vehiculo_id, mantenimiento_id)
    
    def clear_fields(self):
        super().clear_fields()  # Limpia los campos comunes
        self.detalles_falla_text.delete("1.0", "end")
        self.danos_colaterales_text.delete("1.0", "end")
        # Desmarcar todos los checkboxes
        for var in self.trabajos_vars.values():
            var.set(False)
    
    def on_buscar_trabajo_focus_in(self, event):
        """Elimina el placeholder cuando el campo recibe foco"""
        if self.buscar_trabajo_entry.get() == "Buscar trabajo...":
            self.buscar_trabajo_entry.delete(0, 'end')
            self.buscar_trabajo_entry.config(foreground="black")
    
    def on_buscar_trabajo_focus_out(self, event):
        """Restaura el placeholder si el campo está vacío"""
        if not self.buscar_trabajo_entry.get():
            self.buscar_trabajo_entry.insert(0, "Buscar trabajo...")
            self.buscar_trabajo_entry.config(foreground="gray")
    
    def filtrar_trabajos(self, event=None):
        """Filtra la lista de trabajos según el texto de búsqueda"""
        texto_busqueda = self.buscar_trabajo_entry.get().upper().strip()
        
        # No filtrar si es el placeholder
        if texto_busqueda == "BUSCAR TRABAJO...":
            texto_busqueda = ""
        
        # Ocultar/mostrar checkbuttons según el filtro
        for tipo_id, checkbox in self.checkbuttons_trabajos.items():
            texto_checkbox = checkbox.cget("text").upper()
            if not texto_busqueda or texto_busqueda in texto_checkbox:
                checkbox.pack(anchor="w", padx=5, pady=3)
            else:
                checkbox.pack_forget()
        
        # Actualizar el scrollregion del canvas
        self.scrollable_trabajos_frame.update_idletasks()
        self.trabajos_canvas.configure(scrollregion=self.trabajos_canvas.bbox("all"))

    def setup_ui(self):
        # Frame principal con scroll
        titulo = "Editar Mantenimiento Correctivo" if self.modo_edicion else "Nuevo Mantenimiento Correctivo"
        main_frame = self.crear_frame_con_scroll(self.frame, titulo)

        # Campos comunes
        self.setup_common_fields(main_frame)

        # Campos específicos
        row = 5 if not self.vehiculo_id else 4

        ttk.Label(main_frame, text="Detalles de la Falla:", font=("Arial", 9, "bold")).grid(
            row=row, column=0, sticky="ne", padx=(10, 5), pady=(5,0)
        )
        self.detalles_falla_text = tk.Text(main_frame, height=4, width=40, font=("Arial", 9), wrap="word")
        self.detalles_falla_text.grid(row=row, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, text="Daños Colaterales:", font=("Arial", 9, "bold")).grid(
            row=row+1, column=0, sticky="ne", padx=(10, 5), pady=(5,0)
        )
        self.danos_colaterales_text = tk.Text(main_frame, height=4, width=40, font=("Arial", 9), wrap="word")
        self.danos_colaterales_text.grid(row=row+1, column=1, sticky="ew", padx=5, pady=5)

        # Sección de trabajos adicionales
        ttk.Label(main_frame, text="Trabajos Realizados:", font=("Arial", 9, "bold")).grid(
            row=row+2, column=0, sticky="ne", padx=(10, 5), pady=(10,0)
        )
        
        # Frame contenedor para búsqueda y lista de trabajos
        trabajos_container = ttk.Frame(main_frame)
        trabajos_container.grid(row=row+2, column=1, sticky="ew", padx=5, pady=5)
        
        # Frame para el buscador
        buscar_trabajos_frame = ttk.Frame(trabajos_container)
        buscar_trabajos_frame.pack(fill="x", pady=(0, 5))
        
        # Campo de búsqueda
        buscar_icon = ttk.Label(buscar_trabajos_frame, text="🔍", font=("Segoe UI Emoji", 10))
        buscar_icon.pack(side="left", padx=(0, 5))
        
        self.buscar_trabajo_var = tk.StringVar()
        self.buscar_trabajo_entry = ttk.Entry(buscar_trabajos_frame, textvariable=self.buscar_trabajo_var, 
                                               width=40, font=("Arial", 9))
        self.buscar_trabajo_entry.pack(side="left", fill="x", expand=True)
        self.buscar_trabajo_entry.insert(0, "Buscar trabajo...")
        self.buscar_trabajo_entry.config(foreground="gray")
        
        # Eventos para el placeholder y búsqueda
        self.buscar_trabajo_entry.bind("<FocusIn>", self.on_buscar_trabajo_focus_in)
        self.buscar_trabajo_entry.bind("<FocusOut>", self.on_buscar_trabajo_focus_out)
        self.buscar_trabajo_entry.bind("<KeyRelease>", self.filtrar_trabajos)
        
        # Frame con scroll para los trabajos
        trabajos_frame = ttk.Frame(trabajos_container)
        trabajos_frame.pack(fill="both", expand=True)
        
        # Canvas y scrollbar para la lista de trabajos
        canvas = tk.Canvas(trabajos_frame, height=150, width=350, highlightthickness=1, highlightbackground="gray")
        scrollbar = ttk.Scrollbar(trabajos_frame, orient="vertical", command=canvas.yview)
        self.scrollable_trabajos_frame = ttk.Frame(canvas)
        
        self.scrollable_trabajos_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_trabajos_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Guardar referencia al canvas para usarlo en el filtro
        self.trabajos_canvas = canvas
        
        # Cargar tipos de mantenimientos varios desde la BD
        from models.mantenimiento_varios_model import TipoMantenimientoVarios
        try:
            self.tipos_trabajos = TipoMantenimientoVarios.get_all()
            self.checkbuttons_trabajos = {}  # Diccionario para guardar los checkbuttons
            
            for tipo in self.tipos_trabajos:
                var = tk.BooleanVar()
                self.trabajos_vars[tipo.id] = var
                chk = ttk.Checkbutton(self.scrollable_trabajos_frame, text=tipo.nombre, variable=var)
                chk.pack(anchor="w", padx=5, pady=3)
                self.checkbuttons_trabajos[tipo.id] = chk
        except Exception as e:
            import traceback
            error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
            ttk.Label(self.scrollable_trabajos_frame, text=error_msg, foreground="red", wraplength=280).pack()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame para botones centrado
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row+3, column=0, columnspan=3, pady=20)
        
        btn_text = "Actualizar" if self.modo_edicion else "Guardar"
        self.crear_boton_estilizado(btn_frame, btn_text, self.save, "primary").pack(side="left", padx=8)
        self.crear_boton_estilizado(btn_frame, "Cancelar", self.frame.master.destroy, "secondary").pack(side="left", padx=8)

        # Cargar datos si es edición
        if self.modo_edicion:
            self.cargar_datos()

        # Cargar datos si es edición
        if self.modo_edicion:
            self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos del mantenimiento para edición"""
        from models.mantenimiento_model import MantenimientoCorrectivo
        from models.mantenimiento_varios_model import MantenimientoVarios
        from services.db_service import DatabaseService
        
        mantenimiento = MantenimientoCorrectivo.get_by_id(self.mantenimiento_id)
        if mantenimiento:
            self.fecha_entry.delete(0, 'end')
            self.fecha_entry.insert(0, mantenimiento.fecha_mantenimiento.strftime("%Y-%m-%d"))
            self.kilometraje_entry.delete(0, 'end')
            self.kilometraje_entry.insert(0, str(mantenimiento.kilometraje))
            self.mecanico_combo.set(mantenimiento.mecanico)
            self.observaciones_text.delete(0, 'end')
            self.observaciones_text.insert(0, mantenimiento.observaciones or '')
            
            self.detalles_falla_text.delete("1.0", "end")
            self.detalles_falla_text.insert("1.0", mantenimiento.detalles_falla or '')
            self.danos_colaterales_text.delete("1.0", "end")
            self.danos_colaterales_text.insert("1.0", mantenimiento.danos_colaterales or '')
            
            # Cargar trabajos adicionales seleccionados
            db = DatabaseService()
            query = "SELECT tipo_mantenimiento_varios_id FROM mantenimiento_varios WHERE mantenimiento_id = %s"
            trabajos_seleccionados = db.execute_query(query, (self.mantenimiento_id,))
            for trabajo in trabajos_seleccionados:
                tipo_id = trabajo['tipo_mantenimiento_varios_id']
                if tipo_id in self.trabajos_vars:
                    self.trabajos_vars[tipo_id].set(True)

    def save(self):
        try:
            data = self.get_common_data()
            
            if self.modo_edicion:
                self.controller.update_mantenimiento_correctivo(
                    id=self.mantenimiento_id,
                    **data,
                    detalles_falla=self.detalles_falla_text.get("1.0", "end-1c"),
                    danos_colaterales=self.danos_colaterales_text.get("1.0", "end-1c")
                )
                
                # Actualizar trabajos adicionales: eliminar los existentes y agregar los nuevos
                from models.mantenimiento_varios_model import MantenimientoVarios
                from services.db_service import DatabaseService
                db = DatabaseService()
                # Eliminar trabajos existentes
                delete_query = "DELETE FROM mantenimiento_varios WHERE mantenimiento_id = %s"
                db.execute_query(delete_query, (self.mantenimiento_id,))
                
                # Agregar trabajos seleccionados
                for tipo_id, var in self.trabajos_vars.items():
                    if var.get():
                        mv = MantenimientoVarios(mantenimiento_id=self.mantenimiento_id, tipo_mantenimiento_varios_id=tipo_id)
                        mv.save()
                
                self.show_info("Mantenimiento correctivo actualizado exitosamente")
            else:
                mantenimiento_id = self.controller.create_mantenimiento_correctivo(
                    **data,
                    detalles_falla=self.detalles_falla_text.get("1.0", "end-1c"),
                    danos_colaterales=self.danos_colaterales_text.get("1.0", "end-1c")
                )
                
                # Guardar trabajos adicionales seleccionados
                from models.mantenimiento_varios_model import MantenimientoVarios
                for tipo_id, var in self.trabajos_vars.items():
                    if var.get():
                        mv = MantenimientoVarios(mantenimiento_id=mantenimiento_id, tipo_mantenimiento_varios_id=tipo_id)
                        mv.save()
                
                self.show_info("Mantenimiento correctivo registrado exitosamente")
            
            try:
                self.frame.winfo_toplevel().event_generate('<<HistorialActualizado>>', when='tail')
            except Exception:
                pass
            self.frame.master.destroy()
        except Exception as e:
            self.show_error(f"Error al guardar: {str(e)}")