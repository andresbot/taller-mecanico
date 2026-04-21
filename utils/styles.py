"""
Estilos premium para el Sistema de Gestión de Taller Mecánico
Paleta: Acero oscuro + Naranja llama + Blanco puro
"""
from tkinter import ttk


class AppStyles:
    """Estilos visuales premium para toda la aplicación"""

    COLORS = {
        # Sidebar / estructura
        'dark':        '#0D1117',   # Negro carbón profundo
        'dark_mid':    '#161B22',   # Fondo sidebar items
        'dark_hover':  '#21262D',   # Hover en sidebar
        'primary':     '#1C2333',   # Azul-gris oscuro (sidebar activo)

        # Acento y CTA
        'accent':      '#F77F00',   # Naranja llama principal
        'accent_dark': '#CC6800',   # Naranja hover
        'accent_glow': '#FF9F2E',   # Naranja highlight

        # Semánticos
        'success':     '#2EA043',   # Verde GitHub
        'success_bg':  '#0D2A16',   # Verde fondo oscuro
        'warning':     '#D29922',   # Ámbar
        'warning_bg':  '#2A1F0A',
        'danger':      '#DA3633',   # Rojo
        'danger_bg':   '#2A0D0D',
        'info':        '#388BFD',   # Azul brillante
        'info_bg':     '#0A1929',

        # Fondos de contenido
        'bg_main':     '#F0F2F5',   # Gris plateado muy suave
        'bg_frame':    '#FFFFFF',   # Blanco puro para cards
        'bg_row_alt':  '#F8F9FB',   # Filas alternadas tabla
        'header_bg':   '#FFFFFF',   # Topbar

        # Texto
        'text':        '#1A1D21',   # Texto principal oscuro
        'text_light':  '#6B7280',   # Texto secundario gris medio
        'text_muted':  '#9CA3AF',   # Texto muy suave
        'text_white':  '#FFFFFF',
        'text_sidebar':'#CDD5E0',   # Texto en sidebar

        # Bordes
        'border':      '#E2E6EA',   # Borde suave
        'border_dark': '#30363D',   # Borde en dark areas

        # Utilidades
        'white':       '#FFFFFF',
        'highlight':   '#F77F00',
    }

    # ── Sidebar button active highlight color ──────────────────────────────
    SIDEBAR_ACTIVE_BG  = '#F77F00'
    SIDEBAR_ACTIVE_FG  = '#FFFFFF'
    SIDEBAR_NORMAL_BG  = '#161B22'
    SIDEBAR_NORMAL_FG  = '#CDD5E0'
    SIDEBAR_HOVER_BG   = '#21262D'

    @staticmethod
    def configure_styles(root):
        style = ttk.Style(root)

        try:
            style.theme_use('clam')
        except Exception:
            pass

        C = AppStyles.COLORS
        base_font    = ('Segoe UI', 10)
        bold_font    = ('Segoe UI', 10, 'bold')
        small_font   = ('Segoe UI', 9)
        heading_font = ('Segoe UI', 13, 'bold')
        hero_font    = ('Segoe UI', 22, 'bold')

        # ── Base ────────────────────────────────────────────────────────────
        style.configure('.',
            font=base_font,
            background=C['bg_main'],
            foreground=C['text'],
            borderwidth=0,
            focuscolor=C['accent'],
            relief='flat',
        )

        # ── Frames ──────────────────────────────────────────────────────────
        style.configure('Main.TFrame',    background=C['bg_main'])
        style.configure('Surface.TFrame', background=C['bg_frame'])
        style.configure('Header.TFrame',  background=C['header_bg'])
        style.configure('Dark.TFrame',    background=C['dark'])
        style.configure('Card.TFrame',    background=C['bg_frame'],
                        relief='solid', borderwidth=1)

        # ── Labels ──────────────────────────────────────────────────────────
        style.configure('TLabel',
            background=C['bg_frame'],
            foreground=C['text'],
            font=base_font,
            padding=(2, 1),
        )
        style.configure('Main.TLabel',
            background=C['bg_main'],
            foreground=C['text'],
            font=base_font,
        )
        style.configure('HeroTitle.TLabel',
            background=C['bg_main'],
            foreground=C['text'],
            font=hero_font,
        )
        style.configure('Subtitle.TLabel',
            background=C['bg_main'],
            foreground=C['text_light'],
            font=('Segoe UI', 11),
        )
        style.configure('HeaderTitle.TLabel',
            background=C['header_bg'],
            foreground=C['text'],
            font=heading_font,
        )
        style.configure('HeaderMuted.TLabel',
            background=C['header_bg'],
            foreground=C['text_light'],
            font=small_font,
        )
        style.configure('Muted.TLabel',
            background=C['bg_frame'],
            foreground=C['text_muted'],
            font=small_font,
        )
        # Badge labels
        style.configure('Success.TLabel',
            background=C['success_bg'],
            foreground=C['success'],
            font=small_font,
            padding=(6, 2),
        )
        style.configure('Danger.TLabel',
            background=C['danger_bg'],
            foreground=C['danger'],
            font=small_font,
            padding=(6, 2),
        )
        style.configure('Warning.TLabel',
            background=C['warning_bg'],
            foreground=C['warning'],
            font=small_font,
            padding=(6, 2),
        )
        style.configure('Info.TLabel',
            background=C['info_bg'],
            foreground=C['info'],
            font=small_font,
            padding=(6, 2),
        )

        # ── LabelFrames ─────────────────────────────────────────────────────
        style.configure('TLabelframe',
            background=C['bg_frame'],
            borderwidth=1,
            relief='solid',
            bordercolor=C['border'],
            padding=10,
        )
        style.configure('TLabelframe.Label',
            background=C['bg_frame'],
            foreground=C['text'],
            font=bold_font,
        )

        # ── Inputs ──────────────────────────────────────────────────────────
        style.configure('TEntry',
            fieldbackground=C['white'],
            foreground=C['text'],
            borderwidth=1,
            relief='solid',
            padding=(8, 7),
            font=base_font,
        )
        style.map('TEntry',
            fieldbackground=[('focus', C['white'])],
            bordercolor=[('focus', C['accent'])],
        )

        style.configure('TCombobox',
            fieldbackground=C['white'],
            background=C['white'],
            foreground=C['text'],
            borderwidth=1,
            relief='solid',
            padding=(6, 5),
            font=base_font,
        )
        style.map('TCombobox',
            fieldbackground=[('readonly', C['white']), ('focus', C['white'])],
            bordercolor=[('focus', C['accent'])],
        )

        style.configure('TSpinbox',
            fieldbackground=C['white'],
            foreground=C['text'],
            borderwidth=1,
            relief='solid',
            padding=(6, 5),
            font=base_font,
        )

        # ── Buttons ─────────────────────────────────────────────────────────
        def _btn(name, bg, fg, hover_bg, press_bg):
            style.configure(f'{name}.TButton',
                background=bg,
                foreground=fg,
                borderwidth=0,
                relief='flat',
                font=bold_font,
                padding=(14, 8),
                anchor='center',
            )
            style.map(f'{name}.TButton',
                background=[('active', hover_bg), ('pressed', press_bg)],
                foreground=[('active', fg), ('pressed', fg)],
                relief=[('pressed', 'flat')],
            )

        _btn('Primary', C['accent'],   C['white'], C['accent_dark'], '#A35500')
        _btn('Success', C['success'],  C['white'], '#238636', '#1A6B29')
        _btn('Danger',  C['danger'],   C['white'], '#B91C1C', '#991B1B')
        _btn('Warning', C['warning'],  C['white'], '#B07D10', '#8E630B')
        _btn('Info',    C['info'],     C['white'], '#1D6FD6', '#1557B0')
        _btn('Secondary', '#374151',   C['white'], '#4B5563', '#374151')

        style.configure('Ghost.TButton',
            background='transparent',
            foreground=C['text_light'],
            borderwidth=1,
            relief='solid',
            font=base_font,
            padding=(10, 6),
        )
        style.map('Ghost.TButton',
            background=[('active', C['bg_main'])],
            foreground=[('active', C['text'])],
        )

        # ── Treeview (tablas) ────────────────────────────────────────────────
        style.configure('Treeview',
            background=C['white'],
            foreground=C['text'],
            fieldbackground=C['white'],
            borderwidth=0,
            relief='flat',
            font=base_font,
            rowheight=34,
        )
        style.configure('Treeview.Heading',
            background=C['bg_main'],
            foreground=C['text_light'],
            borderwidth=0,
            relief='flat',
            font=('Segoe UI', 9, 'bold'),
        )
        style.map('Treeview.Heading',
            background=[('active', C['border'])],
            relief=[('active', 'flat')],
        )
        style.map('Treeview',
            background=[('selected', C['accent'])],
            foreground=[('selected', C['white'])],
        )

        # ── Notebook ─────────────────────────────────────────────────────────
        style.configure('TNotebook',
            background=C['bg_main'],
            borderwidth=0,
            tabmargins=0,
        )
        style.configure('TNotebook.Tab',
            background=C['header_bg'],
            foreground=C['text_light'],
            padding=(18, 10),
            font=base_font,
            borderwidth=0,
        )
        style.map('TNotebook.Tab',
            background=[('selected', C['bg_main'])],
            foreground=[('selected', C['accent'])],
            expand=[('selected', [0, 0, 0, 0])],
        )

        # ── Scrollbars ────────────────────────────────────────────────────────
        style.configure('TScrollbar',
            background=C['bg_main'],
            troughcolor=C['bg_main'],
            borderwidth=0,
            arrowsize=14,
            relief='flat',
        )
        style.map('TScrollbar',
            background=[('active', C['border'])],
        )

        # ── Separator ────────────────────────────────────────────────────────
        style.configure('TSeparator',
            background=C['border'],
        )

        # ── Progressbar ──────────────────────────────────────────────────────
        style.configure('TProgressbar',
            background=C['accent'],
            troughcolor=C['bg_main'],
            borderwidth=0,
            thickness=6,
        )

        return style

    @staticmethod
    def get_color(name):
        return AppStyles.COLORS.get(name, '#000000')

    # ── Helper para crear metric cards con barra de acento izquierda ─────────
    @staticmethod
    def create_metric_card(parent, column, accent_color, title,
                           value_var, subtitle=None, subtitle_var=None):
        """
        Card de métrica con barra lateral de color, número grande y subtítulo.
        Devuelve el frame card para customización adicional.
        """
        import tkinter as tk
        C = AppStyles.COLORS

        card = tk.Frame(parent,
                        bg=C['white'],
                        bd=0,
                        highlightbackground=C['border'],
                        highlightthickness=1)
        card.grid(row=0, column=column, padx=6, pady=6, sticky='nsew')

        # Barra de acento izquierda
        bar = tk.Frame(card, bg=accent_color, width=5)
        bar.pack(side='left', fill='y')

        # Contenido
        body = tk.Frame(card, bg=C['white'])
        body.pack(side='left', fill='both', expand=True, padx=12, pady=12)

        tk.Label(body,
                 text=title.upper(),
                 bg=C['white'],
                 fg=C['text_muted'],
                 font=('Segoe UI', 8, 'bold'),
                 anchor='w').pack(fill='x')

        tk.Label(body,
                 textvariable=value_var,
                 bg=C['white'],
                 fg=accent_color,
                 font=('Segoe UI', 26, 'bold'),
                 anchor='w').pack(fill='x')

        if subtitle_var is not None:
            tk.Label(body,
                     textvariable=subtitle_var,
                     bg=C['white'],
                     fg=C['text_light'],
                     font=('Segoe UI', 9),
                     anchor='w').pack(fill='x')
        elif subtitle:
            tk.Label(body,
                     text=subtitle,
                     bg=C['white'],
                     fg=C['text_light'],
                     font=('Segoe UI', 9),
                     anchor='w').pack(fill='x')

        return card