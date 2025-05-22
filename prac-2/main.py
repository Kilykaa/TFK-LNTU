CURRENT_YEAR = 2025

class Human:
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

class Student(Human):
    def __init__(self, name=None, surname=None, year=None, course=1, mediane_score=0.0, reputation=0): # reputation like China ^^
        super().__init__(name, surname, year)
        self.course = course
        self.mediane_score = mediane_score
        self.reputation = reputation

    def _add_reputation(self, value):
        if self.mediane_score is None:
            self.mediane_score = 0
        self.reputation += value * (self.mediane_score / 5)

    def check_reputation(self):
        self._add_reputation((5*self.course)*2)
        if self.reputation >= 80:
            return "respect"
        elif self.reputation >= 50:
            return "ok"
        elif self.reputation >= 20:
            return "looser"
        else:
            return ";-;"

s = Student(name="Daniil", surname="Chvyr", year=2004, course=2, mediane_score=4.5)
print(s.reputation)
print(s.check_reputation())
print(s.reputation)
print(s.check_reputation())