#this module contains functions that display data in CLI in proper format, check existence of accounts and input the type of action the user wants to perform

def display_title():
    ''' displays the title and information of bank '''

    print("-" * 80)
    print("|" + " " * 31 + "Skill Rank Bank" + " " * 32 + "|")
    print("|" + " "*30 + "Phone: 9800000000" + " "*31 + "|")
    print("|" + " "*20 + '"Fulfilling your Banking requirements"'+ " "*20 + "|")
    print("-" * 80, end = "\n")

def display_string(st):
    ''' displays any string passed in parameter with the app's standard '''
    
    rightSpaces = (77 - len(st)) 
    
    print("| " + st + " " * rightSpaces + "|")


def check_accounts():
    from account_ops import accounts, createAccount, accountActions
    if accounts:
        account_nums = len(accounts)
        if account_nums == 1:
            display_text = " Account"
        else: 
            display_text = " Accounts"
        display_string(str(account_nums) + display_text + " Found.")
        display_string("Press 1 to perform operations on an account.")
        display_string("Press 2 to create a new account")
        display_string("Press 3 to Quit the application")
        validChoice = False
        while not validChoice:
            choice = input("| Enter your choice: ")
            if(choice == '1'):
                print("-" * 80)
                accountActions()
                validChoice = True
            elif(choice == '2'):
                print("-" * 80)
                createAccount()
                validChoice = True
            elif (choice == '3'):
                return 'y'
            else: 
                display_string("Invalid choice.")
                validChoice = False
    else:
        display_string("No account found at the moment.")
        display_string("Press 1 to create a new accout.")
        display_string("Press 2 to quit the application.")
        validChoice = False
        while not validChoice:
            choice = input("| Enter your choice: ")
            if (choice == '1'):
                print("-" * 80)
                createAccount()
                validChoice = True
            elif (choice == '2'):
                return 'y'
            else:
                display_string("Invalid choice.")

    return 'n'