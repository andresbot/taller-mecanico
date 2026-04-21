import tkinter as tk
from tkinter import ttk
from datetime import datetime
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
from controllers.cliente_controller import ClienteController
from controllers.vehiculo_controller import VehiculoController
from controllers.mantenimiento_controller import MantenimientoController
from tkinter import messagebox
from utils.styles import AppStyles

class MainWindow:
    def __init__(self):
        self.cliente_controller = ClienteController()
        self.vehiculo_controller = VehiculoController()
        self.mantenimiento_controller = MantenimientoController()
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Mantenimiento Vehicular")
        # Tamaño base de la app
        self.root.geometry("1200x800")
        # Aplicar estilos personalizados
        self.style = AppStyles.configure_styles(self.root)
        # Configurar color de fondo de la ventana principal
        self.root.configure(bg=AppStyles.get_color('bg_main'))
        self.sidebar_buttons = {}
        self.current_section = None
        # Centrar ventana principal
        self._center_window(self.root)
        self.setup_ui()

    def setup_ui(self):
        shell = tk.Frame(self.root, bg=AppStyles.get_color('bg_main'))
        shell.pack(fill='both', expand=True)

        self.sidebar = tk.Frame(shell, bg=AppStyles.get_color('dark'), width=220)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)

        self.content_shell = tk.Frame(shell, bg=AppStyles.get_color('bg_main'))
        self.content_shell.pack(side='left', fill='both', expand=True)

        self._build_sidebar()
        self._build_content_topbar(self.content_shell)

        # Crear notebook para pestañas
        # Oculta pestañas para manejar navegación desde sidebar
        self.style.layout('Hidden.TNotebook.Tab', [])
        self.notebook = ttk.Notebook(self.content_shell, style='Hidden.TNotebook')
        self.notebook.pack(expand=True, fill='both', padx=12, pady=(0, 10))

        # Pestaña Dashboard
        self.setup_dashboard_tab()

        # Pestaña de Clientes
        self.clientes_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.clientes_frame, text='Clientes')
        self.cliente_view = ClienteView(self.clientes_frame)
        self.cliente_view.frame.pack(expand=True, fill='both')

        # Pestaña de Vehículos
        self.vehiculos_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.vehiculos_frame, text='Vehículos')
        self.vehiculo_view = VehiculoView(self.vehiculos_frame)
        self.vehiculo_view.frame.pack(expand=True, fill='both')

        # Pestaña de Mantenimientos
        self.setup_mantenimientos_tab()

        # Pestaña de Reportes
        self.reportes_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.reportes_frame, text='Reportes')
        self.reporte_view = ReporteView(self.reportes_frame)
        self.reporte_view.frame.pack(expand=True, fill='both')

        # Pestaña de Precios
        self.precios_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.precios_frame, text='Precios')
        self.precio_view = PrecioView(self.precios_frame)
        self.precio_view.frame.pack(expand=True, fill='both')

        # Refrescar historial automáticamente al cambiar a la pestaña de Reportes
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)
        self.refresh_dashboard()
        self._select_section('dashboard')

    def _build_sidebar(self):
        brand_wrap = tk.Frame(self.sidebar, bg=AppStyles.get_color('primary'), height=86)
        brand_wrap.pack(fill='x')
        brand_wrap.pack_propagate(False)

        tk.Label(
            brand_wrap,
            text='FleetControl',
            bg=AppStyles.get_color('primary'),
            fg='white',
            font=('Segoe UI', 16, 'bold')
        ).pack(anchor='w', padx=16, pady=(14, 0))
        tk.Label(
            brand_wrap,
            text='GESTION INDUSTRIAL',
            bg=AppStyles.get_color('primary'),
            fg='#93A4BF',
            font=('Segoe UI', 8, 'bold')
        ).pack(anchor='w', padx=16)

        nav_wrap = tk.Frame(self.sidebar, bg=AppStyles.get_color('dark'))
        nav_wrap.pack(fill='x', pady=8)

        items = [
            ('dashboard', 'Dashboard', '[DB]'),
            ('clientes', 'Clientes', '[CL]'),
            ('vehiculos', 'Vehiculos', '[VH]'),
            ('mantenimientos', 'Ordenes de Servicio', '[OS]'),
            ('reportes', 'Reportes', '[RP]'),
            ('precios', 'Precios', '$'),
        ]

        for key, label, icon in items:
            self._build_sidebar_button(nav_wrap, key, f'{icon}  {label}')

        footer = tk.Frame(self.sidebar, bg=AppStyles.get_color('primary'))
        footer.pack(side='bottom', fill='x')
        tk.Label(
            footer,
            text='Admin Taller',
            bg=AppStyles.get_color('primary'),
            fg='white',
            font=('Segoe UI', 10, 'bold')
        ).pack(anchor='w', padx=16, pady=(12, 0))
        tk.Label(
            footer,
            text='Jefe de Operaciones',
            bg=AppStyles.get_color('primary'),
            fg='#93A4BF',
            font=('Segoe UI', 8)
        ).pack(anchor='w', padx=16, pady=(0, 12))

    def _build_sidebar_button(self, parent, key, text):
        btn = tk.Button(
            parent,
            text=text,
            anchor='w',
            relief='flat',
            bd=0,
            highlightthickness=0,
            padx=16,
            pady=12,
            bg=AppStyles.get_color('dark'),
            fg='#C7D2E5',
            activebackground=AppStyles.get_color('dark_hover'),
            activeforeground='white',
            font=('Segoe UI', 10),
            command=lambda k=key: self._select_section(k)
        )
        btn.pack(fill='x')
        self.sidebar_buttons[key] = btn

    def _build_content_topbar(self, parent):
        topbar = ttk.Frame(parent, style='Header.TFrame', padding=(14, 10))
        topbar.pack(fill='x', padx=12, pady=(10, 8))

        self.section_title_var = tk.StringVar(value='Dashboard Operativo')
        ttk.Label(topbar, textvariable=self.section_title_var, style='HeaderTitle.TLabel').pack(side='left')

        right = ttk.Frame(topbar, style='Header.TFrame')
        right.pack(side='right')

        self.global_search_var = tk.StringVar()
        self.global_search_var.trace('w', self._on_topbar_search)
        search_entry = ttk.Entry(right, textvariable=self.global_search_var, width=34)
        search_entry.pack(side='left', padx=(0, 10))

        self.top_action_btn = ttk.Button(right, text='Nueva Orden', style='Primary.TButton', command=self._go_to_mantenimientos)
        self.top_action_btn.pack(side='left')

    def _select_section(self, section):
        section_map = {
            'dashboard': self.dashboard_frame,
            'clientes': self.clientes_frame,
            'vehiculos': self.vehiculos_frame,
            'mantenimientos': self.mantenimientos_frame,
            'reportes': self.reportes_frame,
            'precios': self.precios_frame,
        }
        target = section_map.get(section)
        if not target:
            return

        self.notebook.select(target)
        self.current_section = section

        for key, btn in self.sidebar_buttons.items():
            is_active = key == section
            btn.configure(
                bg=AppStyles.get_color('primary') if is_active else AppStyles.get_color('dark'),
                fg='white' if is_active else '#C7D2E5'
            )

        self._update_topbar_by_section(section)

    def _update_topbar_by_section(self, section):
        labels = {
            'dashboard':      ('Dashboard Operativo',     'Nueva Orden',         self._go_to_mantenimientos),
            'clientes':       ('Gestion de Clientes',     'Nuevo Cliente',        self._accion_nuevo_cliente),
            'vehiculos':      ('Inventario de Vehiculos', 'Registrar Vehiculo',   self._accion_nuevo_vehiculo),
            'mantenimientos': ('Ordenes de Servicio',     'Crear Orden',          self._go_to_mantenimientos),
            'reportes':       ('Reportes Analiticos',     'Exportar Excel',       self._exportar_reporte_desde_topbar),
            'precios':        ('Gestion de Precios',      'Ver Precios',          lambda: self._select_section('precios')),
        }

        title, btn_text, command = labels.get(section, labels['dashboard'])
        self.section_title_var.set(title)
        self.top_action_btn.configure(text=btn_text, command=command)
        self.global_search_var.set('')

    def _accion_nuevo_cliente(self):
        self._select_section('clientes')
        if hasattr(self, 'cliente_view'):
            self.cliente_view.clear_fields()

    def _accion_nuevo_vehiculo(self):
        self._select_section('vehiculos')
        if hasattr(self, 'vehiculo_view'):
            self.vehiculo_view.clear_fields()

    def _on_topbar_search(self, *args):
        query = self.global_search_var.get()
        if self.current_section == 'clientes' and hasattr(self, 'cliente_view'):
            self.cliente_view.busqueda_var.set(query)
            self.cliente_view.buscar_clientes()
        elif self.current_section == 'vehiculos' and hasattr(self, 'vehiculo_view'):
            self.vehiculo_view.busqueda_var.set(query)
            self.vehiculo_view.buscar_vehiculos()

    def _exportar_reporte_desde_topbar(self):
        self._select_section('reportes')
        try:
            self.reporte_view.exportar_excel()
        except Exception:
            pass

    def setup_dashboard_tab(self):
        self.dashboard_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.dashboard_frame, text='Dashboard')

        self.dashboard_total_clientes = tk.StringVar(value='0')
        self.dashboard_total_vehiculos = tk.StringVar(value='0')
        self.dashboard_total_servicios = tk.StringVar(value='0')
        self.dashboard_hoy = tk.StringVar(value='0')
        self.dashboard_subtitle_vehiculos = tk.StringVar(value='Flota activa registrada')
        self.dashboard_subtitle_servicios = tk.StringVar(value='Mantenimientos historicos')
        self.dashboard_subtitle_hoy = tk.StringVar(value='Servicios completados hoy')

        hero = ttk.Frame(self.dashboard_frame, style='Main.TFrame')
        hero.pack(fill='x', padx=14, pady=(14, 8))

        ttk.Label(hero, text='Operations Dashboard', style='HeroTitle.TLabel').pack(anchor='w')
        ttk.Label(
            hero,
            text='Estado general del taller y actividad reciente en tiempo real.',
            style='Subtitle.TLabel'
        ).pack(anchor='w', pady=(2, 12))
        ttk.Button(
            hero,
            text='Nuevo mantenimiento',
            style='Primary.TButton',
            command=self._go_to_mantenimientos
        ).pack(anchor='w')

        cards_wrap = ttk.Frame(self.dashboard_frame, style='Main.TFrame')
        cards_wrap.pack(fill='x', padx=14, pady=8)
        cards_wrap.grid_columnconfigure(0, weight=1)
        cards_wrap.grid_columnconfigure(1, weight=1)
        cards_wrap.grid_columnconfigure(2, weight=1)
        cards_wrap.grid_columnconfigure(3, weight=1)

        self._create_metric_card(
            cards_wrap,
            column=0,
            accent=AppStyles.get_color('primary'),
            title='Clientes',
            value_var=self.dashboard_total_clientes,
            subtitle='Directorio total de clientes'
        )
        self._create_metric_card(
            cards_wrap,
            column=1,
            accent=AppStyles.get_color('accent'),
            title='Vehiculos',
            value_var=self.dashboard_total_vehiculos,
            subtitle_var=self.dashboard_subtitle_vehiculos
        )
        self._create_metric_card(
            cards_wrap,
            column=2,
            accent=AppStyles.get_color('info'),
            title='Servicios',
            value_var=self.dashboard_total_servicios,
            subtitle_var=self.dashboard_subtitle_servicios
        )
        self._create_metric_card(
            cards_wrap,
            column=3,
            accent=AppStyles.get_color('success'),
            title='Completados Hoy',
            value_var=self.dashboard_hoy,
            subtitle_var=self.dashboard_subtitle_hoy
        )

        table_card = ttk.LabelFrame(self.dashboard_frame, text='Actividad Reciente', padding=10)
        table_card.pack(fill='both', expand=True, padx=14, pady=(8, 14))

        table_wrap = ttk.Frame(table_card)
        table_wrap.pack(fill='both', expand=True)
        table_wrap.grid_columnconfigure(0, weight=1)
        table_wrap.grid_rowconfigure(0, weight=1)

        self.dashboard_tree = ttk.Treeview(
            table_wrap,
            columns=('Vehiculo', 'Servicio', 'Fecha', 'Mecanico'),
            show='headings',
            height=12
        )
        self.dashboard_tree.heading('Vehiculo', text='Vehiculo')
        self.dashboard_tree.heading('Servicio', text='Tipo Servicio')
        self.dashboard_tree.heading('Fecha', text='Fecha')
        self.dashboard_tree.heading('Mecanico', text='Mecanico')

        self.dashboard_tree.column('Vehiculo', width=180, anchor='center')
        self.dashboard_tree.column('Servicio', width=220, anchor='center')
        self.dashboard_tree.column('Fecha', width=120, anchor='center')
        self.dashboard_tree.column('Mecanico', width=200, anchor='center')

        tree_sb = ttk.Scrollbar(table_wrap, orient='vertical', command=self.dashboard_tree.yview)
        self.dashboard_tree.configure(yscrollcommand=tree_sb.set)
        self.dashboard_tree.grid(row=0, column=0, sticky='nsew')
        tree_sb.grid(row=0, column=1, sticky='ns')

    def _create_metric_card(self, parent, column, accent, title, value_var, subtitle=None, subtitle_var=None):
        card = tk.Frame(parent, bg=AppStyles.get_color('white'), bd=1, relief='solid', highlightthickness=0)
        card.grid(row=0, column=column, padx=6, pady=6, sticky='nsew')

        accent_bar = tk.Frame(card, bg=accent, width=6)
        accent_bar.pack(side='left', fill='y')

        content = tk.Frame(card, bg=AppStyles.get_color('white'))
        content.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        tk.Label(
            content,
            text=title.upper(),
            bg=AppStyles.get_color('white'),
            fg=AppStyles.get_color('text_light'),
            font=('Segoe UI', 9, 'bold')
        ).pack(anchor='w')

        tk.Label(
            content,
            textvariable=value_var,
            bg=AppStyles.get_color('white'),
            fg=AppStyles.get_color('primary'),
            font=('Segoe UI', 24, 'bold')
        ).pack(anchor='w')

        if subtitle_var is not None:
            tk.Label(
                content,
                textvariable=subtitle_var,
                bg=AppStyles.get_color('white'),
                fg=AppStyles.get_color('text_light'),
                font=('Segoe UI', 9)
            ).pack(anchor='w')
        elif subtitle:
            tk.Label(
                content,
                text=subtitle,
                bg=AppStyles.get_color('white'),
                fg=AppStyles.get_color('text_light'),
                font=('Segoe UI', 9)
            ).pack(anchor='w')

    def _go_to_mantenimientos(self):
        if hasattr(self, 'mantenimientos_frame'):
            self._select_section('mantenimientos')

    def refresh_dashboard(self):
        try:
            clientes = self.cliente_controller.get_all()
            vehiculos = self.vehiculo_controller.get_all()
            mantenimientos = self.mantenimiento_controller.get_all()

            hoy = datetime.now().date()
            completados_hoy = sum(
                1 for m in mantenimientos
                if getattr(m, 'fecha_mantenimiento', None)
                and m.fecha_mantenimiento.date() == hoy
            )

            tipo_correctivo = sum(
                1 for m in mantenimientos
                if getattr(m, 'tipo_mantenimiento', '') == 'correctivo'
            )

            self.dashboard_total_clientes.set(str(len(clientes)))
            self.dashboard_total_vehiculos.set(str(len(vehiculos)))
            self.dashboard_total_servicios.set(str(len(mantenimientos)))
            self.dashboard_hoy.set(str(completados_hoy))

            self.dashboard_subtitle_vehiculos.set('Flota activa registrada')
            self.dashboard_subtitle_servicios.set(f'Correctivos acumulados: {tipo_correctivo}')
            self.dashboard_subtitle_hoy.set('Servicios completados hoy')

            self._render_recent_activity(mantenimientos, vehiculos)
        except Exception:
            if hasattr(self, 'dashboard_tree'):
                for it in self.dashboard_tree.get_children():
                    self.dashboard_tree.delete(it)

    def _render_recent_activity(self, mantenimientos, vehiculos):
        for it in self.dashboard_tree.get_children():
            self.dashboard_tree.delete(it)

        vehiculos_map = {getattr(v, 'id', None): f"{v.placa}" for v in vehiculos}
        historial = sorted(
            mantenimientos,
            key=lambda m: getattr(m, 'fecha_mantenimiento', datetime.min),
            reverse=True
        )

        tipo_label = {
            'cambio_aceite': 'Oil Change',
            'frenos': 'Brake Service',
            'general': 'General Maintenance',
            'correctivo': 'Corrective Repair'
        }

        for m in historial[:12]:
            vehiculo_id = getattr(m, 'vehiculo_id', None)
            placa = vehiculos_map.get(vehiculo_id, str(vehiculo_id) if vehiculo_id else 'N/A')
            fecha = getattr(m, 'fecha_mantenimiento', None)
            fecha_txt = fecha.strftime('%Y-%m-%d') if fecha else ''
            tipo = tipo_label.get(getattr(m, 'tipo_mantenimiento', ''), getattr(m, 'tipo_mantenimiento', 'N/A'))
            mecanico = getattr(m, 'mecanico', '')
            self.dashboard_tree.insert('', 'end', values=(placa, tipo, fecha_txt, mecanico))

    def setup_mantenimientos_tab(self):
        mant_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.mantenimientos_frame = mant_frame
        self.notebook.add(mant_frame, text='Mantenimientos')

        mant_frame.grid_columnconfigure(0, weight=1)
        mant_frame.grid_rowconfigure(0, weight=1)

        container = ttk.Frame(mant_frame, style='Main.TFrame')
        container.grid(row=0, column=0, padx=14, pady=12, sticky='nsew')
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)

        # ── Hero ────────────────────────────────────────────────────────────
        hero = ttk.Frame(container, style='Main.TFrame')
        hero.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(hero, text='Ordenes de Servicio', style='HeroTitle.TLabel').pack(anchor='w')
        ttk.Label(
            hero,
            text='Crea ordenes de mantenimiento y administra los tipos de servicio disponibles.',
            style='Subtitle.TLabel'
        ).pack(anchor='w')

        # ── KPIs ────────────────────────────────────────────────────────────
        self.mant_kpi_total_var   = tk.StringVar(value='0')
        self.mant_kpi_aceite_var  = tk.StringVar(value='0')
        self.mant_kpi_correct_var = tk.StringVar(value='0')
        self.mant_kpi_mes_var     = tk.StringVar(value='0')

        kpi_row = ttk.Frame(container, style='Main.TFrame')
        kpi_row.grid(row=1, column=0, sticky='ew', pady=(2, 10))
        for col in range(4):
            kpi_row.grid_columnconfigure(col, weight=1)

        self._create_metric_card(kpi_row, 0, AppStyles.get_color('accent'),  'Total Ordenes',     self.mant_kpi_total_var,   'Historial completo')
        self._create_metric_card(kpi_row, 1, AppStyles.get_color('info'),    'Cambios de Aceite', self.mant_kpi_aceite_var,  'Preventivos registrados')
        self._create_metric_card(kpi_row, 2, AppStyles.get_color('danger'),  'Correctivos',       self.mant_kpi_correct_var, 'Reparaciones')
        self._create_metric_card(kpi_row, 3, AppStyles.get_color('success'), 'Este Mes',          self.mant_kpi_mes_var,     'Ordenes del mes actual')

        # ── Body: dos columnas ──────────────────────────────────────────────
        body = ttk.Frame(container, style='Main.TFrame')
        body.grid(row=2, column=0, sticky='nsew')
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        # ── Izquierda: Nueva Orden ──────────────────────────────────────────
        order_frame = ttk.LabelFrame(body, text='Nueva Orden de Servicio', padding=16)
        order_frame.grid(row=0, column=0, padx=(0, 8), sticky='nsew')
        order_frame.columnconfigure(1, weight=1)

        ttk.Label(order_frame, text='Tipo de Mantenimiento:').grid(
            row=0, column=0, sticky='w', padx=(0, 8), pady=6)

        tipos_mant = [
            'Cambio de Aceite',
            'Mantenimiento de Frenos',
            'Mantenimiento General',
            'Mantenimiento Correctivo',
        ]
        self.tipo_mant_var = tk.StringVar()
        tipo_combo = ttk.Combobox(
            order_frame, textvariable=self.tipo_mant_var,
            values=tipos_mant, state='readonly'
        )
        tipo_combo.grid(row=0, column=1, padx=0, pady=6, sticky='ew')
        tipo_combo.bind('<<ComboboxSelected>>', self._on_tipo_mant_selected)

        self.tipo_desc_var = tk.StringVar(value='Seleccione un tipo de mantenimiento para continuar.')
        ttk.Label(
            order_frame, textvariable=self.tipo_desc_var,
            style='Muted.TLabel', wraplength=320, justify='left'
        ).grid(row=1, column=0, columnspan=2, sticky='w', pady=(4, 18))

        ttk.Button(
            order_frame, text='Crear Nueva Orden',
            command=self.crear_mantenimiento, style='Primary.TButton'
        ).grid(row=2, column=0, columnspan=2, ipady=8, sticky='ew')

        # ── Derecha: Tipos Varios ───────────────────────────────────────────
        varios_frame = ttk.LabelFrame(body, text='Tipos de Mantenimiento Varios', padding=14)
        varios_frame.grid(row=0, column=1, padx=(8, 0), sticky='nsew')
        varios_frame.columnconfigure(0, weight=1)
        varios_frame.grid_rowconfigure(1, weight=1)

        add_row = ttk.Frame(varios_frame)
        add_row.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 10))
        add_row.columnconfigure(0, weight=1)

        self.nuevo_tipo_var = tk.StringVar()
        nuevo_entry = ttk.Entry(add_row, textvariable=self.nuevo_tipo_var)
        nuevo_entry.grid(row=0, column=0, padx=(0, 8), sticky='ew')
        nuevo_entry.bind('<KeyRelease>', lambda e: self.nuevo_tipo_var.set(self.nuevo_tipo_var.get().upper()))
        ttk.Button(add_row, text='Agregar', command=self.agregar_tipo_varios, style='Success.TButton').grid(row=0, column=1)

        self.tipos_tree = ttk.Treeview(varios_frame, columns=('Nombre',), show='headings', height=10)
        self.tipos_tree.heading('Nombre', text='Tipo de Mantenimiento')
        self.tipos_tree.column('Nombre', anchor='w')
        self.tipos_tree.grid(row=1, column=0, sticky='nsew')

        sb = ttk.Scrollbar(varios_frame, orient='vertical', command=self.tipos_tree.yview)
        self.tipos_tree.configure(yscrollcommand=sb.set)
        sb.grid(row=1, column=1, sticky='ns')

        ttk.Button(
            varios_frame, text='Eliminar seleccionado',
            command=self.eliminar_tipo_vario, style='Danger.TButton'
        ).grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky='w')

        self.cargar_tipos_varios()
        self._refresh_mant_kpis()

    def _on_tipo_mant_selected(self, event=None):
        descs = {
            'Cambio de Aceite':         'Cambio de aceite, filtros y lubricantes del motor.',
            'Mantenimiento de Frenos':  'Inspeccion de pastillas, discos, liquido de frenos y campanas.',
            'Mantenimiento General':    'Revision de luces, frenos, correa de accesorios y sistemas generales.',
            'Mantenimiento Correctivo': 'Diagnostico y reparacion de fallas especificas del vehiculo.',
        }
        self.tipo_desc_var.set(descs.get(self.tipo_mant_var.get(), ''))

    def _refresh_mant_kpis(self):
        try:
            mantenimientos = self.mantenimiento_controller.get_all()
            hoy = datetime.now()
            self.mant_kpi_total_var.set(str(len(mantenimientos)))
            self.mant_kpi_aceite_var.set(str(sum(
                1 for m in mantenimientos if getattr(m, 'tipo_mantenimiento', '') == 'cambio_aceite'
            )))
            self.mant_kpi_correct_var.set(str(sum(
                1 for m in mantenimientos if getattr(m, 'tipo_mantenimiento', '') == 'correctivo'
            )))
            self.mant_kpi_mes_var.set(str(sum(
                1 for m in mantenimientos
                if getattr(m, 'fecha_mantenimiento', None)
                and m.fecha_mantenimiento.month == hoy.month
                and m.fecha_mantenimiento.year == hoy.year
            )))
        except Exception:
            pass

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
            elif tab_text == 'Dashboard':
                self.refresh_dashboard()
            elif tab_text == 'Clientes':
                self.current_section = 'clientes'
            elif tab_text == 'Vehículos':
                self.current_section = 'vehiculos'
            elif tab_text == 'Mantenimientos':
                self.current_section = 'mantenimientos'
                self._refresh_mant_kpis()
            elif tab_text == 'Reportes':
                self.current_section = 'reportes'
            elif tab_text == 'Precios':
                self.current_section = 'precios'
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