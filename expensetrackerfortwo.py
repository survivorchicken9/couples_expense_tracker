# create/connect to database
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

# hardcode input
with open("db_filepath.txt") as file: # Use file to refer to the file object
   db = file.read()

# all functions

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
    
    # tuple for SQL input
    inputs = (transaction_person,
              transaction_amount,
              transaction_category,
              transaction_date,)
    return inputs
                                   
def enterTransaction():
    """ Enter a transaction into the expense table """
    transaction = addTransactionInformation()
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""INSERT INTO Expenses(Person, Amount, Category, Date)
                 VALUES(?, ?, ?, ?); """, transaction)
    conn.commit() # autoincrement primary key built-in to commit
    conn.close()
    print(f"""Entry added: 
    Date: {transaction[0]}
    Amount: {transaction[1]}
    Person: {transaction[2]}
    Category: {transaction[3]}""")


def specifyTimeFrame():
    """Create a mask that filters the df rows based on specified input.
    Standard input to choose is last 7 and 30 days. 
    User can also enter custom input for number of days back they want.
    Used as input in other functions."""
    conn = sqlite3.connect(db)
    raw = pd.read_sql_query("Select * FROM Expenses ORDER BY Date", conn, index_col='ID')
    desired_date = int(input('Enter a number from 1-3 to look at your transactions for: \
                         \n (1) The last 7 days \
                         \n (2) The last 30 days \
                         \n (3) All time \
                         \n (4) Custom \n'))    
    if desired_date == 1:
        days_ago_input = 7
    elif desired_date == 2:
        days_ago_input = 30
    elif desired_date == 3:
        days_ago_input = 10000 # don't judge me it works
    elif desired_date == 4:
        days_ago_input = int(input('Enter how many days behind you want to see transactions for: '))
    # datetime values to use in filter calculation
    today = datetime.now()
    days_ago = datetime.now() - timedelta(days=days_ago_input)
    
    raw['Date Object'] = pd.to_datetime(raw['Date'], dayfirst=True, infer_datetime_format=True)
    mask = (raw['Date Object'] > days_ago) & (raw['Date Object'] <= today)
    
    return mask # usage is with loc -> df = df.loc[mask]


def viewAllByTime():
    """Looks at all transactions falling under the user specified time frame.
    Takes the mask created by specifyTimeFrame()"""
    conn = sqlite3.connect(db)
    raw = pd.read_sql_query("Select * FROM Expenses ORDER BY Date", conn, index_col='ID')
    desired_date = raw.loc[specifyTimeFrame()]
    desired_date = desired_date[['Date','Person','Amount','Category']] # filter columns for viewing
    
    os.system('clear')
    print(desired_date)

    
def viewCategoryByTime():
    """Looks at sum of all transactions per categories under the user specified time frame.
    Takes the mask created by specifyTimeFrame()"""
    conn = sqlite3.connect(db)
    raw = pd.read_sql_query("Select * FROM Expenses ORDER BY Date", conn, index_col='ID')
    grouped = raw.loc[specifyTimeFrame()] # take the desired date
    grouped = grouped[['Category','Amount']].groupby('Category').sum()
    
    os.system('clear')
    print(grouped) # print out transactions that fit in category and date specified
    

def viewPersonByTime():
    """Looks at sum of all transactions per person under the user specified time frame.
    Takes the mask created by specifyTimeFrame()"""
    conn = sqlite3.connect(db)
    raw = pd.read_sql_query("Select * FROM Expenses ORDER BY Date", conn, index_col='ID')
    grouped = raw.loc[specifyTimeFrame()] # take the desired date
    grouped = grouped[['Person','Amount']].groupby('Person').sum()
    
    os.system('clear')
    print(grouped) # print out transactions that fit in category and date specified
    

def viewDebt():
    """Look at who has paid more and what the difference is between the two.
    Display the name and the amount needed to pay."""
    conn = sqlite3.connect(db)
    raw = pd.read_sql_query("Select * FROM Expenses ORDER BY Date", conn, index_col='ID')
    debt_df = raw[['Person','Amount']].groupby('Person').sum() # groupby person to sum all transactions
    person = debt_df[debt_df['Amount']==int(debt_df.min())].index.values[0] # get name of person in debt
    amount_owed = int(debt_df.max()-debt_df.min()) # get amount by doing max - min
    
    os.system('clear')
    print(f"{person} owes: €{amount_owed}") # print out difference between max min and person name
    

def viewPerPersonSpending():
    """Look the expense per month per person if everything was even. (Total tranasction amount/ 2)
    Display the name and the amount needed to pay."""
    conn = sqlite3.connect(db)
    raw = pd.read_sql_query("Select * FROM Expenses ORDER BY Date", conn, index_col='ID')
    total_per_person = raw['Amount'].sum()/2 # take the total amount and divide it by two
    
    os.system('clear')
    print(f"The total spending per person is: €{total_per_person}") # print total / 2
