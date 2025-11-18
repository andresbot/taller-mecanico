"""
Configuración de estilos y temas para la aplicación
"""
from tkinter import ttk

class AppStyles:
    """Clase para configurar y aplicar estilos personalizados a la aplicación"""
    
    # Paleta de colores profesional
    COLORS = {
        'primary': '#2C3E50',      # Azul oscuro
        'secondary': '#34495E',    # Gris azulado
        'success': '#27AE60',      # Verde
        'warning': '#F39C12',      # Naranja
        'danger': '#E74C3C',       # Rojo
        'info': '#3498DB',         # Azul claro
        'light': '#ECF0F1',        # Gris muy claro
        'dark': '#2C3E50',         # Azul muy oscuro
        'white': '#FFFFFF',
        'bg_main': '#F8F9FA',      # Fondo principal
        'bg_frame': '#FFFFFF',     # Fondo de frames
        'text': '#2C3E50',         # Texto principal
        'text_light': '#7F8C8D',   # Texto secundario
        'border': '#BDC3C7',       # Bordes
        'highlight': '#3498DB',    # Resaltado
    }
    
    @staticmethod
    def configure_styles(root):
        """Configura los estilos personalizados para toda la aplicación"""
        style = ttk.Style(root)
        
        # Intentar usar tema moderno si está disponible
        try:
            style.theme_use('clam')  # Tema más personalizable
        except:
            pass
        
        # Configurar colores generales
        style.configure('.',
            background=AppStyles.COLORS['bg_main'],
            foreground=AppStyles.COLORS['text'],
            borderwidth=0,
            focuscolor=AppStyles.COLORS['highlight']
        )
        
        # Estilo para frames principales
        style.configure('Main.TFrame',
            background=AppStyles.COLORS['bg_main']
        )
        
        # Estilo para LabelFrames
        style.configure('TLabelframe',
            background=AppStyles.COLORS['bg_frame'],
            borderwidth=2,
            relief='solid',
            bordercolor=AppStyles.COLORS['border']
        )
        
        style.configure('TLabelframe.Label',
            background=AppStyles.COLORS['bg_frame'],
            foreground=AppStyles.COLORS['primary'],
            font=('Segoe UI', 10, 'bold')
        )
        
        # Estilo para Labels
        style.configure('TLabel',
            background=AppStyles.COLORS['bg_frame'],
            foreground=AppStyles.COLORS['text'],
            font=('Segoe UI', 9)
        )
        
        # Estilo para Entry
        style.configure('TEntry',
            fieldbackground=AppStyles.COLORS['white'],
            foreground=AppStyles.COLORS['text'],
            borderwidth=1,
            relief='solid'
        )
        
        # Estilo para Combobox
        style.configure('TCombobox',
            fieldbackground=AppStyles.COLORS['white'],
            background=AppStyles.COLORS['white'],
            foreground=AppStyles.COLORS['text'],
            borderwidth=1
        )
        
        # Estilos para botones
        # Botón Success (Guardar)
        style.configure('Success.TButton',
            background=AppStyles.COLORS['success'],
            foreground=AppStyles.COLORS['white'],
            borderwidth=0,
            font=('Segoe UI', 9, 'bold'),
            padding=(15, 8)
        )
        style.map('Success.TButton',
            background=[('active', '#229954'), ('pressed', '#1E8449')],
            foreground=[('active', AppStyles.COLORS['white'])]
        )
        
        # Botón Info (Modificar/Editar)
        style.configure('Info.TButton',
            background=AppStyles.COLORS['info'],
            foreground=AppStyles.COLORS['white'],
            borderwidth=0,
            font=('Segoe UI', 9, 'bold'),
            padding=(15, 8)
        )
        style.map('Info.TButton',
            background=[('active', '#2E86C1'), ('pressed', '#2874A6')],
            foreground=[('active', AppStyles.COLORS['white'])]
        )
        
        # Botón Danger (Eliminar)
        style.configure('Danger.TButton',
            background=AppStyles.COLORS['danger'],
            foreground=AppStyles.COLORS['white'],
            borderwidth=0,
            font=('Segoe UI', 9, 'bold'),
            padding=(15, 8)
        )
        style.map('Danger.TButton',
            background=[('active', '#CB4335'), ('pressed', '#B03A2E')],
            foreground=[('active', AppStyles.COLORS['white'])]
        )
        
        # Botón Warning (Limpiar/Cancelar)
        style.configure('Warning.TButton',
            background=AppStyles.COLORS['warning'],
            foreground=AppStyles.COLORS['white'],
            borderwidth=0,
            font=('Segoe UI', 9, 'bold'),
            padding=(15, 8)
        )
        style.map('Warning.TButton',
            background=[('active', '#D68910'), ('pressed', '#CA6F1E')],
            foreground=[('active', AppStyles.COLORS['white'])]
        )
        
        # Botón Primary (General)
        style.configure('Primary.TButton',
            background=AppStyles.COLORS['primary'],
            foreground=AppStyles.COLORS['white'],
            borderwidth=0,
            font=('Segoe UI', 9, 'bold'),
            padding=(15, 8)
        )
        style.map('Primary.TButton',
            background=[('active', '#1C2833'), ('pressed', '#17202A')],
            foreground=[('active', AppStyles.COLORS['white'])]
        )
        
        # Botón Secondary (Secundario)
        style.configure('Secondary.TButton',
            background=AppStyles.COLORS['secondary'],
            foreground=AppStyles.COLORS['white'],
            borderwidth=0,
            font=('Segoe UI', 9),
            padding=(12, 6)
        )
        style.map('Secondary.TButton',
            background=[('active', '#2C3E50'), ('pressed', '#273746')],
            foreground=[('active', AppStyles.COLORS['white'])]
        )
        
        # Estilo para Treeview (tablas)
        style.configure('Treeview',
            background=AppStyles.COLORS['white'],
            foreground=AppStyles.COLORS['text'],
            fieldbackground=AppStyles.COLORS['white'],
            borderwidth=1,
            relief='solid',
            font=('Segoe UI', 9)
        )
        
        style.configure('Treeview.Heading',
            background=AppStyles.COLORS['primary'],
            foreground=AppStyles.COLORS['white'],
            borderwidth=0,
            font=('Segoe UI', 9, 'bold'),
            relief='flat'
        )
        
        style.map('Treeview.Heading',
            background=[('active', AppStyles.COLORS['secondary'])]
        )
        
        style.map('Treeview',
            background=[('selected', AppStyles.COLORS['highlight'])],
            foreground=[('selected', AppStyles.COLORS['white'])]
        )
        
        # Estilo para Notebook (pestañas)
        style.configure('TNotebook',
            background=AppStyles.COLORS['bg_main'],
            borderwidth=0
        )
        
        style.configure('TNotebook.Tab',
            background=AppStyles.COLORS['light'],
            foreground=AppStyles.COLORS['text'],
            padding=(20, 10),
            font=('Segoe UI', 10),
            borderwidth=0
        )
        
        style.map('TNotebook.Tab',
            background=[('selected', AppStyles.COLORS['primary'])],
            foreground=[('selected', AppStyles.COLORS['white'])],
            expand=[('selected', [1, 1, 1, 0])]
        )
        
        return style
    
    @staticmethod
    def get_color(color_name):
        """Obtiene un color específico de la paleta"""
        return AppStyles.COLORS.get(color_name, '#000000')
