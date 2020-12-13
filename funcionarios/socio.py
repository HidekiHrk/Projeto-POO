from funcionarios.funcionario import Funcionario
from orm.horario import Horario


class Socio(Funcionario):
    def __init__(self, name: str):
        super().__init__(name)

    def reservar(self, sala_id: int, horario: Horario):
        pass 

    # ---- inherited methods ---- #
    def get_reservas(self, *ids: int):
        pass
