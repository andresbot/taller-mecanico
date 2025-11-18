from controllers.base_controller import BaseController
from models.vehiculo_model import Vehiculo

class VehiculoController(BaseController):
    def create(self, placa, marca, modelo, linea, kilometraje, cliente_id):
        vehiculo = Vehiculo(
            placa=placa,
            marca=marca,
            modelo=modelo,
            linea=linea,
            kilometraje=kilometraje,
            cliente_id=cliente_id
        )
        return vehiculo.save()

    def update(self, id, placa, marca, modelo, linea, kilometraje, cliente_id):
        vehiculo = Vehiculo(
            id=id,
            placa=placa,
            marca=marca,
            modelo=modelo,
            linea=linea,
            kilometraje=kilometraje,
            cliente_id=cliente_id
        )
        return vehiculo.update()

    def delete(self, id):
        vehiculo = Vehiculo(id=id)
        return vehiculo.delete()

    def get_all(self):
        return Vehiculo.get_all()

    def get_by_id(self, id):
        return Vehiculo.get_by_id(id)

    def get_by_cliente(self, cliente_id):
        return Vehiculo.get_by_cliente(cliente_id)

    def actualizar_kilometraje(self, id, nuevo_kilometraje):
        vehiculo = self.get_by_id(id)
        if vehiculo:
            return vehiculo.actualizar_kilometraje(nuevo_kilometraje)
        return False