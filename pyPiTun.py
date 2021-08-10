from bs4 import BeautifulSoup
from colorama import Fore, Style
from getpass import getpass
import requests, sys
import argparse, json


appName = sys.argv[0]
parser = argparse.ArgumentParser(usage="python {} --session test and -ck test --check or --user pi/etc".format(appName))
parser.add_argument("-Gs","--session", help="Getting a session from the web. ex: python pyPiTun.py --session fileCookie", nargs="?")
parser.add_argument("-Ck", "--cookie", help="select cookies file. ex: -ck test", type=str, nargs='?')
parser.add_argument("-ci","--check", help="Get device information. ex : python pyPiTun.py --cookie fileCookie --check",  action="store_true")
parser.add_argument("-u","--user", help="Input user of SSH. ex: python pyPiTun.py --cookie fileCookie --user pi", nargs="?")
parser.add_argument("-r", "--reboot", help="Reboot system. ex: python pyPiTun.py --cookie fileCookie --reboot", action="store_true")

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

def reboot():
    host_url = "https://www.pitunnel.com/devices_table_json"
    host_device = "https://www.pitunnel.com/devices"
    reboot_url = "https://www.pitunnel.com/reboot_device"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    fileCookie = open('sesi/{}.json'.format(args.cookie), 'r')
    cookie = json.load(fileCookie)

    req_deviceID = requests.get(host_url, cookies=cookie, headers=headers)
    #
    jLoads = json.loads(req_deviceID.text)
    jDumps = json.loads(json.dumps(jLoads['data'], indent=4))

    csrf_getToken = requests.get(host_device,  cookies=cookie, headers=headers)
    bs = BeautifulSoup(csrf_getToken.text, 'lxml')
    input_search = bs.find('input', {"name": "csrf_token"})

    headers1 = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.pitunnel.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.pitunnel.com/devices',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    data = {
    'device_id': jDumps[0]['DT_RowId'],
    'csrf_token': input_search['value']
    }

    reboot_process = requests.post(reboot_url, headers=headers1, cookies=cookie, data=data)
    if reboot_process.status_code == 200:
        print(Fore.GREEN + "Reboot Success" + Style.RESET_ALL)
    else :
        print(Fore.RED + "Reboot Failed" + Style.RESET_ALL)



def main():
    if args.session:
        getSession()
    if args.check:
        checkInfo()
    if args.user:
        getSSH()
    if args.reboot:
        reboot()

if __name__ == "__main__":
    main()
