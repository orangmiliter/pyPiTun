from bs4 import BeautifulSoup
from keys import keys
from kue import cookie
from colorama import Fore, Style
import requests, sys
import argparse


appName = sys.argv[0]
parser = argparse.ArgumentParser(usage="python {} --session or --check or --user pi/etc".format(appName))
parser.add_argument("-gs","--session", help="Getting a session from the web. ex: --session", action="store_true")
parser.add_argument("-ci","--check", help="Get device information",  action="store_true")
parser.add_argument("-u","--user", help="Input user of SSH. ex: --user pi", nargs="?")

args = parser.parse_args()

def getSession():
    login_url = "https://www.pitunnel.com/login"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    ses = requests.Session()
    data = {
        "email": keys['email'],
        "password": keys['password'],
        "commit": "Login"
    }

    login = ses.post(login_url, data=data, headers=headers)
    get_cookie = ses.cookies.get_dict()
    f = open('kue.py', 'w')
    f.write("cookie = dict(\n\tsession='{}'\n)".format(get_cookie['session']))
    f.close()
def checkInfo():

    host_url = "https://www.pitunnel.com/devices_table"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    get_host = requests.get(host_url, cookies=cookie, headers=headers)

    bs = BeautifulSoup(get_host.text, 'lxml')
    ## find rpi model or name
    device_name = bs.find("span", {"id": "device_display_name_7254"})
    device_name_rpi = device_name.text.split('\n')
    print("-------"*5)
    print(device_name_rpi[2])
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

    get_host = requests.get(host_url, cookies=cookie, headers=headers)
    # print(get_host.text)
    bs = BeautifulSoup(get_host.text, 'lxml')
    tBody = bs.find('tbody')
    td_Search = tBody.find_all('tr', class_=None)
    for td_row in td_Search:
        td_kolom = td_row.findAll('td')
        out = td_kolom[1].text.replace('\n', "").replace("                                                                                      ","").replace("                                                                                  ","")#IniBiarPanjang
        td_split = out.strip('\n').split(':')
        print("{}@{} -p{}".format(args.user, td_split[0], td_split[1]))#biargampang

def main():
    if args.session:
        getSession()
    if args.check:
        checkInfo()
    if args.user:
        getSSH()

if __name__ == "__main__":
    main()
