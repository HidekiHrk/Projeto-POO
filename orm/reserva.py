from funcionarios.funcionario import Funcionario
from orm.db import c, conn


class Reserva:
    def __init__(self, reserva_id: int, socio: 'Socio', sala: 'Sala', horario: 'Horario'):
        self.__id = reserva_id
        self.__socio = socio
        self.__sala = sala
        self.__horario = horario
        # get reserva by id

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

    def create(self, socio: 'Socio', sala: 'Sala', horario: 'Horario'):
        # check if another reserva with same socio/sala/horario parameters already exists.
        c.execute(
            "SELECT id FROM Reserva WHERE (socio_id = ? OR sala_id = ?) AND horario = ?",
            (socio.id, sala.id, str(horario),)
        )
        if c.fetchone():
            raise self.AlreadyExistsException(
                "Uma reserva já foi feita nesta combinação de sócio/sala e horário.")
        c.execute("INSERT INTO Reserva (socio_id, sala_id, horario) (?,?,?)",
                  (socio.id, sala.id, str(horario),))
        this_id = c.lastrowid
        conn.commit()
        return Reserva(this_id, socio, sala, horario)

    def get_by(self, field_name: str) -> 'Reserva':
        """
        :param field_name: id | socio_id | sala_id | horario
        :return: orm.reserva.Reserva
        """
        pass

    def add_funcionario(self, funcionario: Funcionario):
        c.execute("SELECT funcionario_id FROM Ramal WHERE funcionario_id = ?, reserva_id = ?",
                  (funcionario.id, self.__id,))
        if c.fetchone():
            raise self.AlreadyExistsException("O funcionário em questão já possui um Ramal nesta reserva.")
        c.execute("INSERT INTO Ramal (funcionario_id, reserva_id) (?,?)",
                  (funcionario.id, self.id,))
        conn.commit()

    class AlreadyExistsException(Exception):
        pass
