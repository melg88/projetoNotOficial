#print('client')

import socket

HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 8080         # Porta do servidor

# Cria um objeto socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta o socket ao servidor
client_socket.connect((HOST, PORT))

# Envia uma requisição GET para o caminho '/'
request = "GET / HTTP/1.1\r\nHost: %s\r\nContent-Length: 0\r\n\r\n" % HOST
client_socket.sendall(request.encode())

# Recebe a resposta do servidor
response = ''
status_code = 0
chunk_size = 1024
while True:
    data = client_socket.recv(chunk_size)
    if not data:
        break
    response += data.decode()
    if '\r\n\r\n' in response:
        status_code = int(response.split()[1])
    if status_code != 0 and len(response) >= status_code + response.find('\r\n\r\n'):
        break

# Trata o código de status da resposta
if status_code == 200:
    print(response.split('\r\n\r\n')[1])
else:
    error_message = 'Erro desconhecido'
    if status_code == 400:
        error_message = 'Bad Request'
    elif status_code == 403:
        error_message = 'Forbidden'
    elif status_code == 404:
        error_message = 'Not Found'
    elif status_code == 505:
        error_message = 'Version Not Supported'
    print('<html><head><title>%d %s</title></head><body><h1>%d %s</h1></body></html>' % (status_code, error_message, status_code, error_message))

# Fecha a conexão
client_socket.close()