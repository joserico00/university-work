#import random
from random import randint
def shakebag(M):
    matched=[]
    while(M):
        l=len(M)
        M=randomize(M,l) #O(n)
        removematches(M,matched)
        
    return matched
def removematches(m,matched):
    i=0
    while( i < len(m)-1):
        if m[i] == m[i+1]:
            matched.append(m[i])
            matched.append(m[i+1])
            m.pop(i)
            m.pop(i)
            i=i-1
        i = i+1

def randomize (arr, n):
    # Start from the last element and swap one by one. We don't
    # need to run for the first element that's why i > 0
    for i in range(n-1,0,-1):
        # Pick a random index from 0 to i
        j = randint(0,i+1)
 
        # Swap arr[i] with the element at random index
        arr[i],arr[j] = arr[j],arr[i]
    return arr

bag=["a","b","c","a","b","c"]
print(shakebag(bag))

bag=["a","d","b","l","c","d","a","b","l","c"]
print(shakebag(bag))