import random
def SELECT(A, p, r, i):
    if p == r:
        return A[p]
    #utilizando la esquema de select con mediano de medianos para resolver esto
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

A=list(range(1,101))
ran = random.sample(range(1000),1000)
ran.sort()
A.sort()
print(A)
print(ran)
print(percent25(ran))
