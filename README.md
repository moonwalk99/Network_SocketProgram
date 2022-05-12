# 컴퓨터네트워크 중간고사 대체 프로젝트

학과: 소프트웨어학과

학번: 20181608

이름: 문원기

> GET한 파일이 client 위치에 생성되는 것까지 구현했습니다. 이는 3.1)에서 자세히 확인하실 수 있습니다.
>
> 또한 WireShark로 매전송마다 캡처하여 사진 첨부하였습니다.



## 1. 실행환경

운영체제 : Windows 10

사용 언어 : python

사용한 IDE : PyCharm Community Edition 2020.1.1

소켓 구현에 사용한 라이브러리 : socket





## 2. 소스 파일

**server.py**

```python
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

```



**client.py**

```python
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
```





## 3. 프로그램 실행 결과

서버를 먼저 실행시키면 서버는 소켓을 준비하기 전에 hello.html 파일을 작성합니다.

![image-20220502101449900](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502101449900.png)

위 파일을 기준으로 GET과 POST, HEAD를 처리할 것이며,

특이사항으로는 POST 메소드가 지금 구현에서는 client의 입력을 신뢰할 수 없다는 판단 하에 Method Not Allowed를 리턴하도록 하였습니다. 

POST 설명하는 부분에서 자세히 설명하겠습니다.



서버는 이후에 소켓을 설정한 후에 연결을 기다립니다.

![image-20220502101715459](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502101715459.png)

연결이 되면 위와 같은 메시지를 출력하는데, 보시면 포트번호가 80이 아닌 것을 확인할 수 있습니다. 

wireShark에서 확인해본 결과, 1079는 source port이며 80을 destination으로 삼는 것을 확인할 수 있었습니다. 즉, 정상적으로 작동하는 것이 맞습니다.

![image-20220502102118831](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502102118831.png)

이후에는 5가지 경우로 나뉘어지는 분기가 이어지기 때문에 각각 따로 서술하겠습니다.





### 3.1) GET 메소드 - 2XX 응답.

**서버 출력:**

![image-20220503145653150](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220503145653150.png)

**클라이언트 출력:**

![image-20220503145713070](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220503145713070.png)



**wireShark 출력 결과물:**

![image-20220503145758487](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220503145758487.png)

**동작 설명 :**

client가 GET method를 request에 작성하여 전송합니다. 이때 요청하는 파일은 hello.html이며, 이는 서버가 가지고 있는 파일입니다.

중요한 점은 GET method를 작성할 때 makeFile이라는 변수를 1로 바꿉니다. 

request 메시지를 받은 server는 해당하는 hello.html 파일을 read합니다. 이때 hello.html은 엄연히 서버가 가지고 있는 파일이기에 IO Error가 발생하지 않습니다.

따라서 정상적으로 작동하여 200 OK를 response에 작성하여 전송합니다. 이때 hello.html 또한 같이 전송합니다.

클라이언트는 해당 response message를 받은 후에, 그것을 출력합니다.

그후에 client는 makeFile이 1이기에 if문에서 분기됩니다. 여기서 response message를 분석하여 200 OK인지 확인합니다.

200 OK라면 response message의 body 부분에 전송된 hello.html의 내용을 변환하여

**client_hello.html 파일을 만듭니다.**

![image-20220503143938245](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220503143938245.png)

이렇게 함으로써 GET에 대한 response 메시지가 200 OK인 경우, 제대로 파일이 같이 전송되는 것을 확인할 수 있습니다.

![image-20220503144138488](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220503144138488.png)

이 전송된 파일이 클라이언트 위치에서 생성되는 것을 확인할 수 있었습니다. 



### 3.2) GET 메소드 - 4XX 응답

**서버 출력 결과물:**

![image-20220502102914811](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502102914811.png)

**클라이언트 출력 결과물:**

![image-20220502102926028](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502102926028.png)

**wireShark 캡처 결과물:**

![image-20220502102950097](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502102950097.png)

**동작 설명 : **

client가 GET method를 request에 작성하여 전송합니다. 이때 요청하는 파일은 notExisting.html이며, 이는 서버에 없는 파일입니다.

위에 설명한 GET method와 마찬가지로 makeFile이라는 변수를 1로 바꿉니다.

server에서는 client가 요청한 notExisting.html 파일을 열고자하나, 해당 파일은 존재하지 않는 파일이기에 IO Error가 발생합니다.

이때 IO Error를 따로 분기시키는 try except문이 발동하여 server는 404 NOT FOUND를 response에 작성하여 전송합니다. 

클라이언트는 해당 response message를 받은 후에, 그것을 출력합니다.

그후에 client는 makeFile이 1이기에 if문에서 분기됩니다.

해당 if문에서 response message를 나누어서 200 OK인지 확인합니다.

200 OK가 아닌 404 NOT FOUND이기에 별다른 동작없이 종료됩니다.





### 3.3) POST 메소드 - 4XX 응답

**서버 출력 결과물:**

![image-20220502103209567](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502103209567.png)

**클라이언트 출력 결과물:**

![image-20220502103220742](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502103220742.png)

**wireShark 캡처 결과물:**

![image-20220502103233486](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502103233486.png)

**동작 설명 : **

client가 POST method를 request에 작성하여 전송합니다. 

저는 client가 server에 생성하려고 하는 내용이 올바른 내용인지 의문이 들었습니다.

만약 client가 생성하는 내용이 신뢰할 수 있는 올바른 내용인지 확인할 수 있었다면 server에서도 POST 메소드를 받아들이고 올바르게 작동하도록 할 수 있었겠지만, 시간과 구현의 부족함으로 인해 거기까지 해내지는 못했습니다.

따라서 POST 메소드는 405 Method not allowed로 응답하도록 했으며, 어차피 무조건 405가 응답되기에 request 메시지에서도 body 부분은 비어있도록 했습니다.

 

### 3.4) HEAD 메소드 - 2XX 응답

**서버 출력 결과물:**

![image-20220502103328370](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502103328370.png)

**클라이언트 출력 결과물:**

![image-20220502103339394](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502103339394.png)

**wireShark 캡처 결과물:**

![image-20220502103406887](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502103406887.png)

**동작 설명 : **

client가 HEAD method를 request에 작성하여 전송합니다. 이때 요청하는 파일은 hello.html이며, 이는 서버가 가지고 있는 파일입니다.

서버에서는 이 파일을 찾아 열어본 후에, GET할 때와 마찬가지로 response 메시지를 준비합니다. 

이때, HEAD 메소드이기 때문에 response 헤더만 전송하며, 실질적인 파일의 내용은 이어붙이지 않습니다.

GET과는 다르게 HEAD 메소드는 response 헤더만 요구하는 메소드이기 때문입니다.



### 3.5) HEAD 메소드 - 4XX 응답

**서버 출력 결과물:**

![image-20220502103520646](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502103520646.png)

**클라이언트 출력 결과물:**

![image-20220502103501959](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502103501959.png)

**wireShark 캡처 결과물:**

![image-20220502103441278](C:\Users\wkm99\AppData\Roaming\Typora\typora-user-images\image-20220502103441278.png)



**동작 설명 : **

client가 HEAD method를 request에 작성하여 전송합니다. 이때 요청하는 파일은 notExisting.html이며, 이는 서버가 가지고 있지 않은 파일입니다.

서버에서는 이 파일을 찾아 열려고 하나 파일이 존재하지 않기 때문에 IO Error가 발생합니다. 

이때 try except문으로 인해 분기되어 server는 404 NOT FOUND를 response에 작성하여 전송합니다. 
