import socket			
import hashlib
import time
import os
from assets import *


def cria_socket_client():
    for i in range(1, 10):
        try: 
            host = socket.gethostname()
            port = 5000
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            print("Conectado com o servidor!")
            login(client_socket)
        except:
            print(f"Erro ao conectar com o servidor, tentando novamente... {i}/10")
            time.sleep(10)
            continue


def login(client_socket):
    # Recebe mensagem de boas vindas do servidor
    print(client_socket.recv(1024).decode())
    
    # Envia username para o servidor
    username = input("Digite seu username:")
    while (" " in username):    
        username = input("Não é permitido o uso de espaços no nome de usuário, digite novamente:")
    client_socket.send(username.encode())

    # Envia password para o servidor
    password = input("Digite sua senha:")
    password = Sha512Hash(password)
    client_socket.send(password.encode())

    # Recebe mensagem de login efetuado ou falhou
    data = client_socket.recv(2048).decode()

    cls()
    print(data)
    if(data == "Login efetuado com sucesso\n"):
        comunicacao(client_socket)
    else:    
        login(client_socket)
        

def comunicacao(conn):
    while True:
        # recebe comunicacao do servidor
        print(conn.recv(2048).decode())

        # envia comunicacao para o servidor
        data = input()
        conn.send(data.encode())
       

def main():
    inicializa()
    cria_socket_client()

main()

