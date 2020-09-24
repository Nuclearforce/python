from datetime import date
class longterm:
    def __init__(self,monthly_amount,interest,retire_age,birth_date,death_age):
        self.monthly_amount=monthly_amount
        self.interest=interest
        self.retire_age=retire_age
        self.birth_date=birth_date
        self.today_date=date.today().strftime("%d/%m/%Y")
        self.death_age=death_age

    def pension_total(self):
        years_missed = int(self.today_date.split("/")[2]) - int(self.birth_date.split("/")[2])
        period= (int(self.retire_age) - years_missed)
        pension_total=0
        for i in range(period):
            pension_total+=self.monthly_amount*12
            self.monthly_amount=self.monthly_amount*(1+self.interest/100)
        return pension_total

    def investment_calc(self):
        self.monthly_amount=self.monthly_amount*(1+(self.interest/100))
        return self.monthly_amount
