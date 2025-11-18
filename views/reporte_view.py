import tkinter as tk
from tkinter import ttk, filedialog
from views.base_view import BaseView
from controllers.mantenimiento_controller import MantenimientoController
from controllers.vehiculo_controller import VehiculoController
import pandas as pd
from datetime import datetime
from services.db_service import DatabaseService

class ReporteView(BaseView):
    def __init__(self, master=None):
        self.mantenimiento_controller = MantenimientoController()
        self.vehiculo_controller = VehiculoController()
        super().__init__(master)

    def setup_ui(self):
        # Variables de búsqueda
        self.busqueda_var = tk.StringVar()
        self.criterio_busqueda_var = tk.StringVar(value="Tipo")
        
        # Contenedor centrado
        self.frame.grid_columnconfigure(0, weight=1)
        container = ttk.Frame(self.frame)
        container.grid(row=0, column=0, padx=10, pady=10)

        # Frame principal
        main_frame = ttk.LabelFrame(container, text="Reportes", padding=10)
        main_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Selector de vehículo
        ttk.Label(main_frame, text="Vehículo:").grid(row=0, column=0, sticky="w")
        self.vehiculo_combo = ttk.Combobox(main_frame, state="readonly", width=40)
        self.vehiculo_combo.grid(row=0, column=1, padx=5, pady=2)
        self.vehiculo_combo.bind('<<ComboboxSelected>>', lambda e: self.ver_historial())
        self.cargar_vehiculos()

        # Checkbox para todos los vehículos
        self.todos_var = tk.BooleanVar(value=False)
        self.todos_check = ttk.Checkbutton(
            main_frame, text="Todos los vehículos", variable=self.todos_var,
            command=self._toggle_todos
        )
        self.todos_check.grid(row=0, column=2, padx=10, sticky="w")

        # Fecha del reporte (día actual)
        self.fecha_label = ttk.Label(main_frame, text=f"Fecha de reporte: {datetime.now().strftime('%Y-%m-%d')}")
        self.fecha_label.grid(row=0, column=3, padx=10, sticky="e")

        # Botones de reportes
        ttk.Button(main_frame, text="Ver Historial", 
                  command=self.ver_historial, style='Primary.TButton').grid(row=1, column=0, pady=10, padx=5)
        
        ttk.Button(main_frame, text="Editar Mantenimiento", 
                  command=self.editar_mantenimiento, style='Info.TButton').grid(row=1, column=1, pady=10, padx=5)
        
        ttk.Button(main_frame, text="Eliminar Mantenimiento", 
                  command=self.eliminar_mantenimiento, style='Danger.TButton').grid(row=1, column=2, pady=10, padx=5)
        
        ttk.Button(main_frame, text="Exportar a Excel", 
                  command=self.exportar_excel, style='Success.TButton').grid(row=1, column=3, pady=10, padx=5)

        # Frame de búsqueda/consulta
        search_frame = ttk.LabelFrame(main_frame, text="Consultar Mantenimientos", padding=12)
        search_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        
        ttk.Label(search_frame, text="Buscar por:").grid(row=0, column=0, sticky="w", padx=5)
        criterio_combo = ttk.Combobox(search_frame, textvariable=self.criterio_busqueda_var, 
                                      values=["Tipo", "Mecánico", "Fecha", "Placa"], state="readonly", width=12)
        criterio_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(search_frame, text="Texto:").grid(row=0, column=2, sticky="w", padx=5)
        busqueda_entry = ttk.Entry(search_frame, textvariable=self.busqueda_var, width=25)
        busqueda_entry.grid(row=0, column=3, padx=5)
        busqueda_entry.bind('<KeyRelease>', lambda e: self.buscar_mantenimientos())
        
        ttk.Button(search_frame, text="Buscar", command=self.buscar_mantenimientos, style='Primary.TButton').grid(row=0, column=4, padx=5)
        ttk.Button(search_frame, text="Limpiar Búsqueda", command=self.limpiar_busqueda, style='Secondary.TButton').grid(row=0, column=5, padx=5)

        # Tabla de historial
        self.setup_tabla_historial(main_frame)

        # Escuchar evento global cuando se guarde un mantenimiento
        try:
            self.frame.winfo_toplevel().bind('<<HistorialActualizado>>', lambda e: self.refresh())
        except Exception:
            pass

    def setup_tabla_historial(self, parent):
        # Frame para la tabla
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky="nsew")

        # Crear Treeview con columna ID oculta
        self.tree = ttk.Treeview(table_frame, columns=(
            "ID", "Vehículo", "Fecha", "Tipo", "Kilometraje", "Mecánico", "Observaciones"
        ), show="headings", height=12)

        # Configurar columnas (ID oculta)
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.column("ID", width=0, stretch=False)  # Oculta pero accesible
        self.tree.heading("Vehículo", text="Vehículo", anchor="center")
        self.tree.heading("Fecha", text="Fecha", anchor="center")
        self.tree.heading("Tipo", text="Tipo de Mantenimiento", anchor="center")
        self.tree.heading("Kilometraje", text="Kilometraje", anchor="center")
        self.tree.heading("Mecánico", text="Mecánico", anchor="center")
        self.tree.heading("Observaciones", text="Observaciones", anchor="center")

        # Ajustar anchos de columna y centrar el contenido
        self.tree.column("Vehículo", width=180, anchor="center")
        self.tree.column("Fecha", width=100, anchor="center")
        self.tree.column("Tipo", width=180, anchor="center")
        self.tree.column("Kilometraje", width=100, anchor="center")
        self.tree.column("Mecánico", width=150, anchor="center")
        self.tree.column("Observaciones", width=300, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def cargar_vehiculos(self):
        vehiculos = self.vehiculo_controller.get_all()
        self.vehiculos_data = {
            f"{v.placa} - {v.marca} {v.modelo}": v.id for v in vehiculos
        }
        sel = self.vehiculo_combo.get()
        self.vehiculo_combo['values'] = list(self.vehiculos_data.keys())
        # mantener selección si sigue existiendo
        if sel in self.vehiculo_combo['values']:
            self.vehiculo_combo.set(sel)

    def ver_historial(self):
        try:
            vehiculo_seleccionado = self.vehiculo_combo.get()
            if not self.todos_var.get() and not vehiculo_seleccionado:
                self.show_warning("Debe seleccionar un vehículo o marcar 'Todos los vehículos'")
                return

            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Obtener historial (uno o todos)
            registros = []
            if self.todos_var.get():
                # Obtener todos los mantenimientos y anotar el vehículo
                historial = self.mantenimiento_controller.get_all()
                for m in historial:
                    try:
                        v = self.vehiculo_controller.get_by_id(m.vehiculo_id)
                        vehiculo_txt = f"{v.placa} - {v.marca} {v.modelo}" if v else str(m.vehiculo_id)
                    except Exception:
                        vehiculo_txt = str(m.vehiculo_id)
                    registros.append((vehiculo_txt, m))
            else:
                vehiculo_id = self.vehiculos_data[vehiculo_seleccionado]
                historial = self.mantenimiento_controller.get_historial_completo(vehiculo_id)
                vehiculo_txt = vehiculo_seleccionado
                registros = [(vehiculo_txt, m) for m in historial]

            # Mostrar datos
            for vehiculo_txt, m in registros:
                self.tree.insert("", "end", values=(
                    m.id,  # ID oculto pero accesible
                    vehiculo_txt,
                    m.fecha_mantenimiento.strftime("%Y-%m-%d") if hasattr(m, 'fecha_mantenimiento') and m.fecha_mantenimiento else "",
                    m.tipo_mantenimiento if hasattr(m, 'tipo_mantenimiento') else "",
                    m.kilometraje if hasattr(m, 'kilometraje') else "",
                    m.mecanico if hasattr(m, 'mecanico') else "",
                    m.observaciones if hasattr(m, 'observaciones') else "",
                ))

        except Exception as e:
            self.show_error(f"Error al cargar historial: {str(e)}")

    def refresh(self):
        """Recarga vehículos y, si hay vehículo seleccionado, actualiza historial."""
        try:
            self.cargar_vehiculos()
            if self.todos_var.get() or self.vehiculo_combo.get():
                self.ver_historial()
        except Exception as e:
            self.show_error(f"Error al refrescar: {e}")

    def editar_mantenimiento(self):
        """Abre la ventana de edición del mantenimiento seleccionado"""
        try:
            # Verificar que haya una selección
            selected = self.tree.selection()
            if not selected:
                self.show_warning("Debe seleccionar un mantenimiento para editar")
                return
            
            # Obtener datos del mantenimiento seleccionado
            values = self.tree.item(selected[0])["values"]
            mantenimiento_id = values[0]  # ID está en la primera columna (oculta)
            tipo_mantenimiento = values[3]  # Tipo está en la columna 3
            
            # Obtener el mantenimiento completo para saber el vehiculo_id
            mantenimiento = self.mantenimiento_controller.get_by_id(mantenimiento_id)
            if not mantenimiento:
                self.show_error("No se pudo cargar el mantenimiento")
                return
            
            # Abrir ventana de edición según el tipo
            ventana_edicion = tk.Toplevel(self.frame)
            ventana_edicion.title("Editar Mantenimiento")
            
            from views.mantenimiento_view import (
                CambioAceiteView, 
                MantenimientoFrenosView, 
                MantenimientoGeneralView, 
                MantenimientoCorrectivoView
            )
            
            if tipo_mantenimiento == 'cambio_aceite':
                vista = CambioAceiteView(
                    master=ventana_edicion, 
                    vehiculo_id=mantenimiento.vehiculo_id,
                    mantenimiento_id=mantenimiento_id
                )
            elif tipo_mantenimiento == 'frenos':
                vista = MantenimientoFrenosView(
                    master=ventana_edicion, 
                    vehiculo_id=mantenimiento.vehiculo_id,
                    mantenimiento_id=mantenimiento_id
                )
            elif tipo_mantenimiento == 'general':
                vista = MantenimientoGeneralView(
                    master=ventana_edicion, 
                    vehiculo_id=mantenimiento.vehiculo_id,
                    mantenimiento_id=mantenimiento_id
                )
            elif tipo_mantenimiento == 'correctivo':
                vista = MantenimientoCorrectivoView(
                    master=ventana_edicion, 
                    vehiculo_id=mantenimiento.vehiculo_id,
                    mantenimiento_id=mantenimiento_id
                )
            else:
                self.show_error(f"Tipo de mantenimiento '{tipo_mantenimiento}' no soportado")
                ventana_edicion.destroy()
                return
            
            # ¡Importante! Empaquetar el frame para que se muestre
            vista.frame.pack(expand=True, fill='both', padx=15, pady=10)
            
        except Exception as e:
            import traceback
            self.show_error(f"Error al abrir edición: {str(e)}\n{traceback.format_exc()}")

    def eliminar_mantenimiento(self):
        """Elimina el mantenimiento seleccionado después de confirmar"""
        try:
            # Verificar que haya una selección
            selected = self.tree.selection()
            if not selected:
                self.show_warning("Debe seleccionar un mantenimiento para eliminar")
                return
            
            # Obtener datos del mantenimiento seleccionado
            values = self.tree.item(selected[0])["values"]
            mantenimiento_id = values[0]  # ID está en la primera columna (oculta)
            vehiculo_txt = values[1]
            fecha = values[2]
            tipo = values[3]
            
            # Confirmar eliminación
            mensaje = f"¿Está seguro de eliminar este mantenimiento?\n\n"
            mensaje += f"Vehículo: {vehiculo_txt}\n"
            mensaje += f"Fecha: {fecha}\n"
            mensaje += f"Tipo: {tipo}\n\n"
            mensaje += "Esta acción no se puede deshacer."
            
            if not self.show_question(mensaje):
                return
            
            # Eliminar el mantenimiento
            self.mantenimiento_controller.delete(mantenimiento_id)
            
            # Actualizar la vista
            self.show_info("Mantenimiento eliminado exitosamente")
            self.ver_historial()
            
            # Notificar al sistema
            try:
                self.frame.winfo_toplevel().event_generate('<<HistorialActualizado>>', when='tail')
            except Exception:
                pass
            
        except Exception as e:
            import traceback
            self.show_error(f"Error al eliminar mantenimiento: {str(e)}\n{traceback.format_exc()}")

    def exportar_excel(self):
        try:
            vehiculo_seleccionado = self.vehiculo_combo.get()
            if not self.todos_var.get() and not vehiculo_seleccionado:
                self.show_warning("Debe seleccionar un vehículo o marcar 'Todos los vehículos'")
                return

            # Solicitar ubicación para guardar
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Guardar reporte"
            )

            if not filename:
                return

            # Crear Excel
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Resumen con fecha del reporte
                resumen = pd.DataFrame([{
                    'Fecha de reporte': datetime.now().strftime('%Y-%m-%d'),
                    'Modo': 'Todos los vehículos' if self.todos_var.get() else 'Por vehículo'
                }])
                resumen.to_excel(writer, sheet_name='Resumen', index=False)
                if self.todos_var.get():
                    # Todos los vehículos: una sola hoja con todo
                    historial = self.mantenimiento_controller.get_all()
                    rows = []
                    for m in historial:
                        try:
                            v = self.vehiculo_controller.get_by_id(m.vehiculo_id)
                            vehiculo_txt = f"{v.placa} - {v.marca} {v.modelo}" if v else str(m.vehiculo_id)
                            cliente_txt = f"{v.cliente.nombre} ({v.cliente.cedula})" if v and v.cliente else ''
                            cliente_tel = f"{v.cliente.telefono}" if v and v.cliente else ''
                        except Exception:
                            v = None
                            vehiculo_txt = str(m.vehiculo_id)
                            cliente_txt = ''
                            cliente_tel = ''
                        detalles = self._get_detalles(m)
                        rows.append({
                            'Vehículo': vehiculo_txt,
                            'Placa': getattr(v, 'placa', '') if v else '',
                            'Marca': getattr(v, 'marca', '') if v else '',
                            'Modelo': getattr(v, 'modelo', '') if v else '',
                            'Cliente': cliente_txt,
                            'Cliente Teléfono': cliente_tel,
                            'Fecha': getattr(m, 'fecha_mantenimiento', None),
                            'Tipo': getattr(m, 'tipo_mantenimiento', ''),
                            'Kilometraje': getattr(m, 'kilometraje', ''),
                            'Mecánico': getattr(m, 'mecanico', ''),
                            'Observaciones': getattr(m, 'observaciones', ''),
                            # Detalles por tipo (columnas fijas)
                            'Filtro Aceite': detalles.get('filtro_aceite', ''),
                            'Filtro Aire': detalles.get('filtro_aire', ''),
                            'Tipo Aceite': detalles.get('tipo_aceite', ''),
                            'Estado Pastillas': detalles.get('estado_pastillas', ''),
                            'Estado Discos': detalles.get('estado_discos', ''),
                            'Estado Líquido': detalles.get('estado_liquido', ''),
                            'Estado Campanas': detalles.get('estado_campanas', ''),
                            'Fecha Última Correa': detalles.get('fecha_ultima_correa', ''),
                            'Estado Luces': detalles.get('estado_luces', ''),
                            'Estado Frenos': detalles.get('estado_frenos', ''),
                            'Estado Correa Accesorios': detalles.get('estado_correa_accesorios', ''),
                            'Detalles Falla': detalles.get('detalles_falla', ''),
                            'Daños Colaterales': detalles.get('danos_colaterales', ''),
                            'Trabajos Adicionales': detalles.get('trabajos_adicionales', ''),
                        })
                    df = pd.DataFrame(rows)
                    df.to_excel(writer, sheet_name='Historial Global', index=False)
                else:
                    vehiculo_id = self.vehiculos_data[vehiculo_seleccionado]
                    historial = self.mantenimiento_controller.get_historial_completo(vehiculo_id)
                    vehiculo = self.vehiculo_controller.get_by_id(vehiculo_id)

                    # Información del vehículo
                    info_vehiculo = pd.DataFrame([{
                        'Placa': vehiculo.placa,
                        'Marca': vehiculo.marca,
                        'Modelo': vehiculo.modelo,
                        'Cliente': f"{vehiculo.cliente.nombre} ({vehiculo.cliente.cedula})",
                        'Cliente Teléfono': getattr(vehiculo.cliente, 'telefono', '')
                    }])
                    info_vehiculo.to_excel(writer, sheet_name='Info Vehículo', index=False)

                    # Historial de mantenimientos
                    data = []
                    for m in historial:
                        detalles = self._get_detalles(m)
                        data.append({
                            'Fecha': m.fecha_mantenimiento,
                            'Tipo de Mantenimiento': m.tipo_mantenimiento,
                            'Kilometraje': m.kilometraje,
                            'Mecánico': m.mecanico,
                            'Observaciones': m.observaciones,
                            # Detalles por tipo (columnas fijas)
                            'Filtro Aceite': detalles.get('filtro_aceite', ''),
                            'Filtro Aire': detalles.get('filtro_aire', ''),
                            'Tipo Aceite': detalles.get('tipo_aceite', ''),
                            'Estado Pastillas': detalles.get('estado_pastillas', ''),
                            'Estado Discos': detalles.get('estado_discos', ''),
                            'Estado Líquido': detalles.get('estado_liquido', ''),
                            'Estado Campanas': detalles.get('estado_campanas', ''),
                            'Fecha Última Correa': detalles.get('fecha_ultima_correa', ''),
                            'Estado Luces': detalles.get('estado_luces', ''),
                            'Estado Frenos': detalles.get('estado_frenos', ''),
                            'Estado Correa Accesorios': detalles.get('estado_correa_accesorios', ''),
                            'Detalles Falla': detalles.get('detalles_falla', ''),
                            'Daños Colaterales': detalles.get('danos_colaterales', ''),
                            'Trabajos Adicionales': detalles.get('trabajos_adicionales', ''),
                        })
                    df = pd.DataFrame(data)
                    df.to_excel(writer, sheet_name='Historial', index=False)

            self.show_info("Reporte exportado exitosamente")

        except Exception as e:
            self.show_error(f"Error al exportar: {str(e)}")

    def imprimir_reporte(self):
        """Genera un documento HTML imprimible del historial de mantenimiento"""
        try:
            vehiculo_seleccionado = self.vehiculo_combo.get()
            if not vehiculo_seleccionado:
                self.show_warning("Debe seleccionar un vehículo")
                return

            # Verificar que el vehículo existe en el diccionario
            if vehiculo_seleccionado not in self.vehiculos_data:
                self.show_warning("Por favor, seleccione un vehículo válido de la lista")
                self.cargar_vehiculos()
                return

            # Obtener datos del vehículo y su historial
            vehiculo_id = self.vehiculos_data[vehiculo_seleccionado]
            historial = self.mantenimiento_controller.get_historial_completo(vehiculo_id)
            vehiculo = self.vehiculo_controller.get_by_id(vehiculo_id)

            if not vehiculo:
                self.show_error("No se pudo obtener la información del vehículo")
                return

            if not historial:
                self.show_warning("No hay mantenimientos registrados para este vehículo")
                return

            # Solicitar ubicación para guardar
            filename = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
                title="Guardar reporte para imprimir"
            )

            if not filename:
                return

            # Generar HTML
            html_content = self._generar_html_reporte(vehiculo, historial)

            # Guardar archivo
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)

            self.show_info("Reporte generado exitosamente. Puede abrirlo con su navegador e imprimirlo.")
            
            # Preguntar si desea abrir el archivo
            if self.show_question("¿Desea abrir el reporte ahora?"):
                import os
                import webbrowser
                webbrowser.open('file://' + os.path.realpath(filename))

        except Exception as e:
            self.show_error(f"Error al generar reporte: {str(e)}")

    def _generar_html_reporte(self, vehiculo, historial):
        """Genera el contenido HTML del reporte"""
        fecha_reporte = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        # Obtener datos del cliente de forma segura
        cliente_nombre = getattr(vehiculo.cliente, 'nombre', 'N/A') if hasattr(vehiculo, 'cliente') and vehiculo.cliente else 'N/A'
        cliente_cedula = getattr(vehiculo.cliente, 'cedula', 'N/A') if hasattr(vehiculo, 'cliente') and vehiculo.cliente else 'N/A'
        cliente_telefono = getattr(vehiculo.cliente, 'telefono', 'N/A') if hasattr(vehiculo, 'cliente') and vehiculo.cliente else 'N/A'
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Historial de Mantenimiento - {vehiculo.placa}</title>
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
            margin-bottom: 30px;
            border-bottom: 3px solid #2C3E50;
            padding-bottom: 20px;
        }}
        .header h1 {{
            color: #2C3E50;
            margin-bottom: 5px;
        }}
        .header p {{
            color: #7F8C8D;
            margin: 5px 0;
        }}
        .info-vehiculo {{
            background-color: #ECF0F1;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .info-vehiculo h2 {{
            color: #2C3E50;
            margin-top: 0;
            border-bottom: 2px solid #3498DB;
            padding-bottom: 10px;
        }}
        .info-row {{
            display: flex;
            margin: 10px 0;
        }}
        .info-label {{
            font-weight: bold;
            width: 150px;
            color: #2C3E50;
        }}
        .info-value {{
            color: #555;
        }}
        .mantenimiento {{
            border: 1px solid #BDC3C7;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            page-break-inside: avoid;
        }}
        .mantenimiento-header {{
            background-color: #3498DB;
            color: white;
            padding: 12px;
            border-radius: 5px;
            margin: -20px -20px 15px -20px;
        }}
        .mantenimiento-header h3 {{
            margin: 0;
            font-size: 18px;
        }}
        .mantenimiento-tipo {{
            display: inline-block;
            background-color: rgba(255,255,255,0.2);
            padding: 3px 10px;
            border-radius: 3px;
            margin-left: 10px;
            font-size: 14px;
        }}
        .detalle-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 15px;
        }}
        .detalle-item {{
            padding: 10px;
            background-color: #F8F9FA;
            border-left: 3px solid #3498DB;
        }}
        .detalle-label {{
            font-weight: bold;
            color: #2C3E50;
            font-size: 13px;
        }}
        .detalle-value {{
            color: #555;
            margin-top: 5px;
        }}
        .observaciones {{
            background-color: #FFF3CD;
            border-left: 4px solid #FFC107;
            padding: 15px;
            margin-top: 15px;
            border-radius: 4px;
        }}
        .observaciones-label {{
            font-weight: bold;
            color: #856404;
            margin-bottom: 5px;
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
        <button class="btn-print" onclick="window.print()">🖨️ Imprimir Reporte</button>
    </div>

    <div class="header">
        <h1>Historial de Mantenimiento</h1>
        <p>Fecha de Reporte: {fecha_reporte}</p>
    </div>

    <div class="info-vehiculo">
        <h2>Información del Vehículo</h2>
        <div class="info-row">
            <span class="info-label">Placa:</span>
            <span class="info-value">{vehiculo.placa}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Marca:</span>
            <span class="info-value">{vehiculo.marca}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Modelo:</span>
            <span class="info-value">{vehiculo.modelo}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Kilometraje Actual:</span>
            <span class="info-value">{getattr(vehiculo, 'kilometraje', 'N/A')} km</span>
        </div>
        <div class="info-row">
            <span class="info-label">Cliente:</span>
            <span class="info-value">{cliente_nombre} ({cliente_cedula})</span>
        </div>
        <div class="info-row">
            <span class="info-label">Teléfono:</span>
            <span class="info-value">{cliente_telefono}</span>
        </div>
    </div>

    <h2 style="color: #2C3E50; border-bottom: 2px solid #3498DB; padding-bottom: 10px;">
        Registro de Mantenimientos ({len(historial)})
    </h2>
"""

        # Agregar cada mantenimiento
        for m in historial:
            tipo_nombre = {
                'cambio_aceite': 'Cambio de Aceite',
                'frenos': 'Mantenimiento de Frenos',
                'general': 'Mantenimiento General',
                'correctivo': 'Mantenimiento Correctivo'
            }.get(getattr(m, 'tipo_mantenimiento', ''), 'Desconocido')
            
            # Manejar la fecha de forma segura
            fecha_mant = getattr(m, 'fecha_mantenimiento', '')
            if hasattr(fecha_mant, 'strftime'):
                fecha_str = fecha_mant.strftime('%d/%m/%Y')
            else:
                fecha_str = str(fecha_mant)

            html += f"""
    <div class="mantenimiento">
        <div class="mantenimiento-header">
            <h3>
                📅 {fecha_str}
                <span class="mantenimiento-tipo">{tipo_nombre}</span>
            </h3>
        </div>

        <div class="detalle-grid">
            <div class="detalle-item">
                <div class="detalle-label">Kilometraje</div>
                <div class="detalle-value">{getattr(m, 'kilometraje', 'N/A')} km</div>
            </div>
            <div class="detalle-item">
                <div class="detalle-label">Mecánico</div>
                <div class="detalle-value">{getattr(m, 'mecanico', 'N/A')}</div>
            </div>
"""

            # Agregar detalles específicos según el tipo
            detalles = self._get_detalles(m)
            
            tipo_mant = getattr(m, 'tipo_mantenimiento', '')
            if tipo_mant == 'cambio_aceite':
                html += f"""
            <div class="detalle-item">
                <div class="detalle-label">Tipo de Aceite</div>
                <div class="detalle-value">{detalles.get('tipo_aceite', 'N/A')}</div>
            </div>
            <div class="detalle-item">
                <div class="detalle-label">Filtro de Aceite</div>
                <div class="detalle-value">{detalles.get('filtro_aceite', 'N/A')}</div>
            </div>
            <div class="detalle-item">
                <div class="detalle-label">Filtro de Aire</div>
                <div class="detalle-value">{detalles.get('filtro_aire', 'N/A')}</div>
            </div>
"""
            elif tipo_mant == 'frenos':
                html += f"""
            <div class="detalle-item">
                <div class="detalle-label">Estado Pastillas</div>
                <div class="detalle-value">{detalles.get('estado_pastillas', 'N/A')}</div>
            </div>
            <div class="detalle-item">
                <div class="detalle-label">Estado Discos</div>
                <div class="detalle-value">{detalles.get('estado_discos', 'N/A')}</div>
            </div>
            <div class="detalle-item">
                <div class="detalle-label">Estado Líquido</div>
                <div class="detalle-value">{detalles.get('estado_liquido', 'N/A')}</div>
            </div>
            <div class="detalle-item">
                <div class="detalle-label">Estado Campanas</div>
                <div class="detalle-value">{detalles.get('estado_campanas', 'N/A')}</div>
            </div>
"""
            elif tipo_mant == 'general':
                html += f"""
            <div class="detalle-item">
                <div class="detalle-label">Fecha Última Correa</div>
                <div class="detalle-value">{detalles.get('fecha_ultima_correa', 'N/A')}</div>
            </div>
            <div class="detalle-item">
                <div class="detalle-label">Estado Luces</div>
                <div class="detalle-value">{detalles.get('estado_luces', 'N/A')}</div>
            </div>
            <div class="detalle-item">
                <div class="detalle-label">Estado Frenos</div>
                <div class="detalle-value">{detalles.get('estado_frenos', 'N/A')}</div>
            </div>
            <div class="detalle-item">
                <div class="detalle-label">Estado Correa Accesorios</div>
                <div class="detalle-value">{detalles.get('estado_correa_accesorios', 'N/A')}</div>
            </div>
"""
            elif tipo_mant == 'correctivo':
                html += f"""
            <div class="detalle-item" style="grid-column: span 2;">
                <div class="detalle-label">Detalles de la Falla</div>
                <div class="detalle-value">{detalles.get('detalles_falla', 'N/A')}</div>
            </div>
            <div class="detalle-item" style="grid-column: span 2;">
                <div class="detalle-label">Daños Colaterales</div>
                <div class="detalle-value">{detalles.get('danos_colaterales', 'N/A')}</div>
            </div>
"""
                trabajos = detalles.get('trabajos_adicionales', '')
                if trabajos:
                    html += f"""
            <div class="detalle-item" style="grid-column: span 2;">
                <div class="detalle-label">Trabajos Adicionales Realizados</div>
                <div class="detalle-value">{trabajos}</div>
            </div>
"""

            html += """
        </div>
"""

            # Agregar observaciones si existen
            observaciones = getattr(m, 'observaciones', '')
            if observaciones:
                html += f"""
        <div class="observaciones">
            <div class="observaciones-label">📝 Observaciones:</div>
            <div>{observaciones}</div>
        </div>
"""

            html += """
    </div>
"""

        # Cerrar HTML
        html += f"""
    <div class="footer">
        <p>Reporte generado el {fecha_reporte}</p>
        <p>Sistema de Gestión de Mantenimiento de Vehículos</p>
    </div>

    <div class="no-print" style="text-align: center; margin: 30px 0;">
        <button class="btn-print" onclick="window.print()">🖨️ Imprimir Reporte</button>
    </div>
</body>
</html>
"""
        return html

    def clear_fields(self):
        self.vehiculo_combo.set('')
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _toggle_todos(self):
        """Maneja el cambio del checkbox 'Todos los vehículos'."""
        if self.todos_var.get():
            self.vehiculo_combo.configure(state="disabled")
            self.ver_historial()
        else:
            self.vehiculo_combo.configure(state="readonly")
            if self.vehiculo_combo.get():
                self.ver_historial()
            else:
                # Limpiar tabla si no hay vehículo seleccionado
                for item in self.tree.get_children():
                    self.tree.delete(item)

    def _get_detalles(self, mantenimiento):
        """Devuelve un dict con los campos de detalle según el tipo de mantenimiento."""
        try:
            db = DatabaseService()
            tipo = getattr(mantenimiento, 'tipo_mantenimiento', None)
            mid = getattr(mantenimiento, 'id', None)
            if not tipo or not mid:
                return {}
            if tipo == 'cambio_aceite':
                q = "SELECT filtro_aceite, filtro_aire, tipo_aceite FROM cambio_aceite WHERE mantenimiento_id = %s"
            elif tipo == 'frenos':
                q = "SELECT estado_pastillas, estado_discos, estado_liquido, estado_campanas FROM mantenimiento_frenos WHERE mantenimiento_id = %s"
            elif tipo == 'general':
                q = "SELECT fecha_ultima_correa, estado_luces, estado_frenos, estado_correa_accesorios FROM mantenimiento_general WHERE mantenimiento_id = %s"
            elif tipo == 'correctivo':
                q = "SELECT detalles_falla, danos_colaterales FROM mantenimiento_correctivo WHERE mantenimiento_id = %s"
            else:
                return {}
            rows = db.execute_query(q, (mid,))
            detalles = rows[0] if rows else {}
            
            # Si es correctivo, agregar los trabajos adicionales realizados
            if tipo == 'correctivo':
                q_trabajos = """
                    SELECT t.nombre 
                    FROM mantenimiento_varios mv
                    JOIN tipos_mantenimiento_varios t ON mv.tipo_mantenimiento_varios_id = t.id
                    WHERE mv.mantenimiento_id = %s
                """
                trabajos_rows = db.execute_query(q_trabajos, (mid,))
                if trabajos_rows:
                    trabajos_list = [r['nombre'] for r in trabajos_rows]
                    detalles['trabajos_adicionales'] = ', '.join(trabajos_list)
                else:
                    detalles['trabajos_adicionales'] = 'Ninguno'
            
            return detalles
        except Exception:
            return {}

    def buscar_mantenimientos(self):
        """Busca mantenimientos según el criterio seleccionado"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener criterio y texto de búsqueda
        criterio = self.criterio_busqueda_var.get()
        texto_busqueda = self.busqueda_var.get().strip().upper()

        # Si no hay texto de búsqueda, mostrar historial normal
        if not texto_busqueda:
            self.ver_historial()
            return

        # Obtener mantenimientos según el filtro de vehículo
        registros = []
        if self.todos_var.get():
            # Todos los vehículos
            historial = self.mantenimiento_controller.get_all()
            for m in historial:
                try:
                    v = self.vehiculo_controller.get_by_id(m.vehiculo_id)
                    vehiculo_txt = f"{v.placa} - {v.marca} {v.modelo}" if v else str(m.vehiculo_id)
                except Exception:
                    vehiculo_txt = str(m.vehiculo_id)
                registros.append((vehiculo_txt, m))
        else:
            vehiculo_seleccionado = self.vehiculo_combo.get()
            if not vehiculo_seleccionado:
                self.show_warning("Debe seleccionar un vehículo o marcar 'Todos los vehículos'")
                return
            vehiculo_id = self.vehiculos_data[vehiculo_seleccionado]
            historial = self.mantenimiento_controller.get_historial_completo(vehiculo_id)
            vehiculo_txt = vehiculo_seleccionado
            registros = [(vehiculo_txt, m) for m in historial]

        # Filtrar según criterio
        registros_filtrados = []
        for vehiculo_txt, m in registros:
            incluir = False
            
            if criterio == "Tipo":
                tipo = getattr(m, 'tipo_mantenimiento', '').upper()
                if texto_busqueda in tipo:
                    incluir = True
            elif criterio == "Mecánico":
                mecanico = getattr(m, 'mecanico', '').upper()
                if texto_busqueda in mecanico:
                    incluir = True
            elif criterio == "Fecha":
                fecha = getattr(m, 'fecha_mantenimiento', None)
                if fecha:
                    fecha_str = fecha.strftime("%Y-%m-%d")
                    if texto_busqueda in fecha_str:
                        incluir = True
            elif criterio == "Placa":
                if texto_busqueda in vehiculo_txt.upper():
                    incluir = True
            
            if incluir:
                registros_filtrados.append((vehiculo_txt, m))

        # Mostrar resultados
        if registros_filtrados:
            for vehiculo_txt, m in registros_filtrados:
                self.tree.insert("", "end", values=(
                    m.id,
                    vehiculo_txt,
                    m.fecha_mantenimiento.strftime("%Y-%m-%d") if hasattr(m, 'fecha_mantenimiento') and m.fecha_mantenimiento else "",
                    m.tipo_mantenimiento if hasattr(m, 'tipo_mantenimiento') else "",
                    m.kilometraje if hasattr(m, 'kilometraje') else "",
                    m.mecanico if hasattr(m, 'mecanico') else "",
                    m.observaciones if hasattr(m, 'observaciones') else "",
                ))
        else:
            self.show_info(f"No se encontraron mantenimientos con {criterio}: '{texto_busqueda}'")

    def limpiar_busqueda(self):
        """Limpia el campo de búsqueda y muestra todos los registros"""
        self.busqueda_var.set("")
        self.ver_historial()