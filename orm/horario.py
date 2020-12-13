

class Horario:
    def __init__(self, day: int, month: int, hour: int):
        ranges = (
            (hour, 'As horas', 24),
            (month, 'Os meses', 13),
            (day, 'Os dias', 32 if month != 2 else 29)
        )
        for value, name, vrange in ranges:
            if value not in range(1, vrange):
                raise self.TimeException(f'{name} precisam estar entre 1 e {vrange-1}')
        self.hour = hour
        self.month = month
        self.day = day

    def timestring(self):
        return f'{self.day}.{self.month}.{self.hour}'

    def __str__(self):
        return self.timestring()

    def __repr__(self):
        return f'{self.day}/{self.month} {self.hour}h'

    @staticmethod
    def get_by_timestring(timestring: str):
        return Horario(*timestring.split('.'))

    class TimeException(Exception):
        pass
