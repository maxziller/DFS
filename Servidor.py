"""
Servidor local - ainda sem conexão
Necessidades: Controle de nomes e metadados

"""
import hashlib
import shutil
import ctypes
import os
from datetime import datetime

Files = "Files/"
Control = "Control/"
Meta = "Meta/"
usuarios = "Control/users.txt"

class arquivo:
    def __init__(self,nome,tamanho,datahoracriacao,usuariocriacao):
        self.nome = nome
        self.tamanho = tamanho
        self.datahoracriacao = datahoracriacao
        self.usuariocriacao = usuariocriacao
        self.listamodificacao = [(usuariocriacao,datetime.now())]
        self.listaacessos = [(usuariocriacao,datetime.now())]
        self.listapermissoes = [usuariocriacao]
        self.caminho = Files + self.nome

    def atualizatamanho(self):
        self.tamanho = os.path.getsize(self.caminho)

    def novoacesso(self,usuario):
        if usuario in self.listapermissoes:
            self.listaacessos.append( (usuario,datetime.now()) )
            return True
        else:
            return False

    #def atualiza(self,novoarquivo)
    #def copia(self)
    #def excluir(self)
    #def renomear(self)
    #def mostrapermissoes(self)
    #def addpermissao(self,usuario)
    #def mostraacessos(self)
    

"""
Função chamada logo que o app começa a rodar
Cria no servidor as pastas que serão utilizadas
a pasta Files servirá para salvar os arquivos dos usuários
a pasta Control servirá para salvar os arquivos inerentes do próprio sistema, como lista de usuários
a pasta Meta servirá para salvar arquivos espelho de cada arquivo do usuário, só que contendo seus metadados
"""
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

def abrearquivo(nome, endereco):
    abrir = endereco + "/" + nome
    arquivo = open(abrir,'r',encoding='UTF-8')

"""
Função para trazer para a pasta de arquivos do sistema um arquivo através de seu endereço
""" 
def importaarquivo(original):
    arquivo = original[original.rfind("/")+1:]
    shutil.copyfile(original,Files+arquivo)

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

"""
A maior parte dessa função será transferida para o .py Usuário posteriormente, pois o Servidor não precisa de interface
Mas por enquanto é o que tá tendo
Depois rearranja
""" 
def login():
    while(1):
        user = input("Usuário: ")
        if (" " in user):
            print("Não é permitido o uso de espaços no nome de usuário")
        else:
    
            if (verificausuario(user)):
                senha = input("Senha: ")
                if (verificasenha(user,senha)):
                    print("Seja bem-vindo, "+user)
                    break
                else:
                    print("Senha incorreta")
            else:
                senha = input("Crie sua senha para o novo usuário: ")
                insereusuario(user,senha)
                print("Seja bem-vindo, "+user)
                break
    return user

"""
Função que faz o hash de forma determinística e estável, podendo ser comparado com vezes posteriores
"""
def Sha512Hash(Password):
    HashedPassword=hashlib.sha512(Password.encode('utf-8')).hexdigest()
    return(HashedPassword)



print("Doodle Grive\n")
inicializa()
print("Faça seu login\n")
user = login()
f = input("Caminho até o arquivo a ser copiado\n")
importaarquivo(f)

