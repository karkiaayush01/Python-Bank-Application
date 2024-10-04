#this module contains functions regarding account operations such as creating account, validating user input, and performing actions on accounts

from operations import display_string

class Account:
    def __init__(self, username, pincode, current_balance):
        self.username = username
        self.pincode = pincode
        self.current_balance = current_balance


accounts = {} #initial account dictionary.

def inputUsername():
    ''' this function helps to get a valid username '''
    validUsername = False
    while not validUsername:
        username = input("| Create a username: ")
        if (len(username) < 4):
            display_string("Username should be at least 4 characters.")
        else:
            validUserName = True
            return username

def inputPincode():
    ''' this function helps to get a valid 4 digit pincode '''
    validPincode = False
    while not validPincode:
        try:
            pincode = input("| Create a four digit pin: ")
            if(len(pincode) != 4):
                display_string("Pincode should be 4 digit long.")  
            else:
                intPincode = int(pincode)
                validPincode = True
                return pincode
        except ValueError:
            display_string("Enter only numbers.")

def inputBalance(prompt):
    ''' this function helps to get a valid balance amount '''
    validAmt = False
    while not validAmt:
        try:
            deposit_amt = float(input("| " + prompt + ": "))
            if(deposit_amt < 0):
                display_string("Amount should be greater than 0.")
            else:
                validAmt = True
                return deposit_amt
        except ValueError:
            display_string("Invalid amount.")



def createAccount():
    ''' this function helps to create an account '''
    username = inputUsername()
    pincode = inputPincode()
    deposit_amt = inputBalance("Enter starting balance amount")
    
    accounts[username] = Account(username, pincode, deposit_amt)
    display_string("Account successfully created.")
    print("-" * 80)



def accountActions():
    ''' this function performs operations on existing accounts '''
    username = input("| Enter username: ")
    if username in accounts:
        current_user = accounts[username]
        pincode = input("| Enter pincode: ")
        if (pincode == current_user.pincode):
            display_string("User Validated.")
            print("-" * 80)
            loggedIn = True
            while loggedIn:
                display_string("Press 1 to check your balance.")
                display_string("Press 2 to withdraw balance.")
                display_string("Press 3 to deposit balance.")
                display_string("Press 4 to log out.")
                validChoice = False
                while not validChoice:
                    choice = input("| Enter your choice: ")
                    if(choice == '1'):
                        print("-" * 80)
                        checkBalance(current_user)
                        validChoice = True
                    elif(choice == '2'):
                        print("-" * 80)
                        withdrawBalance(current_user)
                        validChoice = True
                    elif (choice == '3'):
                        print("-" * 80)
                        depositBalance(current_user)
                        validChoice = True
                    elif (choice == '4'):
                        display_string("Logged out successfully.")
                        print("-" * 80)
                        loggedIn = False
                        validChoice = True
                    else: 
                        display_string("Invalid choice.")
                        validChoice = False
        else:
            display_string("Username or pincode don't match.")
            print("-" * 80)
    else: 
        display_string("Username not found. Please try again.")
        print("-") * 80

def checkBalance(user):
    display_string("Your current balance is Rs. " + str(round(user.current_balance,2)))
    print("-" * 80)

def withdrawBalance(user):
    balance_amount = inputBalance("Enter the withdrawal amount")
    if balance_amount > user.current_balance:
        display_string("Requested amount exceeds current balance. Please try again.")
    else:
        user.current_balance -= balance_amount
        display_string("Withdrawal successful. Current Balance is Rs. " + str(round(user.current_balance, 2)))
    
    print("-" * 80)

def depositBalance(user):
    balance_amount = inputBalance("Enter the deposit amount")
    user.current_balance += balance_amount
    display_string("Deposit successful. Current balance is Rs. " + str(round(user.current_balance, 2)))
    print("-" * 80)
