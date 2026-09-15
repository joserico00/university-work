# Enter your code here. Read input from STDIN. Print output to STDOUT
n = input()
tup= input()
lst=tup.split(' ')
lst=[int(x) for x in lst]
print(lst)
res=tuple(lst)
print(res)


tp=()
#tp=[]
#for i in range(len(n)):
 #   tp= tp+ (int(lst[i]))

print(lst)
#res = tuple(tp)
print(hash(res))
