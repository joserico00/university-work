def binarysearch(A,T):
   p = 0
   r = len(A) - 1
   while p <= r:
       mid=(p+r)//2
       if A[mid] ==T:
           return True
       elif A[mid]  >T:
           r= mid -1
       else:
           p= mid +1
   return False






def sumT(A,T):
   for i in range(len(A)):
       needs= T -A[i]
       if binarysearch(A[i +1:],needs):
           return "YES"


   return "NO"

a=[1 ,2 ,3 ,4  ,7 ,8 ,9 ,11]

print(sumT(a,1))


