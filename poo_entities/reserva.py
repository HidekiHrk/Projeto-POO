from typing import *
from poo_entities.data import Data
from poo_entities.sala import Sala
from poo_entities.funcionario import Funcionario


class Reserva:
    def __init__(self, data: Data, socio: 'Socio', sala: Sala):
        if not type(socio).__name__ == 'Socio':
            raise Exception('O funcionário precisa ser um sócio para poder reservar uma sala')
        if data.reservas and any(reserva.sala == sala for reserva in data.reservas):
            raise Exception('Já existe uma reserva para esta sala e horário')

        self.data = data
        self.data.reservas.append(self)
        self.sala = sala
        self.socio = socio
        self.__ramais: List[Funcionario] = [None] * self.sala.vagas
        sala.add_reserva(self)

    def view_ramais(self):
        return list(map(lambda y: f'Ramal {y[0]} - {y[1].nome}', filter(lambda x: x[1] is not None, enumerate(self.__ramais))))

    def set_funcionario(self, ramal: int, funcionario: Funcionario):
        try:
            self.__ramais[ramal] = funcionario
            funcionario.add_reserva(self)
        except IndexError:
            print('Este ramal não existe')

    def remove_funcionario(self, ramal: int):
        try:
            self.__ramais[ramal].remove_reserva(self)
            self.__ramais[ramal] = None
        except IndexError:
            print('Este ramal não existe')

    def get_ramal_by_funcionario(self, funcionario: Funcionario):
        try:
            return self.__ramais.index(funcionario)
        except ValueError:
            return None

    def remove(self):
        self.sala.remove_reserva(self)
        self.socio.remove_reserva(self)
        self.data.remove_reserva(self)
        for ramal in filter(lambda x: isinstance(x, Funcionario), self.__ramais):
            ramal.remove_reserva(self)

    def __del__(self):
        self.remove()
