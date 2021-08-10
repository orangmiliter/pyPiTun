# pyPiTun
Easy the remote to the [pitunnel](https://www.pitunnel.com/).

#### Requirement :

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirement.

```bash
pip install -r requirement.txt
```

#### Usage :
##### **Linux**
```bash
get Sessions : 

python3 pyPiTun.py --session test
Enter e-mail Pitunnel :pitunnel@example.com
Input password pitunnel :
```
```bash
Get Devices Information 
python3 pyPiTun.py -ck or --cookie fileCookie --check
output :
-----------------------------------
          Pi4 Model B
----------------------------------- 
Hostame : raspberrypi
MAC Adress : xx:xx:xx:xx:xx:xx      
Operation System : Linux Debian 10.9
Hardware : Pi4 Model B
Memory Usage : 21.1%
Disk Usage : 70.5%
CPU Usage : 2.7%
CPU Temperature : 61.3°C
GPU Temperature : 61.3°C
```
```bash
ssh $(python3 pyPiTun.py -ck or --cookie fileCookie --user pi)
```

##### **Windows**
```bash
get Sessions : 

python3 pyPiTun.py --session fileCookie
Enter e-mail Pitunnel :pitunnel@example.com
Input password pitunnel :
```
```bash
Get Devices Information 
python3 pyPiTun.py -ck or --cookie fileCookie --check
output :
-----------------------------------
          Pi4 Model B
----------------------------------- 
Hostame : raspberrypi
MAC Adress : xx:xx:xx:xx:xx:xx        
Operation System : Linux Debian 10.9
Hardware : Pi4 Model B
Memory Usage : 21.1%
Disk Usage : 70.5%
CPU Usage : 2.7%
CPU Temperature : 61.3°C
GPU Temperature : 61.3°C
```
```bash
python3 pyPiTun.py -ck or --cookie fileCookie --user pi
output :
pi@pitunnexx.com -p123423
ssh pi@pitunnexx.com -p123423
```
