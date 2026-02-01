import socket
import random
import struct
import os
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
separator_token = "<SEP>"
DOWNLOAD_DIR = "archivador"

# SERVER_HOST = "192.168.0.192"
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.connect(("8.8.8.8", 80)) 
SERVER_HOST = c.getsockname()[0]
c.close()

def port(data):
    global s, file_socket
    SERVER_PORT = data
    FILE_PORT = SERVER_PORT + 1
    
    s = socket.socket()
    file_socket = socket.socket()
    
    print(f'[>] Conectando a {SERVER_HOST}:{SERVER_PORT}...')
    
    s.connect((SERVER_HOST,SERVER_PORT))
    file_socket.connect((SERVER_HOST, FILE_PORT))
    
    if s and file_socket:
        print(f'[✓] Conectado.')
    else:
        print(f'[!] No se pudo conectar al servidor.')
    
    def Inicio_de_mensajes():
        while True:
            try:
                message = s.recv(1024).decode()
                if not message:
                    print("[!] Servidor desconectado.")
                    break
                message = message.replace(separator_token, ": ")
                print(message)
            except:
                print("[!] Conexión cerrada.")
                break
    
    def recibir_archivos():
        while True:
            try:
                header_len = file_socket.recv(1024)
                if not header_len:
                    break

                header_len = struct.unpack("I", header_len)[0]
                header = file_socket.recv(header_len)
            
                filename, filesize = header.decode().split(separator_token)
                filesize = int(filesize)

                os.makedirs(DOWNLOAD_DIR, exist_ok=True)

                filename = os.path.basename(filename)

                save_path = os.path.join(DOWNLOAD_DIR, filename)

                with open(save_path, "wb") as f:
                    received = 0
                    while received < filesize:
                        chunk = file_socket.recv(256000000)
                        if not chunk:
                            break
                        f.write(chunk)
                        received += len(chunk)

                print(f"[↓] Descargado: {save_path}")

            except Exception as e:
                print("Error recibiendo archivo:", e)
                break
                # with open(filename, "wb") as f:
                #     received = 0
                #     while received < filesize:
                #         chunk = file_socket.recv(4096)##tenla en cuenta##
                #         chunk = file_socket.recv(256000000)
                #         f.write(chunk)
                #         received += len(chunk)

                # print(f"[↓] Descargado: {filename}")
                
    Thread(target=Inicio_de_mensajes, daemon=True).start()
    Thread(target=recibir_archivos,daemon=True).start()

def env(ruta):
    if not os.path.exists(ruta):
        print("[!] Archivo no encontrado")
        return

    filename = os.path.basename(ruta)
    filesize = os.path.getsize(ruta)

    print(f"[>] Enviando {filename} ({filesize} bytes)")

    # enviar metadata (nombre + tamaño)
    header = f"{filename}{separator_token}{filesize}".encode()
    file_socket.send(struct.pack("I", len(header)))
    file_socket.send(header)

    with open(ruta, "rb") as f:
        while True:
            chunk = f.read(256000000)  
            if not chunk:
                break
            file_socket.sendall(chunk)

    print("[✓] Archivo enviado completamente")

def user(name):
    #cuando hagas la confi
    pass

name = "Usuario"

def enviar(data):
    # enviar = input()
    enviar = data
    if enviar.lower() == 'q':
        print("Adios")
        cerrar_conexion()
    elif data.lower().startswith("/file "):
        ruta = data.split(" ", 1)[1]
        env(ruta)
        return
    else:
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        to_send = f"{client_color}[{fecha}] {name}{separator_token}{enviar}{Fore.RESET}"
        s.send(to_send.encode())
    
def cerrar_conexion():
    try:
        s.close()
        file_socket.close()
    except:
        pass
    print("[!] Socket cerrado correctamente.")
