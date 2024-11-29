我们需要批量读取文件，并且分析每个帧内1024bit模数N | 1024bit加密指数e | 1024bit密文$m^{e}$ mod N是否存在相互关系


```python
import os
from pyexpat.errors import messages

import gmpy2
```

首先我们设置4个列表，分别存储N，e，c，m


```python
n_list = {}
e_list = {}
c_list = {}
m_list = {}

```

其次我们需要读取文件，然后分析每个帧内的N，e，c，m


```python
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
```

分析是否有相同的参数e和N


```python
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
```

    e0:46786465362686334917265996843779843233606992585424976481745055335468678697948774988450305612127967926533923268260412557000125153569622340353246096040604284883505587337829322949633637609180797447754513992039018904786537115087888005528547900640339270052628915440787357271345416818313808448127098885767015748889
    e1:65537
    e2:65537
    e3:5
    e4:152206992575706893484835984472544529509325440944131662631741403414037956695665533186650071476146389737020554215956181827422540843366433981607643940546405002217220286072880967331118344806315756304650248634546597784597963886656422706197757265316981889118026978865295597135470735576032282694348773714479076093197
    e5:65537
    e6:65537
    e7:3
    e8:5
    e9:65537
    e10:65537
    e11:3
    e12:5
    e13:65537
    e14:65537
    e15:3
    e16:5
    e17:65537
    e18:65537
    e19:65537
    e20:5
    n0 = n4 = 90058705186558569935261948496132914380077312570281980020033760044382510933070450931241348678652103772768114420567119848142360867111065753301402088676701668212035175754850951897103338079978959810673297215370534716084813732883918187890434411552463739669878295417744080700424913250020348487161014643951785502867


我们发现第0帧和第4帧的n值相同并且e是互素的，根据题目所知，Alice初步发送的时候会重复发送相同明文分片。接下来我们假设他们加密的是相同的密文。


```python
def same_N(c1, c2, e1, e2, n):
    g, s, t = gmpy2.gcdext(e1, e2)
    if g != 1:
        return None
    m = gmpy2.powmod(c1,s,n) * gmpy2.powmod(c2,t,n) % n
    return m
m = same_N(c_list[0], c_list[4], e_list[0], e_list[4], n_list[0])
byte = bytes.fromhex(hex(m)[-16:]).decode('utf-8')
print(f'0和4的明文是：{byte}')
m_list[0] = m_list[4] = byte
```

    0和4的明文是：My secre


然后我们发现第3，8，12，16，20帧的e均为5相对较小，根据题目所知，Alice初步发送的时候会重复发送相同明文分片。接下来我们假设他们加密的是相同的密文。


```python
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
```

根据中国剩余定理，我们可以解出密文m，再对答案求5次方根得到明文


```python
c5_list = [c_list[3], c_list[8], c_list[12], c_list[16], c_list[20]]
n5_list = [n_list[3], n_list[8], n_list[12], n_list[16], n_list[20]]
m = crt(c5_list, n5_list)
m = gmpy2.iroot(m, 5)[0]
byte = bytes.fromhex(hex(m)[-16:]).decode('utf-8')
print(f'3，8，12，16，20的明文是：{byte}')
for i in [3, 8, 12, 16, 20]:
    m_list[i] = byte
```

    3，8，12，16，20的明文是：t is a f


接下来我们来探寻N里面是否有不相同且不互素的情况，这样就能够求出相应的大素数p和q。


```python
for i, n_1 in n_list.items():
    for j, n_2 in n_list.items():
        if i < j and gmpy2.gcd(n_1, n_2) != 1 and n_1 != n_2:
            print(f'n{i}和n{j}不相同且不互素')
```

    n1和n18不相同且不互素


考虑到n1和n18不互素，这样就能够求出相应的大素数p和q然后计算出d1和d18私钥进行解密


```python
def decrypt(c1, c2, e1, e2, n1, n2):
    p = gmpy2.gcd(n1, n2)
    q1 = n1 // p
    q2 = n2 // p
    d1 = gmpy2.invert(e1, (p-1)*(q1-1))
    d2 = gmpy2.invert(e2, (p-1)*(q2-1))
    m1 = gmpy2.powmod(c1, d1, n1)
    m2 = gmpy2.powmod(c2, d2, n2)
    return m1, m2
```

以上函数编写的是解密函数，接下来我们调用函数进行解密


```python
m1, m18 = decrypt(c_list[1], c_list[18], e_list[1], e_list[18], n_list[1], n_list[18])
byte1 = bytes.fromhex(hex(m1)[-16:]).decode('utf-8')
byte18 = bytes.fromhex(hex(m18)[-16:]).decode('utf-8')
print(f'1的明文是：{byte1}')
print(f'18的明文是：{byte18}')
m_list[1] = byte1
m_list[18] = byte18
```

    1的明文是：. Imagin
    18的明文是：m A to B



```python
for i, byte in m_list.items():
    print(f'明文{i}:{byte}'.format(i, byte))
```

    明文0:My secre
    明文4:My secre
    明文3:t is a f
    明文8:t is a f
    明文12:t is a f
    明文16:t is a f
    明文20:t is a f
    明文1:. Imagin
    明文18:m A to B


对于帧10和帧14我们可以运用费马分解来分解大整数N得到素数p和q，然后计算出私钥d进行解密


```python
def fermat(n):  # 费马分解n为p、q
    a = gmpy2.isqrt(n)+1
    while True:
        b = gmpy2.isqrt(a * a - n)
        if n == (a + b) * (a - b):
            return a + b, a - b
        a += 1
```


```python
for i in [10,14]:
    p, q = fermat(n_list[i])
    d = gmpy2.invert(e_list[i], (p - 1) * (q - 1))
    m = gmpy2.powmod(c_list[i], d, n_list[i])
    byte = bytes.fromhex(hex(m)[-16:]).decode('utf-8')
    print(f'{i}的明文是：{byte}')
    m_list[i] = byte
```

    10的明文是：will get
    14的明文是： you fro


对于帧2,6,19可以利用pollard_rho算法进行分解大整数N得到素数p和q，然后计算出私钥d进行解密


```python
def pollard_rho(n):
    x = 2
    for i in range(2, 1000000):
        x = pow(x, i, n)
        y = gmpy2.gcd(x-1, n)
        if y != 1 and y != n:
            return y
```

接下来我们调用函数进行解密


```python
for i in [2, 6, 19]:
    p = pollard_rho(n_list[i])
    q = n_list[i] // p
    d = gmpy2.invert(e_list[i], (p - 1) * (q - 1))
    m = gmpy2.powmod(c_list[i], d, n_list[i])
    byte = bytes.fromhex(hex(m)[-16:]).decode('utf-8')
    print(f'{i}的明文是：{byte}')
    m_list[i] = byte
```

    2的明文是： That is
    6的明文是： "Logic 
    19的明文是：instein.



```python
for i, byte in m_list.items():
    print(f'明文{i}:{byte}'.format(i, byte))
```

    明文0:My secre
    明文4:My secre
    明文3:t is a f
    明文8:t is a f
    明文12:t is a f
    明文16:t is a f
    明文20:t is a f
    明文1:. Imagin
    明文18:m A to B
    明文10:will get
    明文14: you fro
    明文2: That is
    明文6: "Logic 
    明文19:instein.


通过这些帧的明文我们能够猜出明文是b'My secret is a famous saying of Albert Einstein. That is "Logic will get you from A to B. Imagination will take you everywhere."'
