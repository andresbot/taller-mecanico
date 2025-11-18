from models.base_model import BaseModel
from services.db_service import DatabaseService

class TipoMantenimientoVarios(BaseModel):
    def __init__(self, nombre=None, id=None):
        super().__init__()
        self.id = id
        self.nombre = nombre.upper() if nombre else None

    def save(self):
        # Verificar si ya existe
        existente = self.get_by_nombre(self.nombre)
        if existente:
            raise ValueError(f"El mantenimiento '{self.nombre}' ya existe en el sistema")

        if self.id is None:
            query = "INSERT INTO tipos_mantenimiento_varios (nombre) VALUES (%s)"
            params = (self.nombre,)
            self.id = self.db.execute_query(query, params)
            return self.id
        return self.update()

    def update(self):
        if self.id is None:
            return None
        
        query = "UPDATE tipos_mantenimiento_varios SET nombre = %s WHERE id = %s"
        params = (self.nombre, self.id)
        self.db.execute_query(query, params)
        return self.id

    @classmethod
    def get_all(cls):
        db = DatabaseService()
        query = "SELECT * FROM tipos_mantenimiento_varios ORDER BY nombre"
        results = db.execute_query(query)
        items = []
        for result in results:
            # soportar mayúsculas/minúsculas en claves devueltas por el cursor
            _id = result.get('ID') or result.get('id')
            _nombre = result.get('nombre') or result.get('NOMBRE')
            items.append(cls(nombre=_nombre, id=_id))
        return items

    @classmethod
    def get_by_nombre(cls, nombre):
        db = DatabaseService()
        query = "SELECT * FROM tipos_mantenimiento_varios WHERE UPPER(nombre) = UPPER(%s)"
        results = db.execute_query(query, (nombre,))
        if not results:
            return None
        res = results[0]
        _id = res.get('ID') or res.get('id')
        _nombre = res.get('nombre') or res.get('NOMBRE')
        return cls(nombre=_nombre, id=_id)

    @classmethod
    def get_by_id(cls, id):
        db = DatabaseService()
        query = "SELECT * FROM tipos_mantenimiento_varios WHERE ID = %s"
        results = db.execute_query(query, (id,))
        if not results:
            return None
        res = results[0]
        _id = res.get('ID') or res.get('id')
        _nombre = res.get('nombre') or res.get('NOMBRE')
        return cls(nombre=_nombre, id=_id)

    def delete(self):
        if self.id is None:
            return False
        query = "DELETE FROM tipos_mantenimiento_varios WHERE ID = %s"
        self.db.execute_query(query, (self.id,))
        return True

class MantenimientoVarios(BaseModel):
    def __init__(self, mantenimiento_id=None, tipo_mantenimiento_varios_id=None, id=None):
        super().__init__()
        self.id = id
        self.mantenimiento_id = mantenimiento_id
        self.tipo_mantenimiento_varios_id = tipo_mantenimiento_varios_id

    def save(self):
        if self.id is None:
            query = """
                INSERT INTO mantenimiento_varios 
                (mantenimiento_id, tipo_mantenimiento_varios_id)
                VALUES (%s, %s)
            """
            params = (self.mantenimiento_id, self.tipo_mantenimiento_varios_id)
            self.id = self.db.execute_query(query, params)
            return self.id
        return self.update()

    def update(self):
        if self.id is None:
            return None
        query = "UPDATE mantenimiento_varios SET mantenimiento_id = %s, tipo_mantenimiento_varios_id = %s WHERE ID = %s"
        params = (self.mantenimiento_id, self.tipo_mantenimiento_varios_id, self.id)
        self.db.execute_query(query, params)
        return self.id

    def delete(self):
        if self.id is None:
            return False
        query = "DELETE FROM mantenimiento_varios WHERE ID = %s"
        self.db.execute_query(query, (self.id,))
        return True

    @classmethod
    def get_all(cls):
        db = DatabaseService()
        query = "SELECT * FROM mantenimiento_varios"
        results = db.execute_query(query)
        items = []
        for res in results:
            _id = res.get('ID') or res.get('id')
            mantenimiento_id = res.get('mantenimiento_id') or res.get('MANTENIMIENTO_ID')
            tipo_id = res.get('tipo_mantenimiento_varios_id') or res.get('TIPO_MANTENIMIENTO_VARIOS_ID')
            items.append(cls(mantenimiento_id=mantenimiento_id, tipo_mantenimiento_varios_id=tipo_id, id=_id))
        return items

    @classmethod
    def get_by_id(cls, id):
        db = DatabaseService()
        query = "SELECT * FROM mantenimiento_varios WHERE ID = %s"
        results = db.execute_query(query, (id,))
        if not results:
            return None
        res = results[0]
        _id = res.get('ID') or res.get('id')
        mantenimiento_id = res.get('mantenimiento_id') or res.get('MANTENIMIENTO_ID')
        tipo_id = res.get('tipo_mantenimiento_varios_id') or res.get('TIPO_MANTENIMIENTO_VARIOS_ID')
        return cls(mantenimiento_id=mantenimiento_id, tipo_mantenimiento_varios_id=tipo_id, id=_id)

    @classmethod
    def get_by_mantenimiento(cls, mantenimiento_id):
        db = DatabaseService()
        query = """
            SELECT mv.*, tmv.nombre as tipo_nombre
            FROM mantenimiento_varios mv
            JOIN tipos_mantenimiento_varios tmv ON mv.tipo_mantenimiento_varios_id = tmv.id
            WHERE mv.mantenimiento_id = %s
        """
        results = db.execute_query(query, (mantenimiento_id,))
        return results  # Retornamos los resultados directamente para mostrar los nombres