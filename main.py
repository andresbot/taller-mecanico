from views.main_window import MainWindow
from services.db_service import DatabaseService

if __name__ == "__main__":
    # Inicializa la base local SQLite y genera respaldo diario si aplica.
    DatabaseService().connect()
    app = MainWindow()
    app.run()