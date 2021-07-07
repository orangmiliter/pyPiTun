from bs4 import BeautifulSoup
from colorama import Fore, Style
from getpass import getpass
import requests, sys
import argparse, json


appName = sys.argv[0]
parser = argparse.ArgumentParser(usage="python {} --session test and -ck test --check or --user pi/etc".format(appName))
parser.add_argument("-gs","--session", help="Getting a session from the web. ex: --session test", type=str, nargs='?')
parser.add_argument("-ck", "--cookie", help="select cookies file. ex: -ck test", type=str, nargs='?')
parser.add_argument("-ci","--check", help="Get device information",  action="store_true")
parser.add_argument("-u","--user", help="Input user of SSH. ex: --user pi", nargs="?")

args = parser.parse_args()

def getSession():
#input form
    usernamedash = input("Enter e-mail Pitunnel : ")
    passworddash = getpass(prompt="Input password pitunnel : ")

    login_url = "https://www.pitunnel.com/login"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    ses = requests.Session()
    data = {
        "email": usernamedash,
        "password": passworddash,
        "commit": "Login"
    }

    login = ses.post(login_url, data=data, headers=headers)
    get_cookie = ses.cookies.get_dict()
    with open('sesi/{}.json'.format(args.session), 'w') as sesifile:
        sesifile.write(json.dumps(get_cookie))
def checkInfo():

    host_url = "https://www.pitunnel.com/devices_table"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    fileCookie = open('sesi/{}.json'.format(args.cookie), 'r')
    cookie = json.load(fileCookie)

    get_host = requests.get(host_url, cookies=cookie, headers=headers)

    bs = BeautifulSoup(get_host.text, 'lxml')
    print("-------"*5)
    print("Device Info".center(30))
    print("-------"*5)
    ## find info device
    find_tbody = bs.find('tbody')
    find_td = find_tbody.find_all('span', {"class":"pull-right"})
    find_td_by_class = find_tbody.find_all('td', {"align":"right"})
    print(Fore.GREEN + "Hostame : " + Style.RESET_ALL + find_td_by_class[0].text)
    print(Fore.GREEN + "MAC Adress : " + Style.RESET_ALL  + find_td_by_class[1].text)
    print(Fore.GREEN + "Operation System : " + Style.RESET_ALL  + find_td_by_class[2].text)
    print(Fore.GREEN + "Hardware : " + Style.RESET_ALL  + find_td_by_class[3].text)
    print(Fore.GREEN + "Memory Usage : " + Style.RESET_ALL  + find_td[0].text)
    print(Fore.GREEN + "Disk Usage : " + Style.RESET_ALL  + find_td[1].text)
    print(Fore.GREEN + "CPU Usage : " + Style.RESET_ALL  + find_td_by_class[4].text)
    print(Fore.GREEN + "CPU Temperature : " + Style.RESET_ALL  + find_td_by_class[5].text)
    print(Fore.GREEN + "GPU Temperature : " + Style.RESET_ALL  + find_td_by_class[6].text)

def getSSH():
    host_url = "https://www.pitunnel.com/active_table"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    fileCookie = open('sesi/{}.json'.format(args.cookie), 'r')
    cookie = json.load(fileCookie)

    get_host = requests.get(host_url, cookies=cookie, headers=headers)
    bs = BeautifulSoup(get_host.text, 'lxml')
    tBody = bs.find('tbody')
    td = tBody.find_all('td')
    tdRep = td[1].text.replace('\n', "").replace("                                                                                      ","").replace("                                                                                  ","")#IniBiarPanjang
    tdSplit = tdRep.strip('\n').split(':')
    print("{}@{} -p{}".format(args.user, tdSplit[0], tdSplit[1]))#biargampang

def main():
    if args.session:
        getSession()
    if args.check:
        checkInfo()
    if args.user:
        getSSH()

if __name__ == "__main__":
    main()
