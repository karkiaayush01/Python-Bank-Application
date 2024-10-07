#this module contains functions regarding account operations such as creating account, validating user input, and performing actions on accounts

from operations import display_string
import csv

class Account:
    def __init__(self, username, pincode, current_balance):
        self.username = username
        self.pincode = pincode
        self.current_balance = current_balance

def addToDatabase(account):
    is_first_record = False

    if len(accounts) == 1: #checking if this is the 1st account in the database
        is_first_record = True

    newAccount = [account.username, account.pincode, str(account.current_balance)]
    with open('accounts.csv', mode='a', newline='') as file: #using newline as '' because csv writer leaves a newline by default. It prevents a blank line
        account_writer = csv.writer(file)

        if is_first_record:
            file.write('')
            is_first_record: False

        #Appending new records
        account_writer.writerow(newAccount)

def updateAccountDatabase(accounts):
    header = ['username', 'pincode', 'balance']
    with open('accounts.csv', mode = 'w', newline='') as file:
        accounts_writer = csv.writer(file)
        accounts_writer.writerow(header)
        for account in accounts.values():
            row = [account.username, account.pincode, account.current_balance]
            accounts_writer.writerow(row)


def getAccounts():
    accounts = {} #empty dictionary

    with open('accounts.csv', mode='r') as file:
        accounts_reader = csv.reader(file)
        next(accounts_reader) #skipping the 1st (header) row
        for row in accounts_reader:
            username = row[0]
            pincode = row[1]
            balance = row[2]
            accounts[username] = Account(username, pincode, float(balance))
            
    return accounts

accounts = getAccounts() #initial account dictionary.

def inputUsername(prompt): #prompt can be to "Create" or "Enter" username depending on the condition
    ''' this function helps to get a valid username '''
    validUsername = False
    while not validUsername:
        username = input("| " + prompt + ": ")
        if (len(username) < 4):
            display_string("Username should be at least 4 characters.")
        else:
            validUserName = True
            return username

def inputPincode(prompt): #prompt can be to "Create" or "Enter" pincode epending on the condition
    ''' this function helps to get a valid 4 digit pincode '''
    validPincode = False
    while not validPincode:
        try:
            pincode = input("| " + prompt + ": ")
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
    username_exists = True
    while username_exists:
        username = inputUsername("Create a username")
        if username in accounts:
            display_string("Username already exists. Please enter a different username.")
        else:
            username_exists = False

    pincode = inputPincode("Create a four digit pincode")
    deposit_amt = inputBalance("Enter starting balance amount")
    
    accounts[username] = Account(username, pincode, deposit_amt)

    addToDatabase(accounts[username])

    display_string("Account successfully created.")
    print("-" * 80)

def removeAccount():
    username = inputUsername("Enter username")
    if username in accounts:
        pincode = inputPincode("Enter four digit pincode")
        if accounts[username].pincode == pincode:
            if accounts[username].current_balance > 0:
                display_string("This account still has balance remaining.")
                display_string("Please log in and completely withdraw the balance.")
                print("-" * 80)
            else:
                choice = input("| Are you sure you want to delete the account? (y/n): ")
                if choice.lower() == 'y':
                    del(accounts[username])
                    updateAccountDatabase(accounts)
                    display_string("Account successfully deleted.")
                else:
                    display_string("Operation successfully aborted.")
                
                print("-" * 80)
        else:
            display_string("Username or pincode mismatch. Please try again")
            print("-" * 80)
    else: 
        display_string("Username not found. Please try again.")
        print("-" * 80)

def accountActions():
    ''' this function performs operations on existing accounts '''
    username = inputUsername("Enter username")
    if username in accounts:
        current_user = accounts[username]
        pincode = inputPincode("Enter four digit pincode")
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
        print("-"* 80)

def checkBalance(user):
    display_string("Your current balance is Rs. " + str(round(user.current_balance,2)))
    print("-" * 80)

def withdrawBalance(user):
    balance_amount = inputBalance("Enter the withdrawal amount")
    if balance_amount > user.current_balance:
        display_string("Requested amount exceeds current balance. Please try again.")
    else:
        user.current_balance -= balance_amount
        updateAccountDatabase(accounts)
        display_string("Withdrawal successful. Current Balance is Rs. " + str(round(user.current_balance, 2)))
    
    print("-" * 80)

def depositBalance(user):
    balance_amount = inputBalance("Enter the deposit amount")
    user.current_balance += balance_amount
    updateAccountDatabase(accounts)
    display_string("Deposit successful. Current balance is Rs. " + str(round(user.current_balance, 2)))
    print("-" * 80)
