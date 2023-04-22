
import socket

HOST = ''  # Endereço IP do servidor
PORT = 8080  # Porta do servidor

# Cria um socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liga o socket ao endereço e porta especificados
server_socket.bind((HOST, PORT))

# Espera por conexões de entrada
server_socket.listen()

print(f'Servidor HTTP rodando na porta {PORT}...')

while True:
    # Aceita a conexão de entrada
    client_socket, client_address = server_socket.accept()
    print(f'Conexão recebida de {client_address}')

    # Recebe a solicitação do cliente
    request = client_socket.recv(1024).decode('utf-8')

    # Separa a linha da solicitação HTTP
    request_line = request.split('\n')[0]

    # Extrai a URL da solicitação
    url = request_line.split()[1]

    # Remove a barra inicial da URL
    if url.startswith('/'):
        url = url[1:]

    # Abre o arquivo solicitado
    try:
        file = open(url, 'rb')
        content = file.read()
        file.close()

        # Define o cabeçalho de resposta
        response = 'HTTP/1.1 200 OK\r\n'
        response += 'Content-Type: application/octet-stream\r\n'
        response += f'Content-Length: {len(content)}\r\n'
        response += '\r\n'

        # Envia o cabeçalho e o conteúdo do arquivo para o cliente
        client_socket.sendall(response.encode('utf-8') + content)
    except FileNotFoundError:
        # Se o arquivo não for encontrado, envia uma resposta 404
        response = 'HTTP/1.1 404 Not Found\r\n'
        response += 'Content-Type: text/html\r\n'
        response += '\r\n'
        response += '<h1>404 Not Found</h1>'
        client_socket.sendall(response.encode('utf-8'))
    except:
        # Se houver algum outro erro, envia uma resposta 500
        response = 'HTTP/1.1 500 Internal Server Error\r\n'
        response += 'Content-Type: text/html\r\n'
        response += '\r\n'
        response += '<h1>500 Internal Server Error</h1>'
        client_socket.sendall(response.encode('utf-8'))

    # Encerra a conexão com o cliente
    client_socket.close()
