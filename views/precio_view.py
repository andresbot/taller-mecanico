import tkinter as tk
from tkinter import ttk, filedialog
from views.base_view import BaseView
from controllers.mantenimiento_controller import MantenimientoController
from controllers.vehiculo_controller import VehiculoController
from services.db_service import DatabaseService
from datetime import datetime
import webbrowser
import os

class PrecioView(BaseView):
    def __init__(self, master=None):
        self.mantenimiento_controller = MantenimientoController()
        self.vehiculo_controller = VehiculoController()
        self.db = DatabaseService()
        super().__init__(master)

    def setup_ui(self):
        # Contenedor centrado
        self.frame.grid_columnconfigure(0, weight=1)
        container = ttk.Frame(self.frame)
        container.grid(row=0, column=0, padx=10, pady=10)

        # Frame principal
        main_frame = ttk.LabelFrame(container, text="Gestión de Precios de Mantenimientos", padding=10)
        main_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Selector de vehículo
        ttk.Label(main_frame, text="Vehículo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.vehiculo_combo = ttk.Combobox(main_frame, state="readonly", width=40)
        self.vehiculo_combo.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Botón para actualizar/refrescar
        ttk.Button(main_frame, text="🔄 Actualizar", command=self.refresh, style='Secondary.TButton').grid(row=0, column=3, padx=5, pady=5)
        
        self.cargar_vehiculos()

        # Tabla de mantenimientos
        ttk.Label(main_frame, text="Seleccione un mantenimiento:").grid(row=1, column=0, columnspan=3, sticky="w", padx=5, pady=(15, 5))
        
        # Frame para tabla de mantenimientos
        mant_frame = ttk.Frame(main_frame)
        mant_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        
        self.tree_mant = ttk.Treeview(mant_frame, columns=(
            "ID", "Fecha", "Tipo", "Kilometraje", "Mecánico"
        ), show="headings", height=6)
        
        # Configurar columnas
        self.tree_mant.heading("ID", text="ID", anchor="center")
        self.tree_mant.column("ID", width=0, stretch=False)  # Oculto
        self.tree_mant.heading("Fecha", text="Fecha", anchor="center")
        self.tree_mant.heading("Tipo", text="Tipo", anchor="center")
        self.tree_mant.heading("Kilometraje", text="Kilometraje", anchor="center")
        self.tree_mant.heading("Mecánico", text="Mecánico", anchor="center")
        
        self.tree_mant.column("Fecha", width=100, anchor="center")
        self.tree_mant.column("Tipo", width=180, anchor="center")
        self.tree_mant.column("Kilometraje", width=100, anchor="center")
        self.tree_mant.column("Mecánico", width=150, anchor="center")
        
        scrollbar_mant = ttk.Scrollbar(mant_frame, orient="vertical", command=self.tree_mant.yview)
        self.tree_mant.configure(yscrollcommand=scrollbar_mant.set)
        self.tree_mant.grid(row=0, column=0, sticky="nsew")
        scrollbar_mant.grid(row=0, column=1, sticky="ns")
        
        self.tree_mant.bind("<<TreeviewSelect>>", self.on_select_mantenimiento)

        # Frame de detalles y precios
        details_frame = ttk.LabelFrame(main_frame, text="Detalles y Precios", padding=10)
        details_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=15, sticky="nsew")

        # Variables para los campos
        self.precio_principal_var = tk.StringVar()
        self.detalles_text = None
        
        # Precio principal
        ttk.Label(details_frame, text="Precio Mantenimiento Principal:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        precio_entry = ttk.Entry(details_frame, textvariable=self.precio_principal_var, width=20)
        precio_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        precio_entry.bind('<KeyRelease>', lambda e: self.validar_precio_y_calcular())
        ttk.Label(details_frame, text="COP").grid(row=0, column=2, sticky="w", padx=5, pady=5)

        # Frame para detalles adicionales (trabajos en correctivo, repuestos, etc)
        ttk.Label(details_frame, text="Detalles Adicionales y Precios:", font=('Arial', 10, 'bold')).grid(row=1, column=0, columnspan=3, sticky="w", padx=5, pady=(15, 5))
        
        # Text widget con scrollbar para detalles adicionales
        text_frame = ttk.Frame(details_frame)
        text_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        
        self.detalles_text = tk.Text(text_frame, height=10, width=70, wrap=tk.WORD)
        scrollbar_text = ttk.Scrollbar(text_frame, orient="vertical", command=self.detalles_text.yview)
        self.detalles_text.configure(yscrollcommand=scrollbar_text.set)
        self.detalles_text.grid(row=0, column=0, sticky="nsew")
        scrollbar_text.grid(row=0, column=1, sticky="ns")
        # Evento para actualizar total en tiempo real cuando se escribe en detalles
        self.detalles_text.bind('<KeyRelease>', lambda e: self.calcular_total())

        # Instrucciones (será actualizada dinámicamente)
        self.instrucciones_label = ttk.Label(details_frame, 
                                 text="Formato: Descripción | Precio\nEjemplo: Cambio de filtro de aceite | 15.00\nNota: Para Mantenimientos Correctivos se cargarán automáticamente los trabajos realizados.",
                                 foreground="gray", wraplength=600, justify="left")
        self.instrucciones_label.grid(row=3, column=0, columnspan=3, sticky="w", padx=5, pady=5)

        # Total calculado
        ttk.Label(details_frame, text="Total:", font=('Arial', 12, 'bold')).grid(row=4, column=0, sticky="e", padx=5, pady=(15, 5))
        self.total_var = tk.StringVar(value="0.00")
        self.total_label = ttk.Label(details_frame, textvariable=self.total_var, font=('Arial', 12, 'bold'), foreground='#27AE60')
        self.total_label.grid(row=4, column=1, sticky="w", padx=5, pady=(15, 5))
        ttk.Label(details_frame, text="COP", font=('Arial', 12, 'bold')).grid(row=4, column=2, sticky="w", padx=5, pady=(15, 5))

        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=15)

        ttk.Button(button_frame, text="Calcular Total", command=self.calcular_total, style='Primary.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Guardar Precios", command=self.guardar_precios, style='Success.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Generar Factura", command=self.generar_factura, style='Warning.TButton').grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_fields, style='Secondary.TButton').grid(row=0, column=3, padx=5)

        # Escuchar evento global cuando se guarde un mantenimiento
        try:
            self.frame.winfo_toplevel().bind('<<HistorialActualizado>>', lambda e: self.refresh())
        except Exception:
            pass

        # Bind para cambio de vehículo (al final, después de crear todas las variables)
        self.vehiculo_combo.bind('<<ComboboxSelected>>', self.on_vehiculo_changed)

    def on_vehiculo_changed(self, event=None):
        """Cuando cambia el vehículo seleccionado"""
        # Limpiar campos de precio y detalles
        self.clear_fields()
        # Cargar los mantenimientos del nuevo vehículo
        self.cargar_mantenimientos()

    def refresh(self):
        """Refrescar la vista cargando los vehículos y mantenimientos nuevamente"""
        try:
            vehiculo_actual = self.vehiculo_combo.get()
            self.cargar_vehiculos()
            
            # Mantener el vehículo seleccionado si aún existe
            if vehiculo_actual and vehiculo_actual in self.vehiculos_data:
                self.vehiculo_combo.set(vehiculo_actual)
                self.cargar_mantenimientos()
        except Exception:
            pass

    def cargar_vehiculos(self):
        vehiculos = self.vehiculo_controller.get_all()
        self.vehiculos_data = {
            f"{v.placa} - {v.marca} {v.modelo}": v.id for v in vehiculos
        }
        self.vehiculo_combo['values'] = list(self.vehiculos_data.keys())

    def cargar_mantenimientos(self):
        """Cargar mantenimientos del vehículo seleccionado"""
        # Limpiar tabla
        for item in self.tree_mant.get_children():
            self.tree_mant.delete(item)
        
        vehiculo_seleccionado = self.vehiculo_combo.get()
        if not vehiculo_seleccionado:
            return
        
        try:
            vehiculo_id = self.vehiculos_data[vehiculo_seleccionado]
            historial = self.mantenimiento_controller.get_historial_completo(vehiculo_id)
            
            for m in historial:
                tipo_nombre = {
                    'cambio_aceite': 'Cambio de Aceite',
                    'frenos': 'Mantenimiento de Frenos',
                    'general': 'Mantenimiento General',
                    'correctivo': 'Mantenimiento Correctivo'
                }.get(m.tipo_mantenimiento, m.tipo_mantenimiento)
                
                fecha_str = m.fecha_mantenimiento.strftime('%Y-%m-%d') if hasattr(m.fecha_mantenimiento, 'strftime') else str(m.fecha_mantenimiento)
                
                self.tree_mant.insert("", "end", values=(
                    m.id,
                    fecha_str,
                    tipo_nombre,
                    m.kilometraje,
                    m.mecanico
                ))
        except Exception as e:
            self.show_error(f"Error al cargar mantenimientos: {str(e)}")

    def on_select_mantenimiento(self, event):
        """Cuando se selecciona un mantenimiento"""
        selected = self.tree_mant.selection()
        if not selected:
            return
        
        item = self.tree_mant.item(selected[0])
        mantenimiento_id = item['values'][0]
        tipo_mantenimiento = item['values'][2]
        
        # Cargar precios existentes si los hay
        self.cargar_precios_existentes(mantenimiento_id, tipo_mantenimiento)

    def cargar_precios_existentes(self, mantenimiento_id, tipo_mantenimiento=None):
        """Cargar los precios guardados previamente"""
        try:
            # Consultar si existen precios para este mantenimiento
            query = "SELECT precio_principal, detalles_adicionales FROM precios_mantenimiento WHERE mantenimiento_id = %s"
            result = self.db.execute_query(query, (mantenimiento_id,))
            
            if result:
                self.precio_principal_var.set(str(result[0]['precio_principal']))
                detalles = result[0]['detalles_adicionales'] or ""
                self.detalles_text.delete('1.0', tk.END)
                self.detalles_text.insert('1.0', detalles)
                self.calcular_total()
            else:
                # No hay precios guardados, limpiar campos
                self.clear_fields()
                
                # Si es mantenimiento correctivo, cargar trabajos adicionales realizados
                if tipo_mantenimiento and "Correctivo" in tipo_mantenimiento:
                    self.cargar_trabajos_correctivo(mantenimiento_id)
                    
        except Exception as e:
            self.show_error(f"Error al cargar precios: {str(e)}")

    def cargar_trabajos_correctivo(self, mantenimiento_id):
        """Cargar los trabajos adicionales realizados en un mantenimiento correctivo"""
        try:
            query = """
                SELECT t.nombre 
                FROM mantenimiento_varios mv
                JOIN tipos_mantenimiento_varios t ON mv.tipo_mantenimiento_varios_id = t.id
                WHERE mv.mantenimiento_id = %s
                ORDER BY t.nombre
            """
            trabajos = self.db.execute_query(query, (mantenimiento_id,))
            
            if trabajos:
                # Construir el texto con los trabajos y espacio para precios
                texto_trabajos = ""
                for trabajo in trabajos:
                    nombre_trabajo = trabajo['nombre']
                    texto_trabajos += f"{nombre_trabajo} | 0.00\n"
                
                # Insertar en el text widget
                self.detalles_text.delete('1.0', tk.END)
                self.detalles_text.insert('1.0', texto_trabajos.strip())
                
                # Actualizar instrucciones
                self.instrucciones_label.config(
                    text=f"✓ Mantenimiento Correctivo: Se cargaron {len(trabajos)} trabajos adicionales.\n"
                         f"Modifique los precios (reemplace 0.00 con el precio real) y agregue más líneas si es necesario.\n"
                         f"Formato: Descripción | Precio",
                    foreground="#E67E22"
                )
            else:
                self.instrucciones_label.config(
                    text="Mantenimiento Correctivo sin trabajos adicionales registrados.\n"
                         "Puede agregar detalles manualmente en formato: Descripción | Precio",
                    foreground="gray"
                )
        except Exception as e:
            self.show_error(f"Error al cargar trabajos: {str(e)}")

    def calcular_total(self):
        """Calcular el total sumando precio principal y detalles"""
        try:
            total = 0.0
            
            # Precio principal - limpiar comas si las hay
            precio_principal = self.precio_principal_var.get().strip().replace(',', '')
            if precio_principal:
                try:
                    total += float(precio_principal)
                except ValueError:
                    pass  # Ignorar si no es un número válido
            
            # Detalles adicionales
            detalles = self.detalles_text.get('1.0', tk.END).strip()
            if detalles:
                lineas = detalles.split('\n')
                for linea in lineas:
                    if '|' in linea:
                        partes = linea.split('|')
                        if len(partes) >= 2:
                            try:
                                # Limpiar comas del precio
                                precio_str = partes[1].strip().replace(',', '')
                                precio = float(precio_str)
                                total += precio
                            except ValueError:
                                pass
            
            # Formatear sin comas (formato simple con punto decimal)
            self.total_var.set(f"{total:.2f}")
        except Exception as e:
            # No mostrar error, solo mantener el valor anterior
            pass

    def guardar_precios(self):
        """Guardar los precios en la base de datos"""
        selected = self.tree_mant.selection()
        if not selected:
            self.show_warning("Por favor seleccione un mantenimiento")
            return
        
        item = self.tree_mant.item(selected[0])
        mantenimiento_id = item['values'][0]
        
        try:
            precio_principal = self.precio_principal_var.get().strip()
            if not precio_principal:
                precio_principal = "0.00"
            
            precio_principal = float(precio_principal)
            detalles_adicionales = self.detalles_text.get('1.0', tk.END).strip()
            
            # Verificar si ya existe un registro
            check_query = "SELECT id FROM precios_mantenimiento WHERE mantenimiento_id = %s"
            exists = self.db.execute_query(check_query, (mantenimiento_id,))
            
            if exists:
                # Actualizar
                update_query = """
                    UPDATE precios_mantenimiento 
                    SET precio_principal = %s, detalles_adicionales = %s, fecha_actualizacion = NOW()
                    WHERE mantenimiento_id = %s
                """
                self.db.execute_query(update_query, (precio_principal, detalles_adicionales, mantenimiento_id))
            else:
                # Insertar
                insert_query = """
                    INSERT INTO precios_mantenimiento (mantenimiento_id, precio_principal, detalles_adicionales)
                    VALUES (%s, %s, %s)
                """
                self.db.execute_query(insert_query, (mantenimiento_id, precio_principal, detalles_adicionales))
            
            self.show_info("Precios guardados exitosamente")
            self.calcular_total()
        except ValueError:
            self.show_error("El precio principal debe ser un número válido")
        except Exception as e:
            self.show_error(f"Error al guardar precios: {str(e)}")

    def generar_factura(self):
        """Generar una factura en HTML para imprimir"""
        selected = self.tree_mant.selection()
        if not selected:
            self.show_warning("Por favor seleccione un mantenimiento")
            return
        
        vehiculo_seleccionado = self.vehiculo_combo.get()
        if not vehiculo_seleccionado:
            self.show_warning("Por favor seleccione un vehículo")
            return
        
        item = self.tree_mant.item(selected[0])
        mantenimiento_id = item['values'][0]
        
        try:
            # Obtener datos
            vehiculo_id = self.vehiculos_data[vehiculo_seleccionado]
            vehiculo = self.vehiculo_controller.get_by_id(vehiculo_id)
            mantenimiento = self.mantenimiento_controller.get_by_id(mantenimiento_id)
            
            # Calcular total
            self.calcular_total()
            
            # Generar HTML
            html_content = self._generar_html_factura(vehiculo, mantenimiento, item['values'])
            
            # Guardar archivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
                title="Guardar factura",
                initialfile=f"Factura_{vehiculo.placa}_{item['values'][1]}.html"
            )
            
            if not filename:
                return
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.show_info("Factura generada exitosamente")
            
            if self.show_question("¿Desea abrir la factura ahora?"):
                webbrowser.open('file://' + os.path.realpath(filename))
                
        except Exception as e:
            self.show_error(f"Error al generar factura: {str(e)}")

    def _generar_html_factura(self, vehiculo, mantenimiento, mant_values):
        """Generar el HTML de la factura"""
        fecha_factura = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        cliente_nombre = getattr(vehiculo.cliente, 'nombre', 'N/A') if hasattr(vehiculo, 'cliente') and vehiculo.cliente else 'N/A'
        cliente_cedula = getattr(vehiculo.cliente, 'cedula', 'N/A') if hasattr(vehiculo, 'cliente') and vehiculo.cliente else 'N/A'
        cliente_telefono = getattr(vehiculo.cliente, 'telefono', 'N/A') if hasattr(vehiculo, 'cliente') and vehiculo.cliente else 'N/A'
        
        tipo_nombre = mant_values[2]
        fecha_mant = mant_values[1]
        
        precio_principal = float(self.precio_principal_var.get() or 0)
        detalles = self.detalles_text.get('1.0', tk.END).strip()
        total = float(self.total_var.get())
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Factura - {vehiculo.placa}</title>
    <style>
        @media print {{
            .no-print {{ display: none; }}
            body {{ margin: 0; }}
        }}
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            color: #333;
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #2C3E50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #2C3E50;
            margin: 0;
        }}
        .header p {{
            color: #7F8C8D;
            margin: 5px 0;
        }}
        .info-section {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .info-box {{
            background-color: #ECF0F1;
            padding: 15px;
            border-radius: 8px;
        }}
        .info-box h3 {{
            color: #2C3E50;
            margin-top: 0;
            border-bottom: 2px solid #3498DB;
            padding-bottom: 5px;
        }}
        .info-row {{
            margin: 8px 0;
        }}
        .info-label {{
            font-weight: bold;
            color: #2C3E50;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th {{
            background-color: #3498DB;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            border: 1px solid #ddd;
            padding: 10px;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .total-section {{
            background-color: #27AE60;
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: right;
            margin-top: 20px;
        }}
        .total-section h2 {{
            margin: 0;
            font-size: 28px;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            color: #7F8C8D;
            font-size: 12px;
            border-top: 1px solid #BDC3C7;
            padding-top: 20px;
        }}
        .btn-print {{
            background-color: #27AE60;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 20px 0;
        }}
        .btn-print:hover {{
            background-color: #229954;
        }}
    </style>
</head>
<body>
    <div class="no-print" style="text-align: center;">
        <button class="btn-print" onclick="window.print()">🖨️ Imprimir Factura</button>
    </div>

    <div class="header">
        <h1>FACTURA DE SERVICIO</h1>
        <p>Fecha de emisión: {fecha_factura}</p>
    </div>

    <div class="info-section">
        <div class="info-box">
            <h3>Datos del Cliente</h3>
            <div class="info-row">
                <span class="info-label">Nombre:</span> {cliente_nombre}
            </div>
            <div class="info-row">
                <span class="info-label">Cédula:</span> {cliente_cedula}
            </div>
            <div class="info-row">
                <span class="info-label">Teléfono:</span> {cliente_telefono}
            </div>
        </div>
        
        <div class="info-box">
            <h3>Datos del Vehículo</h3>
            <div class="info-row">
                <span class="info-label">Placa:</span> {vehiculo.placa}
            </div>
            <div class="info-row">
                <span class="info-label">Marca:</span> {vehiculo.marca}
            </div>
            <div class="info-row">
                <span class="info-label">Modelo:</span> {vehiculo.modelo}
            </div>
        </div>
    </div>

    <div class="info-box">
        <h3>Información del Servicio</h3>
        <div class="info-row">
            <span class="info-label">Tipo de Mantenimiento:</span> {tipo_nombre}
        </div>
        <div class="info-row">
            <span class="info-label">Fecha de Servicio:</span> {fecha_mant}
        </div>
        <div class="info-row">
            <span class="info-label">Mecánico:</span> {mant_values[4]}
        </div>
        <div class="info-row">
            <span class="info-label">Kilometraje:</span> {mant_values[3]} km
        </div>
    </div>

    <h3 style="color: #2C3E50; margin-top: 30px;">Detalle de Servicios</h3>
    <table>
        <thead>
            <tr>
                <th>Descripción</th>
                <th style="text-align: right; width: 150px;">Precio (COP)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>{tipo_nombre} - Servicio Principal</strong></td>
                <td style="text-align: right;">${precio_principal:.2f}</td>
            </tr>
"""
        
        # Agregar detalles adicionales
        if detalles:
            lineas = detalles.split('\n')
            for linea in lineas:
                if '|' in linea:
                    partes = linea.split('|')
                    if len(partes) >= 2:
                        descripcion = partes[0].strip()
                        try:
                            # Limpiar comas del precio
                            precio_str = partes[1].strip().replace(',', '')
                            precio = float(precio_str)
                            html += f"""
            <tr>
                <td>{descripcion}</td>
                <td style="text-align: right;">${precio:.2f}</td>
            </tr>
"""
                        except ValueError:
                            pass
        
        html += f"""
        </tbody>
    </table>

    <div class="total-section">
        <h2>TOTAL: ${total:.2f} COP</h2>
    </div>

    <div class="footer">
        <p>Gracias por confiar en nuestros servicios</p>
        <p>Factura generada el {fecha_factura}</p>
    </div>

    <div class="no-print" style="text-align: center; margin: 30px 0;">
        <button class="btn-print" onclick="window.print()">🖨️ Imprimir Factura</button>
    </div>
</body>
</html>
"""
        return html

    def clear_fields(self):
        """Limpiar todos los campos"""
        self.precio_principal_var.set("")
        self.detalles_text.delete('1.0', tk.END)
        self.total_var.set("0.00")
        # Restaurar instrucciones por defecto
        self.instrucciones_label.config(
            text="Formato: Descripción | Precio\nEjemplo: Cambio de filtro de aceite | 15.00\nNota: Para Mantenimientos Correctivos se cargarán automáticamente los trabajos realizados.",
            foreground="gray"
        )
    
    def validar_precio(self, variable):
        """Permite solo numeros y un punto decimal"""
        valor = variable.get()
        # Permitir solo digitos y un punto decimal
        valor_limpio = ''
        punto_encontrado = False
        for c in valor:
            if c.isdigit():
                valor_limpio += c
            elif c == '.' and not punto_encontrado:
                valor_limpio += c
                punto_encontrado = True
        if valor != valor_limpio:
            variable.set(valor_limpio)
    
    def validar_precio_y_calcular(self):
        """Valida el precio y luego calcula el total"""
        self.validar_precio(self.precio_principal_var)
        self.calcular_total()
