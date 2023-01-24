usuarios = "Control/users.txt"
Files = "Files/"
Control = "Control/"
Meta = "Meta/"

import socket			
import time
import hashlib
import shutil
import ctypes
import os
import threading
from datetime import datetime

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

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def listarArquivos(conn, addr):
    cls()
    conn.send("Listando arquivos".encode('utf-8'))
    lista = os.listdir(Files)
    # criando string da lista com numero para cada arquivo e nome do arquivo
    for i in range(len(lista)):
        lista[i] = str(i) + " - " + lista[i]

    return lista



def enviarArquivo(conn, addr, numeroArquivo):
    # selecionar pelo numero do arquivo
    lista = listarArquivos(conn, addr)
    nomeArquivo = lista[numeroArquivo].split(" - ")[1]
    conn.send("Download de arquivo".encode('utf-8'))
    # envia o arquivo
    with open(Files + nomeArquivo, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            conn.send(data)
    conn.send("Fim do arquivo".encode('utf-8'))

def receberArquivo(conn, addr):
    conn.send("Salvar arquivo".encode('utf-8'))

def deletarArquivo(conn, addr):
    conn.send("Deletar arquivo".encode('utf-8'))


