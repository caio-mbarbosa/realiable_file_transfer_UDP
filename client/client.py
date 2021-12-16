from socket import *
import sys
import os

# Abrindo um socket UDP e setando o ip, porta e número de bytes do buffer
socket_client = socket(AF_INET, SOCK_DGRAM)
client_ip = gethostbyname(gethostname())
client_port = 4455
server_ip = client_ip # pois a troca de pacotes está acontecendo no mesmo IP
server_port = 6789
buffer_size = 1024
server_ip_port_tuple = (server_ip, server_port)


###### Etapa 1: Enviando o arquivo ######

print("======= Envio do arquivo ========")

file_name = sys.argv[1]
f = open('./' + file_name, 'rb')    # Abrindo um arquivo

file_size = os.path.getsize(file_name)

# Enviando o nome do arquivo para o servidor
socket_client.sendto(file_name.encode(), server_ip_port_tuple)
# socket_client.sendto(str(file_size).encode(), server_ip_port_tuple)

# Enviando pacotes de 1024 em 1024 bytes para o servidor, até que o arquivo seja completamente enviado
file_data = f.read(buffer_size)                 # Lendo os primeiros *buffer_size* bytes do arquivo
while(file_data):
    if(socket_client.sendto(file_data, server_ip_port_tuple)):
        print("Enviando...")
        file_data = f.read(buffer_size)

print("Fim do envio do arquivo")

# Caso o código 200 seja recebido, saberemos que o arquivo foi recebido devidamente pelo servidor
received_message, ip_port_tuple = socket_client.recvfrom(buffer_size)
if(received_message.decode() == '200'):
    print("'" + file_name + "'" + " foi recebido com sucesso pelo servidor")

f.close()


###### Etapa 2: Receber o arquivo de volta ######

print("====== Devolucao do arquivo ======")

# Recebendo o nome do arquivo enviado pelo servidor
server_file_name, server_ip_port_tuple = socket_client.recvfrom(buffer_size)
server_file_name = server_file_name.decode().strip()
print("Nome do arquivo: ", server_file_name)

# Criando um arquivo novo em modo de escrita binário
f = open(server_file_name.strip(), 'wb')

server_file_data, server_ip_port_tuple = socket_client.recvfrom(buffer_size)   
try:  
    while(server_file_data):
        f.write(server_file_data)
        socket_client.settimeout(2)
        server_file_data, server_ip_port_tuple = socket_client.recvfrom(buffer_size)

except timeout:
    print("'" + server_file_name + "'" + " foi recebido com sucesso")
    socket_client.sendto('200'.encode(), server_ip_port_tuple)


f.close()
socket_client.close()