import threading
import time
import socket
import random
import queue
import sys 
from collections import Counter
host = 'localhost'
port= int(sys.argv[1])
size=15
lista = [] #lista para simular un unsychronized queue
mutex=threading.Lock()
consume= threading.Semaphore()
full= 0 # nth message
index=[] #para tener los indexs
comp=[]#para tener la sumas
class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        
        global full
        
        global size
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.bind(('localhost',port)) #connectando a mobile
        
        while True:


            if (full < size):
                #print("producing")
                mobile_id  = sock.recv(1024)                #recibiendo el request 
                
                mutex.acquire()                             #entrando a crittical fuction
                lista.append(mobile_id)                     #anade un request al queue
                full = full + 1

                mutex.release()
                consume.release()                          # Para levantar consuminador por que se ha producido algo 
               # mutex.acquire()
                #print("produce ", threadcount, size)
                #mutex.release()

                
                if (full == size):
                    #print("closes production")
                    break
                
        #print("producer() closes")
        sock.close()                                        #se cierra el mobile que esta conectado por que ya se saco los datos

                
        
        
class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global full
        
        consume.acquire()                                   #consumador debe comenzar cerrado por que el producer debe producir un item primero y abrirlo
        while True:
            #print("start consuming")
            count= 0
            mutex.acquire()                                 #para evitar deadlocks en la programa
            threadcount = full
            if not lista:                                   # si el queue esta vacio me da 1 si tiene algo 0
                threadempty= 1
            else:
                threadempty =0
        
            mutex.release()
           # mutex.acquire()
           # print(threadcount, size, threadempty)
           # mutex.release()
            
            if not threadempty:                             #problema en donde no entra a al tread porque el liste.empty lo esta viendo como global  
                mutex.acquire()
                mobile_id= lista.pop(0)
                mutex.release()
                mobile_id= mobile_id.decode()
                #print(mobile_id)
                mobile_id = mobile_id.split("/")            #ej  1 / 6    mob[0]= 1 el id mob[1]= 6 el tiempo
                mobile_id[0]=int(mobile_id[0])              #convierte a int
                if mobile_id[0] in index:                    #si  esta la llave en mydict
                    comp[index.index(mobile_id[0])] = comp[index.index(mobile_id[0])]  + int(mobile_id[1]) # suma los computaciones que ya esta en la dicionario en la llave 
                    #print("consuming dentro del  com")
                else:
                    index.append(mobile_id[0])   #crea un nuevo index que va a ser el nuevo mobile en la lista index y anade el computacion en el lista comp
                    comp.append(int(mobile_id[1]))
                    #print("consuming se supone q fucione")
                #print("consumes something")  
                time.sleep(int(mobile_id[1]))               #tiempo de computacion 
            if (threadcount==size) and (threadempty):     #debe parra en el nth variable de queue
                 #print("consumed all")
                 break
            if (threadcount != size) and  (threadempty):  #bloquear elthread hasta que consigue un mensaje 
                 consume.acquire()
            #print("exiting consumer")
def main():
    global consume
    consume.acquire()                                       #block comsumer antes para esperar al producer
    producer = Producer()
    consumer = Consumer()
    consumer.start()
    producer.start()
    consumer.join()                                         #primero espera que termine consumer
    producer.join()                                         #despues esera que termine producer
    #print("termino los treads")
    
    for b in range(len(index)):
        print("mobile id is " , index[b] ,"and consumed " ,comp[b])


  
if __name__ == "__main__":
    main()
                  
                
