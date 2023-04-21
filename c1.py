# virtual box client
import time
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SOCK_DGRAM, IPPROTO_TCP, TCP_NODELAY

other_port = 21000
other_ip = '10.0.2.3'


def client_tcp():
    while True:
        #clientSocket = socket(AF_INET, SOCK_STREAM)
        #clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 10)
        #clientSocket.connect(('10.0.2.9', 22000))
        try:
            
            serverName = other_ip
            port = other_port
            serverPort = port

            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 10)
            a=time.time()
            clientSocket.connect((serverName, serverPort))
            
            #print(time.time()-a)
            time.sleep(3)
            #server_socket.setsockopt(IPPROTO_TCP, TCP_NODELAY, True)
            #clientSocket.close()
            #clientSocket.connect((serverName, serverPort))
            
            msg = 'Hi, I am Atomy'
            for i in range(5):
                msg='Hi, I am Atomy '+str(i)
                clientSocket.send(msg.encode())
                #print(len(msg))                
                mssg = clientSocket.recv(300)
                print(mssg.decode())
                time.sleep(1)

            #print(time.time()-a-3)
            time.sleep(1)
            clientSocket.close()
            print('over')
            break


        except Exception as e:
            #time.sleep(1)
            #print(str(e))
            pass


def client_udp():
    while True:
        server_name = other_ip
        server_port = other_port
        try:
            clientSocket = socket(AF_INET, SOCK_DGRAM)
            message = "Hi,I am client"
            print(time.time())
            for i in range(10):
                clientSocket.sendto(message.encode(), (server_name, server_port))
                modifiedMessage, serverAddress = clientSocket.recvfrom(20480)
                print(modifiedMessage.decode())
            time.sleep(5)
            # clientSocket.close()
            break
        except Exception as e:
            time.sleep(1)
            # print('try to connect')
            pass


if __name__ == '__main__':
    client_tcp();
     #client_udp();

