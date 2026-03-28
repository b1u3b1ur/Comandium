import os
import socket
import random
import struct
import threading
import base64
import atexit
import hashlib
from threading import Thread
from cryptography.fernet import Fernet

def leer_puerto():
    try:
        with open("port.txt", "r") as f:
            contenido = f.read().strip()
            if not contenido:
                return "No hay datos previos."
            else:
                return contenido
    except FileNotFoundError:
        return "No hay datos previos."

if leer_puerto() == "No hay datos previos.":
    SERVER_PORT = int(input("Elija su puerto:"))
else:
    SERVER_PORT = int(leer_puerto())
CLAVE_SECRETA = str(input("Elija la clave de su chat:"))
key = base64.urlsafe_b64encode(hashlib.sha256(CLAVE_SECRETA.encode()).digest())
cipher = Fernet(key)
SERVER_HOST = "0.0.0.0"
separator_token = "<SEP>"
DOWNLOAD_DIR = "Comandium/server"
data_traveler = 256000000
aceptando = True

lock = threading.Lock()

client_sockets = set()
file_sockets = set()
pending = set()

s = socket.socket()
fs = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
fs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((SERVER_HOST, SERVER_PORT))
fs.bind((SERVER_HOST, SERVER_PORT + 1))

s.listen()
fs.listen()

F_C_PORT= SERVER_PORT + 1
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.connect(("8.8.8.8", 80)) 
Server_name = c.getsockname()[0]
c.close()

print(f'[*] Servidor inicializado como: {SERVER_HOST}:{SERVER_PORT}',flush=True)
print(f"[*] Canal archivos en {F_C_PORT}",flush=True)
print(f"[*] Clave de chat: {CLAVE_SECRETA}",flush=True)
print(f"[*] IP de conexion {Server_name}")
print(f'''Para que la aplicacion se pueda aceptar fuera de una red local dirijase a la red de su modem (IP)
y habilite los puertos que selecciono en la opcion reenvio de puerto o port forwarding''',flush=True)

def Inicializacion_de_cliente(cs):
    while True:
        try:
            msg_encriptado = cs.recv(4096)
            if not msg_encriptado: break

            try:
                msg_descifrado = cipher.decrypt(msg_encriptado).decode()
                text = msg_descifrado.replace(separator_token, ": ")
                print(f'[*] {text}',flush=True)
                
                with lock:
                    for client_socket in client_sockets.copy():
                        if client_socket != cs:
                            try:
                                client_socket.sendall(msg_encriptado)
                            except:
                                client_sockets.remove(client_socket)
            except Exception as e:
                print(f"[!] Error al descifrar o reenviar: {e}",flush=True)
        except:
            break
    
    with lock:
        if cs in client_sockets: client_sockets.remove(cs)
    cs.close()
    print("[!] Cliente desconectado.",flush=True)

def recibir_archivos(cliente):
    while True:
        try:
            header_len_data = cliente.recv(4)
            if not header_len_data: break

            header_len = struct.unpack("I", header_len_data)[0]
            header = cliente.recv(header_len)
            
            filename, filesize = header.decode().split(separator_token)
            filesize = int(filesize)
            print(f"[>] Recibiendo: {filename} ({filesize} bytes)",flush=True)

            target_dir = os.path.join(os.path.expanduser("~"), "Documents", DOWNLOAD_DIR)
            os.makedirs(target_dir, exist_ok=True)
            save_path = os.path.join(target_dir, filename)
            
            # Notificar a otros sockets de archivo
            with lock:
                for fl_sk in file_sockets.copy():
                    if fl_sk != cliente:
                        try:
                            fl_sk.sendall(header_len_data)
                            fl_sk.sendall(header)
                        except:
                            file_sockets.remove(fl_sk)
            
            remaining = filesize
            with open(save_path, "wb") as f:
                while remaining > 0:
                    chunk = cliente.recv(min(data_traveler, remaining))
                    if not chunk: break
                    f.write(chunk)

                    with lock:
                        for fl_sk in file_sockets.copy():
                            if fl_sk != cliente:
                                try: fl_sk.sendall(chunk)
                                except: pass
                    remaining -= len(chunk)
            print(f"[I] Archivo {filename} distribuido.",flush=True)
        except:
            break

# def aprobar_cliente(addr):
#     while True:
#         decision = input(f"[?] Permitir conexion desde {addr}? (y/n): ").lower()
#         if decision in ("y", "n"):
#             return decision == "y"

def aceptar_clientes():
    global aceptando
    while True:
        client_socket, client_address = s.accept()
        file_client, file_address = fs.accept()

        if not aceptando:
            client_socket.close()
            file_client.close()
            continue

        print(f"[+] Nueva solicitud desde {client_address}. Agregado a /pending",flush=True)
        with lock:
            pending.add((client_socket, file_client, client_address))

        # Thread(target=Inicializacion_de_cliente, args=(client_socket,), daemon= True).start()
        # Thread(target=recibir_archivos, args=(file_client,), daemon=True).start()

def comandos_de_servidor():
    global aceptando

    while True:
        cmd = input("\n[ADMIN]> ").strip()
        if not cmd:
            continue

        parts = cmd.split()
        comando = parts[0].lower()
        args = parts[1:]

        if comando == "/help":
            print("""
/help                 -> Muestra comandos
/pending              -> Lista clientes pendientes
/accept <id>          -> Acepta cliente pendiente
/reject <id>          -> Rechaza cliente pendiente
/usuarios             -> Lista usuarios conectados
/kick <ip:puerto>     -> Expulsa usuario conectado
/lock                 -> Bloquea nuevas conexiones
/unlock               -> Permite nuevas conexiones
/broadcast            -> Mensaje a todos
/limpiar              -> Limpia consola (tener cuidado elimina los puertos y sus llaves)
/salir                -> Apaga el servidor
""",flush=True)

        elif comando == "/usuarios":
            with lock:
                print(f"[*] Usuarios conectados: {len(client_sockets)}",flush=True)
                for uid in client_sockets:
                    print(" -", uid)
        
        elif comando == "/mute":
            pass
        
        elif comando == "/unmute":
            pass
        
        elif comando == "/warn":
            pass
        
        elif comando == "/warning":
            pass
        
        elif comando == "/":
            pass

        elif comando == "/lock":
            aceptando = False
            print("[!] Servidor bloqueado.",flush=True)
            continue

        elif comando == "/unlock":
            aceptando = True
            print("[!] Servidor desbloqueado.",flush=True)
            continue

        elif comando == "/pending":
            with lock:
                if not pending: print("[*] No hay pendientes."); continue
                for i, (_, _, addr) in enumerate(list(pending)):
                    print(f" [{i}] {addr[0]}:{addr[1]}",flush=True)

        elif comando == "/accept":
            if not args: continue
            idx = int(args[0])
            with lock:
                pend_list = list(pending)
                if 0 <= idx < len(pend_list):
                    cs, fsoc, addr = pend_list[idx]
                    pending.remove(pend_list[idx])
                    client_sockets.add(cs)
                    file_sockets.add(fsoc)
                    Thread(target=Inicializacion_de_cliente, args=(cs,), daemon=True).start()
                    Thread(target=recibir_archivos, args=(fsoc,), daemon=True).start()
                    print(f"[+] {addr} aceptado.",flush=True)

        elif comando == "/reject":
            if not args:
                print("[!] Uso: /reject <index>",flush=True)
                continue

            try:
                idx = int(args[0])
            except:
                print("[!] El index debe ser un número.",flush=True)
                continue

            with lock:
                pend_list = list(pending)

                if idx < 0 or idx >= len(pend_list):
                    print("[!] Index inválido.",flush=True)
                    continue

                client_socket, file_client, addr = pend_list[idx]
                pending.remove(pend_list[idx])

            try:
                client_socket.sendall(f"SERVER{separator_token}Conexión rechazada.".encode())
            except:
                pass

            try:
                client_socket.close()
            except:
                pass

            try:
                file_client.close()
            except:
                pass

            print(f"[X] Cliente rechazado: {addr[0]}:{addr[1]}",flush=True)

        elif comando == "/kick":
            if not args:
                print("[!] Uso: /kick <ip>",flush=True)
                continue

            target_ip = args[0]
            kicked = False

            with lock:
                for cs in list(client_sockets):
                    try:
                        ip, port = cs.getpeername()
                    except:
                       continue

                    if ip == target_ip:
                        try:
                            cs.sendall(f"SERVER{separator_token}Has sido expulsado.".encode())
                        except:
                            pass

                        try:
                            cs.close()
                        except:
                            pass

                        client_sockets.remove(cs)
                        kicked = True
                        break

                for fsoc in list(file_sockets):
                    try:
                        ip, port = fsoc.getpeername()
                    except:
                        continue

                    if ip == target_ip:
                        try:
                            fsoc.close()
                        except:
                            pass

                        file_sockets.remove(fsoc)
                        break

            if kicked:
                print(f"[V] Expulsado: {target_ip}")
            else:
                print("[!] No se encontró ese usuario.")

        elif comando == "/broadcast":
            msg = input("Mensaje: ").strip()
            # IMPORTANTE: Cifrar el mensaje del servidor
            payload = cipher.encrypt(f"SERVER{separator_token}{msg}".encode())
            with lock:
                for cs in client_sockets:
                    try: cs.sendall(payload)
                    except: pass
            print("[V] Enviado.",flush=True)
            print("[V] Broadcast enviado.",flush=True)

        elif comando == "/limpiar":
            os.system("cls" if os.name == "nt" else "clear")

        elif comando == "/salir":
            print("[!] Apagando...")
            os._exit(0)

        else:
            print(f"[?] Comando '{comando}' no reconocido. Usa /help",flush=True)

try:
    print("[*] Consola de administración lista. Escribe '/help' para ver info.",flush=True)
    Thread(target=comandos_de_servidor, daemon=True).start()
    aceptar_clientes()
except KeyboardInterrupt:
    print("\n[!] Cerrando servidor...",flush=True)
finally:
    for cs in client_sockets:
        cs.close()
    s.close()
    fs.close()
    print("[/] Servidor cerrado correctamente.",flush=True)

def save(data):
    if data:
        with open("port.txt", "w") as f:
            f.write(data)
    else:
        pass
    
atexit.register(save(SERVER_PORT))