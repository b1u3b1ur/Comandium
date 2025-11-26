import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

init()
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

client_color = random.choice(colors)

SERVER_HOST = "192.168.0.192"
SERVER_PORT = int(input("Puerto: "))
separator_token = "<SEP>"

s = socket.socket()
print(f'[>] Conectando a {SERVER_HOST}:{SERVER_PORT}...')
s.connect((SERVER_HOST,SERVER_PORT))
print(f'[>] Conectado.')

name = input("Pon tu nombre: ")

def Inicio_de_mensajes():
    while True:
        try:
            message = s.recv(1024).decode()
            if not message:
                print("[!] Servidor desconectado.")
                break
            print(message)
        except:
            print("[!] Conexión cerrada.")
            break
        
t = Thread(target=Inicio_de_mensajes)
t.daemon = True
t.start()

while True:
    enviar = input()
    if enviar.lower() == 'q':
        print("Adios")
        break
    else:
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        to_send = f"{client_color}[{fecha}] {name}{separator_token}{enviar}{Fore.RESET}"
        s.send(to_send.encode())
s.close()