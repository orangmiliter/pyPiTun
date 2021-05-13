from bs4 import BeautifulSoup
from keys import keys
import requests, sys
import argparse

appName = sys.argv[0]
parser = argparse.ArgumentParser(usage="python {} --user pi/etc".format(appName))
parser.add_argument("--user", help="Input user of SSH. ex: --user pi", required=True, nargs="?")

args = parser.parse_args()


login_url = "https://www.pitunnel.com/login"
host_url = "https://www.pitunnel.com/active_table"
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
get_host = ses.get(host_url, headers=headers)
# print(get_host.text)
bs = BeautifulSoup(get_host.text, 'lxml')
tBody = bs.find('tbody')
td_Search = tBody.find_all('tr', class_=None)
for td_row in td_Search:
    td_kolom = td_row.findAll('td')
    out = td_kolom[1].text.replace('\n', "").replace("                                                                                      ","").replace("                                                                                  ","")#IniBiarPanjang
    td_split = out.strip('\n').split(':')
    print("{}@{} -p{}".format(args.user, td_split[0], td_split[1]))#biargampang
