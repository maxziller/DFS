import socket			
import time
import hashlib
import shutil
import ctypes
import os
import threading
from datetime import datetime
from assets import *

def start_server():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    		
    server_socket.listen(5)
    print ("Server listening")	
    conns = set() # armazena as conexões dos clientes
    while True:
        conn, addr = server_socket.accept()	
        print ('Conexão aceita, bem vindo ' + str(addr))
        try:
            conns.add(conn)
            thread = threading.Thread(target=execute_server, args = (conn, addr))
            thread.start()
        except:
            print("Erro ao iniciar thread")
            conn.close()
            continue


def execute_server(conn, addr):
    while True:
        conn.send('Bem vindo ao servidor de arquivos!\n'.encode())
        time.sleep(5)
        
        # verifica se o usuário já existe
        if(login(conn)):
            menu(conn, addr)
        else:
            print("Erro ao fazer login")
            conn.close()
            break

def menu(conn, addr):
    while True:
        conn.send('1 - Listar arquivos\n'.encode())
        conn.send('2 - Enviar arquivo\n'.encode())
        conn.send('3 - Receber arquivo\n'.encode())
        conn.send('4 - Deletar arquivo\n'.encode())
        conn.send('5 - Sair\n'.encode())
        time.sleep(5)
        data = conn.recv(2048).decode()
        if(data == "1"):
            listarArquivos(conn, addr)
        elif(data == "2"):
            enviarArquivo(conn, addr)
        elif(data == "3"):
            receberArquivo(conn, addr)
        elif(data == "4"):
            deletarArquivo(conn, addr)
        elif(data == "5"):
            conn.close()
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
                print("Login efetuado com sucesso\n")
                time.sleep(5)
                return True
                break
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