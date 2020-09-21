import expensetrackerfortwo as ex
import argparse
from gooey import Gooey, GooeyParser
# https://docs.python.org/3/howto/argparse.html#id1
# https://github.com/chriskiehl/Gooey
# https://docs.python.org/3/library/argparse.html#sub-commands

@Gooey(program_name='Expense Tracker',
	   program_description='A handy tool to enter and track your living expenses.',
	   default_size=(700, 700)
)
def main():
	"""
	Collects command line arguments with GooeyParser and run functions
	from expensetrackkerfortwogui.

	Possible functions are entering a transaction (EnterExpense) and
	viewing expenses and expense breakdowns (ViewExpenses). 
	"""
	parser = GooeyParser()
	subparsers = parser.add_subparsers()	

	# create the parser and arguments for the "EnterExpense" command
	parser_enter = subparsers.add_parser('EnterExpense')
	parser_enter.add_argument("Name",
	                    help="Who paid for this expense?")
	parser_enter.add_argument("Amount",
	                    help="How much was the expense?",
	                    type=int)
	parser_enter.add_argument("Category",
	                    help="What type of expense was it?")
	parser_enter.add_argument("ExpenseDate",
						widget="DateChooser",
	                    help="What was the date of the expense?")
	parser_enter.set_defaults(func=ex.enterExpense)	

	# create the parser and arguments for the "View" command
	parser_view = subparsers.add_parser('ViewExpenses')
	parser_view.add_argument("DateRange",
						widget='Listbox',
						nargs='+',
						choices=['Last 7 days','Last 30 days','All time'],
						default='Last 30 days',
	                    help="Select the date range for expenses")
	parser_view.add_argument("Total",
						widget='Listbox',
						nargs='+',
						choices=['Yes','No'],
						default='Yes',
	                    help="View total expenses")
	parser_view.add_argument("Category",
						widget='Listbox',
						nargs='+',
						choices=['Yes','No'],
						default='Yes',
	                    help="View category breakdown of expenses")
	parser_view.add_argument("Person",
						widget='Listbox',
						nargs='+',
						choices=['Yes','No'],
						default='Yes',
	                    help="View per person breakdown of expenses")
	parser_view.set_defaults(func=ex.viewExpenses)	


	# parsing command line arguments and running functions
	args = parser.parse_args()
	args.func(args)
	

if __name__ == '__main__':
    main()
