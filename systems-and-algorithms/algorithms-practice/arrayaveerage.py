def bruteforce(array,K):

    result=[]
    aritarray=array
    while len(aritarray)>=K:
        cal=sum(aritarray[:K])/K
        result.append(cal)
        aritarray.pop(0)
    print(result)


def sliding(array,K):
    result=[]
    windowsum=0
    aritarray=array
    windowstart=0
    
    for windowend in range(len(array)):
        windowsum=windowsum+array[windowend]
        if windowend>=K-1:
            result.append(windowsum/K)
            windowsum=windowsum-array[windowstart]  
            windowstart = windowstart +1
            
        
    print(result)


array= [1,3,2,6,-1,4,1,8,2]
K=5 

sliding(array,K)