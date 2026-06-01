import socket
import ssl
import base64
from data import username, password

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
heloCommand = 'HELO Artem\r\n'
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
context = ssl.create_default_context() # Задаём базовые настройки
secureSocket = context.wrap_socket(clientSocket, server_hostname=mailserver) # Оборачиваем наш сокет в защищенный
print("Защищённое соединение установлено.", end="\n\n")

# Отправляем команду AUTH LOGIN для аутентификации
authCommand = 'AUTH LOGIN\r\n'
secureSocket.send(authCommand.encode())
recv2 = secureSocket.recv(1024).decode()
print("Ответ на AUTH LOGIN:", recv2, end="")

# Отправляем имя пользователя в base64
encoded_username = base64.b64encode(username.encode()).decode()  # Кодируем в base64
secureSocket.send((encoded_username + '\r\n').encode())
recv3 = secureSocket.recv(1024).decode()
print("Ответ на имя пользователя:", recv3, end="")

# Отправляем пароль в base64
encoded_password = base64.b64encode(password.encode()).decode()  # Кодируем в base64
secureSocket.send((encoded_password + '\r\n').encode())
recv4 = secureSocket.recv(1024).decode()
print("Ответ на пароль:", recv4, end="")
if recv4[:3] == '235': 
    print("Код 235 от сервера получен. Аутентификация прошла успешно!", end="\n\n")
else:
    print("Код 235 от сервера не получен. Ошибка аутентификации.", end="\n\n")

# Отправляем команду MAIL FROM и выводим ответ сервера.
mailFromCommand = "MAIL FROM:<skimez76@gmail.com>\r\n" # от кого письмо
secureSocket.send(mailFromCommand.encode())
recv5 = secureSocket.recv(1024).decode()
print(recv5, end="")
if recv5[:3] == "250":
    print("Код 250 от сервера успешно получен!", end="\n\n")
else:
    print("Код 250 от сервера не получен :(", end="\n\n")  

# Отправляем команду RCPT TO и выводим ответ сервера.
rcptToCommand = "RCPT TO:<skimez76@gmail.com>\r\n" # кому письмо
secureSocket.send(rcptToCommand.encode())
recv6 = secureSocket.recv(1024).decode()
print(recv6, end="")
if recv6[:3] == "250":
    print("Код 250 от сервера успешно получен!", end="\n\n")
else:
    print("Код 250 от сервера не получен :(", end="\n\n")

# Отправляем команду DATA и выводим ответ сервера.
dataCommand = "DATA\r\n" # даём серверу понять, что готовы писать письмо
secureSocket.send(dataCommand.encode())
recv7 = secureSocket.recv(1024).decode()
print(recv7, end="")
if recv7[:3] == "354":
    print("Код 354 от сервера получен. Сервер готов принять письмо!", end="\n\n")
else:
    print("Сервер не готов принять письмо :(", end="\n\n")

# Заголовки письма
from_email = "skimez76@gmail.com"
to_email = "skimez76@gmail.com"
subject = "Subject: Письмо с изображением\r\n"

# Границы MIME
boundary = "boundary"

# MIME-заголовок
headers = (
    f"From: {from_email}\r\n"
    f"To: {to_email}\r\n"
    f"{subject}"
    f"Content-Type: multipart/mixed; boundary={boundary}\r\n\r\n"
)

# Текст сообщения
body = (
    f"--{boundary}\r\n"
    f"Content-Type: text/plain; charset=utf-8\r\n"
    f"Content-Transfer-Encoding: 7bit\r\n\r\n"
    f"Привет!\nЭто письмо с вложенными изображениями.\n\r\n"
)

# Подготовка изображения
images = ["image2.jpeg", "image3.jpg"] 
image_parts = []
for image_path in images:
    with open(image_path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode()

    # MIME для изображения
    image_part = (
        f"--{boundary}\r\n"
        f"Content-Type: image/jpeg; {image_path}\r\n"
        f"Content-Transfer-Encoding: base64\r\n"
        f"Content-Disposition: attachment; filename={image_path}\r\n\r\n"
        f"{encoded_image}\r\n"
    )
    image_parts.append(image_part)

endMessage = f"--{boundary}--\r\n.\r\n"

message = headers + body + "".join(image_parts) + endMessage # Собираем всё письмо

# Отправляем сообщение
secureSocket.send(message.encode())  # Отправляем письмо
recv8 = secureSocket.recv(1024).decode()  # Читаем ответ сервера
print("Ответ на отправку сообщения:", recv8, end="")
if recv8[:3] == "250":
    print("Код 250 от сервера получен. Письмо успешно отправлено!", end="\n\n")
else:
    print("Возникла ошибка при отправке письма :(", end="\n\n")

# Завершаем сессию
quitCommand = "QUIT\r\n"
secureSocket.send(quitCommand.encode())
recv9 = secureSocket.recv(1024).decode()
print("Ответ на QUIT:", recv9, end="")
if recv9[:3] == "221":
    print("Код 221 от сервера получен. Сессия успешно завершена!")
else:
    print("Возникли ошибки при завершении сессии")