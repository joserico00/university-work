import cmath
def recursive_vtt(a):
    n=len(a)
    y=[0]*n
    if n ==1:
        return a
    wn=cmath.exp(2*cmath.pi*1j/n )  
    w=complex(1,0)
    a0=a[0:n:2]
    a1=a[1:n:2] 
    y0=recursive_vtt(a0)
    y1=recursive_vtt(a1)
    for k in  range(n//2):
        y[k]=y0[k] + w*y1[k]
        y[k+n//2]= y0[k] - w*y1[k]
        w=w*wn
    return y

a=[3,5,4,1]
print(recursive_vtt(a))