def bruteforce(a,target):
    array=a
    target=target
    size=len(array)
    for i in range(size):
        for k in range(size):
            if a[i]+ a[k] == target and i != k:
                return "yes"
def PowRec(x,n):
    exp=0
    
    if n==0:
        return 1
    elif n ==1:
        return x
    else:
        
        return x* PowRec(x,n-1)


PowRec(2,6)


def Powiter(x,n):
    iter=0
    sum=1
    if n==0:
        return 1
    elif n ==1:
        return 
    
    while(iter<n):
        sum=sum*x
        iter+=1
    return sum

Powiter(2,6)

def PowDC(x,n):#O(N)
    
    if n ==0:   #O(1)
        return 1  #O(1)
    m=n//2 #O(1)
    z= PowDC(x,m)  #O(N/2) =O(M)
    if n % 2==0: #O(1)
        y = z*z #O(1)
    else: #O(1)
        y= z*z*x #O(1)
    return y #O(1)
PowDC(2,6)
            #t(n)=O(1)+ T(n/2)
            #T(0)=O(1)
            #T(n)= O(1), n==0 and T(n/2) + O(1), n>0
            #
def PowDCIterFast(x,n):
    y=1
    z=x
    m= n
    while(m>0):
        if (m%2==1):
            y=z*y
        z = z*z
        m=m//2
    return y




def PowDCIterFast(x,n):

    if (n==0): #base case
        return 1
    m=n/2#divide
    y=pow(x,m)#conquer
    if (n&1==1):
        return y * y * x #combine
    return y*y #combine

PowDCIterFast(2,6)


def merge(A,p,q,r):
    