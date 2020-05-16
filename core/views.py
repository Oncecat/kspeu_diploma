from django.shortcuts import render
import subprocess
from django.http import HttpResponse


def iptable(request):
    call = subprocess.check_output('arp -a').decode('cp866')
    new = list(call.split(" "))
    new = [new.rstrip() for new in new] #убирает символы \r\n из текста
    while('' in new):   #убирает пустые значения из массива
        new.remove('')

    #  удаление ненужной инфы
    del new[:10]
    ips = new[0::3]
    macs = new[1::3]
    types = new[2::3]

    three_lists = zip(ips,macs,types)

    return render(request,'ui-tables.html',{'data':three_lists})
   