import tkinter as tk
from views.main_window import MainWindow
from services.db_service import DatabaseService

def _apply_dpi_scaling():
    """Ajusta el escalado de Tk al DPI real de la pantalla para evitar pérdida de calidad."""
    root = tk.Tk()
    root.withdraw()
    dpi = root.winfo_fpixels('1i')
    root.destroy()
    return dpi / 72.0

if __name__ == "__main__":
    scaling = _apply_dpi_scaling()

    import tkinter as _tk
    _scale = scaling

    _original_init = _tk.Tk.__init__
    def _patched_init(self, *args, **kwargs):
        _original_init(self, *args, **kwargs)
        self.tk.call('tk', 'scaling', _scale)
    _tk.Tk.__init__ = _patched_init

    DatabaseService().connect()
    app = MainWindow()
    app.run()