import subprocess as sb



def get_ip():
    call = sb.check_output('arp -a').decode('cp866')
    new = list(call.split(" "))
    new = [new.rstrip() for new in new] #убирает символы \r\n из текста
    while('' in new):   #убирает пустые значения из массива
        new.remove('')
    #  удаление ненужной инфы
    del new[:10]
    return new

ip_dict = get_ip()
ip_dict = ip_dict[0::3]
print(ip_dict)
ip_dict = {ip_dict[i]: ip_dict[i] for i in range (0,len(ip_dict))}
print(ip_dict)