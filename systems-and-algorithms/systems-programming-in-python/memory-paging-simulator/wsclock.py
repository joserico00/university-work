# Author: Jose E. Rodriguez Rios
# This program simulates the page replacement algorithm WSclock Page Replacement

import sys
#defining class named oag with three variabled 
#frame where we store the memory
#ref: where we know if its referenced
#time: to know when it was last used by the system
class page:  #making a page class to simplify when to intialize a page
	def __init__(self, frame, ref, time):  
		self.frame = frame  #number or item
		self.ref = ref #reference bit
		self.time = time #virtual time of last acess
	#def __str__(self):
	#	print("frame:  {self.frame} ref:  {self.ref}  time:  {self.time} ") 
	def __str__(self):   #mainly use ti debug and see the state of the memory
		return "frame: " + str(self.frame)+ " ref: "+ str(self.ref)+ " time: " + str(self.time)


  
def searchClock(memory, item): #check if item is already in the memory
    
    print("page: " , memory[0])
    
    for i in range(len(memory)):
        print("index: " , i)
        page=memory[i]
        if (memory[i].frame == item):
            return True
    return False
def findIndex(memory, item):#returns the index of the item in memory
	for i in range(len(memory)):
			if (memory[i].frame == item):
				return i
	return -1
#def searchCllock(item,clock):
#   for clo in clock:
  #      if clo[0] == item:
  #          return True
  #  return False


clockindex=0 #always module the index with the size of the memory

memory=[] # memory should be a list of pages
positive_infinity = float('inf') # needed
size= int(sys.argv[1])
tau= int(sys.argv[2])

clocklist=[]
virtualtime=0
#for i in range(size):
#    clocklist.append([0,1,0])
print(clocklist)
pagefault=0
hit=0
file=sys.argv[3]
f = open(file,"r")
data= f.read()
data= data.split() # split on any whitespace so newlines and extra spaces don't break page matching
print(data) 
com = [j.strip('RW:') for j in data]
#print(data.strip(':'))
#com=list(data.strip(" "))
print(com)

index=15
oldest=page(0,0,positive_infinity)
oldestIndex=0
working=False
foundnotref=False
copy=[]
for i in range(len(com)): 
    var= int(com[i])
    copy.append(var)
com=copy.copy()
while(len(memory) < size and com): #before the memory is full adds the page if it isnt there (stops if the sequence runs out)
		p= com.pop(0)

		print("size: ", len(memory))
		index =findIndex(memory,p)
		if (index < 0):
				memory.append( page(p,1,virtualtime) )
				pagefault+=1

		else:
			hit+=1 #page already loaded during warm-up counts as a hit
			memory[index].ref=1
			memory[index].time= virtualtime
 
		virtualtime+= 1

for item in com: #when memory is full
    index=-1
    print("item: ", item)
    #print("acessing comlist: ", com)
    #print("acessing Copiedlist: ", copiedlist)
    for i  in range(len(memory)):
        print("memory:  ",memory[i])
    #print(memory[clockindex])
    if findIndex(memory,item) >= 0: #if page already in memory then hit
    #if searchClock(memory,item):
        hit=hit+1
        index=findIndex(memory,item)
        memory[index].ref= 1
        memory[index].time= virtualtime
        virtualtime= virtualtime + 1
        continue
        
    else: #if page is not in memory
            pagefault= pagefault + 1
        
        #while (not foundnotref):
            
            clockindex= clockindex  % size  #clockindex simulates the pointer or the clock pointer
            foundnotref=False #used if something not referenced is found
            working=False #reset for each page fault, otherwise an old value makes it evict a page that isn't in memory
            oldest=page(0,0,positive_infinity) #intialize the oldest page in the clock
            
            for i in range(len(memory)): #make a loop  by the size of the clock
                #print("clockindex poinmting at: ", clockindex)
                clockindex= clockindex  % size
                if memory[clockindex].ref == 0: #if the page is not referenced
                    if virtualtime - memory[clockindex].time > tau:   # if time that was last accesed was bigger than the working set then remove it and change it to the new one
                        #memory[clockindex] = [item,1,virtualtime]
                        memory[clockindex].frame=item
                        memory[clockindex].ref = 1
                        memory[clockindex].time = virtualtime 
                        
                        clockindex = (clockindex + 1) % size
                        foundnotref=True
                 
                        break
                    else: #if its in the working set then remember the oldest time 
                        if oldest.time > memory[clockindex].time:
                            oldest = memory[clockindex]
                            working = True
                    
                    clockindex = (clockindex + 1) % size
                    break
                else: #if referenced set the referenced bit to 0 and update the time
                    memory[clockindex].ref = 0
                    clockindex = (clockindex + 1) % size
                        
            if not foundnotref and working:# if something has not been found and everything we found was in the workingset then remove oldest
                index= findIndex(memory, oldest.frame)
                memory[index].frame = item
                memory[index].ref = 1
                memory[index].time = virtualtime 
                
                
                  
            elif not foundnotref and not working:# if something has not been found  then remove the page the clockindex is pointing 
                clockindex= clockindex % size
                
                memory[clockindex].frame = item
                memory[clockindex].ref = 1
                memory[clockindex].time = virtualtime 
                clockindex= (clockindex + 1) % size
            #oldest.time=10000
                  
                  
                             
    virtualtime+=1 #virtual adds 
    print("virtual time: ", virtualtime)      
                    
    for i  in range(len(memory)):
        print("memory at the final:  ",memory[i])
print("pagefaults:  ",   pagefault)
print("hits:   ",   hit)
        
    
f.close()



        
    