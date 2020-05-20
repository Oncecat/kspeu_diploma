import socket

socket.setdefaulttimeout(0.25)
target_ip = input('Введите IP для проверки порта: ')
ip = socket.gethostbyname(target_ip)

target_port = int(input('Введите порт для проверки: '))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создание сокета 

try:
    sock.connect((target_ip,target_port)) # попытка соединения по порту
except:
    print("Порт %s закрыт" % target_port)
else:
    print("Порт %s открыт" % target_port)
sock.close()