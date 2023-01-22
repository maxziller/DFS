"""
Servidor local - ainda sem conexão
Necessidades: Controle de nomes e metadados

"""
import hashlib
import shutil
import ctypes
import os
import filecmp
import datetime

Files = "Files/"
Control = "Control/"
Meta = "Meta/"
usuarios = "Control/users.txt"

"""
Inicializa o objeto para manipulação dos meta-dados do arquivo
Cria listas que serão usadas para controlar as permissões de acesso e os históricos de modificações e acessos
Chama função que cria arquivo para salvar estes meta-dados
Seus atributos são:

nome - O nome do arquivo
caminho - O endereço até o arquivo na máquina
tamanho - O tamanho atual do arquivo
usuariocriacao - O nome do usuário que criou o arquivo
datahoracriacao - Quando o arquivo foi criado
listamodificacao - Lista de tuplas, cada tupla contém o usuário e o datetime da modificação salva
listaacessos - Lista de tuplas, cada tupla contém o usuário e o datetime do acesso ao arquivo
listapermissões - Lista de nomes de usuário que têm permissão para acessar o arquivo
ocupado - Colocado como False quando ninguém está acessando o arquivo ou com o nome do usuário que acessa como forma de hardlock
"""
class File:
    def __init__(self,nome,usuario):
        self.nome = nome
        self.caminho = Files + self.nome
        self.tamanho = self.atualizatamanho()
        self.usuariocriacao = usuario
        self.metaarquivo = self.achameta()
        self.ocupado = False

    """
    Função chamada logo na inicialização
    Cria arquivo que salva os metadados com o mesmo nome do arquivo original, mas na pasta secreta de meta-arquivos
    """
    def achameta(self):
        endereco = Meta + self.nome
        try:
            arquivo = open(endereco,'r',encoding='utf8')
            self.lemeta(arquivo)
            arquivo.close()
        except IOError:
            agora = datetime.now()
            metaarquivo = open(endereco,'x')
            metaarquivo.write("Criação: ")
            metaarquivo.write(str(agora))
            self.datahoracriacao = agora
            metaarquivo.write("\nUsuário criador: "+self.usuariocriacao)
            self.listamodificacao = [(self.usuariocriacao,agora)]
            metaarquivo.write("\nLista de modificações: {" + self.usuariocriacao + "\\" + str(agora)+"}\n")
            metaarquivo.write("\nLista de acessos: {" + self.usuariocriacao + "\\" + str(agora)+"}\n")
            self.listaacessos = [(self.usuariocriacao,agora)]
            metaarquivo.write("\nLista de permissões: {" + self.usuariocriacao + "}\n")
            self.listapermissoes = [self.usuariocriacao]
            metaarquivo.close()
        return endereco
        
    """
    Função a ser chamada sempre que houver uma atualização do arquivo para atualizar a informação de tamanho
    """
    def atualizatamanho(self):
        self.tamanho = os.path.getsize(self.caminho)

    """
    Função usada quando um novo acesso e solicitado
    Verifica se o usuário solicitante tem permissão
    """
    def permitiracesso(self,usuario):
        if usuario in self.listapermissoes:
            self.listaacessos.append( (usuario,datetime.now()) )
            return True
        else:
            return False

    """
    Função que verifica se houve, de fato, alguma mudança no arquivo
    Caso não tenha havido, mesmo que tenha sido pedido para atualizar para uma nova versão, o pedido pode ser ignorado
    """
    def testamudanca(self,novoarquivo):
        atual = open(self.caminho,'r')
        novo = open(novoarquivo,'r')
        return filecmp(atual,novo)

    """
    Função que recebe um novo arquivo para atualizar um antigo
    """
    def atualiza(self,novoarquivo,usuario):
        if not self.testamudanca(novoarquivo):
            os.remove(self.caminho)
            importaarquivo(novoarquivo)
            self.listamodificacoes.append((usuario,datetime.now()))
            self.atualizameta()
            return True
        else:
            return False

    """
    Função que cria uma cópia do arquivo
    """
    def copia(self,usuario):
        i = 2
        while (os.path.isfile(Files+self.name+"("+str(i)+")")):
               i += 1
        novonome = Files+self.name+"("+str(i)+")","x"
        novoarquivo = open(novonome,'x')
        velhoarquivo = open(self.nome,'r')   
        novo = File(novonome,datetime.now(),usuario)
        for linha in velhoarquivo:
               novoarquivo.write(linha)
        novoarquivo.close()
        velhoarquivo.close()
        novo.listapermissoes = copy.deepcopy(self.listapermissoes)
        novo.atualizameta()
        return novonome
    
    """
    Função para deletar o arquivo
    """
    def excluir(self):
        os.remove(self.metaarquivo)
        os.remove(self.caminho)
        return
        
    """
    Função que renomeia o arquivo no sistema
    """
    def renomear(self,novonome):
        os.rename(self.caminho,Files + novonome)
        os.rename(self.metaarquivo, Meta + novonome)
        self.nome = novonome
        return
        
    """
    Função que adiciona um usuário na lista de permissões
    """
    def darpermissao(self,usuario):
        if usuario not in self.listapermissoes:
            self.listapermissoes.append(usuario)
            return self.atualizameta()
        else:
            return False

    """
    Função que deleta um usuário que não seja criador do arquivo das permissões
    """
    def tirapermissao(self,usuario):
        if ( (usuario == self.usuariocriacao) or (usuario not in self.listapermissoes) ):
            return False
        else:
            self.listapermissoes.remove(usuario)
            return self.atualizameta()
        
    def mostraacessos(self):
        return self.listaacessos

    """
    Função que é chamada a cada modificação confirmada para atualizar o metaarquivo com as informações devidas
    """
    def atualizameta(self):
        try:
            return self.escrevenovometa()
        except IOError:
            return False
        
    def escrevenovometa(self):
        endereco = Meta + self.nome
        try:
            metaarquivo = open(endereco,'w',encoding='utf8')
        except IOError:
            metaarquivo = open(endereco,'x',encoding='utf8')
        metaarquivo.write("Criação: ")
        metaarquivo.write(str(self.datahoracriacao))
        metaarquivo.write("\nUsuário criador: "+self.usuariocriacao)
        metaarquivo.write("\nLista de modificações: ")
        for mod in self.listamodificacoes:
            metaarquivo.write("{" + mod[0] + "\\" + str(mod[1]) + "}")
        metaarquivo.write("\n")
        metaarquivo.write("\nLista de acessos: ")
        for acesso in self.listaacessos:
            metaarquivo.write("{" + acesso[0] + "\\" + str(acesso[1]) + "}")
        metaarquivo.write("\n")
        metaarquivo.write("\nLista de permissões: ")
        for permissao in self.listapermissoes:
            metaarquivo.write("{" + permissao + "}")
        metaarquivo.close()
        return True

    def lemeta(arquivo):
        int i
        for linha in arquivo:
            if (i == 1):
                horario = linha.lstrip("Criação: ")
                self.datahoracriacao = datetime.strptime(horario.strip())
            elif (i == 2):
                criador = linha.strip()
                criador = criador.lstrip("Usuário criador: ")
                self.usuariocriacao = criador
            elif (i == 3):
                self.listamodificacoes = []
                lista = linha.strip()
                lista = lista.lstrip("Lista de modificações: {")
                lista = lista.rstrip("}")
                lista.split("}{")
                for mod in lista:
                    x = tuple(mod.split("\\"))
                    y = (x[0],datetime.strptime(x[1]))
                    self.listamodificacoes.append(y)
            elif (i == 4):
                self.listaacessos = []
                lista = linha.strip()
                lista = lista.lstrip("Lista de acessos: {")
                lista = lista.rstrip("}")
                lista.split("}{")
                for acesso in lista:
                    x = tuple(acesso.split("\\"))
                    y = (x[0],datetime.strptime(x[1]))
                    self.listaacessos.append(y)
            elif (i == 5):
                lista = linha.strip()
                lista = lista.lstrip("Lista de acessos: {")
                lista = lista.rstrip("}")
                lista.split("}{")
                self.listapermissoes = lista
            i += 1
    


class Servidor:
    def __init__(self):
        self.usuarios = self.listausuarios()
        self.arquivos = {}
        self.pasta = os.listdir(Files)
        for arquivo in pasta:
            novo = File(arquivo,"System")
            self.arquivos[arquivo] = novo
        self.exibearquivos("System")

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
    def listausuarios(self):
        lista = []
        users = carregausuarios()
        for user in users:
            lista.append(user[0])
        return lista

    """
    Função temporária só pra testes - o servidor não precisa de interface
    """
    def exibearquivos(self,usuario):
        print("Arquivos disponíveis: \n")
        for arquivo in self.arquivos:
            if ( (usuario in arquivo.listaacessos) or (usuario == "System") ):
                if (arquivo[1] == True):
                    situacao = "Disponível
                else:
                    situacao = "Ocupado por " + arquivo[1]
                print(arquivo[0] + " - " + situacao)
    
    def pedeacesso(usuario,arquivo):
        if ( (arquivo in self.arquivos.keys()) and (usuario in self.arquivos[arquivo].listapermissoes) and (self.arquivos[arquivo].ocupado == False) ):
            #
            #
            #Enviar o arquivo
            #
            #
            self.arquivos[arquivo].ocupado = usuario
            return True
        else:
            return False

    def fechaarquivo(arquivo):
        if (arquivo in self.arquivos.keys()):
            self.arquivos[arquivo].ocupado = False
            return True
        else:
            return False

    """
    Função para trazer para a pasta de arquivos do sistema um arquivo através de seu endereço
    """ 
    def importaarquivo(original):
        try:
            arquivo = original[original.rfind("/")+1:]
            shutil.copyfile(original,Files+arquivo)
            return True
        except IOError:
            return False


    
    


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
        ret = ctypes.windll.kernel32.SetFileAttributesW(Control, FILE_ATTRIBUTE_HIDDEN)
    return 0



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
    lista = carregausuarios()
    h = Sha512Hash(senha).strip()
    if (h == lista[user]):
        return True
    else:
        return False

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
    print("Menu")


f = input("Caminho até o arquivo a ser copiado\n")
importaarquivo(f)
