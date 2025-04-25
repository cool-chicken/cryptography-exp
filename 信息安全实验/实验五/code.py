import random
import binascii
import math
from gmssl import sm3 ,func
import numpy as np

p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
gx= 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
gy= 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
h = 1
 
def egcd(a, b):
    if b == 0:          
        return 1, 0, a     
    else:         
        x, y, gcd = egcd(b, a % b) 
        x, y = y, (x - (a // b) * y)          
        return x, y, gcd

def add(x1, y1, x2, y2):
    if x1 == math.inf:
        return x2,y2
    if x2 == math.inf:
        return x1,y1
    if x1 == x2 and y1 == -y2:
        return math.inf,math.inf
    if x1 == x2 and y1 == y2:
        l = (3 * x1 * x1 + a) * egcd(2 * y1, p)[0] % p
    else:
        l = (y2 - y1) * egcd(x2-x1,p)[0] % p
    x3 = l * l - x1 - x2
    y3 = l * (x1 - x3) - y1
    return x3 % p, y3 % p

def mul(x1, y1, k):
    k = bin(k)[2:]
    x3,y3 = math.inf,math.inf
    for i in k:
        x3,y3 = add(x3,y3,x3,y3)
        if int(i) == 1:
            x3,y3 = add(x3,y3,x1,y1)
    return x3,y3

def keygen(q):
    d = random.randint(1,n-2)
    # d = 0x1649AB77A00637BD5E2EFE283FBF353534AA7F7CB89463F208DDBC2920BB0DA0
    xp,yp = mul(gx,gy,d)
    if publickeytest(q,xp,yp) == False:
        return keygen(q)
    else:
        return d,[xp,yp]

def publickeytest(q,x1,y1):
    if x1 == math.inf or y1 == math.inf:
        return False
    if x1 < 0 or x1 >= q-1:
        return False
    if y1 < 0 or y1 >=q-1:
        return False
    if y1*y1 % q != (x1**3 + a*x1 + b) % q:
        return False
    xx,yy = mul(x1,y1,n)
    # if  xx!= math.inf and yy != math.inf:
    #     return False
    return True


d, PB = keygen(p)

def KDF(Z,klen):
    ct = 0x00000001
    v = 256
    num = klen//v
    K = ''
    for i in range(num):
        ct_bytes = ct.to_bytes(4, byteorder='big') 
        K += sm3.sm3_hash(func.bytes_to_list(Z + ct_bytes))
        ct += 1
    if klen % v == 0:
        return K
    else:
        ct_bytes = ct.to_bytes(4, byteorder='big') 
        Ha = sm3.sm3_hash(func.bytes_to_list(Z + ct_bytes))
        K += Ha[:(klen-(v*math.ceil(klen/v)))//4]
    return K

def bytes_to_point(S,l):
    PC = S[:2]
    x = int(S[2:l+1],16)
    y = int(S[l+1:],16)
    if PC != '04':
        return False
    return x,y


def point_to_bytes(xp,yp):
    xp = hex(xp)[2:]
    yp_bit = bin(yp)[2:]
    yp = hex(yp)[2:]
    ypp = yp_bit[-1]
    # if ypp == '0':
    #     PC = '02'
    # elif ypp == '1':
    #     PC = '03'
    # S = PC + xp
    PC = '04'
    S = PC + xp + yp
    print(S)
    return S

def bits_to_hex(bit_string):
    integer_value = int(bit_string, 2)
    hex_string = hex(integer_value)[2:]
    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string
    return hex_string

def encrypt(M):
    m = ''.join(format(ord(i),'08b') for i in M)
    # m = format(int(binascii.hexlify(M.encode()), 16), '8b')
    klen = len(m)
    print(klen)
    print(f'明文的二进制比特串为：{m}')
    k = random.randint(1,n-1)
    # k = 0x4C62EEFD6ECFC2B95B92FD6C3D9575148AFA17425546D49018E5388D49DD7B4F
    print(f'随机数k为：{hex(k)}')
    x1,y1 = mul(gx,gy,k)
    # print(f'x1为:{hex(x1)}\ny1为:{hex(y1)})')
    c1 = point_to_bytes(x1,y1)
    # print(f'c1为:{c1}')

    S = mul(PB[0],PB[1],h)
    if S[0] == math.inf or S[1] == math.inf:
        return False
    x2,y2 = mul(PB[0],PB[1],k)
    # print(f'x2为:{hex(x2)}\ny2为:{hex(y2)}')
    x2_to_bytes = x2.to_bytes(32, byteorder='big') 
    y2_to_bytes = y2.to_bytes(32, byteorder='big')
    string = x2_to_bytes + y2_to_bytes
    t = KDF(string,klen)
    # print(f't = {t}')
    # print(hex(int(t,16)))
    t = bin(int(t,16))[2:]
    if t == '0'*len(t):
        raise ValueError('KDF输出全为0')
    c2 = int(m,2) ^ int(t,2)
    # print(f'c2为:{hex(c2)}')
    m_to_bytes = int(m,2).to_bytes((len(m) + 7) // 8, byteorder='big')
    c3 = sm3.sm3_hash(func.bytes_to_list(x2_to_bytes + m_to_bytes + y2_to_bytes))
    # print(f'c3为:{c3}')
    C = c1 + hex(c2)[2:] + c3
    print(f'密文为:{C}')
    return C

def decrypt(C):
    l = math.ceil(math.log2(p)/8)
    slen = 2*l + 1
    C1 = C[:2*slen]
    print(f'解密C1为:{C1}')
    klen = len(C) - 2*slen - 64
    C2 = C[2*slen:-64]
    print(f'解密C2为:{C2}')
    C3 = C[-64:]
    print(f'解密C3为:{C3}')
    xp,yp = bytes_to_point(C1,slen)
    print(f'解密x1为:{hex(xp)}\ny1为:{hex(yp)}')
    if yp * yp % p != (xp**3 + a*xp + b) % p:
        raise ValueError("解密失败，C1不是椭圆曲线上的点")
    S = mul(xp,yp,h)
    if S[0] == math.inf or S[1] == math.inf:
        return False
    x2,y2 = mul(xp,yp,d)
    x2_to_bytes = x2.to_bytes(32, byteorder='big') 
    y2_to_bytes = y2.to_bytes(32, byteorder='big')
    string = x2_to_bytes + y2_to_bytes
    t = KDF(string,klen*4)
    if t == '0'*len(t):
        raise ValueError('KDF输出全为0')
    print(t)
    M = int(C2,16) ^ int(t,16)
    print(f'解密明文为:{hex(M)}')
    hex_string = hex(M)[2:]  # 将整数转换为十六进制字符串，并去掉前缀 '0x'
    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string  # 确保长度为偶数
    # 将十六进制字符串转换为字节串
    byte_data = bytes.fromhex(hex_string)
    
    # 将字节串进行 UTF-8 解码
    utf8_encoded = byte_data.decode('utf-8')
    print(f'解密明文的UTF-8编码为:{utf8_encoded}')
    u = sm3.sm3_hash(func.bytes_to_list(x2_to_bytes + byte_data + y2_to_bytes))
    if u == C3:
        print('解密成功')
    else:
        print('解密失败')
    



if __name__ == '__main__':

    M = input('请输入明文：')
    C = encrypt(M)
    decrypt(C)
