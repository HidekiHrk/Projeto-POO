from random import randint

from poo_entities.sala import Sala
from poo_entities.socio import Socio
from poo_entities.programador import Programador
from poo_entities.secretario import Secretario


def main():
    salas = [Sala(id, randint(5, 15)) for id in range(4)]
    socio1 = Socio("Ricardo")
    socio2 = Socio("Rayan")
    secretario1 = Secretario("Jefferson")
    programador1 = Programador("Diego")
    reserva1 = socio1.create_reserva((22, 8, 13), salas[0])
    reserva1.set_funcionario(0, socio2)
    reserva1.set_funcionario(3, secretario1)
    reserva1.set_funcionario(2, programador1)
    print(*reserva1.view_ramais(), sep="\n")


if __name__ == '__main__':
    main()
