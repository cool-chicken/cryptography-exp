#中国剩余定理代码
import sys
def egcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x1, y1 = egcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return g, x, y
    
def invmod(a, b):
    g, x, y = egcd(a, b)
    if g != 1:
        raise ValueError('模逆不存在')
    else:
        return x % b
    
def crt(a,m):
    for i in range(len(m)):
        for j in range(i+1,len(m)):
            if egcd(m[i],m[j])[0] != 1:
                print(f"m[{i}]和m[{j}]不互素,不能直接利用中国剩余定理".format(i,j))
                sys.exit(1)
    M = 1
    for i in m:
        M *= i
    print(f"m = {M}".format(M))
    M_j = [0]*len(m)
    N_j = [0]*len(m)
    x_j = [0]*len(m)
    x_ans = 0
    for j in range(len(m)):
        M_j[j] = M//m[j]
        N_j[j] = invmod(M_j[j],m[j])
        x_j[j] = a[j]*M_j[j]*N_j[j]%M
        print(f"M[{j}] = {M_j[j]}\nM[{j}]^-1 = {N_j[j]}\nx[{j}] = {x_j[j]}".format(j))
        x_ans += x_j[j]
        x_ans %= M
    return x_ans%M

if __name__ == '__main__':
    with open("4.txt",'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    a = [int(line) for line in lines[:3]]
    m = [int(line) for line in lines[3:6]]
    x = crt(a,m)
    print(f"x = {x}".format(x))