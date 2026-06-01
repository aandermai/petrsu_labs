import socket
import ssl
import base64

# Тело письма
subject = "Subject: Профбюро ИМИТ тут <3\r\n"  # Заголовок письма
message = "\r\n Геля крутая!"
endmessage = "\r\n.\r\n"

# Выбираем почтовый сервер
mailserver = "smtp.gmail.com"
port = 587

# Создаем сокет clientSocket и устанавливаем TCP-соединение
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET означает использование IPv4, а SOCK_STREAM указывает на использование протокола TCP.
clientSocket.connect((mailserver, port)) 

# Получаем ответ от сервера
recv11 = clientSocket.recv(1024).decode()
print(recv11, end="")
if recv11[:3] == "220": 
    print("Соединение установлено. Код 220 от сервера успешно получен!", end="\n\n")
else: 
    print("Код 220 от сервера не получен :(", end="\n\n")

# Отправляем команду HELO и выводим ответ сервера.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv = clientSocket.recv(1024).decode() 
print(recv, end="")
if recv[:3] == '250':
    print("Код 250 от сервера успешно получен!", end="\n\n")
else:    
    print("Код 250 от сервера не получен :(", end="\n\n")

# Отправляем команду STARTTLS
starttlsCommand = 'STARTTLS\r\n'
clientSocket.send(starttlsCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1, end="")
if recv1[:3] != '220':
    print("Ошибка: Команда STARTTLS не принята.")

# Переход на защищённое соединение
context = ssl.create_default_context()
secureSocket = context.wrap_socket(clientSocket, server_hostname="smtp.gmail.com")
print("Защищённое соединение установлено.")

# Отправляем команду AUTH LOGIN для аутентификации
authCommand = 'AUTH LOGIN\r\n'
secureSocket.send(authCommand.encode())
recv2 = secureSocket.recv(1024).decode()
print("Ответ на AUTH LOGIN:", recv2)

# Отправляем имя пользователя в base64
username = "skimez76@gmail.com"
encoded_username = base64.b64encode(username.encode()).decode()  # Кодируем в base64
secureSocket.send((encoded_username + '\r\n').encode())
recv3 = secureSocket.recv(1024).decode()
print("Ответ на имя пользователя:", recv3)

# Отправляем пароль в base64
password = "lwmm uapl oozh eidj"
encoded_password = base64.b64encode(password.encode()).decode()  # Кодируем в base64
secureSocket.send((encoded_password + '\r\n').encode())
recv4 = secureSocket.recv(1024).decode()
print("Ответ на пароль:", recv4)
if recv4[:3] == '235': 
    print("Код 235 от сервера получен. Аутентификация прошла успешно!", end="\n\n")
else:
    print("Код 235 от сервера не получен. Ошибка аутентификации.", end="\n\n")

# Отправляем команду MAIL FROM и выводим ответ сервера.
mailFromCommand = "MAIL FROM:<skimez76@gmail.com>\r\n"
secureSocket.send(mailFromCommand.encode())
recv5 = secureSocket.recv(1024).decode()
print(recv5, end="")
if recv5[:3] == "250":
    print("Код 250 от сервера успешно получен!", end="\n\n")
else:
    print("Код 250 от сервера не получен :(", end="\n\n")  

# Отправляем команду RCPT TO и выводим ответ сервера.
rcptToCommand = "RCPT TO:<skimez76@gmail.com>\r\n"
secureSocket.send(rcptToCommand.encode())
recv6 = secureSocket.recv(1024).decode()
print(recv6, end="")
if recv6[:3] == "250":
    print("Код 250 от сервера успешно получен!", end="\n\n")
else:
    print("Код 250 от сервера не получен :(", end="\n\n")

# Отправляем команду DATA и выводим ответ сервера.
dataCommand = "DATA\r\n"
secureSocket.send(dataCommand.encode())
recv7 = secureSocket.recv(1024).decode()
print(recv7, end="")
if recv7[:3] == "354":
    print("Код 354 от сервера получен. Сервер готов принять письмо!", end="\n\n")
else:
    print("Сервер не готов принять письмо :(", end="\n\n")

# Собираем всё сообщение
finalmessage = subject + message + endmessage
secureSocket.send(finalmessage.encode())  # Отправляем сообщение
recv8 = secureSocket.recv(1024).decode()  # Читаем ответ сервера
print("Ответ на отправку сообщения:", recv8, end="")
if recv8[:3] == "250":
    print("Код 250 от сервера получен. Письмо успешно отправлено!", end="\n\n")
else:
    print("Возникла ошибка при отправке письма :(", end="\n\n")

# Завершаем сессию
quitCommand = "QUIT\r\n"
secureSocket.send(quitCommand.encode())  # Отправляем команду QUIT
recv9 = secureSocket.recv(1024).decode()  # Читаем ответ сервера
print("Ответ на QUIT:", recv9, end="")
if recv9[:3] == "221":
    print("Код 221 от сервера получен. Сессия успешно завершена!")
else:
    print("Возникли ошибки при завершении сессии")