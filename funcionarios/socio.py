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

