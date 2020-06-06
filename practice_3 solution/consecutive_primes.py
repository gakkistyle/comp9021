from math import sqrt

suquence = []
sign = 0
for i in range (10001,100000,2):
    for j in range(2,round(sqrt(i))+1):
        if i%j == 0:
            sign = 1
            break
    if sign == 0:
        suquence.append(i)
    sign = 0

print('The solutions are:')
print()
for e in range(len(suquence)-5):
    if suquence[e] == suquence[e+1]-2==suquence[e+2]-6==suquence[e+3]-12==suquence[e+4]-20==suquence[e+5]-30:
        for _ in range(e,e+6):
            print(f'{suquence[_]:9}',end='')
        print()
        e += 5

