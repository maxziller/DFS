import socket			
import hashlib
import time
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
    #data = client_socket.recv(1024).decode()
    username = input("Digite seu username:")
    while (" " in username):    
        username = input("Não é permitido o uso de espaços no nome de usuário, digite novamente:")
    client_socket.send(username.encode())

    # Envia password para o servidor
    #data = client_socket.recv(1024).decode()
    password = input("Digite sua senha:")
    password = Sha512Hash(password)
    client_socket.send(password.encode())


    # Recebe mensagem de login efetuado ou falhou
    data = client_socket.recv(1024).decode()
    if(data == "Login efetuado com sucesso\n"):
        print(data)
        print("Agora você pode enviar mensagens para o servidor")
        print("1 - Listar arquivos")
        print("2 - Enviar arquivo")
        print("3 - Receber arquivo")
        print("4 - Deletar arquivo")
        print("5 - Sair")

        while True:
            data = input("Digite a opcao desejada: ")
            client_socket.send(data.encode())
            if(data == "exit"):
                break
    else:
        print(data)
        input("Press any key to exit")
        client_socket.close()

def Sha512Hash(Password):
    HashedPassword=hashlib.sha512(Password.encode('utf-8')).hexdigest()
    return(HashedPassword)

cria_socket_client()

