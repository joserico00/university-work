
from collections import deque
def dfsisland(matrix):
    row = len(matrix)
    cols=len(matrix[0])
    totalIslands=0
    for i in range(row):
        for j in range(cols):
            if(matrix[i][j]==1):
                totalIslands+=1
                visitislandDFS(matrix,i,j)
    return(totalIslands)
def visitislandDFS(matrix,x,y):
    if (x<0 or x>= len(matrix) or y<0 or y>=len(matrix[0])):
        return
    if(matrix[x][y] == 0):
        return
    matrix[x][y]=0
    visitislandDFS(matrix,x-1,y)
    visitislandDFS(matrix,x+1,y)
    visitislandDFS(matrix,x,y+1)
    visitislandDFS(matrix,x,y-1)
    
print("islands",dfsisland([[0, 1, 1, 1, 0], [0, 0, 0, 1, 1], [0, 1, 1, 1, 0], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0]]))





def dfsisland(matrix):
    row = len(matrix)
    cols=len(matrix[0])
    totalIslands=0
    for i in range(row):
        for j in range(cols):
            if(matrix[i][j]==1):
                totalIslands+=1
                visitislandBFS(matrix,i,j)
    return(totalIslands)
def visitislandBFS(matrix,x,y):
    neighbors=deque([(x,y)])
    while neighbors:
        row,col=neighbors.popleft(0)
        if (row<0 or row>= len(matrix) or col<0 or col>=len(matrix[0])):
            continue
        if (matrix[row][col] == 0):
            continue
        matrix[row][col] = 0

    neighbors.extend([(row + 1, col)])
    neighbors.extend([(row - 1, col)])
    neighbors.extend([(row , col+1)])
    neighbors.extend([(row , col-1)])
    
print("islands",dfsisland([[0, 1, 1, 1, 0], [0, 0, 0, 1, 1], [0, 1, 1, 1, 0], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0]]))