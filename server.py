import os
import socket
import random
import struct
import threading
from threading import Thread

SERVER_HOST = "0.0.0.0"
SERVER_PORT = random.randint(2000, 9000)
separator_token = "<SEP>"

lock = threading.Lock()

client_sockets = set()
file_sockets = set()

s = socket.socket()
fs = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
fs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((SERVER_HOST, SERVER_PORT))
fs.bind((SERVER_HOST, SERVER_PORT + 1))

s.listen()
fs.listen()

print(f'[*] Servidor inicializado como: {SERVER_HOST}:{SERVER_PORT}')
print(f"[*] Canal archivos en {SERVER_PORT + 1}")

def Inicializacion_de_cliente(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
            if not msg:  
                break
            text = msg.replace(separator_token, ": ")
            print(f'[*] {text}')
            for client_socket in client_sockets.copy():
                if client_socket != cs:
                    try:
                        client_socket.send(msg.encode())
                    except:
                        client_sockets.remove(client_socket)
                        client_socket.close()
        except ConnectionResetError:
            break
        except Exception as e:
            print(f'[!] Error en cliente: {e}')
            break
    try:
        cs.close()
        client_sockets.remove(cs)
    except:
        pass
    print("[!] Cliente desconectado.")

def recibir_archivos(cliente):
    while True:
        try:
            header_len = cliente.recv(1024)
            if not header_len:
                break

            header_len = struct.unpack("I", header_len)[0]
            header = cliente.recv(header_len)

            filename, filesize = header.decode().split(separator_token)
            filesize = int(filesize)

            print(f"[>] Recibiendo archivo: {filename} ({filesize} bytes)")

            carpeta = os.path.dirname(filename)
            if carpeta:
                os.makedirs(carpeta, exist_ok=True)
                
            for fl_sk in file_sockets.copy():
                if fl_sk != cliente:
                    try:
                        fl_sk.send(struct.pack("I", header_len))
                        fl_sk.send(header)
                    except:
                        file_sockets.remove(fl_sk)
                        fl_sk.close()
            
            remaining = filesize
            with open(filename, "wb") as f:
                while remaining > 0:
                    chunk = cliente.recv(min(256000000, remaining))
                    if not chunk:
                        break

                    f.write(chunk)
                    remaining -= len(chunk)
            
            for fl_sk in file_sockets.copy():
                if fl_sk != cliente:
                    fl_sk.sendall(chunk)
                    
            print(f"[↓] Archivo distribuido: {filename}")
                    
        except:
            break

def aprobar_cliente(addr):
    while True:
        decision = input(f"[?] Permitir conexión desde {addr}? (y/n): ").lower()
        if decision in ("y", "n"):
            return decision == "y"

def aceptar_clientes():
    while True:
        client_socket, client_address = s.accept()
        file_client, file_adress = fs.accept()

        print(f"[+] Solicitud de conexion {client_address}.")

        if not aprobar_cliente(client_address):
            print("[✗] Conexión rechazada")
            client_socket.close()
            file_client.close()
            continue

        print("[✓] Cliente aceptado")
        
        with lock:
            client_sockets.add(client_socket)
            file_sockets.add(file_client)

        Thread(target=Inicializacion_de_cliente, args=(client_socket,), daemon= True).start()
        Thread(target=recibir_archivos, args=(file_client,), daemon=True).start()

def comandos_de_servidor():
    pass

try:
    aceptar_clientes()
except KeyboardInterrupt:
    print("\n[!] Cerrando servidor...")
finally:
    for cs in client_sockets:
        cs.close()
    s.close()
    fs.close()
    print("[/] Servidor cerrado correctamente.")
#habilitar comados de server