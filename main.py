# proyecto chat
import socket
from threading import Thread

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5005
separator_token = "<SEP>"

client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f'[*] Servidor inicializado como: {SERVER_HOST}:{SERVER_PORT}')

def Inicializacion_de_cliente(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
            if not msg:  
                break
            msg = msg.replace(separator_token, ": ")
            print(f'[*] {msg}')
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

try:
    while True:
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} conectado.")
        client_sockets.add(client_socket)
        t = Thread(target=Inicializacion_de_cliente, args=(client_socket,))
        t.daemon = True  
        t.start()
except KeyboardInterrupt:
    print("\n[!] Cerrando servidor...")
finally:
    for cs in client_sockets:
        cs.close()
    s.close()
    print("[/] Servidor cerrado correctamente.")

# remember to change it's no finished 