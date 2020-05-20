import platform, os, re, socket, wmi
import psutil as ps
import subprocess as sb
from urllib.request import urlopen
from getmac import get_mac_address
import cpuinfo as cp


#current system info
os_info = str(platform.system() + " " + platform.release())
print()
print("Current system is " + os_info)

#total ram info
mem = str(sb.check_output('wmic memorychip get Capacity').decode('cp866'))
mem = mem.replace('Capacity','')
mem = int(mem)/(2**30)  # перевод байты в гигабайты
print("Current RAM is " + str(int(mem)) + " Gb")

#ram frequency
mem_fr = str(sb.check_output('wmic memorychip get Speed').decode('cp866'))
mem_fr = mem_fr.replace('Speed','').replace('\r\r\n','')
print("RAM frequency is" + str(mem_fr)) # Частота оперативной памяти

#hdd f/t/u
hdd = ps.disk_usage('/')
hdd_t = int(hdd.total/(2**30)*100)/100
hdd_u = hdd.used/(2**30)
hdd_f = hdd.free/(2**30)

print("free hdd memory: %.2f Gb"% hdd_f)
print("total hdd memory: %.2f Gb"% hdd_t)
print("used hdd memory: %.2f Gb"% hdd_u)

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

#motherboard info
motherboard_manufact = list(str(sb.check_output('wmic baseboard get manufacturer').decode('cp866').replace('Manufacturer','').replace('\r','').replace('\n','')))
motherboard_product = list(str(sb.check_output('wmic baseboard get product').decode('cp866').replace('Product','').replace('\r','').replace('\n','')))
while (' ' in motherboard_product):
    motherboard_product.remove(' ')

while(' ' in motherboard_manufact):
    motherboard_manufact.remove(' ')

motherboard_manufact = "".join(motherboard_manufact)
motherboard_product = "".join(motherboard_product)
motherboard_total = motherboard_manufact + " " + motherboard_product
print("your motherboard: " + motherboard_total)

#cpu info
cpu_cores = ps.cpu_count()
cpu_model = cp.get_cpu_info()
cpu_model = cpu_model["brand"]
print("your cpu: %s %d cores" % (cpu_model, cpu_cores))

#gpu info
pc = wmi.WMI()
gpu_info = pc.Win32_VideoController()[0].Name
print("your gpu: " + gpu_info)