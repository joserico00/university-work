import sys

data = sys.stdin.read().splitlines()
colors=["White", "Black", "Blue", "Red" ,"Yellow."]

count=data[0]
for i in range(count):
    colors.remove(data[i+1])
print(data[1])