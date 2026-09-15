def minsum(t,A):
    l=0
    
    lenght=float("inf")
    current=0
    for r in range(len(t)):
        
        
class Solution:
    def calPoints(self, operations: List[str]) -> int:
        record =0
        stack=[]
        for op in operations:
            if op.isdigit():
                stack.append(int(op))
                previous=int(op)
            elif op == '+':
                stack.append(previous+stack[-2])
            elif op == 'D':
                stack.append(previous*2)
            elif op == 'C':
                stack.pop()
            print(previous)
        print(stack)
        return sum(stack)

