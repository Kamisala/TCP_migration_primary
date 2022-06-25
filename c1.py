# virtual box client
import time
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SOCK_DGRAM
import os
os.system('sysctl -w net.ipv4.tcp_timestamps=0')

other_port = 21000
other_ip = '10.0.2.3'


def client_tcp():
    while True:
        try:
            serverName = other_ip
            port = other_port
            serverPort = port

            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            clientSocket.connect((serverName, serverPort))
            msg = 'Hi, I am Atomy'
            for i in range(5):
                clientSocket.send(msg.encode())
                mssg = clientSocket.recv(1024)
                print(mssg.decode())

            time.sleep(0)
            clientSocket.close()
            print('over')
            time.sleep(3)
           
            break


        except Exception as e:
            time.sleep(1)
            # print('try to connect')
            pass


def client_udp():
    while True:
        server_name = other_ip
        server_port = other_port
        try:
            clientSocket = socket(AF_INET, SOCK_DGRAM)
            message = "Hi,I am client"
            for i in range(15):
                clientSocket.sendto(message.encode(), (server_name, server_port))
                modifiedMessage, serverAddress = clientSocket.recvfrom(20480)
                print(modifiedMessage.decode())
            time.sleep(5)
            # clientSocket.close()
            # break
        except Exception as e:
            time.sleep(1)
            # print('try to connect')
            pass


if __name__ == '__main__':
    client_tcp();
    #client_udp();
