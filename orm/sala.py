from orm.db import c, conn


class Sala:
    def __init__(self, sala_id: int, vagas: int):
        self.__id = sala_id
        self.__vagas = vagas

    @property
    def id(self):
        return self.__id

    @property
    def vagas(self):
        return self.__vagas

    @classmethod
    def create(cls, vagas: int):
        c.execute("INSERT INTO Sala (spaces) (?)", (vagas,))
        this_id = c.lastrowid
        conn.commit()
        return Sala(this_id, vagas)

    @classmethod
    def get(cls, sala_id: int):
        c.execute("SELECT id, spaces FROM Sala WHERE id = ?", (sala_id,))
        data = c.fetchone()
        if data:
            return Sala(*data)
        raise cls.NotFoundException("Sala não encontrada")

    @classmethod
    def get_all(cls):
        c.execute("SELECT id, spaces FROM Sala")
        salas = map(lambda d: Sala(*d), c.fetchall())
        return salas

    def delete(self):
        c.execute("DELETE FROM Sala WHERE id = ?", (self.__id,))
        conn.commit()
        c.execute("DELETE FROM Reserva WHERE sala_id IS NULL")
        conn.commit()
        c.execute("DELETE FROM Ramal WHERE reserva_id IS NULL")
        conn.commit()

    class NotFoundException(Exception):
        pass

    class ExceedingLengthException(Exception):
        pass
