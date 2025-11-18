from controllers.base_controller import BaseController
from models.mantenimiento_model import (
    Mantenimiento,
    CambioAceite, 
    MantenimientoFrenos, 
    MantenimientoGeneral, 
    MantenimientoCorrectivo
)

class MantenimientoController(BaseController):
    def create_cambio_aceite(self, vehiculo_id, kilometraje, mecanico, observaciones,
                           filtro_aceite, filtro_aire, tipo_aceite, fecha_mantenimiento=None):
        mantenimiento = CambioAceite(
            vehiculo_id=vehiculo_id,
            kilometraje=kilometraje,
            mecanico=mecanico,
            observaciones=observaciones,
            filtro_aceite=filtro_aceite,
            filtro_aire=filtro_aire,
            tipo_aceite=tipo_aceite,
            fecha_mantenimiento=fecha_mantenimiento
        )
        return mantenimiento.save()

    def create_mantenimiento_frenos(self, vehiculo_id, kilometraje, mecanico, observaciones,
                                  estado_pastillas, estado_discos, estado_liquido, estado_campanas, fecha_mantenimiento=None):
        mantenimiento = MantenimientoFrenos(
            vehiculo_id=vehiculo_id,
            kilometraje=kilometraje,
            mecanico=mecanico,
            observaciones=observaciones,
            estado_pastillas=estado_pastillas,
            estado_discos=estado_discos,
            estado_liquido=estado_liquido,
            estado_campanas=estado_campanas,
            fecha_mantenimiento=fecha_mantenimiento
        )
        return mantenimiento.save()

    def create_mantenimiento_general(self, vehiculo_id, kilometraje, mecanico, observaciones,
                                   fecha_ultima_correa, estado_luces, estado_frenos, 
                                   estado_correa_accesorios, fecha_mantenimiento=None):
        mantenimiento = MantenimientoGeneral(
            vehiculo_id=vehiculo_id,
            kilometraje=kilometraje,
            mecanico=mecanico,
            observaciones=observaciones,
            fecha_ultima_correa=fecha_ultima_correa,
            estado_luces=estado_luces,
            estado_frenos=estado_frenos,
            estado_correa_accesorios=estado_correa_accesorios,
            fecha_mantenimiento=fecha_mantenimiento
        )
        return mantenimiento.save()

    def create_mantenimiento_correctivo(self, vehiculo_id, kilometraje, mecanico, observaciones,
                                      detalles_falla, danos_colaterales, fecha_mantenimiento=None):
        mantenimiento = MantenimientoCorrectivo(
            vehiculo_id=vehiculo_id,
            kilometraje=kilometraje,
            mecanico=mecanico,
            observaciones=observaciones,
            detalles_falla=detalles_falla,
            danos_colaterales=danos_colaterales,
            fecha_mantenimiento=fecha_mantenimiento
        )
        return mantenimiento.save()

    def create(self, *args, **kwargs):
        raise NotImplementedError("Use specific create methods for each maintenance type")

    def update_cambio_aceite(self, id, vehiculo_id, kilometraje, mecanico, observaciones,
                            filtro_aceite, filtro_aire, tipo_aceite, fecha_mantenimiento=None):
        mantenimiento = CambioAceite(
            id=id,
            vehiculo_id=vehiculo_id,
            kilometraje=kilometraje,
            mecanico=mecanico,
            observaciones=observaciones,
            filtro_aceite=filtro_aceite,
            filtro_aire=filtro_aire,
            tipo_aceite=tipo_aceite,
            fecha_mantenimiento=fecha_mantenimiento
        )
        return mantenimiento.update()

    def update_mantenimiento_frenos(self, id, vehiculo_id, kilometraje, mecanico, observaciones,
                                   estado_pastillas, estado_discos, estado_liquido, estado_campanas, fecha_mantenimiento=None):
        mantenimiento = MantenimientoFrenos(
            id=id,
            vehiculo_id=vehiculo_id,
            kilometraje=kilometraje,
            mecanico=mecanico,
            observaciones=observaciones,
            estado_pastillas=estado_pastillas,
            estado_discos=estado_discos,
            estado_liquido=estado_liquido,
            estado_campanas=estado_campanas,
            fecha_mantenimiento=fecha_mantenimiento
        )
        return mantenimiento.update()

    def update_mantenimiento_general(self, id, vehiculo_id, kilometraje, mecanico, observaciones,
                                    fecha_ultima_correa, estado_luces, estado_frenos, 
                                    estado_correa_accesorios, fecha_mantenimiento=None):
        mantenimiento = MantenimientoGeneral(
            id=id,
            vehiculo_id=vehiculo_id,
            kilometraje=kilometraje,
            mecanico=mecanico,
            observaciones=observaciones,
            fecha_ultima_correa=fecha_ultima_correa,
            estado_luces=estado_luces,
            estado_frenos=estado_frenos,
            estado_correa_accesorios=estado_correa_accesorios,
            fecha_mantenimiento=fecha_mantenimiento
        )
        return mantenimiento.update()

    def update_mantenimiento_correctivo(self, id, vehiculo_id, kilometraje, mecanico, observaciones,
                                       detalles_falla, danos_colaterales, fecha_mantenimiento=None):
        mantenimiento = MantenimientoCorrectivo(
            id=id,
            vehiculo_id=vehiculo_id,
            kilometraje=kilometraje,
            mecanico=mecanico,
            observaciones=observaciones,
            detalles_falla=detalles_falla,
            danos_colaterales=danos_colaterales,
            fecha_mantenimiento=fecha_mantenimiento
        )
        return mantenimiento.update()

    def update(self, *args, **kwargs):
        raise NotImplementedError("Use specific update methods for each maintenance type")

    def delete(self, id):
        # Se puede eliminar cualquier tipo de mantenimiento usando la tabla base
        mantenimiento = Mantenimiento(id=id)
        return mantenimiento.delete()

    def get_all(self):
        return Mantenimiento.get_all()

    def get_by_id(self, id):
        return Mantenimiento.get_by_id(id)

    def get_by_vehiculo(self, vehiculo_id):
        return Mantenimiento.get_by_vehiculo(vehiculo_id)

    def get_historial_completo(self, vehiculo_id):
        mantenimientos = self.get_by_vehiculo(vehiculo_id)
        return sorted(mantenimientos, key=lambda x: x.fecha_mantenimiento, reverse=True)