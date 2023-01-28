import socket			
import hashlib
import time
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def imprimemenu():
    print("\n\n------------------------------------------\n\n")
    print("Opções do sistema: \n")
    print("0 - Exibir arquivos\n")
    print("1 - Abrir um arquivo\n")
    print("2 - Fechar um arquivo\n")
    print("3 - Excluir um arquivo\n")
    print("4 - Renomear um arquivo\n")
    print("5 - Adicionar ou atualizar arquivo\n")
    print("6 - Dar permissão de acesso do arquivo a outro usuário\n")
    print("7 - Retirar permissão de acesso de outro usuário\n")
    print("8 - Mostrar histórico de acessos de um arquivo\n")
    print("9 - Mostrar lista de usuários com permissão de acesso\n")
    print("10 - Mostrar lista de modificações de um arquivo\n")
    print("11 - Sair\n")

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
            time.sleep(6)
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
    print(data)
    if( ("Login efetuado" in data) or ("Cadastro efetuado" in data)):
        cls()
        recebemensagens(client_socket)
        while True:
            imprimemenu()
            data = input("Digite a opcao desejada: ")
            data = data.strip()
            if(data == "10"):
                print("Saindo...")
                client_socket.send("10".encode())
                client_socket.recv(1028).decode()
                client_socket.close()
                break
            elif(data == "0"):
                client_socket.send("0".encode())
                recebemensagens(client_socket)
                print("\n\n")
            elif(data == "1"):
                client_socket.send("1".encode())
                print("Selecione um dos arquivos disponíveis: \n")
                recebemensagens(client_socket)
                arq = input("Filename: ")
                arq = arq.strip()
                client_socket.send(arq.encode())
                #
                #
                # Necessário completar quando tivermos arquivos na pasta
                #
                #
            elif(data == "5"):
                client_socket.send("5".encode())
                print("Coloque o endereço do arquivo a ser enviado: \n")
                arq = input("Endereço: ")
                arq = arq.strip()
                if ("\\") in arq:
                    posinome = arq.rfind("\\")
                else:
                    posinome = arq.rfind("/")
                nome = arq[posinome + 1:]
                client_socket.send(nome.encode())
                with open(arq, 'rb') as arquivo:
                    sendfile = arquivo.read()
                client_socket.sendall(sendfile)
                print("\nArquivo salvo\n")
                
    else:
        print(data)
        input("Press any key to exit")
        client_socket.close()

def Sha512Hash(Password):
    HashedPassword=hashlib.sha512(Password.encode('utf-8')).hexdigest()
    return(HashedPassword)

def recebemensagens(client_socket):
    msg = client_socket.recv(4096).decode()
    while not(msg.endswith("Acabou")):
        print(msg)
        msg = client_socket.recv(4096).decode()
    return

cria_socket_client()

