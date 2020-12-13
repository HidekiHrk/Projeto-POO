import sqlite3

conn = sqlite3.connect('data/data.db')
c = conn.cursor()


def create_tables():
    c.execute("PRAGMA foreign_keys = ON")
    c.execute("""
        CREATE TABLE IF NOT EXISTS Funcionario(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Sala(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            spaces INTEGER NOT NULL DEFAULT 0
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Reserva(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            socio_id INT,
            sala_id INT,
            horario TEXT,
            FOREIGN KEY (socio_id)
                REFERENCES Funcionario (id)
                ON DELETE SET NULL,
            FOREIGN KEY (sala_id)
                REFERENCES Sala (id)
                ON DELETE SET NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Ramal(
            funcionario_id INT,
            reserva_id INT,
            FOREIGN KEY (funcionario_id)
                REFERENCES Funcionario (id)
                ON DELETE SET NULL,
            FOREIGN KEY (reserva_id)
                REFERENCES Reserva (id)
                ON DELETE SET NULL
        )
    """)
    conn.commit()


create_tables()
