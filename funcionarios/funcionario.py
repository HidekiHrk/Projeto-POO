from abc import ABC, abstractmethod
from orm.db import c, conn


class Funcionario(ABC):
    def __init__(self, name: str, funcionario_id: int):
        self.__name = name
        self.__id = funcionario_id

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @classmethod
    def create(cls, name: str):
        role = cls.__name__
        c.execute("INSERT INTO Funcionario (name, role) (?,?)", (name, role,))
        this_id = c.lastrowid
        conn.commit()
        return Funcionario(name, this_id)

    @classmethod
    def get(cls, funcionario_id: int):
        role = cls.__name__
        c.execute("SELECT name FROM Funcionario WHERE id = ? AND role = ?", (funcionario_id, role,))
        query_obj = c.fetchone()
        if query_obj:
            name = query_obj[0]
            return Funcionario(name, funcionario_id)
        raise cls.NotFoundException(f'O usuário de id {funcionario_id} não existe.')

    @abstractmethod
    def get_reservas(self, *ids: int):
        pass

    class NotFoundException(Exception):
        pass
