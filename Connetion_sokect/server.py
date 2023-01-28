import socket			
import time
import hashlib
import shutil
import ctypes
import os
import threading
from datetime import datetime
from assets import *

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        print ("Server listening")	
        while True:
            client, address = self.sock.accept()
            print ('Conexão aceita, bem vindo ' + str(address))
            client.settimeout(600)
            threading.Thread(target = execute_server , args = (client,address)).start()

    def listenToClient(self, client, address):
        return client, address


def start_server():
    host = socket.gethostname()
    port = 5000

    ThreadedServer(host, port).listen()



def execute_server(conn, addr):
    while True:
        conn.send('Bem vindo ao servidor de arquivos!\n'.encode())
        
        # verifica se o usuário já existe
        if(login(conn)):
            menu(conn, addr)
        else:
            print("Erro ao fazer login")
            conn.close()
            break

def menu(conn, addr):
    while True:
        conn.send('\n1 - Listar arquivos\n2 - Download arquivo\n3 - Salvar arquivo\n4 - Deletar arquivo\n5 - Sair\n'.encode())
        data = conn.recv(2048).decode()
        print(data)
        if(data == "1"):
            lista = listarArquivos(conn, addr)
            conn.send(str(lista).encode('utf-8'))
            conn.send("\n".encode()) 
        elif(data == "2"):
            conn.send("Escolha um arquivo para baixar: ".encode())
            numF = conn.recv(2048).decode() # recebe o nome do arquivo
            enviarArquivo(conn, addr, numF) # envia o arquivo
            conn.send("\nArquivo enviado com sucesso!\n".encode())
        elif(data == "3"):
            receberArquivo(conn, addr)
        elif(data == "4"):
            deletarArquivo(conn, addr)
        elif(data == "5"):
            print("Saindo...")
            conn.send("Saindo...\n".encode())
            conn.close()
            start_server()
            break
        else:
            conn.send("Opção inválida\n".encode())
            time.sleep(5)

def login(conn):
    for i in range(3, 1, -1):
        # get username
        username = conn.recv(2048)
        username = username.decode()
       
        # get password 
        password = conn.recv(2048)
        password = password.decode()

        if (verificausuario(username)):
            if (verificasenha(username,password)):
                print("Seja bem-vindo, " + username)
                conn.send("Login efetuado com sucesso\n".encode())
                return True
            else:
                print("Senha incorreta")
                conn.send(f"Login falhou, você tem mais {i} tentativas!".encode())
                time.sleep(5)
        else:
            # caso tenha que cadastrar um novo usuario, requisitar senha de administrador
            print("Usuário não cadastrado, inserindo novo usuário")
            insereusuario(username, password)
            
            conn.send("Login efetuado com sucesso\n".encode())
            print("Login efetuado com sucesso\n")
            time.sleep(5)
            return True
            break

def main():
    inicializa() # cria pastas e arquivos iniciais
    start_server()

main()