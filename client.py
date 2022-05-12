from socket import *

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', 80))

print('연결 확인 됐습니다.')

print("GET 메소드- 응답 2XX 하려면 1")
print('GET 메소드- 응답 4XX 하려면 2')
print('POST 메소드- 응답 4XX 하려면 3')
print('HEAD 메소드- 응답 2XX 하려면 4')
print('HEAD 메소드- 응답 4XX 하려면 5')

inputVal = input('원하는 동작을 입력해주세요: ')
message = ""
fileMake = 0

if inputVal == '1':
    message += "GET /hello.html HTTP/1.1\r\n"+"Host: 127.0.0.1:80\r\n"+"Connection: Keep-Alive\n\n"
    fileMake = 1
elif inputVal == '2':
    message += "GET /notExisting.html HTTP/1.1\r\n"+"Host: 127.0.0.1:80\r\n"+"Connection: Keep-Alive\n\n"
    fileMake = 1
elif inputVal == '3':
    message += "POST / HTTP/1.1\r\n" + "Host: 127.0.0.1:80\r\n" + "Connection: Keep-Alive\n\n"
elif inputVal == '4':
    message += "HEAD /hello.html HTTP/1.1\r\n"+"Host: 127.0.0.1:80\r\n"+"Connection: Keep-Alive\n\n"
elif inputVal == '5':
    message += "HEAD /notExisting.html HTTP/1.1\r\n"+"Host: 127.0.0.1:80\r\n"+"Connection: Keep-Alive\n\n"

clientSock.send(message.encode('utf-8'))
print('\n\n보낸메시지: \n', message)
print('메시지를 전송했습니다.\n\n')

data = clientSock.recv(1024)
print('받은 데이터 : ', data.decode('utf-8'))

if fileMake == 1:
    dataSliced = data.decode('utf-8').split(' ')
    if dataSliced[1] == '200':
        dataSliced = data.decode('utf-8').split('<!DOCTYPE html>')
        dataSliced[1] = "<!DOCTYPE html>\n" + dataSliced[1]
        html_file = open('client_hello.html', 'w')
        html_file.write(dataSliced[1])
        html_file.close()
        print('GET한 파일이 저장되었습니다.')

clientSock.close()