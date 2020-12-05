from poo_entities.havereserva import HaveReserva
from typing import *


def get_date_string(dia: int, mes: int, hora: int):
    return f"{dia}/{mes} - {hora}"


class Data(HaveReserva):
    __datas = []

    @staticmethod
    def get_datas(cls):
        return tuple(cls.__datas)

    def __new__(cls, dia: int, mes: int, hora: int, *args, **kwargs):
        incoming_hash = get_date_string(dia, mes, hora)
        try:
            return cls.__datas[cls.__datas.index(incoming_hash)]
        except ValueError:
            instance = super().__new__(cls, *args, **kwargs)
            cls.__datas.append(instance)
            return instance

    def __init__(self, dia: int, mes: int, hora: int):
        super().__init__()
        self.dia = dia
        self.mes = mes
        self.hora = hora

    def __str__(self):
        return get_date_string(self.dia, self.mes, self.hora)

    def __repr__(self):
        return str(self)

    def __eq__(self, other: 'Data'):
        return str(self) == str(other)

    def __del__(self):
        del Data.__datas[Data.__datas.index(str(self))]
