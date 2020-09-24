from datetime import date
from decimal import Decimal
class loan:
    def __init__(self,item,when,spending_amount,amount,interest,period,rent,rent_interest):
        self.item=item
        self.when=when  
        self.spending_amount=spending_amount
        self.amount=amount
        self.interest=interest
        self.period=period
        self.rent=rent
        self.rent_interest=rent_interest
        self.today_date=date.today().strftime("%d/%m/%Y")

    def loan_monthly_repay(self):
        rate_per_period=self.interest/1200.0
        a=rate_per_period*self.amount
        b=1-((1+rate_per_period)**(-self.period))
        loan_monthly_repay = float(a/b)
        return loan_monthly_repay

    def loan_total(self):
        total_loan_cost = self.loan_monthly_repay()
        return total_loan_cost*self.period

    def apply_interest(self):
        self.rent=self.rent*(1+(self.rent_interest/100))
