# COMP9021 Term 3 2019
# Rachid Hamadi

def fact(n):
    if n <= 1:
        return 1
    return n*fact(n-1)
print(fact(4))

def facti(n):
    res = 1
    for i in range(2,n+1):
        res*=i
    return res
print(facti(4))