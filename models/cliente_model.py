from models.base_model import BaseModel
from services.db_service import DatabaseService

class Cliente(BaseModel):
    def __init__(self, Cedula=None, Nombre=None, Telefono=None, ID=None):
        super().__init__()
        self.id = ID
        self.cedula = Cedula
        self.nombre = Nombre
        self.telefono = Telefono

    def save(self):
        if self.id is None:
            query = """
                INSERT INTO clientes (Cedula, Nombre, Telefono)
                VALUES (%s, %s, %s)
            """
            params = (self.cedula, self.nombre, self.telefono)
            self.id = self.db.execute_query(query, params)
            return self.id
        return self.update()

    def update(self):
        if self.id is None:
            return None
        
        query = """
            UPDATE clientes 
            SET Cedula = %s, Nombre = %s, Telefono = %s
            WHERE ID = %s
        """
        params = (self.cedula, self.nombre, self.telefono, self.id)
        self.db.execute_query(query, params)
        return self.id

    def delete(self):
        if self.id is None:
            return False
        
        # Verificar si el cliente tiene vehículos asociados
        check_query = "SELECT COUNT(*) as count FROM vehiculos WHERE cliente_id = %s"
        result = self.db.execute_query(check_query, (self.id,))
        if result and result[0]['count'] > 0:
            raise Exception("No se puede eliminar el cliente porque tiene vehículos asociados. Elimine primero los vehículos.")
        
        query = "DELETE FROM clientes WHERE ID = %s"
        self.db.execute_query(query, (self.id,))
        return True

    @classmethod
    def get_all(cls):
        db = DatabaseService()
        query = "SELECT * FROM clientes"
        results = db.execute_query(query)
        return [cls(**result) for result in results]

    @classmethod
    def get_by_id(cls, id):
        db = DatabaseService()
        query = "SELECT * FROM clientes WHERE ID = %s"
        results = db.execute_query(query, (id,))
        return cls(**results[0]) if results else None