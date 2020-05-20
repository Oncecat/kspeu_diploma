import socket
import time
import threading
from queue import Queue
socket.setdefaulttimeout(0.25) # время жизни сокета
print_lock = threading.Lock()

target = input('Введите IP для сканирования: ')
t_IP = socket.gethostbyname(target)

def portscan(port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создание сокета 
   try:
      con = s.connect((t_IP, port)) # попытка соединения по указанному порту
      with print_lock:
         print(port, 'открыт')
      con.close()
   except:
      pass

def threader():
   while True:
      worker = q.get()
      portscan(worker)
      q.task_done()
      
q = Queue()
startTime = time.time()

# многопоточность наше всё   
for x in range(100):
   t = threading.Thread(target = threader)
   t.daemon = True
   t.start()
   
for worker in range(1, 1000): # диапазон портов для сканирования
   q.put(worker)
   
q.join()
print('Времени заняло:', time.time() - startTime)