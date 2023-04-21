# encoding:utf-8
from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.cli import CLI
from mininet.link import TCLink
net = Mininet(switch = OVSBridge, link=TCLink)
h1 = net.addHost('h1',ip='10.0.1.1')
h2 = net.addHost('h2',ip='10.0.1.2')
s1=net.addSwitch('s1')
h3 = net.addHost('h3',ip='10.0.2.3')
h4 = net.addHost('h4',ip='10.0.2.4')
net.addLink(h1, h2,0,0,delay='30ms')
net.addLink(h2, s1,1,1)
net.addLink(h3, s1,0,2)
net.addLink(h4, s1,0,3)
net.build()
h1.setMAC('00:00:00:00:00:11','h1-eth0')
h2.setMAC('00:00:00:00:00:12','h2-eth0')
h2.setMAC('00:00:00:00:00:21','h2-eth1')
h3.setMAC('00:00:00:00:00:23','h3-eth0')
h4.setMAC('00:00:00:00:00:24','h4-eth0')
net.build()
h1.cmd('ifconfig h1-eth0 10.0.1.1')
h2.cmd('ifconfig h2-eth0 10.0.1.2')
h2.cmd('ifconfig h2-eth1 10.0.2.1')
h3.cmd('ifconfig h3-eth0 10.0.2.3')
h4.cmd('ifconfig h4-eth0 10.0.2.4')

h2.cmd('route add -net 10.0.1.0/24 gw 10.0.1.2 dev h2-eth0')
h2.cmd('route add -net 10.0.2.0/24 gw 10.0.2.1 dev h2-eth1')


net.get('h1').cmd('route add -net 10.0.2.0/24 gw 10.0.1.2 dev h1-eth0')
net.get('h3').cmd('route add -net 10.0.1.0/24 gw 10.0.2.1 dev h3-eth0')
net.get('h4').cmd('route add -net 10.0.1.0/24 gw 10.0.2.1 dev h4-eth0')

h2.cmd('sysctl -w net.ipv4.tcp_timestamps=0')
h3.cmd('sysctl -w net.ipv4.tcp_timestamps=0')
h4.cmd('sysctl -w net.ipv4.tcp_timestamps=0')
h1.cmd('sysctl -w net.ipv4.tcp_timestamps=0')

h2.cmd('sysctl net.ipv4.ip_forward=1')
net.start()
CLI(net)
net.stop()



