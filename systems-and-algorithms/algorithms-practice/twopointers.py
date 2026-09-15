

def pair_with_targetsum(arra,target):
    pointer1=0
    pointer2=len(arra)-1
    while(pointer1< pointer2):
        sum= pointer1+ pointer2 
        if sum == target:
            return [pointer1,pointer2]
        if sum > target:
            pointer2-=1
        else:
            pointer1 +=1
    return [-1,-1]

print(pair_with_targetsum([1, 2, 3, 4, 6], 6))
print(pair_with_targetsum([2, 5, 9, 11], 11))


def pair_with_targetsum(arr, target_sum):
    hashtable={}
    for i in range(len(arr)):
        
        sum=target_sum-arr[i]
        if sum not in hashtable:
            hashtable[arr[i]]=i
        else:
            return [hashtable[sum],i]
    return [-1,-1]

print(pair_with_targetsum([1, 2, 3, 4, 6], 6))
print(pair_with_targetsum([2, 5, 9, 11], 11))





def make_squares(arr):
    left=0
    right=len(arr) -1
    squaredarr=[]
    while(left<= right):
        leftsqr=arr[left]*arr[left]
        rightsqr=arr[right]*arr[right]
        if leftsqr > rightsqr:
            squaredarr.insert(0,leftsqr)
            left+=1
        else:
            squaredarr.insert(0,rightsqr)
            right-=1
    return squaredarr


print("Squares: " + str(make_squares([-2, -1, 0, 2, 3])))
print("Squares: " + str(make_squares([-3, -1, 0, 1, 2])))



def remove_duplicates(arr):
    i=1
    uniq=0
    for right in range(1,len(arr)):
        if arr[right-1] !=arr[right]:
            
            i+=1 
        right+=1
           
    return i
print(remove_duplicates([2, 3, 3, 3, 6, 9, 9]))
print( remove_duplicates([2, 2, 2, 11]))


def pair_with_targetsum(arra,target):
    pointer1=0
    pointer2=len(arra)-1
    arra.sort()
    while(pointer1< pointer2):
        sum= pointer1+ pointer2 
        if sum == target:
            return [pointer1,pointer2]
        if sum > target:
            pointer2-=1
        else:
            pointer1 +=1
    return [-1,-1]