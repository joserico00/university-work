import random 
import socket
import sys
import time
Rngtime=5
Rngsleep=5
N=30 #how many messages it sends
#to run this program you would need to run it with three arguments the Id, Host and port. Host and port should be the same as the scheduler
id= sys.argv[1]#first argument
sum=0
host=sys.argv[2] #second argument
port=sys.argv[3]# third argument
deviceid=id+":"#
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Udp connection
server.settimeout(15)# make server connection stop if nothing is received
try:
    
    server.connect((host,int(port))) #connection to server of compute_server.py
except socket.error as e:
    print(str(e))
count=0
while(1):#
    jobtime=random.randint(1,Rngtime)#generating random jobtime
    sum=sum+jobtime
    sent=deviceid+str(jobtime)#concatanate device id and jobtime
    server.send(sent.encode())#message sent
    #print(sent)
    #print("expected count: " , count)
    #count=count+1
    server.recv(1024)#device waits until producer from compute_server.py sends back a signal
server.close()
