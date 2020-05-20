from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
import subprocess as sb
import platform, os, re, socket, wmi, urllib
import psutil as ps
from urllib.request import urlopen
from getmac import get_mac_address
import cpuinfo as cp

# функция получения списка ip адресов
def get_ip():
    call = sb.check_output('arp -a').decode('cp866') # виндовая команда и кодировка
    new = list(call.split(" "))
    new = [new.rstrip() for new in new] #убирает символы \r\n из текста
    while('' in new):   #убирает пустые значения из массива
        new.remove('')
    #  удаление ненужной инфы
    del new[:10]
    return new

def iptable(request):
    new = get_ip()
   
    ips = new[0::3]
    macs = new[1::3]
    types = new[2::3]

    three_lists = zip(ips,macs,types)
    # ip_dict = {ips[i]: ips[i] for i in range(0,len(ips))}
    return render(request,'ui-tables.html',{'data':three_lists})

def sysinfo(request):
    #current os info
    os_info = str(platform.system() + " " + platform.release())
    info = {'Ваша ОС': os_info} # список с хар-ками компа

    #total ram info
    mem = str(sb.check_output('wmic memorychip get Capacity').decode('cp866'))
    mem = mem.replace('Capacity','')
    mem = int(mem)/(2**30)  # перевод байты в гигабайты
    info.setdefault('Ваша ОЗУ',mem)

    #ram frequency
    mem_fr = str(sb.check_output('wmic memorychip get Speed').decode('cp866'))
    mem_fr = mem_fr.replace('Speed','').replace('\r\r\n','')
    info.setdefault('Частота ОЗУ',mem_fr)

    #hdd f/t/u
    hdd = ps.disk_usage('/')
    hdd_t = int(hdd.total/(2**30)*100)/100
    hdd_u = int(hdd.used/(2**30)*100)/100
    hdd_f = int(hdd.free/(2**30)*100)/100

    info.setdefault('Общее место на HDD', hdd_t)
    info.setdefault('Занято на HDD', hdd_u)
    info.setdefault('Свободно на HDD', hdd_f)
    
    # get white ip 
    data = str(urlopen('http://checkip.dyndns.com/').read())
    white_ip = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)
    info.setdefault('Внешний IP-адрес',white_ip)

    # get local ip
    hostname = socket.gethostname()    
    local_ip = socket.gethostbyname(hostname)
    info.setdefault('Локальный IP-адрес', local_ip)

    # get local mac
    mac = get_mac_address()
    info.setdefault('Mac-адрес',mac)

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
    info.setdefault('Материнская плата',motherboard_total)

    #cpu info
    cpu_cores = ps.cpu_count()
    cpu_model = cp.get_cpu_info()
    cpu_model = cpu_model["brand"]
    cpu_total = cpu_model + cpu_cores + " cores"
    info.setdefault('Процессор', cpu_total)

    #gpu info
    pc = wmi.WMI()
    gpu_info = pc.Win32_VideoController()[0].Name
    info.setdefault('Видеокарта',gpu_info)

    return render(request, '',{'sysinfo':info}) # дописать тут

# def ip_page(request):
#     ip_dict = get_ip()
#     ip_dict = ip_dict[0::3]
#     ip_dict = {ip_dict[i]: ip_dict[i] for i in range (0,len(ip_dict))}
#     uri = urllib.parse.urlencode(ip_dict)
#     fullurl = "/?" + uri
#     return request.GET.get(fullurl)

    
   