#ElGamal密钥生成———基于Diffie-Hellman密钥交换协议
import gmpy2
import random

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x

def invmod(a, m):
    g, x, y = egcd(a, m)
    if g == 1:
        return x % m
    else:
        return None

def gen_key():
    while True:
        q = random.randint(10**149//2 , 10**150 // 2 - 1)
        if gmpy2.is_prime(q):
            p = 2 * q + 1
            if gmpy2.is_prime(p):
                break
    a = random.randint(0, p - 1)
    while True:
        g = random.randint(2, p - 1)
        if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
            break
    y = pow(g, a, p)
    return p, g, y, a

def enc(p, g, y, m):
    while True:
        k = random.randint(1, p - 1)
        if egcd(k, p - 1)[0] == 1: # k与p-1互素，否则有安全问题
            break
    c1 = pow(g, k, p)
    c2 = m * pow(y, k, p) % p
    return k, c1, c2

def dec(p, a, c1, c2):
    V = pow(c1, a, p)
    m = c2 * invmod(V, p) % p
    return m

if __name__ == '__main__':
    f = open('secret4.txt', 'rb')
    m = int(f.read())
    print(f'明文m = {m}')
    p, g, y, a = gen_key()
    k, c1, c2 = enc(p, g, y, m)
    m_de = dec(p, a, c1, c2)
    print(f'解密m_de = {m_de}')
    if m == m_de:
        print(f'p = {p}\ng = {g}\ny = {y}\nk = {k}')
        print(f'C = (c1,c2)\n= ({c1},{c2})')
        print('明文密文相同，加密解密成功!')
    else:
        print('加密解密失败!')
    f.close()
        

