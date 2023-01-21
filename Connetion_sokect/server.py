import socket			
import time

def cria_socket_server():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    		
    server_socket.listen(2)
    print ("Server listening")		
    c, addr = server_socket.accept()	
    print ('Got connection from ' + str(addr))
    c.send('Bem vindo ao servidor, seu maior pesadelo\n'.encode())
    
    while True:
        # get username
        username = c.recv(2048)
        username = username.decode()
       
        # get password 
        password = c.recv(2048)
        password = password.decode()
        
        if (username == "admin" and password == "admin"):
            c.send("Login efetuado com sucesso\n".encode())
            print("Login efetuado com sucesso\n")
            time.sleep(5)
            # op user

        else:
            c.send("Login falhou, encerrando conexão".encode())
            time.sleep(5)
            c.close()
            break

cria_socket_server()