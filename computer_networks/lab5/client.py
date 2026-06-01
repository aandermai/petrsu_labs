import sys
from socket import *

HOST, PORT, FILE = sys.argv[1], int(sys.argv[2]), sys.argv[3]
message = f"GET /{FILE} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\nConnection: close\r\n\r\n"

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((HOST, PORT))

clientSocket.send(message.encode())       
serverAnswer = clientSocket.recv(1024)
print("Ответ сервера: ", serverAnswer.decode(), end="")

clientSocket.close()                  





