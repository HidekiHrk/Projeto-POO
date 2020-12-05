from poo_entities.funcionario import Funcionario
from poo_entities.data import Data
from poo_entities import reserva


class Socio(Funcionario):
    def __init__(self, nome: str):
        super().__init__(nome)

    def create_reserva(self, time_tuple: (int, int, int,), sala: 'Sala') -> reserva.Reserva:
        horario = Data(*time_tuple)
        if any(r.data == horario for r in self.reservas):
            raise Exception('O sócio já criou uma reserva para este horário.')
        reserva_obj = reserva.Reserva(horario, self, sala)
        self.add_reserva(reserva_obj)
        return reserva_obj
