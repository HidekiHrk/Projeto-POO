from abc import ABC
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

    def delete(self):
        c.execute("DELETE FROM Funcionario WHERE id = ?", (self.id,))
        conn.commit()
        c.execute("DELETE FROM Ramal WHERE funcionario_id IS NULL")
        conn.commit()

    @classmethod
    def get_role(cls):
        return cls.__name__

    @classmethod
    def create(cls, name: str):
        c.execute("INSERT INTO Funcionario (name, role) (?,?)",
                  (name, cls.get_role(),))
        this_id = c.lastrowid
        conn.commit()
        return cls(name, this_id)

    @classmethod
    def get(cls, funcionario_id: int):
        c.execute("SELECT name FROM Funcionario WHERE id = ? AND role = ?",
                  (funcionario_id, cls.get_role(),))
        query_obj = c.fetchone()
        if query_obj:
            name = query_obj[0]
            return cls(name, funcionario_id)
        raise cls.NotFoundException(f'O usuário de id {funcionario_id} não existe.')

    @classmethod
    def get_all(cls):
        c.execute("SELECT name, id FROM Funcionario WHERE role = ?",
                  (cls.get_role(),))
        query_list = c.fetchall()
        funcionarios = []
        for query in query_list:
            funcionarios.append(cls(*query))

    class NotFoundException(Exception):
        pass
