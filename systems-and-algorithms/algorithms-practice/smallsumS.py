def smallsum(array,s):
    windowsum=0
    windowstart=0
    lists=[]
    smallestlen=99
    for windowend in range(len(array)):
        windowsum=windowsum+array[windowend]
        while windowsum>=s:
            if smallestlen >= windowend-windowstart+1:
                smallestlen=windowend-windowstart+1
            windowsum=windowsum-array[windowstart]
            windowstart= windowstart +1
            
    return smallestlen

array= [2,1,5,2,3,2] 
S=7
smallsum(array,S)