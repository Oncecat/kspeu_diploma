import os
import subprocess as sb

target_ip = input("Введите IP: ")

call = sb.check_output('ping %s ' % target_ip).decode('cp866') # виндовая команда и кодировка

print(call)