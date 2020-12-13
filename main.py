from orm.db import create_tables
from funcionarios.socio import Socio
from funcionarios.programador import Programador
from orm.sala import Sala
from orm.reserva import Reserva
from orm.horario import Horario


class Program:
    def __init__(self):
        self.is_running = False

    def update(self):
        pass

    def start(self):
        self.is_running = True
        create_tables()
        while self.is_running:
            self.update()


if __name__ == '__main__':
    program = Program()
    program.start()
