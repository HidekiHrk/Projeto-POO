from typing import *


class HaveReserva:
    def __init__(self):
        self.__reservas: List['Reserva'] = []

    @property
    def reservas(self):
        return self.__reservas

    def add_reserva(self, reserva: 'Reserva'):
        if reserva not in self.__reservas:
            self.__reservas.append(reserva)

    def remove_reserva(self, reserva: 'Reserva'):
        try:
            self.__reservas.remove(reserva)
        except ValueError:
            pass