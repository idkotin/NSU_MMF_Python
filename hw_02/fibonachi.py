def fib_rec(n):
    if n<= 1: return n
    else: return fib_rec(n-1) + fib_rec(n-2)

def fib_for(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a

n = int(input())
print(fib_for(n))
print(fib_rec(n))