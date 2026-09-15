import numpy

def isItEven(num):
   return num % 2 == 0


def MedianOfTwo(A, B, n): # T(n)
   print("MedianNow", A, B)


   if n == 1:
       return (A[0] + B[0]) / 2
   elif n == 2:
       print('LAst 4')
       print(A, B)
       A, B = TwoArraysOfOneElement(A, B)
       return MedianOfTwo(A, B, len(A))


   if isItEven(n):
       indexMedianOfA = n // 2
       medianOfA = (A[indexMedianOfA - 1] + A[indexMedianOfA]) /  2
       print("medianOfA = (A[%s - 1] + A[%s]) / 2 = %s" % (indexMedianOfA, indexMedianOfA, medianOfA))
   else:
       indexMedianOfA = (n - 1) // 2
       medianOfA = A[indexMedianOfA]
       print("medianOfA = A[%s] = %s" % (indexMedianOfA, medianOfA))


   if isItEven(n):
       indexMedianOfB = n // 2
       medianOfB = (B[indexMedianOfB - 1] + B[indexMedianOfB]) /  2
       print("medianOfB = (B[%s - 1] + B[%s]) / 2 = %s" % (indexMedianOfB, indexMedianOfB, medianOfB))
   else:
       indexMedianOfB = (n - 1) // 2
       medianOfB = B[indexMedianOfB]
       print("medianOfB = B[%s] = %s" % (indexMedianOfB, medianOfB))


   print("indexMedianOfA -> %s" % indexMedianOfA)
   print("indexMedianOfB -> %s" % indexMedianOfB)


   if medianOfA > medianOfB:
       print("medianOfA > medianOfB --> %s > %s" % (medianOfA , medianOfB))


       if isItEven(n):
           # indexMedianOfA = n // 2
           # (A[indexMedianOfA - 1] + A[indexMedianOfA])
           # indexMedianOfB = n // 2
           # (B[indexMedianOfB - 1] + B[indexMedianOfB])
           A = A[0:indexMedianOfA + 1]
           B = B[indexMedianOfB - 1:]
       else:
           # indexMedianOfA = (n - 1) // 2
           # indexMedianOfB = (n - 1) // 2


           A = A[0: indexMedianOfA + 1]
           B = B[indexMedianOfB:]
       return MedianOfTwo(A, B, len(A))


   elif medianOfA < medianOfB:
       print("medianOfA < medianOfB -->  %s > %s" % (medianOfA, medianOfB))




       if isItEven(n):
           # indexMedianOfA = n // 2
           # (A[indexMedianOfA - 1] + A[indexMedianOfA])
           # indexMedianOfB = n // 2
           # (B[indexMedianOfB - 1] + B[indexMedianOfB])


           A = A[indexMedianOfA - 1:]
           B = B[0:indexMedianOfB + 1]
       else:
           # indexMedianOfA = (n - 1) // 2
           # indexMedianOfB = (n - 1) // 2


           A = A[indexMedianOfA:]
           B = B[0:indexMedianOfB + 1]




       # A = A[indexMedianOfA:]
       # if indexMedianOfB == 2:
       #     B = B[0:2]
       # else:
       #     B = B[0:indexMedianOfB + 1]
       # print("B[0:%s + 1]" % indexMedianOfB)
       return MedianOfTwo(A, B, len(A))


   return medianOfA




def TwoArraysOfOneElement(A, B):
   print("TwoArraysOfOneElement", A, B)
   i = A[0]
   j = A[1]
   k = B[0]
   l = B[1]
   medianOfA = (i + j) / 2
   medianOfB = (k + l) / 2
   if medianOfA > medianOfB:
       return [minimum(i, j)], [maximum(k, j)]
   # medianOfA < medianOfB:
   return [maximum(i, j)], [minimum(k, l)]


def minimum(num1, num2):
   if num1 <= num2:
       return num1
   return num2


def maximum(num1, num2):
   if num1 >= num2:
       return num1
   return num2



A=[1,2,3,4,5,6]
B=[7,8,9,10,11,12]
A=numpy.random.randint(1,9,6)
B=numpy.random.randint(1,9,6)
A.sort()
B.sort()

print(MedianOfTwo(A, B, len(A)))