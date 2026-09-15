import random

def percent25(A):
    lenght=len(A)
    i=(lenght*0.25)
    p=0
    r=lenght-1
    Select25(A, p, r,i)
    
def Select25(A, p, r,i):
    lenght=len(A)
    #i=(lenght*0.25)-1
    if p==r:
        print( A[p])
        print(A)
        return A[p]
    q=randompartition(A,p,r)
    k=q-p+1
    print(A)
    if i ==k:
        print(A[q])
        print(A)
        return A[q]
    elif i<k:
        return Select25(A,p,q-1,i)
    else:
        return Select25(A,q+1,r,i-k)
    
    
def partition(A,p,r):
    x=A[r]
    i=p-1
    for j in range(p,r):    
        if A[j]<=x:
            i=i+1
            tmp=A[i]
            A[i]=A[j]
            A[j]=tmp
    tmp=A[i+1]
    A[i+1]=A[r]
    A[r]=tmp
    return i+1
    
def randompartition(A,p,r):
    i = random.randint(p,r)
    tmp=A[r]
    A[r]=A[i]
    A[i]=tmp
    return partition(A,p,r)
    
A=list(range(1,101))
ran = random.sample(range(1000),1000)
#print(ran)
#percent25(ran)


def MaxProductSubAaybruteforce(A):
    products=[]
    maxp=0
    lenght=len(A)
    print(A)
    for r in range(lenght):
        for s in range(lenght):
            pro=A[s]*A[r]
            print(r,s)
            if maxp< pro and r!=s:
                maxp=pro
                indexr=r
                indexs=s
    print(indexr,indexs)
    return indexr,indexs
    
    
MaxProductSubAaybruteforce(A)
def MaxProductSubAay(A):
    n=len(A)
    Maxproduct=[0]*n
    minproduct=[0]*n
    Maxproduct[0] = minproduct[0] = currentmax = r = s = A[0]
    for i in range(1,n):
        Maxproduct[i]=max(Maxproduct[i-1]*A[i], minproduct[i-1]*A[i], A[i]) 
        minproduct[i] = min(Maxproduct[i-1]*A[i],minproduct[i-1]*A[i], A[i])
        if Maxproduct[i]>currentmax:
            currentmax=Maxproduct[i]
            r=A.index(max_product[i])
            s=i
def MaxProduct(A):
    n=len(A)
    MaxProduct=A[0]
    currentmax=A[0]
    currentmin=A[0]
    result=(0,0)
    s=0
    r=0
    for i in range(1, n):
        if A[i] < 0:
            currentmax, currentmin = currentmin, currentmax 
            s,r=r,s
          
        currentmax = max(A[i], currentmax * A[i])
        currentmin = min(A[i], currentmin * A[i])
        if MaxProduct< currentmax:
            MaxProduct=currentmax
            result=(s,i)
            r=i
        elif A[i]>0:
            r=i
        else:
            s=i+1
            r=i+1
    return result

def dynamicpro(A):
    Maxproduc=0
    Mini=0
    maxpossibleprd=0
    s=0
    r=0
    
    lenght=len(A)
    for i in range(lenght):
        
        if A[i]<0: # numero negativos
            temp= Maxi
            Maxi=Mini
            Mini=temp
        Maxi= max(A[i], Maxi*n)
        Mini= max(A[i], Mini*n)
        if Maxi> maxpossibleprd:
            s=1
        maxpossibleprd= max(maxpossibleprd,Maxi)
    return maxpossibleprd




A=list(range(1,101))
ran = random.sample(range(1000),1000)
print(percent25(ran))


A = [1, -2, -3, 0, 7, -8, -2 ]
A=[1,-10,4,3,2,4,-2,5]
print(A)
print(MaxProduct(A))

def maxSubAayProduct(A):
    n=len(A)
    currentmax = A[0]
    currentmin = A[0]
    MaxProduct = A[0]
    s = 0
    r = 0
    temp_s = 0

    for i in range(1, n):
        if A[i] < 0:
            currentmax, currentmin = currentmin, currentmax
            temp_s, r = r, temp_s

        currentmax = max(A[i], A[i] * currentmax)
        currentmin = min(A[i], A[i] * currentmin)
        if MaxProduct < currentmax:
            MaxProduct = currentmax
            s = temp_s
            r = i

        elif A[i] <= 0:
            temp_s = i + 1

    return (s, r)
 
print(maxSubAayProduct(A))


# Python3 program to find Maximum Product Subarray
 
#  Returns the product
# of max product subarray.
 
 
def maxSubarrayProduct(arr, n):
 
    # max positive product
    # ending at the current position
    max_ending_here = arr[0]
 
    # min negative product ending
    # at the current position
    min_ending_here = arr[0]
 
    # Initialize overall max product
    max_so_far = arr[0]
 
    # /* Traverse through the array.
    # the maximum product subarray ending at an index
    # will be the maximum of the element itself,
    # the product of element and max product ending previously
    # and the min product ending previously. */
    for i in range(1, n):
        temp = max(max(arr[i], arr[i] * max_ending_here),
                   arr[i] * min_ending_here)
        min_ending_here = min(
            min(arr[i], arr[i] * max_ending_here), arr[i] * min_ending_here)
        max_ending_here = temp
        max_so_far = max(max_so_far, max_ending_here)
 
    return max_so_far
 
 

print(A)
maxSubarrayProduct(A,len(A))


def maxSubarrayProduct(arr):
    n = len(arr)
    max_ending_here = min_ending_here = max_so_far = arr[0]
    start = end = s = 0

    for i in range(1, n):
        if arr[i] < 0:
            max_ending_here, min_ending_here = min_ending_here, max_ending_here
            s, end = end, s

        max_ending_here = max(arr[i], arr[i] * max_ending_here)
        min_ending_here = min(arr[i], arr[i] * min_ending_here)

        if max_so_far < max_ending_here:
            max_so_far = max_ending_here
            start = s
            end = i

        if arr[i] < 0:
            s = i + 1

    return start, end


# Example usage
arr = [2, -3, 4, -1, -2, 1, 5, -3]
start, end = maxSubAayProduct(arr)
print("Indices:", start, end)


def SELECT(A, p, r, i):
    if p == r:
        return A[p]
    #utilizando la esquema de select con medianos de medianos para resolver esto
    # Paso 1
    grupos = [A[j:j + 5] for j in range(p, r + 1, 5)]

    # Paso 2
    medianas = [sorted(grupo)[len(grupo) // 2] for grupo in grupos]

    # Paso 3
    x = SELECT(medianas, 0, len(medianas) - 1, len(medianas) // 2)

    # Paso 4
    q = PARTITION(A, p, r, x)
    k = q - p + 1

    # Paso 5
    if i == k:
        return x
    elif i < k:
        return SELECT(A, p, q - 1, i)
    else:
        return SELECT(A, q + 1, r, i - k)

def PARTITION(A, p, r, x):
    # Encuentra el índice del valor x en A
    idx_x = A.index(x)

    # Intercambia A[idx_x] con A[r]
    A[idx_x], A[r] = A[r], A[idx_x]

    # Proceso de partición estándar
    i = p - 1
    for j in range(p, r):
        if A[j] <= x:
            i += 1
            A[i], A[j] = A[j], A[i]

    A[i + 1], A[r] = A[r], A[i + 1]
    return i + 1

def percent25(A):
    n=len(A)
    i=int(n*0.25)
    p=0
    r=n-1
    return SELECT(A, p, r,i)

print(percent25(A))