#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'timeConversion' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#

def timeConversion(s):
    # Write your code here
    slist=[]
    slist[:0]= s
    max=len(slist)
    oed=slist.pop(max-2)
    oed=oed + slist.pop(max-1)
    time= slist.pop(1)
    time = time + slist.pop(2)
    liststring=""
    for i in slist:
        liststring=liststring+ i
    if oed == "PM":
        time = str((int(time) + 12) %24)
        s= time  + liststring
    
    print(liststring)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = input()

    result = timeConversion(s)

    fptr.write(result + '\n')

    fptr.close()
