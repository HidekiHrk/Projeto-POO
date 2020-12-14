from orm.db import create_tables
from funcionarios.socio import Socio
from funcionarios.funcionario import Funcionario
from funcionarios.programador import Programador
from funcionarios.designer import Designer
from orm.sala import Sala
from orm.reserva import Reserva
from orm.horario import Horario


class Program:
    def __init__(self):
        self.is_running = False

    def update(self):
        comando = int(input('Insira o comando aqui: '))

        if comando == 1:
            quantidade_de_socios = int(input('Insira a quantidade de sócios a serem cadastrados: '))
            print('Cadastre o nome dos sócios')
            for i in range(quantidade_de_socios):
                nome = input(f'{i + 1} - Insira o nome sócio: ')
                Socio.create(nome)
        elif comando == 2:
            cargos = {
                'programador': Programador,
                'designer': Designer
            }
            quantidade_de_funcionarios = int(input('Insira a quantidade de funcionários a serem cadastrados: '))
            print('Cadastre o nome e os cargos dos funcionários')
            print('Cargos: programador - designer')
            for i in range(quantidade_de_funcionarios):
                print(f'Dados do funcionário {i + 1}')
                nome = input('Insira o nome: ')
                cargo = None
                while cargo is None:
                    cargo = cargos.get(input('Insira o cargo: '))
                    if cargo:
                        cargo.create(nome)
                    else:
                        print('Cargo inxestente')
        elif comando == 3:
            reserva_id = int(input('Insira o id da reserva: '))
            reservas = Reserva.get_by(id=reserva_id)
            if len(reservas) > 0:
                print(reservas[0])
        elif comando == 4:
            print(Socio.get_all())
        elif comando == 5:
            print("""OBS: em caso de campos vazios será fornecido todas as informações""")
            socio_id = input("Insira o id do sócio: ")
            dia_e_mes = input("Insira o dia e o mês (d/m): ")
            args = [dia_e_mes.split('/')] if dia_e_mes != '' else []
            kwargs = {"socio_id": int(socio_id)} if socio_id.isnumeric() else {}
            if len(args):
                reservas = Reserva.get_by_day(*args, **kwargs)
            else:
                reservas = Reserva.get_by(**kwargs)

            for reserva in reservas:
                print(reserva)

        elif comando == 6:
            id = int(input('Insira o id do sócio: '))
            socio = Socio.get(id)
            sala_id = int(input('Informe o id da sala: '))
            sala = Sala.get(sala_id)
            agendamento = input('Informe o dia, mês e hora: ').split()
            dia = int(agendamento[0])
            mes = int(agendamento[1])
            hora = int(agendamento[2])
            horario = Horario(dia, mes, hora)
            Reserva.create(socio, sala, horario)
        elif comando == 7:
            quantidade_de_salas = int(input('Insira a quantidade de salas a serem criadas: '))
            for i in range(quantidade_de_salas):
                capacidade_de_pessoas = int(input(f'Insira a quantidade de pessoas que a sala {i + 1} pode comportar: '))
                Sala.create(capacidade_de_pessoas)
        elif comando == 8:
            print(Sala.get_all())
        elif comando == 9:
            reserva_id = int(input('Insira o id da reserva: '))
            reservas = Reserva.get_by(id=reserva_id)
            funcionario_id = int(input('Insira o id funcionário: '))
            funcionario = Funcionario.get(funcionario_id)
            if len(reservas) > 0:
                reserva = reservas[0]
                reserva.add_funcionario(funcionario)

        elif comando == 10:
            print(Programador.get_all())
            print(Designer.get_all())
        elif comando == 11:
            reserva_id = int(input('Insira o id da reserva: '))
            reservas = Reserva.get_by(id=reserva_id)
            if len(reservas) > 0:
                reserva = reservas[0]
                reserva.remove()
        elif comando == 12:
            reserva_id = int(input('Insira o id da reserva: '))
            reservas = Reserva.get_by(id=reserva_id)
            funcionario_id = int(input('Insira o id do funcionário: '))
            funcionario = Funcionario.get(funcionario_id)
            if len(reservas) > 0:
                reserva = reservas[0]
                reserva.remove_funcionario(funcionario)
        elif comando == 13:
            reserva_id = int(input('Insira o id da reserva: '))
            reservas = Reserva.get_by(id=reserva_id)
            if len(reservas) > 0:
                reserva = reservas[0]
                novo_socio = input('Nome do sócio: ')
                Socio.create(novo_socio)
                lista_socio = Socio.get_all()
                reserva.socio = lista_socio[-1]
        elif comando == 14:
            reserva_id = int(input('Insira o id da reserva: '))
            reservas = Reserva.get_by(id=reserva_id)
            if len(reservas) > 0:
                reserva = reservas[0]
                novo_horario = input('Insira o novo horário(d/m/h): ').split('/')
                dia = int(novo_horario[0])
                mes = int(novo_horario[1])
                hora = int(novo_horario[2])
                horario = Horario(dia, mes, hora)
                reserva.horario = horario
        elif comando == 999:
            self.is_running = False
        else:
            print('COMANDO INCORRETO')

    def start(self):
        print('''
                ESCOLHA UMA DAS OPÇÕES
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                COMANDOS PARA CADASTRO
        1 - Cadastro de sócios
        2 - Cadastro de funcionários
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                COMANDOS PARA CONSULTA
        3 - Consultar reserva
        4 - Consultar informações dos sócios
        8 - Consultar salas
        10 - Consultar informações dos funcionários
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                COMANDOS PARA VIZUALIZAÇÃO
        5 - Vizualizar reservas
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                COMANDO PARA RESERVAR SALA
        6 - Criar reserva de sala
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                COMANDO PARA CRIAÇÃO DE SALAS
        7 - Criar sala
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                COMANDO PARA ADCIONAR FUNCIONÁRIO A UMA SALA
        9 - Adiconar funcionário
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                COMANDOS PARA REMOÇÃO
        11 - Remover reserva 
        12 - Remover funcionário da reserva 
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                COMANDOS PARA ALTERAÇÃO
        13 - Alterar nome do sócio na reserva
        14 - Alterar horário da reserva
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                FINALIZAR PROGRAMA
        Insira 999 para encerrar execução
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        ''')
        self.is_running = True
        create_tables()
        while self.is_running:
            try:
                self.update()
            except Exception as e:
                print(e)


if __name__ == '__main__':
    program = Program()
    program.start()
