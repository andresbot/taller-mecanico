from models.base_model import BaseModel
from models.cliente_model import Cliente
from services.db_service import DatabaseService

class Vehiculo(BaseModel):
    def __init__(self, placa=None, marca=None, modelo=None, linea=None, kilometraje=None, cliente_id=None, id=None):
        super().__init__()
        self.id = id
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.linea = linea
        self.kilometraje = kilometraje
        self.cliente_id = cliente_id
        self._cliente = None

    @property
    def cliente(self):
        if self._cliente is None and self.cliente_id:
            self._cliente = Cliente.get_by_id(self.cliente_id)
        return self._cliente

    def save(self):
        if self.id is None:
            query = """
                INSERT INTO vehiculos (Placa, Marca, Modelo, linea, Kilometraje, cliente_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (self.placa, self.marca, self.modelo, self.linea, self.kilometraje, self.cliente_id)
            self.id = self.db.execute_query(query, params)
            return self.id
        return self.update()

    def update(self):
        if self.id is None:
            return None
        
        query = """
            UPDATE vehiculos 
            SET Placa = %s, Marca = %s, Modelo = %s, linea = %s, Kilometraje = %s, cliente_id = %s
            WHERE ID = %s
        """
        params = (self.placa, self.marca, self.modelo, self.linea, self.kilometraje, self.cliente_id, self.id)
        self.db.execute_query(query, params)
        return self.id

    def delete(self):
        if self.id is None:
            return False
        
        # Verificar si el vehículo tiene mantenimientos asociados
        check_query = "SELECT COUNT(*) as count FROM mantenimientos WHERE vehiculo_id = %s"
        result = self.db.execute_query(check_query, (self.id,))
        if result and result[0]['count'] > 0:
            raise Exception("No se puede eliminar el vehículo porque tiene mantenimientos asociados. Elimine primero los mantenimientos.")
        
        query = "DELETE FROM vehiculos WHERE ID = %s"
        self.db.execute_query(query, (self.id,))
        return True

    @classmethod
    def get_all(cls):
        db = DatabaseService()
        query = "SELECT * FROM vehiculos"
        results = db.execute_query(query)
        # Convertir las claves a minúsculas
        formatted_results = []
        for result in results:
            formatted_result = {
                'id': result['ID'],
                'placa': result['Placa'],
                'marca': result['Marca'],
                'modelo': result['Modelo'],
                'linea': result.get('linea', ''),
                'kilometraje': result['Kilometraje'],
                'cliente_id': result['cliente_id']
            }
            formatted_results.append(formatted_result)
        return [cls(**result) for result in formatted_results]

    @classmethod
    def get_by_id(cls, id):
        db = DatabaseService()
        query = """
            SELECT ID, Placa, Marca, Modelo, linea, Kilometraje, cliente_id
            FROM vehiculos 
            WHERE ID = %s
        """
        results = db.execute_query(query, (id,))
        if not results:
            return None
        # Convertir las claves a minúsculas
        result = results[0]
        formatted_result = {
            'id': result['ID'],
            'placa': result['Placa'],
            'marca': result['Marca'],
            'modelo': result['Modelo'],
            'linea': result.get('linea', ''),
            'kilometraje': result['Kilometraje'],
            'cliente_id': result['cliente_id']
        }
        return cls(**formatted_result)

    @classmethod
    def get_by_cliente(cls, cliente_id):
        db = DatabaseService()
        query = """
            SELECT ID, Placa, Marca, Modelo, linea, Kilometraje, cliente_id
            FROM vehiculos 
            WHERE cliente_id = %s
        """
        results = db.execute_query(query, (cliente_id,))
        # Convertir las claves a minúsculas
        formatted_results = []
        for result in results:
            formatted_result = {
                'id': result['ID'],
                'placa': result['Placa'],
                'marca': result['Marca'],
                'modelo': result['Modelo'],
                'linea': result.get('linea', ''),
                'kilometraje': result['Kilometraje'],
                'cliente_id': result['cliente_id']
            }
            formatted_results.append(formatted_result)
        return [cls(**result) for result in formatted_results]

    def actualizar_kilometraje(self, nuevo_kilometraje):
        if nuevo_kilometraje < self.kilometraje:
            raise ValueError("El nuevo kilometraje no puede ser menor al actual")
        
        self.kilometraje = nuevo_kilometraje
        return self.update()