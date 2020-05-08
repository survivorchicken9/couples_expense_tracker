import expensetrackerfortwo as ex


def get_int(prompt):
    """Making sure the input for asking for which function to call is an integer. 
    Prompts for re-entry if non-integer value is entered."""
    while True:
        try:
            value = int(input(prompt))
            if value not in [int(i) for i in range(1,8)]:
                raise ValueError
        except ValueError:
            print("That doesn't work. Please enter a valid number from 1-7")
            continue
        else:
            break
    return value

# Text for function call for use in get_int()
ask_for_input = '\n What would you like to do? \
               \n (1) Enter a transaction \
               \n (2) View all transactions \
               \n (3) View transactions grouped by category \
               \n (4) View transactions grouped by person \
               \n (5) View who owes who \
               \n (6) View the per person spending (total / 2) \
               \n (7) Exit \n'

# Begin the calls
if __name__ == "__main__":
    print('Greetings, master. \n')
    while True:
        top_of_loop = get_int(ask_for_input)
        if top_of_loop == 1:
            ex.enterTransaction()
            continue
        elif top_of_loop == 2:
            ex.viewAllByTime()
            continue
        elif top_of_loop == 3:
            ex.viewCategoryByTime()
            continue
        elif top_of_loop == 4:
            ex.viewPersonByTime()
            continue
        elif top_of_loop ==5:
            ex.viewDebt()
            continue
        elif top_of_loop == 6:
            ex.viewPerPersonSpending()
            continue
        elif top_of_loop == 7:
            print('\n Farewell. May the force be with you.')
            break