import pandas as pd
from datetime import datetime, timedelta
import os

# default excel file path
saved_file = 'shared_expenses.xlsx'


def addTransactionInformation():
    """Ask for inputs regarding the transaction.
    Transaction information is stored in a dictionary 'inputs' and
    returned by the function.
    """
    transaction_person = input('Who paid? ')
    transaction_amount = int(input('How much was the transaction? '))
    transaction_category = input('What was the category of the transaction? ')
    check_today = input('Was the transaction today? y/n ')
    if check_today == 'y':
        transaction_date = str(datetime.today().strftime("%d-%m-%y"))
    else:
        transaction_date = input('Enter the transaction date (dd-mm-yy): ')
                
    inputs = {"Person":transaction_person,
              "Amount":transaction_amount,
              "Category":transaction_category,
              "Date":transaction_date}
    return inputs
                                   
def enterTransaction():
    """Add transaction information to Excel sheet through a Pandas df. 
    'Inputs' taken from addTransactionInformation(), which returns the
    needed dictionary to create a Pandas df.
    """                   
    raw = pd.read_excel(saved_file)              
    new = pd.DataFrame(addTransactionInformation(),
                      index=[0])
    export = raw.append(new, sort=True)
    export = export[['Date','Person','Amount','Category']]
    
    export.to_excel(saved_file)
    print('Transaction successfully entered!')


def specifyTimeFrame():
    """Create a mask that filters the df rows based on specified input.
    Standard input to choose is last 7 and 30 days. 
    User can also enter custom input for number of days back they want.
    Used as input in other functions."""
    df = pd.read_excel(saved_file)
    desired_date = int(input('Enter a number from 1-3 to look at your transactions for: \
                         \n (1) The last 7 days \
                         \n (2) The last 30 days \
                         \n (3) Custom \n'))    
    if desired_date == 1:
        days_ago_input = 7
    elif desired_date == 2:
        days_ago_input = 30
    elif desired_date == 3:
        days_ago_input = int(input('Enter how many days behind you want to see transactions for: '))
    # datetime values to use in filter calculation
    today = datetime.now()
    days_ago = datetime.now() - timedelta(days=days_ago_input)
    
    df['Date Object'] = pd.to_datetime(df['Date'], dayfirst=True, infer_datetime_format=True)
    mask = (df['Date Object'] > days_ago) & (df['Date Object'] <= today)
    
    return mask # usage is with loc -> df = df.loc[mask]


def viewAllByTime():
    """Looks at all transactions falling under the user specified time frame.
    Takes the mask created by specifyTimeFrame()"""
    raw = pd.read_excel(saved_file)
    desired_date = raw.loc[specifyTimeFrame()]
    desired_date = desired_date[['Date','Person','Amount','Category']]
    
    os.system('clear')
    print(desired_date) # only print out transactions that fit in date specified 

    
def viewCategoryByTime():
    """Looks at sum of all transactions per categories under the user specified time frame.
    Takes the mask created by specifyTimeFrame()"""
    raw = pd.read_excel(saved_file)
    grouped = raw.loc[specifyTimeFrame()] # take the desired date
    grouped = grouped[['Category','Amount']].groupby('Category').sum()
    
    os.system('clear')
    print(grouped) # print out transactions that fit in category and date specified
    

def viewPersonByTime():
    """Looks at sum of all transactions per person under the user specified time frame.
    Takes the mask created by specifyTimeFrame()"""
    raw = pd.read_excel(saved_file)
    grouped = raw.loc[specifyTimeFrame()] # take the desired date
    grouped = grouped[['Person','Amount']].groupby('Person').sum()
    
    os.system('clear')
    print(grouped_df) # print out transactions that fit in category and date specified
    

def viewDebt():
    """Look at who has paid more and what the difference is between the two.
    Display the name and the amount needed to pay."""
    raw = pd.read_excel(saved_file)
    debt_df = raw[['Person','Amount']].groupby('Person').sum() # groupby person to sum all transactions
    person = debt_df[debt_df['Amount']==int(debt_df.max())].index.values[0] # get name of person in debt
    amount_owed = int(debt_df.max()-debt_df.min()) # get amount by doing max - min
    
    os.system('clear')
    print(f"{person} owes: €{amount_owed}") # print out difference between max min and person name
    

def viewPerPersonSpending():
    """Look the expense per month per person if everything was even. (Total tranasction amount/ 2)
    Display the name and the amount needed to pay."""
    raw = pd.read_excel(saved_file)
    total_per_person = raw['Amount'].sum()/2 # take the total amount and divide it by two
    
    os.system('clear')
    print(f"The total spending per person is: €{total_per_person}") # print total / 2
