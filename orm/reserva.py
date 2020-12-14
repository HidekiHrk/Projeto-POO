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
        c.execute("INSERT INTO Reserva (socio_id, sala_id, horario) VALUES (?,?,?)",
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
        field_str = ' AND '.join(map(lambda kv: f'{kv} = ?', fields.keys()))
        field_str = 'WHERE ' + field_str if field_str != '' else ''
        c.execute(f"SELECT id, socio_id, sala_id, horario FROM Reserva {field_str}",
                  (*fields.values(),))
        data_list = c.fetchall()
        reservas = []
        if len(data_list) >= 1:
            for data in data_list:
                this_id, socio_id, sala_id, horario = data
                horario = Horario.get_by_timestring(horario)
                socio = Socio.get(socio_id)
                sala = Sala.get(sala_id)
                reservas.append(Reserva(this_id, socio, sala, horario))
        return reservas

    @staticmethod
    def get_by_day(day_and_month: tuple, **fields) -> List['Reserva']:
        """
        :param day_and_month: (day, month,)
        :param fields: id | socio_id | sala_id | horario
        :return: orm.reserva.Reserva
        """
        day_and_month = f'{day_and_month[0]}.{day_and_month[1]}'
        field_str = ' AND '.join(map(lambda kv: f'{kv} = ?', fields.keys()))
        field_str = 'AND ' + field_str if field_str != '' else ''
        c.execute(f"""
                    SELECT id, socio_id, sala_id, horario FROM Reserva
                    WHERE SUBSTR(horario, 0, INSTR(horario, ',')) = ? {field_str}
                """,
                  (day_and_month, *fields.values(),))
        data_list = c.fetchall()
        reservas = []
        if len(data_list) >= 1:
            for data in data_list:
                this_id, socio_id, sala_id, horario = data
                horario = Horario.get_by_timestring(horario)
                socio = Socio.get(socio_id)
                sala = Sala.get(sala_id)
                reservas.append(Reserva(this_id, socio, sala, horario))
        return reservas

    def add_funcionario(self, funcionario: Funcionario):
        if not isinstance(funcionario, Funcionario):
            raise self.NotSocioException('Apenas funcionários podem ser adicionados a ramais.')
        if isinstance(funcionario, Socio):
            raise self.NotSocioException('Sócios não podem ser adicionados a ramais.')
        c.execute("SELECT funcionario_id FROM Ramal WHERE funcionario_id = ? AND reserva_id = ?",
                  (funcionario.id, self.__id,))
        if c.fetchone():
            raise self.AlreadyExistsException("O funcionário em questão já possui um Ramal nesta reserva.")
        c.execute("SELECT reserva_id FROM Ramal WHERE reserva_id = ?", (self.__id,))
        actual_length = len(c.fetchall())
        if actual_length >= self.sala.vagas:
            raise Sala.ExceedingLengthException('A quantidade de vagas na sala acabou.')
        c.execute("INSERT INTO Ramal (funcionario_id, reserva_id) VALUES (?,?)",
                  (funcionario.id, self.id,))
        conn.commit()

    def remove_funcionario(self, funcionario: Funcionario):
        if not isinstance(funcionario, Funcionario):
            raise self.NotSocioException('Apenas funcionários podem ser adicionados a ramais.')
        if isinstance(funcionario, Socio):
            raise self.NotSocioException('Sócios não podem ser adicionados a ramais.')
        c.execute("DELETE FROM Ramal WHERE funcionario_id = ? AND reserva_id = ?",
                  (funcionario.id, self.__id,))
        conn.commit()

    def get_all_funcionarios(self):
        """
        :return: ((id, name, role), ...,)
        """
        c.execute("""
            SELECT id, name, role FROM Funcionario WHERE id IN
            (SELECT funcionario_id FROM Ramal WHERE reserva_id = ?)
        """, (self.__id,))
        data = c.fetchall()
        return data

    def __repr__(self):
        return f'<Reserva {self.__id} {self.__socio} {self.__sala} {repr(self.horario)}>'

    class AlreadyExistsException(Exception):
        pass

    class NotSocioException(Exception):
        pass

    class NotFuncionarioException(Exception):
        pass

