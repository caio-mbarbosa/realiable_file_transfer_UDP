from socket import *

# Função que pega um arquivo: "arq.ext" e transforma em "arq._sent_by_server.ext"
def update_file_name(file_name):
    extension_pos = len(file_name)-1
    for char in reversed(file_name):
        if char == '.':
            break
        else:
            extension_pos -= 1
    
    if extension_pos == -1:
        return file_name + '_sent_by_server'
    else:
        return file_name[:extension_pos] + '_sent_by_server' + file_name[extension_pos:]



# Abrindo um socket UDP e setando o ip, porta e númeero de bytes do buffer
server_ip = gethostbyname(gethostname())
server_port = 6789
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((server_ip, server_port))
buffer_size = 1024


###### Etapa 1: Recebendo e salvando o arquivo ######

print("======= Envio do arquivo ========")

# Recebendo o nome do arquivo enviado pelo cliente
file_name, client_ip_port_tuple = server_socket.recvfrom(buffer_size)

# file_size = int(file_size)
file_name = file_name.decode().strip()
print("Nome do arquivo: ", file_name)

# Criando um arquivo novo em modo de escrita binário
f = open(file_name, 'wb')

file_data, client_ip_port_tuple = server_socket.recvfrom(buffer_size)   
try:  
    while(file_data):
        f.write(file_data)
        server_socket.settimeout(2)
        file_data, client_ip_port_tuple = server_socket.recvfrom(buffer_size)

except timeout:
    print("'" + file_name + "'" + " foi recebido com sucesso")
    server_socket.sendto('200'.encode(), client_ip_port_tuple)

f.close()


###### Etapa 2: Modificar o nome e enviar o arquivo de volta ######

print("====== Devolucao do arquivo ======")

# Enviando o nome do arquivo para o servidor
f = open("./" + file_name, 'rb')

file_name = update_file_name(file_name)
server_socket.sendto(file_name.encode(), client_ip_port_tuple)

# Enviando pacotes de 1024 em 1024 bytes para o cliente, até que o arquivo seja completamente enviado
server_file_data = f.read(buffer_size)
while(server_file_data):
    if(server_socket.sendto(server_file_data, client_ip_port_tuple)):
        print("Enviando...")
        server_file_data = f.read(buffer_size)

print("Fim da devolucao do arquivo")

server_socket.settimeout(20)

# Caso o código 200 seja recebido, saberemos que o arquivo foi recebido devidamente pelo servidor
received_message, client_ip_port_tuple = server_socket.recvfrom(buffer_size)
if(received_message.decode() == '200'):
    print("'" + file_name + "'" +" foi recebido com sucesso pelo cliente")


f.close()
server_socket.close()