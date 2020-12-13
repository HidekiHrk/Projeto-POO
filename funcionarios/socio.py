from orm.db import c, conn
from funcionarios.funcionario import Funcionario


class Socio(Funcionario):
    def delete(self):
        c.execute("DELETE FROM Funcionario WHERE id = ?", (self.id,))
        conn.commit()
        c.execute("DELETE FROM Reserva WHERE socio_id IS NULL")
        conn.commit()
        c.execute("DELETE FROM Ramal WHERE reserva_id IS NULL")
        conn.commit()

    def get_info(self):
        return f"Sócio\nNome: {self.name}\nID no banco de dados: {self.id}"

    def __str__(self):
        return self.get_info()

    def __repr__(self):
        return self.get_info()
