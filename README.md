# TCP-migration_PrimaryEdition
TCP migration test based on mininet, scapy and netfilterqueue.

Introduction: 
    TCP network migration including 4 hosts, The simulated environment is as follows：
    ![image](https://user-images.githubusercontent.com/105418310/175755891-1a2c696b-c0f7-4419-b83e-b877591b2d3a.png)

    Among that: h1 is client, h2 is tcp-migration, h3 is server1 , h4 is server2.
    program aim: client create tcp connection with server1,and send 5 packets to server1; h2 will migrate tcp to server2 after client create the tcp connnection with server1, and migrate the above 5 packets to  server2; server2 receive pactets and respond client.

Usage:

    1,Open virtual machine terminal.
    
    2，running mn.py - > input : xterm h1 h2 h3 h4 (enter).
    
    3,in h2 terminal: running nf.py.
    
    4.in h3 terminal: running s1.py.
    
    5,in h4 terminal: running s2.py.
    
    6,in h1 terminal: running c1.py.
    
Attention:

    There are some defects in this version: 
    
    1. The requirement to disconnect TCP is not considered after running. If you want to use the client again, you need to close the entire mininet and try again (this is recommended). 
    
    2. In addition, the iptables /netfilterqueue of the program is only based on IP selection. If necessary, you can further set it to the port or more precise level.
    

Application principle：

![image](https://user-images.githubusercontent.com/105418310/175755059-3d50df86-a6cc-46cf-b0fc-0ca8e8ea2ef5.png)

Process:

# 1.Running: mn.py in terminal of Virtual Machine, and open the terminal of h1, h2, h3, h4
![截屏2023-04-21 上午11 56 04](https://user-images.githubusercontent.com/105418310/233537321-7037f580-1ddc-4af8-b6f4-701f3e3b19e6.jpg)

# 2. Running: nf.py in h2; s1.py in h3; s2.py in h4; c1.py in h1
![截屏2023-04-21 上午11 59 26](https://user-images.githubusercontent.com/105418310/233537782-b97d243e-fa2c-4310-958c-e6b4e078429a.jpg)

# 3. Waiting:
![截屏2023-04-21 下午12 00 04](https://user-images.githubusercontent.com/105418310/233537842-ab71bb0d-d93b-4437-8e24-f4accbe8ef3d.jpg)
We can see that: h1 has esatblished a tcp connection with h3.

# 4. Waiting:
![截屏2023-04-21 下午12 01 10](https://user-images.githubusercontent.com/105418310/233537961-2e97fd4b-cb77-46fe-b1e9-6f94990c64bc.jpg)
We can see that: h4 was migrated a same tcp connection with h1, and there are 5 tcp data interactions between h1 and h4.
