# Client that lists files stored in the system
# Built on a provided starter framework; implementation completed by Jose E. Rodriguez Rios

import socket
import sys
from packet import *

def usage():
	print ("""Usage: python %s <server>:<port, default=8000>""" % sys.argv[0] )
	sys.exit(0)

def client(ip, port):

	# Contacts the metadata server and ask for list of files.
	
	sock = socket.socket() 
	sock.connect((ip,port))
	pac=Packet()
	pac.BuildListPacket()
	sock.sendall(pac.getEncodedPacket())
	liste=sock.recv(1024)
	pac.DecodePacket(liste)
	liste=pac.getFileArray()
	print liste
	sock.close()
if __name__ == "__main__":

	if len(sys.argv) < 2:
		usage()

	ip = None
	port = None 
	server = sys.argv[1].split(":")
	if len(server) == 1:
		ip = server[0]
		port = 8000
	elif len(server)== 2:
		ip = server[0]
		port = int(server[1])

	if not ip:
		usage()

	client(ip, port)
