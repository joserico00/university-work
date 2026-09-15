# Author: Jose E. Rodriguez Rios
# #This program simulates the page replacement algorithm Optimal Page Replacement

import sys
memory=[]
size=4
pagefault=0
hit=0
size= int(sys.argv[1])#memory size
file=sys.argv[2]#sequence list
f = open(file,"r")
data= f.read()
data= data.split() # split on any whitespace so newlines and extra spaces don't break page matching
print(data) 
com = [j.strip('RW:') for j in data]
#print(data.strip(':'))
#com=list(data.strip(" "))
print(com)

copiedlist=com.copy() #copied sequence list where we use to compare if any pages in the future are needed
index=15
for item in com:#for each item in sequence list
    index=-1 #initialized index of the farthest used page in sequence
    #print("acessing: ", item)
    #print("acessing comlist: ", com)
    #print("acessing Copiedlist: ", copiedlist)
    if item in memory: #if page already in list hit
        hit=hit+1
        
    else:
        pagefault= pagefault + 1#add a pagefault since page wasnt in memory
        if len(memory) < size:#if memory not filled add it
            memory.append(item)
        else: #if memory filled run the page replacement algorithm
            for i in memory: #checks each page
                if i in copiedlist: #checks if item is in the sequence list
                    newindex = copiedlist.index(i) #if it used then get the index of the  stored item
                    if index < newindex: #if newindex is bigger than index then stores the newindex as index since newindex is farthest used
                        index = newindex
                else:  #if page isnt in the sequence list then remove and append the new page
                     
                    memory.remove(i) 
                    memory.append(item)
                    break
            else:  # when the for loop ends removes the farthest used page and adds a new page
                val= copiedlist[index]
                memory.remove(val)
                memory.append(item)
            
            
                    
    print("memory now:  " , memory)
    copiedlist.pop(0) #pop a item from a copied sequence list
print("pagefaults: ",pagefault)
print("Hits: ",hit)
        
    
f.close()
