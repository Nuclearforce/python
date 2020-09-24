class monthly_item:
    def __init__(self,item,amount, interest_rate):
        self.item=item
        self.interest_rate=interest_rate
        self.amount=amount

    def expense(self):#gives current state of expense
        print(self.item + " increasing at: " + str(self.interest_rate) + "% per year")

    def apply_interest(self): #applies interest and increases amount
        self.amount=self.amount*(1+(self.interest_rate/100))

    def yearly_cost(self):
        return self.amount*12