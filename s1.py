# local service
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SOCK_DGRAM, IPPROTO_TCP, TCP_NODELAY
import time

local_port = 21000
local_ip = '10.0.2.3'


def server():
    server_port = local_port
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(('', server_port))
    server_socket.listen(10)
    a=time.time()
    server_socket.close()
    erver_port = local_port
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(('', server_port))
    server_socket.listen(10)
    #print(time.time()-a)
    flag=1
    print(local_ip, 'The server is ready to receive')
    while True:
        try:
            connectionSocket, addr = server_socket.accept()
            print(addr, 'success connection')
            if flag==0:
                connectionSocket.close()
                flage=1
                connectionSocket, addr = server_socket.accept()
            #print(addr, 'success connection')
            for i in range(5):
                msg = connectionSocket.recv(160)
                print(msg.decode())
                mssg = 'Hello, I am Server1'
                # print(len(mssg))
                connectionSocket.send(mssg.encode())
        except Exception as e:

            # print('Exception')
            pass

def server_udp():
    server_port = local_port
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', server_port))

    print(local_ip, 'The server is ready to receive: UDP')
    flag = 0

    while True:
        message, client_address = server_socket.recvfrom(20480)
        print (message.decode())
        modifiedMessage = "Hello, I AM server_1"
        server_socket.sendto(modifiedMessage.encode(), client_address)
        print (client_address)
        print(time.time())


if __name__ == '__main__':
    server();
# server_udp();

