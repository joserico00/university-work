from argparse import _MutuallyExclusiveGroup
from base64 import encode
from queue import Full
import socket
from threading import *
import sys

import time

from pkg_resources import empty_provider
N=20
count=1
mutex = Semaphore() #mutex needed for the critical regions goes from 1 to 0 
empty= Semaphore(N)#semaphore needed to check if queue is empty or not. goes from n to 0
full = Semaphore(0)#semaphore needed to check if queue is full or not. goes from 0 to n

dictionary={ } #needed to keep a sum of the devices
port=sys.argv[1] # first argument
queue=[] #shared queue that is empty
host = "127.0.0.1" #Ip for the socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)# needs to be a udp server

def consumer():
    global queue #queue is shared between consumer and producer
    global dictionary 
    global count
    for i in range(N):
        
        #print("consumer count: ", count)
        #full
        #Critical region since queue is a shared variable between the two threads and we are removing an element from the thread
        #print("full: ")
        full.acquire()
        mutex.acquire()
        #print("before consume queue now: ", queue)
        process=queue.pop(0)
        #print("afted consumed queue now: ", queue)
        mutex.release()  
        empty.release()
        #MUTEX
        #empty
        #Process receives a string like x:d so we split into two so we can easily get the device and time
        #print("process before removing :: ", process)
        
        process=process.split(':')
       # print("process after removing : ", process)
        id=process[0]
        times=process[1]
        #then we check if the id already exist in the dictionary if not make a new key
        #reason why I did this is because of the way dictionarys worked that if i tried to add the time to a key that does not exists it breaks the program
        if id in dictionary.keys():
            dictionary[id]= int(times) + dictionary[id]
        else:
            dictionary[id]= int(times)
        time.sleep(int(times))
        count= count +1

        
        
    
    
def producer():
    global queue
    global count
    #global nthmessage
    
    #conn, addr =server.accept()
    for i in range(N):
            #print("producer count: ", count)
            #if count == N:
             #   break

            #waits until it receives a message from a device and decodes it

            codedmsg, addr=server.recvfrom(1024)
            msg= codedmsg.decode()
            
           # print("msg: ", msg)
            #empty
            #mutex
            #critical region because we are adding and sorting the shared queue between the two threads and adding the message to the queue
            empty.acquire()
            mutex.acquire()
            queue.append(msg)
           # print("before sorted queue now: ", queue)
            queue.sort(key=lambda x: x.split(':')[1])
           # print("after sorted queue now: ", queue)
            mutex.release()
            full.release()
            finish="fin"
            #signal back to the device thats its ready to send another message
            server.sendto(finish.encode(), addr)
                #mutex
            #full


server.bind((host, int(port)))
#server.listen(4)




t1=Thread(target=producer)
t2=Thread(target=consumer)
t1.start()  #starting threads
t2.start()
t1.join() 
t2.join()

#printing the sum of all processed times
for i in dictionary:
    print("Device " ,i ," consumed " , dictionary[i] ," seconds of CPU time")

server.close() #always needed unless you want hundreds of opened ports in your computer
