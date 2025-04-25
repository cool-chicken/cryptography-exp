import random
import secrets

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
    
def find_d_large(num_bytes,t,n,k):
    while True:
        d=[]
        for i in range(n):
            random_bytes = secrets.token_bytes(num_bytes)
            random_number = int.from_bytes(random_bytes, 'big')
            d.append(random_number)
        d.sort()
        if judge_d(t,n,d,k)[0] == True:
            M,N = judge_d(t,n,d,k)[1],judge_d(t,n,d,k)[2]
            break
    return d,M,N

def judge_d(t,n,d,k):
    flag = True
    for i in range(1,n):
        if d[i] <= d[i-1]:
            flag =  False
    for i in range(n):
        for j in range(n):
            if egcd(d[i],d[j])[0] != 1 and i != j:
                flag =  False
    N = 1
    M = 1
    for i in range(t):
        N = N * d[i]
    for i in range(t-1):
        M = M * d[n-i-1]
    if N <= M or not N > k > M:
        flag = False
    return flag,M,N

def CRT(t,d,k):
    d_1 = {}
    k_1 = {}
    N_1 = 1
    for i in range(t):
    # for i in range(t-1): ## 为了测试t-1个子秘密不能恢复秘密的情况
        d_1[i] = d.pop(random.randint(0,len(d)-1))
        k_1[i] = k % d_1[i]
        N_1 *= d_1[i]
    K = crt(k_1,d_1,N_1)
    print(f'恢复出的秘密K={K}')
    if K == k:
        print('秘密恢复成功')
    else:
        print('秘密恢复失败')

def crt(a,m,M):
    M_j = [0]*len(m)
    N_j = [0]*len(m)
    x_j = [0]*len(m)
    x_ans = 0
    for j in range(len(m)):
        M_j[j] = M//m[j]
        N_j[j] = invmod(M_j[j],m[j])
        x_j[j] = a[j]*M_j[j]*N_j[j]%M
        x_ans += x_j[j]
        x_ans %= M
    return x_ans%M


if __name__ == '__main__':
    t = int(input('请输入t:'))
    n = int(input('请输入n:'))
    f = open('secret4.txt','r')
    k = int(f.readline())
    d,M,N = find_d_large(100,t,n,k)
    print(f'数组d为:{d}')
    print(f'N={N}\nM={M}')
    CRT(t,d,k)
    f.close()


        
    
