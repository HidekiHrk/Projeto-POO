from typing import *
from poo_entities.havereserva import HaveReserva


class Funcionario(HaveReserva):
    def __init__(self, nome: str):
        super().__init__()
        self.nome = nome

