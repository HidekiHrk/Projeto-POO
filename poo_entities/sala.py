from poo_entities.havereserva import HaveReserva
from typing import *


class Sala(HaveReserva):
    def __init__(self, id: int, vagas: int):
        super().__init__()
        self.id = id
        self.vagas = vagas

