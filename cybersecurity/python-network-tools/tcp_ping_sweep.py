import os
import socket

subnet = "192.168.1."
start = 1
end = 255

for i in range(start, end+1):
    ip = subnet + str(i)
    try:
        socket.setdefaulttimeout(1)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((ip, 80))
        print(ip, "is up!")
        socket.close()
    except:
        pass
    
