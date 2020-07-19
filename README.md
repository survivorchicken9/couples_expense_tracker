# Expense tracking for couples

This is a basic expense tracker for couples. To begin using it, run "main.py". You will be prompted to input the person who paid, the date of the transaction, the amount of the transaction, and the category of the transaction. This information is then written into an SQLite database. 

Please create a text file called "db_filepath.txt" and place the full filepath of your SQLite database in it.

All existing functionality can be found in the "expensetrackerfortwo.py" file.

Currently, features include:

- Entering a transaction
- Viewing transactions grouped by category
- Viewing who is in debt (who has spent less)
- View the "per person spending" if spending were equal (total spending / 2)

Use "pip install -r requirements.txt" to get the packages required.