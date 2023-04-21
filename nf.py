# encoding:utf-8
from netfilterqueue import NetfilterQueue
from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.fields import *
import os

os.system('iptables -A FORWARD -d 10.0.1.1 -j NFQUEUE --queue-num 1')
os.system('iptables -A FORWARD -s 10.0.1.1 -j NFQUEUE --queue-num 1')


class MigrationSession:
    def __init__(self):
        # stage1 : client-server TCP
        self.state = 1


# 初始化数据记录ip port
server1 = MigrationSession()
server2 = MigrationSession()
client = MigrationSession()
# dest server
server2.ip = '10.0.2.4'
# dest port
server2.port = 21000
x = -1
y = -1
z = -1
hand1 = None
hand3 = None
mysession = MigrationSession()


def print_and_accept(pkt):
    global server1, server2, client, mysession, x, y, hand1, hand3, z
    ip = IP(pkt.get_payload())
    tcp = ip.getlayer(TCP)
    print(ip.src, '--', ip.dst, tcp.flags)
    if (mysession.state == 1):  # 三次握手
        if tcp.flags == 'S':
            # 记录x 和这个包
            x = tcp.seq
            hand1 = IP(pkt.get_payload())  # 一整个包的数据
            server1.ip = ip.dst
            client.ip = ip.src
            client.port = tcp.sport
            pkt.accept()
        elif tcp.flags == 'SA' and ip.src == server1.ip and ip.dst == client.ip:
            y = tcp.seq
            pkt.accept()
        elif tcp.flags == 'A' and ip.src == client.ip and ip.dst == server1.ip:
            hand3 = IP(pkt.get_payload())
            mysession.state = 2
            pkt.accept()
            print ("1 over")
    elif (mysession.state == 2):
        if tcp.flags == 'PA' and ip.src == client.ip and ip.dst == server1.ip:
            # 建立与server2的连接 第一次握手+第二次握手的回应(备份）
            hand1[IP].dst = server2.ip
            hand1[TCP].dport = server2.port
            del hand1[IP].chksum
            del hand1[TCP].chksum
            ans = srp1(Ether(dst='00:00:00:00:00:24',src='00:00:00:00:00:11') / hand1,iface='h2-eth1')
            z = ans[TCP].seq
            # 建立第三次握手
            hand3[IP].dst = server2.ip
            hand3[TCP].dport = server2.port
            hand3[TCP].ack = z
            del hand3[IP].chksum
            del hand3[TCP].chksum
            sendp(Ether(dst='00:00:00:00:00:24',src='00:00:00:00:00:11') / hand3,iface='h2-eth1')
            ip.dst = server2.ip
            ip.dport = server2.port
            ip[TCP].ack = ip[TCP].ack + z - y
            del ip[IP].chksum
            del ip[TCP].chksum
            pkt.set_payload(bytes(ip))
            pkt.accept()
            print ('send first pkt')
            mysession.state = 3

    elif (mysession.state == 3):
            print ('no.2')
            if ip.src == '10.0.1.1' and ip.dst == '10.0.2.3':
                    # 更改ack 目的地址
                    ip.dst = '10.0.2.4'
                    ip.dport = 21000
                    ip[TCP].ack = ip[TCP].ack + z - y
                    del ip[IP].chksum
                    del ip[TCP].chksum
                    pkt.set_payload(bytes(ip))
                    pkt.accept()
                    print ('change and accept')
                    

            elif ip.src == '10.0.2.4' and ip.dst == '10.0.1.1':
                # 更改seq 原地址
                ip.src = '10.0.2.3'
                ip.sport = 21000
                ip[TCP].seq = ip[TCP].seq + y - z
                del ip[IP].chksum
                del ip[TCP].chksum
                pkt.set_payload(bytes(ip))
                pkt.accept()
                print ('change and accept')
    print ('')


if __name__ == '__main__':
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, print_and_accept)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print('')
        os.system('iptables -F')

    nfqueue.unbind()

# 完成版- 老版- 待更新
# 客户端可发送转移到server2
# 未完成： server2回应字段包收不到， 仅从第四个包开始转发到server2 没有考虑四次挥手


