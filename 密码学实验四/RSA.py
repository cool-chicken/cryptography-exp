import gmpy2
from gmpy2 import iroot, isqrt

n_list = {}
e_list = {}
c_list = {}
m_list = {}

def read_file():
    for i in range(21):
        filename = f'Frame{i}'
        with open(filename, 'r') as f:
            n = int(f.read(256).strip(), 16)
            n_list[i] = n
            e = int(f.read(256).strip(), 16)
            e_list[i] = e
            c = int(f.read(256).strip(), 16)
            c_list[i] = c

def same_N(c1, c2, e1, e2, n):
    g, s, t = gmpy2.gcdext(e1, e2)
    if g != 1:
        return None
    m = gmpy2.powmod(c1,s,n) * gmpy2.powmod(c2,t,n) % n
    return m
def crt(a,m):
    M = 1
    for i in m:
        M *= i
    Mi = [M//i for i in m]
    Mi_ = [gmpy2.invert(M//i, i) for i in m]
    x = 0
    for i in range(len(m)):
        x += a[i]*Mi[i]*Mi_[i]
    return x % M
def decrypt(c1, c2, e1, e2, n1, n2):
    p = gmpy2.gcd(n1, n2)
    q1 = n1 // p
    q2 = n2 // p
    d1 = gmpy2.invert(e1, (p-1)*(q1-1))
    d2 = gmpy2.invert(e2, (p-1)*(q2-1))
    m1 = gmpy2.powmod(c1, d1, n1)
    m2 = gmpy2.powmod(c2, d2, n2)
    return m1, m2


def fermat(n):  # 费马分解n为p、q
    a = gmpy2.isqrt(n)+1
    while True:
        b = gmpy2.isqrt(a * a - n)
        if n == (a + b) * (a - b):
            return a + b, a - b
        a += 1

def pollard_rho(n):
    x = 2
    for i in range(2, 1000000):
        x = pow(x, i, n)
        y = gmpy2.gcd(x-1, n)
        if y != 1 and y != n:
            return y

def coppersmith():
    pass

if __name__ == "__main__":
    read_file()
    # 输出e
    for i, e_1 in e_list.items():
        print(f'e{i}:{e_1}'.format(i, e_1))
    # 输出相同的n
    for i, n_1 in n_list.items():
        for j, n_2 in n_list.items():
            if i < j and n_1 == n_2:
                print(f'n{i} = n{j} = {n_1}'.format(i, j, n_1))
    #输出不互素的n
    for i, n_1 in n_list.items():
        for j, n_2 in n_list.items():
            if i < j and gmpy2.gcd(n_1, n_2) != 1 and n_1 != n_2:
                print(f'n{i}和n{j}不相同且不互素')
    # 0和4的明文
    m = same_N(c_list[0], c_list[4], e_list[0], e_list[4], n_list[0])
    byte = bytes.fromhex(hex(m)[-16:]).decode('utf-8')
    print(f'0和4的明文是：{byte}')
    m_list[0] = bytes
    m_list[4] = bytes
   # 3，8，12，16，20的明文
    c5_list = [c_list[3], c_list[8], c_list[12], c_list[16], c_list[20]]
    n5_list = [n_list[3], n_list[8], n_list[12], n_list[16], n_list[20]]
    m = crt(c5_list, n5_list)
    m = gmpy2.iroot(m, 5)[0]
    byte = bytes.fromhex(hex(m)[-16:]).decode('utf-8')
    print(f'3，8，12，16，20的明文是：{byte}')
    for i in [3, 8, 12, 16, 20]:
        m_list[i] = byte
    #考虑到n1和n18不互素，这样就能够求出相应的大素数p和q然后计算出d1和d18私钥进行解密
    m1, m18 = decrypt(c_list[1], c_list[18], e_list[1], e_list[18], n_list[1], n_list[18])
    byte1 = bytes.fromhex(hex(m1)[-16:]).decode('utf-8')
    byte18 = bytes.fromhex(hex(m18)[-16:]).decode('utf-8')
    print(f'1的明文是：{byte1}')
    print(f'18的明文是：{byte18}')
    m_list[1] = byte1
    m_list[18] = byte18
    #对于帧10可以用费马分解大整数N
    for i in [10,14]:
        p, q = fermat(n_list[i])
        d = gmpy2.invert(e_list[i], (p - 1) * (q - 1))
        m = gmpy2.powmod(c_list[i], d, n_list[i])
        byte = bytes.fromhex(hex(m)[-16:]).decode('utf-8')
        print(f'{i}的明文是：{byte}')
        m_list[i] = byte
    # 对于帧2,6,19可以用Pollard Rho算法分解大整数N
    for i in [2, 6, 19]:
        p = pollard_rho(n_list[i])
        print(f'p{i}={p}')
        q = n_list[i] // p
        d = gmpy2.invert(e_list[i], (p - 1) * (q - 1))
        m = gmpy2.powmod(c_list[i], d, n_list[i])
        byte = bytes.fromhex(hex(m)[-16:]).decode('utf-8')
        print(f'{i}的明文是：{byte}')
        m_list[i] = byte

