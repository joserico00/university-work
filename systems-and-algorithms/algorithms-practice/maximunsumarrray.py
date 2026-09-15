def summaxarray(array,k):
    result=[]
    windowsum=0
    aritarray=array
    windowstart=0
    maxsum=0
    for windowend in range(len(array)):
        windowsum=windowsum+array[windowend]
        if windowend>=k-1:
            if windowsum >maxsum:
                maxsum=windowsum
            windowsum=windowsum-array[windowstart]  
            windowstart = windowstart +1

            
        
    print(maxsum)


array= [2,1,5,1,3,2]
K=3
summaxarray(array,K)

array=[]