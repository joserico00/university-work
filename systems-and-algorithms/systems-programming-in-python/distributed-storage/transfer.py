# Client that copies files into and out of the distributed storage
# Built on a provided starter framework; implementation completed by Jose E. Rodriguez Rios

import socket
import sys
import os.path
import os

from packet import *

def usage():
	print """Usage:\n\tFrom DFS: python %s <server>:<port>:<dfs file path> <destination file>\n\tTo   DFS: python %s <source file> <server>:<port>:<dfs file path>""" % (sys.argv[0], sys.argv[0])
	sys.exit(0)

def copyToDFS(address, fname, path):
	""" Contact the metadata server to ask to copu file fname,
	    get a list of data nodes. Open the file in path to read,
	    divide in blocks and send to the data nodes. 
	"""

	# Create a connection to the data server


	
	metadata = socket.socket() 
	metadata.connect(address)
	# Read file

	
	dire=path+fname
	f=open(path,"r")
	data=f.read()
	# Create a Put packet with the fname and the length of the data,
	# and sends it to the metadata server 

	
	p=Packet()
	size=os.path.getsize(path)
	p.BuildPutPacket(fname, size)
	metadata.sendall(p.getEncodedPacket())
	rec=metadata.recv(1024)
	# If no error or file exists
	# Get the list of data nodes.
	# Divide the file in blocks
	# Send the blocks to the data servers
	metadata.close()
		
	signal=0
	if rec != "DUP":
		f.seek(0)
		
		p.DecodePacket(rec)
		print p
		print rec
		datanodes= p.getDataNodes()
		lenght=len(datanodes)
		blocksize=size/lenght
		blockidlist=[]
		
		for block in datanodes:
			datablock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print block[0]
			print block[1]
			if block==datanodes[-1]:#esencialmente quita los espacios del ultimo bloque que no se va a llenar porque hay un residuo en el division de los bloques
				remainder=size%lenght 
				blocksize=blocksize-remainder
    
			datablock.connect((block[0],block[1]))
			p.BuildPutPacket(fname,blocksize)
			datablock.sendall(p.getEncodedPacket())
			signal=datablock.recv(1024)

			if signal == "OK":
				print "size of fileblock sent to datanode"
				print blocksize
				msg=f.read(blocksize)
				print "real size fileblock sent to datanode"
				print len(msg)
				#while msg:
				datablock.sendall(msg)
				#msg=f.read(1024)
				print "waiting for blockid"
				blockid=datablock.recv(1024)
				blockidlist.append(blockid)
				datablock.close()
				block.append(blockid)
				print "this should be the blockid"
				print blockid
			else:
				datablock.close()
				print "Somethings 	went wrong in putting a block"
				break
		f.close()
		#for lis in datanodes:
			
			


	else:
		print "File already in file system"
     
    

	# Notify the metadata server where the blocks are saved.

	
	print "working on datanodes:"

	metadata = socket.socket() 
	metadata.connect(address)

	if signal == "OK":
		sent = Packet()
		print datanodes
		sent.BuildDataBlockPacket(fname,datanodes)
		metadata.sendall(sent.getEncodedPacket())
	metadata.close()
 
 
 #se puede cacular el tamano del path del archibo que se puede utilizar para la proxima funcion
def copyFromDFS(address, fname, path):
	""" Contact the metadata server to ask for the file blocks of
	    the file fname.  Get the data blocks from the data nodes.
	    Saves the data in path.
	"""

   	# Contact the metadata server to ask for information of fname
    

	
	metadata = socket.socket() 
	metadata.connect(address)
	p=Packet()
	p.BuildGetPacket(fname)
	metadata.sendall(p.getEncodedPacket())
	# If there is no error response Retreive the data blocks

	
	resp=metadata.recv(1024)
	metadata.close()
	if resp != "NFOUND":
		print resp
		p.DecodePacket(resp)
		datanodes= p.getDataNodes()
		f=open(path,"wrb")
		fsize=p.getFsize()
		blocksize=fsize/len(datanodes)
		print datanodes
		for block in datanodes:
			if block==datanodes[-1]:#esencialmente quita los espacios del ultimo bloque que no se va a llenar si va a ver un residuo en el division de los bloques
				remainder=fsize%len(datanodes) 
				blocksize=blocksize-remainder
			msg=""
			tracker=0
			datablock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print "conecting to datablocks"
			print block[0],block[1]
			datablock.connect((block[0],block[1]))
			p.BuildGetDataBlockPacket(block[2])
			datablock.sendall(p.getEncodedPacket())
			#print len(msg), blocksize
			msg=datablock.recv(1024)
			while(len(msg) <blocksize): 
				#print len(msg), blocksize

				#print "legnt of data before", len(msg)
				msg=msg + datablock.recv(1024)
				#print "length of data after ", len(msg)
				#msg = msg + buf
				#msg =  datablock.recv(blocksize) 
				#print len(msg), blocksize
			f.write(msg)
			tracker=os.path.getsize(path)
			print tracker
				
			datablock.close()
		f.close()
	else:
		print "file not found"



		#lenght=len(datanodes)
		#blocksize=size/lenght
		#blockidlist=[]

		
    	# Save the file
	
	
	
 
if __name__ == "__main__":
#	client("localhost", 8000)
	if len(sys.argv) < 3:
		usage()

	file_from = sys.argv[1].split(":")
	file_to = sys.argv[2].split(":")

	if len(file_from) > 1:
		ip = file_from[0]
		port = int(file_from[1])
		from_path = file_from[2]
		to_path = sys.argv[2]

		if os.path.isdir(to_path):
			print "Error: path %s is a directory.  Please name the file." % to_path
			usage()

		copyFromDFS((ip, port), from_path, to_path)

	elif len(file_to) > 2:
		ip = file_to[0]
		port = int(file_to[1])
		to_path = file_to[2]
		from_path = sys.argv[1]

		if os.path.isdir(from_path):
			print "Error: path %s is a directory.  Please name the file." % from_path
			usage()

		copyToDFS((ip, port), to_path, from_path)


