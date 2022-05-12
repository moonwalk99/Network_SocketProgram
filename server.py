from socket import *
import datetime

# html 만들기
html_text = """<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body>

<h1>This is a Heading</h1>
<p>This is a paragraph.</p>

</body>
</html>
"""
html_file = open('hello.html', 'w')
html_file.write(html_text)
html_file.close()

# socket 설정.
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('127.0.0.1', 80))
serverSock.listen(1)

connectionSock, addr = serverSock.accept()

print(str(addr),'에서 접속이 확인되었습니다.')

data = connectionSock.recv(1024)
data = data.decode('utf-8')
print('\n\n받은 데이터 : \n', data)

message = ""
dataSliced = data.split()
try:
    if dataSliced[0] == "GET":
        fileName = dataSliced[1]
        requestedFile = open('.' + fileName, 'rt', encoding='utf-8')
        sendData = requestedFile.read()
        message += "HTTP/1.1 200 OK\r\n" + "Date: " + str(datetime.datetime.now()) + "\r\n"
        message += "Content-Type: text/html\r\n" + "Content-Length: 1" + "\r\n" + sendData + "\n\n"
    elif dataSliced[0] == 'POST':
        message += "HTTP/1.1 405 Method not allowed\r\n" + "Date: " + str(datetime.datetime.now()) + "\r\n"
        message += "Content-type: text/html\r\n" + "Content-length: 0\n\n"
    elif dataSliced[0] == 'HEAD':
        fileName = dataSliced[1]
        requestedFile = open('.' + fileName, 'rt', encoding='utf-8')
        sendData = requestedFile.read()
        message += "HTTP/1.1 200 OK\r\n" + "Date: " + str(datetime.datetime.now()) + "\r\n"
        message += "Content-type: text/html\r\n" + "Content-length: 1\n\n"
except IOError:
    message += "HTTP/1.1 404 NOT FOUND\r\n" + "Date: " + str(datetime.datetime.now()) + "\r\n"
    message += "Content-type: text/html\r\n" + "Content-length: 0\n\n"

connectionSock.send(message.encode('utf-8'))
print('메시지를 보냈습니다.')

serverSock.close()