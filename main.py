from orm.db import create_tables
from funcionarios.socio import Socio
from funcionarios.programador import Programador
from orm.sala import Sala
from orm.reserva import Reserva
from orm.horario import Horario


def main():
    create_tables()


if __name__ == '__main__':
    main()
