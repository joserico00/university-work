#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'diagonalDifference' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY arr as parameter.
#

def diagonalDifference(arr):
    rightdiagonal=0
    leftdiagonal=0
    size= len(arr)
    for i in range(size):
        rightdiagonal= arr[i][i] + rightdiagonal
    for i in range(size):
        leftdiagonal= arr[size-1-i][i] + leftdiagonal
    print(rightdiagonal)
    print(leftdiagonal)
    
    return abs(rightdiagonal - leftdiagonal)
    # Write your code here

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    arr = []

    for _ in range(n):
        arr.append(list(map(int, input().rstrip().split())))

    result = diagonalDifference(arr)

    fptr.write(str(result) + '\n')

    fptr.close()
