from datetime import date
class time:
    def __init__(self,date_of_birth,retire_age,death_age):
        self.date_of_birth=date_of_birth
        self.retire_age=retire_age
        self.death_age=death_age
        self.today_date=date.today().strftime("%d/%m/%Y")

    def years_before_retirement(self):
        years_missed = int(self.today_date.split("/")[2]) - int(self.date_of_birth.split("/")[2])
        return int(self.retire_age) - years_missed

    def years_after_retirement(self):
        return int(self.death_age) - int(self.retire_age)

    def current_year(self):
        return int(self.today_date.split("/")[2])

    def lifetime(self):
        years_missed = int(self.today_date.split("/")[2]) - int(self.date_of_birth.split("/")[2])
        return int(self.death_age) - years_missed