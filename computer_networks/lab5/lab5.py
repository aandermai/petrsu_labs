from socket import *
from threading import *

def HandleClient(connectionSocket, addr):
    print(f"Подключение от: {addr}")
    try:
        # Читаем сообщение от клиента
        message = connectionSocket.recv(1024).decode('utf-8')
        filename = message.split()[1]  # Получаем имя запрашиваемого файла
        with open(filename[1:], 'r') as f:
            outputdata = f.read()

        # Отправляем заголовок HTTP-ответа
        connectionSocket.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")

        # Отправляем содержимое файла
        connectionSocket.send(outputdata.encode('utf-8'))
    except IOError:
        # Отправляем ответ об отсутствии файла
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n")
        connectionSocket.send(("<h1>404 Not Found</h1>").encode())
    finally:
        # Закрываем соединение с клиентом
        connectionSocket.close()


# Настройки сервера
HOST = "172.20.10.5"
PORT = 6789
serverSocket = socket(AF_INET, SOCK_STREAM)

# Подготавливаем сокет сервера
serverSocket.bind((HOST, PORT))
serverSocket.listen(5)
print(f"Сервер запущен на {HOST}:{PORT}")
print("Готов к обслуживанию...")


while True:
    # Устанавливаем соединение
    connectionSocket, addr = serverSocket.accept()
    client_thread = Thread(target=HandleClient, args=(connectionSocket, addr))
    client_thread.start()
