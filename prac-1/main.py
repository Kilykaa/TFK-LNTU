
CURRENT_YEAR = 2025

class Daniil:
    def __init__(self, name=None, surname=None, year=None):
        self.name = name
        self.surname = surname

        self.year = year

    def get_course(self):
        if self.year is None:
            return None

        age = CURRENT_YEAR - self.year

        if age < 18:
            return 0
        elif 18 <= age < 22:
            return age - 17
        else:
            return 4

    def get_list(self):
        return [self.name, self.surname]

student = Daniil(name='Daniil', surname='Chvyr', year=2007,)
print(student.get_list())
print(student.get_course())