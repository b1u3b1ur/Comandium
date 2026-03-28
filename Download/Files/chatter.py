import socket
import random
import struct
import shutil
import base64
import hashlib
import sys
import os
from queue import Queue
from threading import Thread
from datetime import datetime
from cryptography.fernet import Fernet

separator_token = "<SEP>"
DOWNLOAD_DIR = "Comandium/archivador"
data_traveler = 256000000
Username = None
s = None
file_socket = None
send_message = []
out_msg = Queue()

def user(name):
    global Username
    names = []
    names.append(name)
    Username = names[0]

def recvall(sock, n):
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def port(data,port,clave):
    global s, file_socket, key, cipher
    SERVER_IP = data
    # U_ID = ID
    # FILE_PORT = SERVER_PORT + 1
    CLAVE_SECRETA = clave
    key = base64.urlsafe_b64encode(hashlib.sha256(CLAVE_SECRETA.encode()).digest())
    cipher = Fernet(key)
    s = socket.socket()
    file_socket = socket.socket()
    
    try:
        out_msg.put(f"[*] Conectando a {SERVER_IP}...")
        s.connect((SERVER_IP, port))
        file_socket.connect((SERVER_IP, port + 1))
        out_msg.put("[+] Conectado con éxito.")
    except Exception as e:
        out_msg.put(f"[!] Error de conexión: {e}")
        os._exit(1)
    
    def Inicio_de_mensajes():
        while True:
            try:
                data = s.recv(4096)
                if not data:
                    break
                try:
                    msg_descifrado = cipher.decrypt(data).decode()
                    if separator_token in msg_descifrado:
                        autor, contenido = msg_descifrado.split(separator_token, 1)
                        out_msg.put(f"{autor}: {contenido}\n> ")
                        send_message.append(f"{autor}: {contenido}\n> ")
                        print(f"\n{autor}: {contenido}\n> ", end="",flush=True)
                except:
                    try:
                        texto_plano = data.decode()
                        if "SERVER" in texto_plano:
                            out_msg.put("\n[SERVER]: {texto_plano.replace(separator_token, ' ')}\n> ")
                            print(f"\n[SERVER]: {texto_plano.replace(separator_token, ' ')}\n> ", end="",flush=True)
                    except:
                        pass
            except:
                out_msg.put("[!] Conexión cerrada.")
                break
    
    def recibir_archivos():
        while True:
            try:
                raw_len = recvall(file_socket, 4)
                if not raw_len:
                    break

                header_len = struct.unpack("I", raw_len)[0]

                header = recvall(file_socket, header_len)
                if not header:
                    break
            
                documents_path = os.path.join(os.path.expanduser("~"), "Documents")
                target_dir = os.path.join(documents_path, DOWNLOAD_DIR)

                filename, filesize = header.decode().split(separator_token)
                filesize = int(filesize)
                
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)

                filename = os.path.basename(filename)

                save_path = os.path.join(target_dir, filename)

                with open(save_path, "wb") as f:
                    received = 0
                    while received < filesize:
                        chunk = file_socket.recv(data_traveler)
                        if not chunk:
                            break
                        f.write(chunk)
                        received += len(chunk)

                out_msg.put(f"[v] Descargado: {save_path}")

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
        out_msg.put("[!] Archivo no encontrado")
        return

    filename = os.path.basename(ruta)
    filesize = os.path.getsize(ruta)

    out_msg.put(f"[>] Enviando {filename} ({filesize} bytes)")

    # enviar metadata (nombre + tamaño)
    header = f"{filename}{separator_token}{filesize}".encode()
    file_socket.send(struct.pack("I", len(header)))
    file_socket.send(header)

    with open(ruta, "rb") as f:
        while True:
            chunk = f.read(data_traveler)  
            if not chunk:
                break
            file_socket.sendall(chunk)

    out_msg.put("[v] Archivo enviado completamente")

def env_ct(ruta):
    archivo_zip = str(os.path.basename(ruta))
    shutil.make_archive(archivo_zip, 'zip', ruta)
    return archivo_zip + ".zip"

def enviar(data):
    enviar = data
    try:
        if s is None:
            out_msg.put("[!] No estás conectado. Usa primero port(puerto).")
            return
        if enviar.lower() == 'q':
            out_msg.put("Adios")
            cerrar_conexion()
        elif data.lower().startswith("/file "):
            ruta = data.split(" ", 1)[1]
            env(ruta)
            return
        elif data.lower().startswith("/carpet "):
            ruta = data.split(" ", 1)[1]
            ec = env_ct(ruta)
            rt = os.path.dirname(os.path.abspath(sys.argv[0]))
            env(os.path.join(rt, ec))
            ruta_completa = os.path.join(rt, ec)

            if os.path.exists(ruta_completa):
                os.remove(ruta_completa)
                print(f"Archivo borrado en: {ruta_completa}")
            return
        elif data.lower() == '/play':
            pass
        else:
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            to_send = f"[{fecha}] {Username}{separator_token}{enviar}"
            send_message.append(to_send)
            out_msg.put(to_send.replace(separator_token, ' '))
            msg_cifrado = cipher.encrypt(to_send.encode())
            try:
                s.send(msg_cifrado)
            except (ConnectionResetError, BrokenPipeError, OSError):
                return
         
    except (ConnectionResetError, BrokenPipeError):
        out_msg.put("'Se ha forzado la interrupci¾n de una conexi¾n existente por el host remoto'. Eliminando socket...")
        s.close()
        file_socket.close()
    
def cerrar_conexion():
    try:
        s.close()
        file_socket.close()
    except:
        pass
    out_msg.put("[!] Socket cerrado correctamente.")