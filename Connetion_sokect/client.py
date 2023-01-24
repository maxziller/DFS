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

    if(data == "Login efetuado com sucesso\n"):
        print(data)
        cls()
        data = client_socket.recv(2048).decode()
        print(data)
        #'1 - Listar arquivos\n
        # 2 - Download arquivo\n
        # 3 - Salvar arquivo\n
        # 4 - Deletar arquivo\n
        # 5 - Sair\n'
        while True:
            data = input("Digite a opcao desejada: ")
            client_socket.send(data.encode())
            
            if(data == "1"):
                listaArquivos = client_socket.recv(2048).decode()
                cls()
                print("Arquivos disponiveis no servidor: \n", listaArquivos)
            elif(data == "2"):
                # Download arquivo

                msg = client_socket.recv(2048).decode()
                print(msg)
                numArquivo = input()
                client_socket.send(str(NumArquivo).encode())
                filename, filesize = client_socket.recv(1024).decode().split("//")
                filesize = int(filesize)
                client_socket.send("OK".encode())
                with open('./Files//' + filename, "wb") as f:
                    bytes_read = client_socket.recv(1024)
                    f.write(bytes_read)
                    total_recv = len(bytes_read)
                    while total_recv < filesize:
                        bytes_read = client_socket.recv(1024)
                        f.write(bytes_read)
                        total_recv += len(bytes_read)
                        print(f"{total_recv}/{filesize} bytes received")
                print("Download completo!")

            elif(data == "3"):
                # Salvar arquivo
                filename, filesize = client_socket.recv(1024).decode().split("//")
                filesize = int(filesize)
                client_socket.send("OK".encode())
                with open('./Files//' + filename, "wb") as f:
                    bytes_read = client_socket.recv(1024)
                    f.write(bytes_read)
                    total_recv = len(bytes_read)
                    while total_recv < filesize:
                        bytes_read = client_socket.recv(1024)
                        f.write(bytes_read)
                        total_recv += len(bytes_read)
                        print(f"{total_recv}/{filesize} bytes received")
                print("Download completo!")
            elif(data == "4"):
                # deletar arquivo
                filename = input("File to delete : ")
                client_socket.send(filename.encode())
                data = client_socket.recv(2048).decode()
                print(data)
                continue
            elif(data == "5"):
                print("Saindo...")
                client_socket.send("Saindo...\n".encode())
                client_socket.close()
                break
    else:
        print(data)
        input("Press any key to exit")
        client_socket.close()


def main():
    inicializa()
    cria_socket_client()

main()

