import platform
import psutil as ps
import subprocess as sb
import os 
import re
from urllib.request import urlopen
import socket
from getmac import get_mac_address


os_info = str(platform.system() + " " + platform.release())
print()
print("Current system is " + os_info)

mem = str(sb.check_output('wmic memorychip get Capacity').decode('cp866'))
mem = mem.replace('Capacity','')
mem = int(mem)/2**30  # перевод байты в гигабайты
print("Current RAM is " + str(int(mem)) + " Gb")

mem_fr = str(sb.check_output('wmic memorychip get Speed').decode('cp866'))
mem_fr = mem_fr.replace('Speed','').replace('\r\r\n','')
print("RAM frequency is" + str(mem_fr)) # Частота оперативной памяти

hdd = ps.disk_usage('/')
hdd_t = hdd.total/(2**30)
hdd_u = hdd.used/(2**30)
hdd_f = hdd.free/(2**30)
print("total hdd memory: %.2f Gb "% hdd_t)
print("used hdd memory: %.2f Gb "% hdd_u)
print("free hdd memory: %.2f Gb "% hdd_f)

# get white ip 
data = str(urlopen('http://checkip.dyndns.com/').read())
myip = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)
print("white ip: " + myip)
   
# get local ip
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)
print("local ip: " + IPAddr)  

# get local mac
mac = get_mac_address()
print("current mac-address: " + mac)