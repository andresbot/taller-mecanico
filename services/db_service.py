import os
import shutil
import sqlite3
import sys
from datetime import datetime


class DatabaseServiceError(Exception):
    pass

class DatabaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance._initialized = False
        return cls._instance

    def _get_data_dir(self):
        # Permite sobreescribir ruta para pruebas o modo portable.
        custom_dir = os.getenv("TM_DATA_DIR")
        if custom_dir:
            return custom_dir

        if os.name == "nt":
            base_dir = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA")
            if not base_dir:
                base_dir = os.path.expanduser("~")
            return os.path.join(base_dir, "TallerMecanico", "data")

        return os.path.join(os.path.expanduser("~"), ".local", "share", "taller-mecanico", "data")

    def _get_db_path(self):
        return os.path.join(self._get_data_dir(), "registrodb.sqlite3")

    def _get_schema_path(self):
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, "database_schema.sql")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        return os.path.join(project_root, "database_schema.sql")

    def _get_backup_dir(self):
        return os.path.join(self._get_data_dir(), "backups")

    def create_daily_backup_if_needed(self):
        db_path = self._get_db_path()
        if not os.path.exists(db_path):
            return None

        backup_dir = self._get_backup_dir()
        os.makedirs(backup_dir, exist_ok=True)

        date_str = datetime.now().strftime("%Y-%m-%d")
        backup_name = f"registrodb_{date_str}.sqlite3"
        backup_path = os.path.join(backup_dir, backup_name)

        if os.path.exists(backup_path):
            return backup_path

        # Forzamos escritura pendiente antes de copiar.
        if self.connection:
            self.connection.commit()

        shutil.copy2(db_path, backup_path)
        return backup_path

    def _initialize_database(self):
        schema_path = self._get_schema_path()
        if not os.path.exists(schema_path):
            raise DatabaseServiceError(f"No se encontro el esquema de BD: {schema_path}")

        with open(schema_path, "r", encoding="utf-8") as schema_file:
            schema_sql = schema_file.read()

        self.connection.executescript(schema_sql)
        self.connection.commit()

    def _adapt_query(self, query):
        # Mantiene compatibilidad con el codigo existente que usa placeholder %s.
        return query.replace("%s", "?")

    def connect(self):
        try:
            if self.connection is None:
                data_dir = self._get_data_dir()
                os.makedirs(data_dir, exist_ok=True)

                db_path = self._get_db_path()
                db_exists = os.path.exists(db_path)
                self.connection = sqlite3.connect(db_path)
                self.connection.row_factory = sqlite3.Row
                self.connection.execute("PRAGMA foreign_keys = ON")

                if not self._initialized:
                    self._initialize_database()
                    self._initialized = True

                if db_exists:
                    self.create_daily_backup_if_needed()

            return self.connection
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def execute_query(self, query, params=None):
        statement = query.strip().split()[0].lower() if query and query.strip() else ""
        try:
            connection = self.connect()
            cursor = connection.cursor()
            parsed_query = self._adapt_query(query)

            if params:
                cursor.execute(parsed_query, params)
            else:
                cursor.execute(parsed_query)

            if statement == 'select':
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]
            else:
                connection.commit()
                result = cursor.lastrowid

            cursor.close()
            return result

        except sqlite3.Error as e:
            if self.connection:
                self.connection.rollback()
            print(f"Error executing query: {e}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self._initialized = False