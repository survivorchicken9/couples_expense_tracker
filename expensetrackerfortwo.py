# create/connect to database
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

# hardcode input
with open("db_filepath.txt") as file: # Use file to refer to the database file object
   db = file.read()

# all function
def enterExpense(args):
	# formatting date
	edited_date = datetime.fromisoformat(args.ExpenseDate) # convert to datetime object
	edited_date = str(edited_date.strftime("%d-%m-%y")) # reformat for SQL input
	# tuple for SQL input
	inputs = (edited_date, args.Amount, args.Name, args.Category,)
	# SQL execution
	conn = sqlite3.connect(db)
	c = conn.cursor()
	c.execute("""INSERT INTO Expenses(Date, Amount, Person, Category)
            	 VALUES(?, ?, ?, ?); """, inputs)
	conn.commit() # autoincrement primary key built-in to commit
	conn.close()

	print(f"Added: {inputs}")
	return inputs

def viewExpenses(args):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query("Select * FROM Expenses", conn, index_col='ID')

    date_selection = args.DateRange[0]
    if date_selection=='Last 7 days':
    	date_selection = 7
    elif date_selection=='Last 30 days':
    	date_selection = 30
    else:
    	date_selection = 10000
    today = datetime.now()
    days_ago = today - timedelta(days=date_selection)

    df['Date Object'] = pd.to_datetime(df['Date'], dayfirst=True, infer_datetime_format=True)
    df = df.loc[(df['Date Object'] > days_ago) & (df['Date Object'] <= today)]

    # stuff to show
    if args.Total[0]=='Yes':
    	print('Total Spending:')
    	print(df['Amount'].sum())
    	print()

    if args.Category[0]=='Yes':
    	print('Category Spending:')
    	print(df.groupby('Category').sum().to_markdown())
    	print()

    if args.Person[0]=='Yes':
    	print('Per Person Spending:')
    	print(df.groupby('Person').sum().to_markdown())
    	print()

    return 0
