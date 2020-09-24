from Montlhy_deductions_class import monthly_item
from timeline_class import time
from loan_class import loan
import matplotlib.pyplot as plt
import numpy as np
from long_term_investments_class import longterm
import sys

def Individual_plot():
    ##############################timeline
    tiaan=time("23/04/1992",65,90)

    ###############################expense_monthly
    food = monthly_item("food", 3500, 2.6)
    petrol = monthly_item("petrol", 900, 10)
    water_elec = monthly_item("water_elec", 1200, 9)
    hobby = monthly_item("hobby", 800, 2)
    medical = monthly_item("medical", 1900, 2)
    insurance = monthly_item("insurance", 2000, 2)
    pension_young = monthly_item("pension",2500,2.0)
    internet = monthly_item("internet",350,2.0)
    phone= monthly_item("phone",400,2.0)
    vacation = monthly_item("vacation", 1000, 5.0)
   
    #################################long_term_expense
    house_exp = loan("loan",2024,2000000,1000000.0,10,240,2500.0,5.0)
    car_exp = loan("car",2027,300000,200000.0,8,120,0.0,0.0)
    car_exp_two = loan("bakkie",2037,350000,300000.0,8,120,0.0,0.0)
    car_exp_three = loan("bike",2047,400000,350000.0,8,120,0.0,0.0)

    mnth_expense=(food,petrol,water_elec,hobby,medical,insurance,pension_young,internet,phone,vacation)
    long_expense=(house_exp,car_exp,car_exp_two,car_exp_three)
    
    ##################################income
    salary = monthly_item("salary",18000,5.0)
    savings = monthly_item("savings",100000,5.0)
    long_term_investments = monthly_item("investments",440000,6.5)
    income_arr=(salary,savings,long_term_investments)

    ##################################before retirement
    calculations_before_retirement(tiaan,mnth_expense,long_expense,income_arr)
    

def calculations_before_retirement(tiaan,mnth_expense,long_expense,income_arr):
    #calculates and plots expenses and incomes until retirement
    ###################################calculate_expense_until_retirement
    expense_per_year=calculate_yearly_expense_until_retirement(mnth_expense,long_expense,tiaan)
    expense_all_items_per_year=yearly_expense(expense_per_year)
    ###################################calculate_income_until_retirement
    salary_per_year=yearly_item_amount(tiaan.years_before_retirement(),income_arr[0])
    profit_or_loss = yearly_savings_or_loss(expense_all_items_per_year,salary_per_year,income_arr[1])
    investments=yearly_item_amount(tiaan.years_before_retirement(),income_arr[2])
    
    ###################################plots before retirement
    monthly_cost_increase(expense_all_items_per_year,salary_per_year)
    diff_expense_plot(expense_per_year,mnth_expense,long_expense)
    yearly_expense_income_diff(expense_all_items_per_year,salary_per_year,profit_or_loss)
    diff_income(profit_or_loss,salary_per_year,investments)
    plt.show()


def calculate_yearly_expense_until_retirement(short_term_expense,long_term_expense,person):
    #calculates the yearly expenses for all items until retirement
    expense_per_year=[0]*(len(short_term_expense)+len(long_term_expense))
    for i in range(len(short_term_expense)):
        expense_per_year[i] = yearly_item_amount(person.years_before_retirement(),short_term_expense[i])
    for i in range(len(short_term_expense),len(expense_per_year)):
        expense_per_year[i] = loan_yearly_calc(long_term_expense[i-len(short_term_expense)],person)

    return expense_per_year

def loan_yearly_calc(loan_item,time_item):
    #calculates how much you have to repay monthly for a loan
    loan_mnthly_arr=[0]*(time_item.years_before_retirement())
    rent_stop=loan_item.when - time_item.current_year()
    loan_stop=int(loan_item.period/12)
    for i in range (rent_stop):
        loan_mnthly_arr[i]=loan_item.rent*12
        loan_item.apply_interest()
    for i in range(rent_stop,rent_stop+loan_stop):
        loan_mnthly_arr[i]=loan_item.loan_monthly_repay()*12
    return loan_mnthly_arr

def yearly_item_amount(how_many_years,item):
    #calculates the yearly amount for an item
    mnth_expense=[0]*how_many_years
    for i in range(how_many_years):
        mnth_expense[i]=item.yearly_cost()
        item.apply_interest()
    return mnth_expense

def yearly_expense(expense):
    #calculates the yearly amount for all expense items
    item_loop=len(expense)
    yearly_loop=len(expense[0])
    yearly_expense=[0]*yearly_loop
    for i in range(item_loop):
        for j in range(yearly_loop):
            yearly_expense[j]+= expense[i][j]
    return yearly_expense

def yearly_savings_calc(savings,expense,salary):
    #calculates the yearly profit_or_loss
    yearly_loop=len(salary)
    savings_amount=yearly_expense(expense)
    for i in range(yearly_loop):
        if i==0:
            savings_amount[i]=(savings.amount + salary[i] - savings_amount[i])*(1.0+(savings.interest_rate/100))
        else:
            savings_amount[i]=(savings_amount[i-1]+ salary[i] - savings_amount[1])*(1.0+(savings.interest_rate/100))
    return savings_amount

def monthly_cost_increase(expense, salary):
    #monthly income and expenses
    yearly_loop=len(salary)
    mnthly_expense_plot=[0]*yearly_loop
    income=[0]*yearly_loop
    for i in range(yearly_loop):
        income[i]=(salary[i]/12)
        mnthly_expense_plot[i]=expense[i]/12

    plt.figure(1)
    plt.plot(mnthly_expense_plot,label='expense')
    plt.plot(income,label='income')
    plt.title("The monthly income-expense graph")
    plt.legend()
    
def diff_expense_plot(expense,short_term_item,long_term_item):
    #plots the different expense items
    short_item_loop=len(short_term_item)
    total_item_loop=len(expense)
    plt.figure(2)
    for i in range(short_item_loop): 
        plt.plot(expense[i],label=short_term_item[i].item)
    for i in range(short_item_loop,total_item_loop):
        plt.plot(expense[i],label=long_term_item[i-short_item_loop].item)
    plt.title("The different monthly expenses")
    plt.legend()

def yearly_expense_income_diff(expense,salary, overall):
    #plots the different income, expense and overall profit/loss
    plt.figure(3)
    plt.plot(expense,label='expense')
    plt.plot(salary,label='income')
    plt.plot(overall,label='overall')
    plt.title("The yearly income-expense graph")
    plt.legend()

def yearly_savings_or_loss(expense,salary, savings):
    #calculates the different income, expense and overall profit/loss
    yearly_loop=len(salary)
    overall=[0]*yearly_loop
    overall[0]=savings.amount
    for i in range(yearly_loop):
        if i == 0:
            overall[i]=overall[i] + salary[i] - expense[i]
        else:
            overall[i]=overall[i-1]*(1+(savings.interest_rate/100))+salary[i] - expense[i]
    return overall

def diff_income(overall,salary,investments):
    #plots the different income streams
    plt.figure(4)
    plt.plot(overall,label='profit or loss')
    plt.plot(salary,label='salary')
    plt.plot(investments,label='investments')
    plt.title("The different income streams")
    plt.legend()

if __name__ == '__main__':
    Individual_plot()