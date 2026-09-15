#!/usr/bin/env python3
import sys
import time
import random
import socket
Mobile_id=""  
host = ""  #localhost
port =  0       # ports

def main():
        host= sys.argv[2]                               #el host se supone que sea localhost porque tienen que tener el mismo host que el servidor
        port= int(sys.argv[3])                          #el port tiene que ser el mismo del scheduel
        sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #abriendo un port udp
        while True:
            
            Mobile_id = str(sys.argv[1])                #guarda el numero
            job_cpu_time= str(random.randint(1,3))      #tiempo q toma cada cell
            toserver= Mobile_id + "/" + job_cpu_time    #para dividir los datos cuando se envie al servidor
            sock.sendto(toserver.encode(), (host,port)) #sockets  necesita  enviar data encoded
            print(toserver)
            time.sleep(random.randint(1,5))             # dejar dormir por un tiempo para  no enviar datos al misma vez

if __name__ == "__main__":
    main()
