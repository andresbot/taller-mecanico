from datetime import datetime
from models.base_model import BaseModel
from models.vehiculo_model import Vehiculo
from services.db_service import DatabaseService

class Mantenimiento(BaseModel):
    def __init__(self, vehiculo_id=None, tipo_mantenimiento=None, fecha_mantenimiento=None, 
                 kilometraje=None, mecanico=None, observaciones=None, id=None):
        super().__init__()
        self.id = id
        self.vehiculo_id = vehiculo_id
        self.tipo_mantenimiento = tipo_mantenimiento
        self.fecha_mantenimiento = fecha_mantenimiento or datetime.now()
        self.kilometraje = kilometraje
        self.mecanico = mecanico
        self.observaciones = observaciones
        self._vehiculo = None

    @property
    def vehiculo(self):
        if self._vehiculo is None and self.vehiculo_id:
            self._vehiculo = Vehiculo.get_by_id(self.vehiculo_id)
        return self._vehiculo

    def save(self):
        if self.id is None:
            query = """
                INSERT INTO mantenimientos 
                (vehiculo_id, tipo_mantenimiento, fecha_mantenimiento, kilometraje, mecanico, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (self.vehiculo_id, self.tipo_mantenimiento, self.fecha_mantenimiento,
                     self.kilometraje, self.mecanico, self.observaciones)
            self.id = self.db.execute_query(query, params)
            return self.id
        return self.update()

    def update(self):
        if self.id is None:
            return None
        
        query = """
            UPDATE mantenimientos 
            SET vehiculo_id = %s, tipo_mantenimiento = %s, fecha_mantenimiento = %s,
                kilometraje = %s, mecanico = %s, observaciones = %s
            WHERE ID = %s
        """
        params = (self.vehiculo_id, self.tipo_mantenimiento, self.fecha_mantenimiento,
                 self.kilometraje, self.mecanico, self.observaciones, self.id)
        self.db.execute_query(query, params)
        return self.id

    def delete(self):
        if self.id is None:
            return False
        
        query = "DELETE FROM mantenimientos WHERE ID = %s"
        self.db.execute_query(query, (self.id,))
        return True

    @staticmethod
    def _format_result(result):
        return {
            'id': result['ID'],
            'vehiculo_id': result['vehiculo_id'],
            'tipo_mantenimiento': result['tipo_mantenimiento'],
            'fecha_mantenimiento': result['fecha_mantenimiento'],
            'kilometraje': result['kilometraje'],
            'mecanico': result['mecanico'],
            'observaciones': result['observaciones']
        }

    @classmethod
    def get_all(cls):
        db = DatabaseService()
        query = "SELECT * FROM mantenimientos"
        results = db.execute_query(query)
        return [cls(**cls._format_result(result)) for result in results]

    @classmethod
    def get_by_id(cls, id):
        db = DatabaseService()
        query = "SELECT * FROM mantenimientos WHERE ID = %s"
        results = db.execute_query(query, (id,))
        if not results:
            return None
        return cls(**cls._format_result(results[0]))

    @classmethod
    def get_by_vehiculo(cls, vehiculo_id):
        db = DatabaseService()
        query = "SELECT * FROM mantenimientos WHERE vehiculo_id = %s ORDER BY fecha_mantenimiento DESC"
        results = db.execute_query(query, (vehiculo_id,))
        return [cls(**cls._format_result(result)) for result in results]

class CambioAceite(Mantenimiento):
    def __init__(self, filtro_aceite=None, filtro_aire=None, tipo_aceite=None, **kwargs):
        super().__init__(**kwargs)
        self.tipo_mantenimiento = 'cambio_aceite'
        self.filtro_aceite = filtro_aceite
        self.filtro_aire = filtro_aire
        self.tipo_aceite = tipo_aceite

    def save(self):
        mantenimiento_id = super().save()
        if mantenimiento_id:
            query = """
                INSERT INTO cambio_aceite 
                (mantenimiento_id, filtro_aceite, filtro_aire, tipo_aceite)
                VALUES (%s, %s, %s, %s)
            """
            params = (mantenimiento_id, self.filtro_aceite, self.filtro_aire, self.tipo_aceite)
            self.db.execute_query(query, params)
        return mantenimiento_id

    def update(self):
        # Actualizar la tabla base
        mantenimiento_id = super().update()
        if mantenimiento_id:
            # Actualizar la tabla específica
            query = """
                UPDATE cambio_aceite 
                SET filtro_aceite = %s, filtro_aire = %s, tipo_aceite = %s
                WHERE mantenimiento_id = %s
            """
            params = (self.filtro_aceite, self.filtro_aire, self.tipo_aceite, self.id)
            self.db.execute_query(query, params)
        return mantenimiento_id

    @classmethod
    def get_by_id(cls, id):
        db = DatabaseService()
        # Obtener datos base
        query_base = "SELECT * FROM mantenimientos WHERE ID = %s"
        results_base = db.execute_query(query_base, (id,))
        if not results_base:
            return None
        
        # Obtener datos específicos
        query_detalle = "SELECT * FROM cambio_aceite WHERE mantenimiento_id = %s"
        results_detalle = db.execute_query(query_detalle, (id,))
        
        data = cls._format_result(results_base[0])
        if results_detalle:
            data['filtro_aceite'] = results_detalle[0]['filtro_aceite']
            data['filtro_aire'] = results_detalle[0]['filtro_aire']
            data['tipo_aceite'] = results_detalle[0]['tipo_aceite']
        
        return cls(**data)

class MantenimientoFrenos(Mantenimiento):
    def __init__(self, estado_pastillas=None, estado_discos=None, 
                 estado_liquido=None, estado_campanas=None, **kwargs):
        super().__init__(**kwargs)
        self.tipo_mantenimiento = 'frenos'
        self.estado_pastillas = estado_pastillas
        self.estado_discos = estado_discos
        self.estado_liquido = estado_liquido
        self.estado_campanas = estado_campanas

    def save(self):
        mantenimiento_id = super().save()
        if mantenimiento_id:
            query = """
                INSERT INTO mantenimiento_frenos 
                (mantenimiento_id, estado_pastillas, estado_discos, 
                 estado_liquido, estado_campanas)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (mantenimiento_id, self.estado_pastillas, self.estado_discos,
                     self.estado_liquido, self.estado_campanas)
            self.db.execute_query(query, params)
        return mantenimiento_id

    def update(self):
        # Actualizar la tabla base
        mantenimiento_id = super().update()
        if mantenimiento_id:
            # Actualizar la tabla específica
            query = """
                UPDATE mantenimiento_frenos 
                SET estado_pastillas = %s, estado_discos = %s, 
                    estado_liquido = %s, estado_campanas = %s
                WHERE mantenimiento_id = %s
            """
            params = (self.estado_pastillas, self.estado_discos,
                     self.estado_liquido, self.estado_campanas, self.id)
            self.db.execute_query(query, params)
        return mantenimiento_id

    @classmethod
    def get_by_id(cls, id):
        db = DatabaseService()
        # Obtener datos base
        query_base = "SELECT * FROM mantenimientos WHERE ID = %s"
        results_base = db.execute_query(query_base, (id,))
        if not results_base:
            return None
        
        # Obtener datos específicos
        query_detalle = "SELECT * FROM mantenimiento_frenos WHERE mantenimiento_id = %s"
        results_detalle = db.execute_query(query_detalle, (id,))
        
        data = cls._format_result(results_base[0])
        if results_detalle:
            data['estado_pastillas'] = results_detalle[0]['estado_pastillas']
            data['estado_discos'] = results_detalle[0]['estado_discos']
            data['estado_liquido'] = results_detalle[0]['estado_liquido']
            data['estado_campanas'] = results_detalle[0]['estado_campanas']
        
        return cls(**data)

class MantenimientoGeneral(Mantenimiento):
    def __init__(self, fecha_ultima_correa=None, estado_luces=None,
                 estado_frenos=None, estado_correa_accesorios=None, **kwargs):
        super().__init__(**kwargs)
        self.tipo_mantenimiento = 'general'
        self.fecha_ultima_correa = fecha_ultima_correa
        self.estado_luces = estado_luces
        self.estado_frenos = estado_frenos
        self.estado_correa_accesorios = estado_correa_accesorios

    def save(self):
        mantenimiento_id = super().save()
        if mantenimiento_id:
            query = """
                INSERT INTO mantenimiento_general 
                (mantenimiento_id, fecha_ultima_correa, estado_luces,
                 estado_frenos, estado_correa_accesorios)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (mantenimiento_id, self.fecha_ultima_correa, self.estado_luces,
                     self.estado_frenos, self.estado_correa_accesorios)
            self.db.execute_query(query, params)
        return mantenimiento_id

    def update(self):
        # Actualizar la tabla base
        mantenimiento_id = super().update()
        if mantenimiento_id:
            # Actualizar la tabla específica
            query = """
                UPDATE mantenimiento_general 
                SET fecha_ultima_correa = %s, estado_luces = %s,
                    estado_frenos = %s, estado_correa_accesorios = %s
                WHERE mantenimiento_id = %s
            """
            params = (self.fecha_ultima_correa, self.estado_luces,
                     self.estado_frenos, self.estado_correa_accesorios, self.id)
            self.db.execute_query(query, params)
        return mantenimiento_id

    @classmethod
    def get_by_id(cls, id):
        db = DatabaseService()
        # Obtener datos base
        query_base = "SELECT * FROM mantenimientos WHERE ID = %s"
        results_base = db.execute_query(query_base, (id,))
        if not results_base:
            return None
        
        # Obtener datos específicos
        query_detalle = "SELECT * FROM mantenimiento_general WHERE mantenimiento_id = %s"
        results_detalle = db.execute_query(query_detalle, (id,))
        
        data = cls._format_result(results_base[0])
        if results_detalle:
            data['fecha_ultima_correa'] = results_detalle[0]['fecha_ultima_correa']
            data['estado_luces'] = results_detalle[0]['estado_luces']
            data['estado_frenos'] = results_detalle[0]['estado_frenos']
            data['estado_correa_accesorios'] = results_detalle[0]['estado_correa_accesorios']
        
        return cls(**data)

class MantenimientoCorrectivo(Mantenimiento):
    def __init__(self, detalles_falla=None, danos_colaterales=None, **kwargs):
        super().__init__(**kwargs)
        self.tipo_mantenimiento = 'correctivo'
        self.detalles_falla = detalles_falla
        self.danos_colaterales = danos_colaterales

    def save(self):
        mantenimiento_id = super().save()
        if mantenimiento_id:
            query = """
                INSERT INTO mantenimiento_correctivo 
                (mantenimiento_id, detalles_falla, danos_colaterales)
                VALUES (%s, %s, %s)
            """
            params = (mantenimiento_id, self.detalles_falla, self.danos_colaterales)
            self.db.execute_query(query, params)
        return mantenimiento_id

    def update(self):
        # Actualizar la tabla base
        mantenimiento_id = super().update()
        if mantenimiento_id:
            # Actualizar la tabla específica
            query = """
                UPDATE mantenimiento_correctivo 
                SET detalles_falla = %s, danos_colaterales = %s
                WHERE mantenimiento_id = %s
            """
            params = (self.detalles_falla, self.danos_colaterales, self.id)
            self.db.execute_query(query, params)
        return mantenimiento_id

    @classmethod
    def get_by_id(cls, id):
        db = DatabaseService()
        # Obtener datos base
        query_base = "SELECT * FROM mantenimientos WHERE ID = %s"
        results_base = db.execute_query(query_base, (id,))
        if not results_base:
            return None
        
        # Obtener datos específicos
        query_detalle = "SELECT * FROM mantenimiento_correctivo WHERE mantenimiento_id = %s"
        results_detalle = db.execute_query(query_detalle, (id,))
        
        data = cls._format_result(results_base[0])
        if results_detalle:
            data['detalles_falla'] = results_detalle[0]['detalles_falla']
            data['danos_colaterales'] = results_detalle[0]['danos_colaterales']
        
        return cls(**data)