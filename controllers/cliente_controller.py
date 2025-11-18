from controllers.base_controller import BaseController
from models.cliente_model import Cliente

class ClienteController(BaseController):
    def create(self, cedula, nombre, telefono):
        cliente = Cliente(Cedula=cedula, Nombre=nombre, Telefono=telefono)
        return cliente.save()

    def update(self, id, cedula, nombre, telefono):
        cliente = Cliente(Cedula=cedula, Nombre=nombre, Telefono=telefono, ID=id)
        return cliente.update()

    def delete(self, id):
        cliente = Cliente(ID=id)
        return cliente.delete()

    def get_all(self):
        return Cliente.get_all()

    def get_by_id(self, id):
        return Cliente.get_by_id(id)