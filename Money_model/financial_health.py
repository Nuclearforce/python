from Montlhy_deductions_class import monthly_item
from timeline_class import time
from loan_class import loan
import matplotlib.pyplot as plt
import numpy as np
from long_term_investments_class import longterm
import sys

def Individual_plot(retirement):
    ##############################timeline
    tiaan=time("23/04/1992",65,90)

    ###############################expense_monthly
    food = monthly_item("food", 3500, 2.6)
    petrol = monthly_item("petrol", 900, 7)
    water_elec = monthly_item("water_elec", 1200, 7)
    hobby = monthly_item("hobby", 800, 2)
    medical = monthly_item("medical", 1900, 2)
    insurance = monthly_item("insurance", 2000, 2)
    pension_young = monthly_item("pension",3500,2.0)
    internet = monthly_item("internet",350,2.0)
    phone= monthly_item("phone",400,2.0)
    vacation = monthly_item("vacation", 1000, 5.0)
   
    #################################long_term_expense
    house_exp = loan("loan",2025,2000000,1000000.0,10.0,240.0,2500.0,5.0)
    car_exp = loan("car",2032,300000,200000.0,8,120,0.0,0.0)
    car_exp_two = loan("bakkie",2039,350000,300000.0,8,120,0.0,0.0)
    car_exp_three = loan("bike",2045,400000,350000.0,8,120,0.0,0.0)

    mnth_expense=(food,petrol,water_elec,hobby,medical,insurance,pension_young,internet,phone,vacation)
    long_expense=(house_exp,car_exp,car_exp_two,car_exp_three)
    
    ##################################income
    salary = monthly_item("salary",18000,5.0)
    savings = monthly_item("savings",100000,2.0)
    long_term_investments = longterm(440000,6,tiaan.retire_age,tiaan.date_of_birth,tiaan.death_age)
    pension=longterm(mnth_expense[5].amount,12,tiaan.retire_age,tiaan.date_of_birth,tiaan.death_age)
    income_arr=(salary,savings,long_term_investments,pension)

    ##################################before retirement
    calculations_before_retirement(tiaan,mnth_expense,long_expense,income_arr,retirement)
    

def calculations_before_retirement(tiaan,mnth_expense,long_expense,income_arr,retirement):
    #calculates and plots expenses and incomes until retirement
    ###################################calculate_expense_until_retirement
    expense_per_year=calculate_yearly_expense_until_retirement(mnth_expense,long_expense,tiaan)
    expense_all_items_per_year=yearly_expense(expense_per_year)
    ###################################calculate_income_until_retirement
    
    salary_per_year=yearly_item_amount(income_arr[0],tiaan)
    pension_payments=pension_monthly_calc(income_arr[3],tiaan)  
    profit_or_loss = yearly_savings_or_loss(expense_all_items_per_year,salary_per_year,income_arr[1],pension_payments)
    investments=investment_growth_per_year(income_arr[2],tiaan)
    
    
    ###################################plots before retirement
    monthly_cost_increase(expense_all_items_per_year,salary_per_year,pension_payments,tiaan,retirement)
    diff_expense_plot(expense_per_year,mnth_expense,long_expense,tiaan,retirement)
    yearly_expense_income_diff(expense_all_items_per_year,salary_per_year,profit_or_loss,pension_payments,tiaan,retirement)
    diff_income(profit_or_loss,salary_per_year,investments,pension_payments,tiaan,retirement)
    plt.show()

def investment_growth_per_year(investment,person):
    investment_arr=[0]*person.lifetime()
    for i in range(person.lifetime()):
        investment_arr[i]=investment.investment_calc()
    return investment_arr
 
def pension_monthly_calc(pension,person):
    pension_payments=pension.pension_total()/person.years_after_retirement()
    pension_arr=[0]*person.lifetime()
    for i in range(person.years_before_retirement(), person.lifetime()):
        pension_arr[i]=pension_payments
    return pension_arr

def calculate_yearly_expense_until_retirement(short_term_expense,long_term_expense,person):
    #calculates the yearly expenses for all items until retirement
    expense_per_year=[0]*(len(short_term_expense)+len(long_term_expense))
    for i in range(len(short_term_expense)):
        expense_per_year[i] = yearly_item_amount(short_term_expense[i],person)
    for i in range(len(short_term_expense),len(expense_per_year)):
        expense_per_year[i] = loan_yearly_calc(long_term_expense[i-len(short_term_expense)],person)

    return expense_per_year

def loan_yearly_calc(loan_item,time_item):
    #calculates how much you have to repay monthly for a loan
    loan_mnthly_arr=[0]*(time_item.lifetime())
    rent_stop=loan_item.when - time_item.current_year()
    loan_stop=int(loan_item.period/12)
    for i in range (rent_stop):
        loan_mnthly_arr[i]=loan_item.rent*12
        loan_item.apply_interest()
    for i in range(rent_stop,rent_stop+loan_stop):
        loan_mnthly_arr[i]=loan_item.loan_monthly_repay()*12
    return loan_mnthly_arr

def yearly_item_amount(item,tiaan):
    #calculates the yearly amount for an item
    how_many_years=tiaan.lifetime()
    mnth_expense=[0]*how_many_years
    for i in range(how_many_years):
        if i<int(tiaan.years_before_retirement()):
            mnth_expense[i]=item.yearly_cost()
            item.apply_interest()
        else:
            if item.item == "pension":
                mnth_expense[i]=0
            elif item.item == "insurance":
                mnth_expense[i]=0
            elif item.item == "petrol":
                mnth_expense[i]=item.yearly_cost()*0.6
                item.apply_interest()
            elif item.item == "water_elec":
                mnth_expense[i]=item.yearly_cost()*0.6
                item.apply_interest()
            elif item.item == "salary":
                mnth_expense[i]=0
            else:
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

def monthly_cost_increase(expense, salary,pension_payments,person,retired):
    #monthly income and expenses
    if retired==0:
        arr_len=person.years_before_retirement()
    elif retired==1:
        arr_len=person.years_after_retirement()
    else:
        arr_len=person.lifetime()
    before_retire=person.years_before_retirement()
    after_retire=person.lifetime()
    mnthly_expense_plot=[0]*arr_len
    income=[0]*arr_len
    if retired==0:
        for i in range(before_retire):
            income[i]=(salary[i]/12)
            mnthly_expense_plot[i]=expense[i]/12
    elif retired==1:
        for i in range(before_retire,after_retire):
            income[i-before_retire]=(salary[i]/12)+pension_payments[i]/12
            mnthly_expense_plot[i-before_retire]=expense[i]/12
    else:
        for i in range(after_retire):
            income[i]=(salary[i]/12)+pension_payments[i]/12
            mnthly_expense_plot[i]=expense[i]/12

    plt.figure(1)
    plt.plot(mnthly_expense_plot,label='expense')
    plt.plot(income,label='income')
    plt.title("The monthly income-expense graph")
    plt.legend()
    
def diff_expense_plot(expense,short_term_item,long_term_item,person,retired):
    #plots the different expense items
    if retired==0:
        arr_len=person.years_before_retirement()
    elif retired==1:
        arr_len=person.years_after_retirement()
    else:
        arr_len=person.lifetime()
    plot_expense=[0]*len(expense)
    for i in range(len(expense)):
        plot_expense[i]=[0]*arr_len

    before_retire=person.years_before_retirement()
    after_retire=person.lifetime()
    if retired==0:
        for i in range(len(expense)):
            for j in range(before_retire):
                plot_expense[i][j]=expense[i][j]
    elif retired==1:
        for i in range(len(expense)):
            for j in range(before_retire,after_retire):
                plot_expense[i][j-before_retire]=expense[i][j]        
    else:
        for i in range(len(expense)):
            for j in range(after_retire):
                plot_expense[i][j]=expense[i][j]
    short_item_loop=len(short_term_item)
    total_item_loop=len(expense)
    plt.figure(2)
    for i in range(short_item_loop): 
        plt.plot(plot_expense[i],label=short_term_item[i].item)
    for i in range(short_item_loop,total_item_loop):
        plt.plot(plot_expense[i],label=long_term_item[i-short_item_loop].item)
    plt.title("The different monthly expenses")
    plt.legend()

def yearly_expense_income_diff(expense,salary, overall,pension_payments,person,retired):
    #plots the different income, expense and overall profit/loss
    if retired==0:
        arr_len=person.years_before_retirement()
    elif retired==1:
        arr_len=person.years_after_retirement()
    else:
        arr_len=person.lifetime()
    plot_expense=[0]*arr_len
    plot_salary=[0]*arr_len
    plot_overall=[0]*arr_len
    before_retire=person.years_before_retirement()
    after_retire=person.lifetime()
    #print(salary)
    
    if retired==0:
        for i in range(before_retire):
            plot_expense[i]=expense[i]
            plot_salary[i]=salary[i]
            plot_overall[i]=overall[i]
    elif retired==1:
        for i in range(before_retire,after_retire):
            plot_expense[i-before_retire]=expense[i]
            plot_salary[i-before_retire]=salary[i]+pension_payments[i]
            plot_overall[i-before_retire]=overall[i]
    else:
        for i in range(after_retire):
            plot_expense[i]=expense[i]
            plot_salary[i]=salary[i]+pension_payments[i]
            plot_overall[i]=overall[i]
    plt.figure(3)
    plt.plot(plot_expense,label='expense')
    plt.plot(plot_salary,label='income')
    plt.plot(plot_overall,label='overall')
    plt.title("The yearly income-expense graph")
    plt.legend()

def yearly_savings_or_loss(expense,salary, savings,pension):
    #calculates the different income, expense and overall profit/loss
    yearly_loop=len(salary)
    overall=[0]*yearly_loop
    overall[0]=savings.amount
    for i in range(yearly_loop):
        if i == 0:
            overall[i]=overall[i] + salary[i] - expense[i] + pension[i]
        else:
            overall[i]=overall[i-1]*(1+(savings.interest_rate/100))+salary[i] - expense[i] + pension[i]
    return overall

def diff_income(overall,salary,investments,pension_payments,person,retired):
    #plots the different income streams
    if retired==0:
        arr_len=person.years_before_retirement()
    elif retired ==1:
        arr_len=person.years_after_retirement()
    else:
        arr_len=person.lifetime()
    plot_overall=[0]*arr_len
    plot_salary=[0]*arr_len
    plot_investments=[0]*arr_len
    plot_pension=[0]*arr_len
    plot_all_incomes_added=[0]*arr_len
    before_retire=person.years_before_retirement()
    after_retire=person.lifetime()
    
    if retired==0:
        for i in range(before_retire):
            plot_overall[i]=overall[i]
            plot_salary[i]=salary[i]
            plot_investments[i]=investments[i]
            plot_all_incomes_added[i]=overall[i]+salary[i]+investments[i]
    elif retired==1:
        for i in range(before_retire,after_retire):
            plot_overall[i-before_retire]=overall[i]
            plot_salary[i-before_retire]=salary[i]
            plot_pension[i-before_retire]=pension_payments[i]
            plot_investments[i-before_retire]=investments[i]
            plot_all_incomes_added[i-before_retire]=overall[i]+salary[i]+investments[i]
    else:
        for i in range(after_retire):
            plot_overall[i]=overall[i]
            plot_salary[i]=salary[i]
            plot_pension[i]=pension_payments[i]
            plot_investments[i]=investments[i]
            plot_all_incomes_added[i]=overall[i]+salary[i]+investments[i]

    plt.figure(4)
    plt.plot(plot_overall,label='profit or loss')
    plt.plot(plot_salary,label='salary')
    plt.plot(plot_investments,label='investments')
    plt.plot(plot_pension,label='pension')
    plt.plot(plot_all_incomes_added,label='all income sources')
    plt.title("The different income streams")
    plt.legend()

if __name__ == '__main__':
    retirement=2 #0 = working, 1=retired, 2=lifetime
    Individual_plot(retirement)