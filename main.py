import random

try:
    from colorama import Fore, init
except:
    print("Colorama not installed, installing via pip")
    import os; os.system("pip install colorama")
    exit("\nFixed, please re-run the program")

init(True) # Windows cmd color support

#My stuff
import PFArt as art
import MainFunctions as MF

def PrintMainArt():
    MF.clear()
    print(random.choice(art.Rand_Art)) # Add better/more art
    print(f"{Fore.MAGENTA}{random.choice(art.Rand_Msgs)}") #Add more messages later

def Main():
    PrintMainArt()
    print(art.Main_Startup)
    Main_Choice = input(art.Main_Select)

    match Main_Choice:
        case '1':
            MF.clear()
            MF.FindPFs()

        case '2':
            pfid = input(f"{art.question}Title ID:{art.main} ")
            MF.clear()
            MF.FindExploits(pfid) # Make better in 1.0.1 update

        case '3':
            Login_Choice = input(art.Login_Select)

            match Login_Choice:
                case '1':
                    pfid = input(f"{art.question}Title ID:{art.main} ")
                    MF.CustomID_Login(pfid)
                case '2':
                    pfid = input(f"{art.question}Title ID:{art.main} ")
                    MF.EmailPass_Login(pfid)
                case '3':
                    pfid = input(f"{art.question}Title ID:{art.main} ")
                    MF.SteamTicket_Login(pfid)
                case '4':
                    ses_ticket = input(f"{art.question}Session Ticket:{art.main} ")
                    pfid = ses_ticket.split("-")[3].strip()
                    MF.Session_Checker(ses_ticket, pfid)
                case '5':
                    ses_ticket = input(f"{art.question}Entity Token:{art.main} ")
                    MF.Entity_Login(ses_ticket)

        case '4':
            MF.SecretKey()
    Main()

if __name__ == "__main__":
    try:
        Main()
    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}{art.ByeArt}{Fore.RESET}")
