from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import subprocess
from app.models import Myip


def index(request):
    return render(request, "index.html")


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


def iptable(request):
    '''
        Смотри верхнюю херню раскоментируешь, и мой new удалишь.

        Для начала я создаю словарь new_dict, чтобы было удобнее потом работать с данными,
        после чего создаю новые экземпляры Myip. А потом выбираю все объекты Myip и передаю их в шаблон.
        Если тебе нужно передавать данные только одного юзера с его машины(Я так понял), то сохрани какое-нибудь поле,
        которое определяет этого юзера, как я понимаю - это mac(Только я хз какой), и по нему запусти фильтрацию
        в переменной "ips"

    '''
    # call = subprocess.check_output('arp -a').decode('cp866')
    # new = list(call.split(" "))
    # new = [new.rstrip() for new in new]  # убирает символы \r\n из текста
    # while ('' in new):  # убирает пустые значения из массива
    #     new.remove('')

    #  удаление ненужной инфы
    # del new[:10]
    new = ['192.168.1.1', 'f0-82-61-27-6f-c4', 'динамический', '192.168.1.3', 'b0-fc-36-3a-82-45', 'динамический',
           '192.168.1.255', 'ff-ff-ff-ff-ff-ff', 'статический', '224.0.0.22', '01-00-5e-00-00-16', 'статический',
           '224.0.0.251', '01-00-5e-00-00-fb', 'статический', '224.0.0.252', '01-00-5e-00-00-fc', 'статический',
           '239.255.255.250', '01-00-5e-7f-ff-fa', 'статический', '255.255.255.255', 'ff-ff-ff-ff-ff-ff', 'статический']
    n = 0
    new_dict = []
    for i in range(0, len(new[::3])):
        new_dict.append({
            'ip': new[0::3][n],
            'mac': new[1::3][n],
            'type': new[2::3][n]
        })
        n += 1
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


def iptable_detail(request, slug):
    '''
    Здесь я получаю слаг одного объекта из шаблоны и ищу его экземпляр Myip и передаю его на новый шаблон
    '''
    ip = Myip.objects.get(slug=slug)
    return render(request, 'ui-tables_detail.html', {'ip': ip})


'''     раскомментить чтобы возвращать 500ую
    except:

        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))



'''
