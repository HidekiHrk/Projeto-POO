from typing import List
from funcionarios.funcionario import Funcionario
from funcionarios.socio import Socio
from orm.sala import Sala
from orm.horario import Horario
from orm.db import c, conn


class Reserva:
    def __init__(self, reserva_id: int, socio: 'Socio', sala: 'Sala', horario: 'Horario'):
        self.__id = reserva_id
        self.__socio = socio
        self.__sala = sala
        self.__horario = horario

    @property
    def id(self):
        return self.__id

    @property
    def socio(self):
        return self.__socio

    @socio.setter
    def socio(self, value: 'Socio'):
        socio_id = value.id
        c.execute("UPDATE Reserva SET socio_id = ? WHERE id = ?", (socio_id, self.__id,))
        conn.commit()
        self.__socio = value

    @property
    def sala(self):
        return self.__sala

    @property
    def horario(self):
        return self.__horario

    @horario.setter
    def horario(self, value: 'Horario'):
        c.execute("UPDATE Reserva SET horario = ? WHERE id = ?", (str(value), self.__id,))
        conn.commit()
        self.__horario = value

    def remove(self):
        c.execute("DELETE FROM Reserva WHERE id = ?", (self.__id,))
        conn.commit()
        c.execute("DELETE FROM Ramal WHERE reserva_id IS NULL")
        conn.commit()

    @classmethod
    def create(cls, socio: 'Socio', sala: 'Sala', horario: 'Horario'):
        if not isinstance(socio, Socio):
            raise cls.NotSocioException('É necessário ser um sócio para fazer uma reserva.')
        # check if another reserva with same socio/sala/horario parameters already exists.
        c.execute(
            "SELECT id FROM Reserva WHERE (socio_id = ? OR sala_id = ?) AND horario = ?",
            (socio.id, sala.id, str(horario),)
        )
        if c.fetchone():
            raise cls.AlreadyExistsException(
                "Uma reserva já foi feita nesta combinação de sócio/sala e horário.")
        c.execute("INSERT INTO Reserva (socio_id, sala_id, horario) (?,?,?)",
                  (socio.id, sala.id, str(horario),))
        this_id = c.lastrowid
        conn.commit()
        return Reserva(this_id, socio, sala, horario)

    @staticmethod
    def get_by(**fields) -> List['Reserva']:
        """
        :param fields: id | socio_id | sala_id | horario
        :return: orm.reserva.Reserva
        """
        field_str = ' AND '.join(map(lambda kv: f'{kv[0]} = ?', fields.keys()))
        field_str = 'WHERE ' + field_str if field_str != '' else ''
        c.execute(f"SELECT id, socio_id, sala_id, horario FROM Reserva {field_str}",
                  (*fields.values(),))
        data_list = c.fetchall()
        if len(data_list) > 1:
            reservas = []
            for data in data_list:
                this_id, socio_id, sala_id, horario = data
                horario = Horario.get_by_timestring(horario)
                socio = Socio.get(socio_id)
                sala = Sala.get(sala_id)
                reservas.append(Reserva(this_id, socio, sala, horario))
            return reservas

    def add_funcionario(self, funcionario: Funcionario):
        if isinstance(funcionario, Socio):
            raise self.NotSocioException('Sócios não podem ser adicionados a ramais.')
        c.execute("SELECT funcionario_id FROM Ramal WHERE funcionario_id = ?, reserva_id = ?",
                  (funcionario.id, self.__id,))
        if c.fetchone():
            raise self.AlreadyExistsException("O funcionário em questão já possui um Ramal nesta reserva.")
        c.execute("SELECT reserva_id FROM Ramal WHERE reserva_id = ?", (self.__id,))
        actual_length = len(c.fetchall())
        if actual_length >= self.sala.vagas:
            raise Sala.ExceedingLengthException('A quantidade de vagas na sala acabou.')
        c.execute("INSERT INTO Ramal (funcionario_id, reserva_id) (?,?)",
                  (funcionario.id, self.id,))
        conn.commit()

    def remove_funcionario(self, funcionario: Funcionario):
        c.execute("DELETE FROM Ramal WHERE funcionario_id = ?, reserva_id = ?",
                  (funcionario.id, self.__id,))
        conn.commit()

    class AlreadyExistsException(Exception):
        pass

    class NotSocioException(Exception):
        pass