import socket			
import time
import hashlib
import shutil
import ctypes
import os
from datetime import datetime

Files = "Files/"
Control = "Control/"
Meta = "Meta/"
usuarios = "Control/users.txt"

def cria_socket_server():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    		
    server_socket.listen(2)
    print ("Server listening")		
    c, addr = server_socket.accept()	
    print ('Got connection from ' + str(addr))
    c.send('Bem vindo ao servidor caralho!\n'.encode())
    
    while True:
        # get username
        username = c.recv(2048)
        username = username.decode()
       
        # get password 
        password = c.recv(2048)
        password = password.decode()

        if (verificausuario(username)):
            if (verificasenha(username,password)):
                print("Seja bem-vindo, " + username)
                c.send("Login efetuado com sucesso\n".encode())
                print("Login efetuado com sucesso\n")
                time.sleep(5)
                break
            else:
                print("Senha incorreta")
                c.send("Login falhou, encerrando conexão".encode())
                time.sleep(5)
                c.close()
                break
        else:
            print("Usuário não cadastrado, inserindo novo usuário")
            insereusuario(username, password)
            print("Seja bem-vindo, "+ username)
            c.send("Login efetuado com sucesso\n".encode())
            print("Login efetuado com sucesso\n")
            time.sleep(5)
            # tem que listar os arquivos do usuário
            input("Press any key to exit")
                        

def Sha512Hash(Password):
    HashedPassword=hashlib.sha512(Password.encode('utf-8')).hexdigest()
    return(HashedPassword)

"""
Função que abre o arquivo com as informações dos usuários e as organiza num dicionário
No dicionário, o nome do usuário é a chave e o hash da senha é o dado
O dicionário é retornado
"""
def carregausuarios():
    users = {}
    try:
        arquivo = open(usuarios,'r',encoding='utf8')
        for linha in arquivo:
            senha = (linha.strip()).split(' ',1)
            users[senha[0]] = senha[1]
        
    except IOError:
        arquivo = open(usuarios,'x',encoding='utf8')
    arquivo.close()
    return users

"""
Função que retorna uma lista com todos os nomes de usuário
"""
def listausuarios():
    lista = []
    users = carregausuarios()
    for user in users:
        lista.append(user[0])
    return lista

"""
Função que verifica se o usuário já está ou não registrado no sistema
"""
def verificausuario(user):
    users = carregausuarios()
    if user in users.keys():
        return True
    else:
        return False

"""
Função que insere novo usuário no sistema com sua senha já em hash
"""
def insereusuario(usuario,senha):
    arquivo = open(usuarios,'a',encoding='utf8')
    arquivo.write(usuario)
    arquivo.write(" ")

    arquivo.write(Sha512Hash(senha))
    arquivo.write("\n")
    arquivo.close()

def inicializa():
    if not os.path.isdir(Files):
        os.mkdir('./Files')
    if not os.path.isdir(Control):
        os.mkdir('./Control')
    if not os.path.isdir(Meta):
        os.mkdir('./Meta')
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ret = ctypes.windll.kernel32.SetFileAttributesW(Meta, FILE_ATTRIBUTE_HIDDEN)
    return 0

"""
Funçãoque verifica se o hash da senha colocada no input é igual ao hash da senha salvo
"""
def verificasenha(user,senha):
    arquivo = open(usuarios,'r',encoding='utf8')
    for linha in arquivo:
        linha = linha.strip()
        usuario = linha.split(" ",1)
        if (usuario[0] == user):
            h = Sha512Hash(senha).strip()
            if (h == usuario[1]):
                return True
            else:
                return False
            break

def main():
    inicializa()
    cria_socket_server()

if __name__ == "__main__":
    main()