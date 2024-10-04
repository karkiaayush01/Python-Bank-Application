from operations import display_title, check_accounts, display_string
    
def main():
    """ this is the entry point of the application. """

    display_title()
    
    run = True
    
    while run:
        endProgram = check_accounts()
        if(endProgram == 'y'):
            display_string("Quitting the Application. Thank you!")
            break

    print("-" * 80)

main()

