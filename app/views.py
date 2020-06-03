from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import template
import subprocess as sb
import platform, os, re, socket, urllib, time
import psutil as ps
from urllib.request import urlopen
from getmac import get_mac_address
import cpuinfo as cp
from queue import Queue
from ping3 import ping, verbose_ping
from app.models import Myip

def index(request):
    return render(request, "index.html")

#вывод системной инфы
def sysinfo(request):
    #current os info
    info = {}
    os_info = str(platform.system() + " " + platform.release())
    info.setdefault('os',os_info) # список с хар-ками компа

    #total ram info
    mem = str(sb.check_output('wmic memorychip get Capacity').decode('cp866'))
    mem = mem.replace('Capacity','')
    mem = int(mem)/(2**30)  # перевод байты в гигабайты
    mem = str(int(mem)) + " Gb"
    info.setdefault('ram',str(mem))

    #ram frequency
    mem_fr = str(sb.check_output('wmic memorychip get Speed').decode('cp866'))
    mem_fr = mem_fr.replace('Speed','').replace('\r\r\n','')
    info.setdefault('ramfreq',mem_fr)

    #hdd f/t/u
    hdd = ps.disk_usage('/')
    hdd_t = int(hdd.total/(2**30)*100)/100
    hdd_t = str(int(hdd_t)) + " Gb"
    hdd_u = int(hdd.used/(2**30)*100)/100
    hdd_u = str(int(hdd_u)) + " Gb"
    hdd_f = int(hdd.free/(2**30)*100)/100
    hdd_f = str(int(hdd_f)) + " Gb"

    info.setdefault('hdd_total', hdd_t)
    info.setdefault('hdd_used', hdd_u)
    info.setdefault('hdd_free', hdd_f)
    
    # get white ip 
    try:
        data = str(urlopen('http://checkip.dyndns.com/').read())
        white_ip = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)
        info.setdefault('white_ip',white_ip)
    except:
        info.setdefault('white_ip','Ошибка получения адреса!')
 
    # get local ip
    hostname = socket.gethostname()    
    local_ip = socket.gethostbyname(hostname)
    info.setdefault('local_ip', local_ip)

    # get local mac
    mac = get_mac_address()
    info.setdefault('mac',mac)

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
    info.setdefault('motherboard',motherboard_total)

    #cpu info
    cpu_model = cp.get_cpu_info()
    cpu_model = cpu_model["brand"]
    info.setdefault('cpu', cpu_model)

    #gpu info
    gpu = list(str(sb.check_output('wmic PATH Win32_videocontroller GET name').decode('cp866').replace('Name',' ').replace('\n','')))
    gpu = "".join(gpu)
    info.setdefault('gpu',gpu)
    return render(request, 'ui-sysinfo.html',{'sysinfo':info}) 

def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('error-404.html')
        return HttpResponse(html_template.render(context, request))

# получение ip, mac и типов адресов для вывода на страницу
def iptable(request):
    '''
        Для начала я создаю словарь new_dict, чтобы было удобнее потом работать с данными,
        после чего создаю новые экземпляры Myip. А потом выбираю все объекты Myip и передаю их в шаблон.
    '''
    call = sb.check_output('arp -a').decode('cp866')
    new = list(call.split(" "))
    new = [new.rstrip() for new in new]  # убирает символы \r\n из текста
    while ('' in new):  # убирает пустые значения из массива
        new.remove('')

    #  удаление ненужной инфы
    del new[:10]

    n = 0
    new_dict = []
    for i in range(0, len(new[::3])):
        new_dict.append({
            'ip': new[0::3][n],
            'mac': new[1::3][n],
            'type': new[2::3][n]
        })
        n += 1
    Myip.objects.all().delete()  # если что убрать 
    for i in new_dict:
        if i['type'] == 'динамический':
            type = 0
        elif i['type'] == 'статический':
            type = 1
        else:
            type = 2
        myip, cmyip = Myip.objects.get_or_create(ip=i['ip'], mac=i['mac'], type=type)
        print(myip.id, myip.slug)
    ips = Myip.objects.all()
    return render(request, 'ui-tables.html', {'ips': ips})


# данные для рендера страницы с данными, проверки портов, ip 
def iptable_detail(request, slug):
    ip = Myip.objects.get(slug=slug)
    socket.setdefaulttimeout(0.01)
    respond = ""
    ports = []
    ping_status = ""
    target_ip = socket.gethostbyname(ip.ip)
    if request.method == 'POST':
        if request.POST.get('port'):
            port = request.POST.get('port')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создание сокета 
            try:
                sock.connect((target_ip,int(port)))
            except:
                respond = "port " + port + " is closed :c"
            else:
                respond = "port " + port + " is opened!"
            sock.close() 
        elif request.POST.get('port_list'):
            for port in range (1,1000):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    sock.connect((target_ip,int(port)))
                except:
                    sock.close()
                else:
                    ports.append(port)
                    sock.close()
            if len(ports) == 0:
                ports.append('all ports are closed!')
        elif request.POST.get('ping'):
            try:
                call = sb.check_output('ping3 -w 1 %s' % target_ip).decode('cp866').replace('\r','  ').replace('\n','')
                ping_status = list(call.split(" "))
            except:
                ping_st = "Device is unavailable to connect!"
                ping_status = list(ping_st.split(" "))
    return render(request, 'ui-tables_detail.html', {
    'ip': ip,
    'respond': respond,
    'ports': ports,
    'ping':ping_status,
    })

'''     раскомментить чтобы возвращать 500ую
    except:
        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))

'''

