# Author: Jose E. Rodriguez Rios
# This program simulates the page replacement algorithm First in First Out Page Replacement

import sys
memory=[]
size=3
pagefault=0
hit=0
size= int(sys.argv[1]) #memory size
file=sys.argv[2] #sequence to read from
f = open(file,"r")
data= f.read()
data= data.split() # split on any whitespace so newlines and extra spaces don't break page matching
print(data) 
com = [j.strip('RW:') for j in data]
#print(data.strip(':'))
#com=list(data.strip(" "))
print(com)


for item in com:# for each sequence inthe list
    if item in memory: #if page already in the memory then hit
        hit=hit+1
        
    else:
        pagefault= pagefault + 1 #if page isnt in the memory then page fault
        if len(memory) < size:# if memory not filled then add page to the end
            memory.append(item)
        else:# if memory is filled remove first elemtn and add to the end the new page
            memory.pop(0)
            memory.append(item)
    print(memory)
print("pagefault: ",pagefault)
print("hits: ",hit)
        
    
f.close()
