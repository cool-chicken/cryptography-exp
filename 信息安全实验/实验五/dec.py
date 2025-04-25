import random
import math
import os
import binascii
from gmpy2 import powmod, invert, is_prime
import re
# SM3的初始向量
IV = [
    0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
    0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E
]
 
# 布尔函数FFj
# SM2的曲线参数
p = 0xfffffffeffffffffffffffffffffffffffffffff00000000ffffffffffffffff
a = 0xfffffffeffffffffffffffffffffffffffffffff00000000fffffffffffffffc
b = 0x28e9fa9e9d9f5e344d5a9e4bcf6509a7f39789f515ab8f92ddbcbd414d940e93
gx = 0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7
gy = 0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0
n = 0xfffffffeffffffffffffffffffffffff7203df6b21c6052b53bbf40939d54123
 
E_order = n
# 椭圆曲线点加法
 
 
def FF(X, Y, Z, j):
    if j < 16:
        return X ^ Y ^ Z
    else:
        return (X & Y) | (X & Z) | (Y & Z)
 
# 置换函数
 
 
def P0(X):
    return X ^ LS(X, 9) ^ LS(X, 17)
 
 
def P1(X):
    return X ^ LS(X, 15) ^ LS(X, 23)
 
# 循环左移
 
 
def LS(X, n):
    return ((X << n) & 0xFFFFFFFF) | (X >> (32 - n))
 
# 布尔函数GGj
 
 
def GG(X, Y, Z, j):
    if j < 16:
        return X ^ Y ^ Z
    else:
        return (X & Y) | (~X & Z)
 
# 消息填充函数
 
 
def pad_message(message):
    mlen1 = len(message)
    mlen = mlen1
    message += b'\x80'
    mlen += 1
    while mlen % 64 != 56:
        message += b'\x00'
        mlen += 1
    message += (mlen1 * 8).to_bytes(8, 'big')
    return message
 
# SM3压缩函数
 
 
def SM3_CF(V, B, k):
    W = [0] * 68
    W_ = [0] * 64
    for i in range(16):
        W[i] = int.from_bytes(B[i*4:i*4+4], 'big')
    for i in range(16, 68):
        W[i] = P1(W[i-16] ^ W[i-9] ^ LS(W[i-3], 15)) ^ LS(W[i-13], 7) ^ W[i-6]
    for i in range(64):
        W_[i] = W[i] ^ W[i+4]
    # for i in range(0, len(W), 4):
    #     print(' '.join(hex(value) for value in W[i:i+4]))
 
    A, B, C, D, E, F, G, H = V
    for i in range(64):
        SS1 = LS((LS(A, 12) + E + LS(T(i), i % 32)) & 0xFFFFFFFF, 7)
        SS2 = SS1 ^ LS(A, 12)
        TT1 = (FF(A, B, C, i) + D + SS2 + W_[i]) & 0xFFFFFFFF
        TT2 = (GG(E, F, G, i) + H + SS1 + W[i]) & 0xFFFFFFFF
        D = C
        C = LS(B, 9)
        B = A
        A = TT1
        H = G
        G = LS(F, 19)
        F = E
        E = P0(TT2)
        # print(
        #     f"Step {i+1} - A: {A:08X}, B: {B:08X}, C: {C:08X}, D: {D:08X}, E: {E:08X}, F: {F:08X}, G: {G:08X}, H: {H:08X}")
    return A, B, C, D, E, F, G, H
 
# T函数
 
 
def T(j):
    if j < 16:
        return 0x79CC4519
    else:
        return 0x7A879D8A
 
# SM3哈希函数
 
 
def string_to_ascii(s):
    return [ord(c) for c in s]
 
 
def or_16(A, B):
    A = int(A, 16)
    B = int(B, 16)
    C = A ^ B
    C = '{:08x}'.format(C)
    return C
# SM3哈希函数
 
 
# # 示例
# message = 'abc'
# hash_value = SM3(message)
# formatted_hex_string2 = re.sub(r'(.{8})', r'\1 ', hash_value)
# print("Hash Value:", formatted_hex_string2)
 
 
def sm3_hash(message):
    return SM3(message)
 
 
# def modinv(a, m):
#     # 使用扩展欧几里得算法来计算模逆
#     def extended_gcd(a, b):
#         if a == 0:
#             return b, 0, 1
#         else:
#             gcd, x, y = extended_gcd(b % a, a)
#             return gcd, y - (b // a) * x, x
 
#     gcd, x, _ = extended_gcd(a, m)
#     if gcd != 1:
#         raise ValueError('模逆不存在')
#     else:
#         return x % m
def modinv(a, m):
    def extended_gcd(a, b):
        x0, x1, y0, y1 = 1, 0, 0, 1
        while b != 0:
            q, a, b = a // b, b, a % b
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        return a, x0, y0
 
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError('模逆不存在')
    else:
        return x % m
 
 
def add(x1, y1, x2, y2, a, p):
    if x1 == x2 and y1 != y2:
        return 0, 0
    if x1 == x2 and y1 == y2:
        l = (3 * x1 * x1 + a) * modinv(2 * y1, p)
    else:
        l = (y2 - y1) * modinv(x2 - x1, p)
    x3 = l * l - x1 - x2
    y3 = l * (x1 - x3) - y1
    return x3 % p, y3 % p
 
# 椭圆曲线点乘法
 
 
def mul(x1, y1, k, a, p):
    if k == 0:
        return 0, 0
    if k == 1:
        return x1, y1
    if k % 2 == 0:
        x2, y2 = mul(x1, y1, k // 2, a, p)
        return add(x2, y2, x2, y2, a, p)
    else:
        x2, y2 = mul(x1, y1, (k - 1) // 2, a, p)
        return add(x2, y2, x1, y1, a, p)
 
# KDF函数
 
 
def KDF(Z, klen):
    ct = 1
    v = 256  # SM3 输出是256位
    Ha = b""
    for i in range((klen + v - 1) // v):  # 向上取整 (klen / v)
        hash_input = Z + ct.to_bytes(4, byteorder='big')
        Ha += SM3(hash_input)
        ct += 1
    return Ha[:klen // 8]  # 只取前 klen 位
 
# 判断是否为全0比特串
 
 
def is_all_zeros(bitstring):
    return all(b == 0 for b in bitstring)
 
 
# def SM3(message_bytes):
#     padded_message = pad_message(message_bytes)
#     V = IV.copy()
#     for i in range(len(padded_message) // 64):
#         B = padded_message[i*64:(i+1)*64]
#         V = SM3_CF(V, B, i)
#         hex_string1 = binascii.hexlify(B).decode()
#         formatted_hex_string1 = re.sub(r'(.{8})', r'\1 ', hex_string1)
#         print(f"Extended Message at Step {i+1}: {formatted_hex_string1}")
 
#     result = ''.join('{:08x}'.format(v) for v in V)
#     result_bytes = bytes.fromhex(result)
#     return result_bytes
def SM3(message_bytes):
    # ascii_values = string_to_ascii(message)
    # message_bytes = bytes(ascii_values)
    padded_message = pad_message(message_bytes)
    result = ''
    for i in IV:
        result += '{:08x}'.format(i)
    V = IV.copy()
    for i in range(len(padded_message) // 64):
        B = padded_message[i*64:(i+1)*64]
        V = SM3_CF(V, B, i)
        hex_string1 = binascii.hexlify(B).decode()
 
        formatted_hex_string1 = re.sub(r'(.{8})', r'\1 ', hex_string1)
        # print(
        #     f"Extended Message at Step {i+1}: {formatted_hex_string1}")
        all = ''
        for iii in V:
            all += '{:08x}'.format(iii)
        result = or_16(all, result)
 
    return bytes.fromhex(result)
 
# 解密函数
 
 
def format_hex_with_spaces(hex_str):
    # 每8个字符插入一个空格
    return ' '.join(hex_str[i:i+8] for i in range(0, len(hex_str), 8))
 
 
def dec(C, d, a, p, mul, KDF, is_all_zeros, sm3_hash):
    while 1:
        # 字节少2倍
        C1 = C[:64]
        C2 = C[64:-32]
        C3 = C[-32:]
        C1_hex = C1.hex()
        C2_hex = C2.hex()
        C3_hex = C3.hex()
        # print(len(C1_hex))
        # print(len(C2_hex))
        # print(len(C3_hex))
        # 打印格式化后的16进制字符串
        print('\n')
        print(f"C1 = {format_hex_with_spaces(C1_hex)}")
        print(f"C2 = {format_hex_with_spaces(C2_hex)}")
        print(f"C3 = {format_hex_with_spaces(C3_hex)}")
        x1 = int.from_bytes(C1[:32], byteorder='big')
        y1 = int.from_bytes(C1[32:], byteorder='big')
 
        # 验证x1盒y1是否满足是椭圆曲线上的点，不满足则报错退出
        # if y1*y1 % p != (x1*x1*x1 + a*x1 + 1) % p:
        #     raise ValueError("解密失败，C1不是椭圆曲线上的点")
        # 验证C1
    # X1
    # 79377281213374464856521762040730683342015462370049267023955583132112479632217
    # Y1
    # 29695191565483698076752985044876734951232190773968731139074079091268997953382
        print(f"C1的x坐标为:{hex(x1)}\n")
        print(f"C1的y坐标为:{hex(y1)}\n")
        h = E_order // n
        xs, ys = mul(gx, gy, h, a, p)
        if xs == 0 and ys == 0:
            raise ValueError("解密失败，S是无穷远点")
        # 验证失败，回到第一步
        x2, y2 = mul(x1, y1, d, a, p)
        Z = x2.to_bytes(32, byteorder='big') + y2.to_bytes(32, byteorder='big')
        print(f"C2的x坐标为:{hex(x2)}\n")
        print(f"C2的y坐标为:{hex(y2)}\n")
    # Z
    # b'\xf0\xef\xa2c\x05{l:\xa5\xd73\xa9\x83N<\x06?\x1bu\xee:J\xd2N\x1fMm\x98\r\xc0\xb3\xb2\\\x07\x9a\x16\x04\x14\x17\xef\x11Q\xea\x1a3\x80\xa4\x0f\x8d\xa5p\x8e\xbf\x95\x7f\x1e\x00m\xe2\x13\xf7\xb9\xf6\xac'
    # b'\xf0\xef\xa2c\x05{l:\xa5\xd73\xa9\x83N<\x06?\x1bu\xee:J\xd2N\x1fMm\x98\r\xc0\xb3\xb2\\\x07\x9a\x16\x04\x14\x17\xef\x11Q\xea\x1a3\x80\xa4\x0f\x8d\xa5p\x8e\xbf\x95\x7f\x1e\x00m\xe2\x13\xf7\xb9\xf6\xac'
    # t
    # b'h\xd6\xf9\x11y\x00\x81\x04t\xec\x7f\x88BHE\xb7\xb0\xde\x88\xbd'
    # b'h\xd6\xf9\x11y\x00\x81\x04t\xec\x7f\x88BHE\xb7\xb0\xde\x88\xbd\xfe\xae\x06\xd4\xcd\xac&\x13\x13\xd3\x0c\xfe@\xa7_\xde\xe5q\xe8\x0c\xafx~\xad\xb0\xaa\xb0vpM\xf8_'
    # 密文
    # af7df2f5 03d2e3e5 cb91003b 0bf53e67 c177009c e2bee109 80e1bd95 5ae4bb59 41a6e200 015d8cb2 cf52b3f9 cb5894a8 15e86bae f995620e 6b12e20c 903d3766 21f6957e 0f65a167 06950ffc 2d2f37d6 c0b6f193 43d8573f d59a6167 f4b7cad3 7bcd9d7c cc77dfc6 e5a2c2d3 dfcae83c 61d28d5e
 
        klen = len(C2) * 8
        t = KDF(Z, klen)
 
        if is_all_zeros(t):
            raise ValueError("解密失败，t是全0比特串")
            # message, klen = string_to_binary_number(input_string)
            # M_bytes = int.to_bytes(message, klen // 8, byteorder='big')
            # # print(len(M_bytes))
            # C2 = bytes(a ^ b for a, b in zip(M_bytes, t))
            # C3_input = x2_bytes + M_bytes + y2_bytes
        else:
            print(f"t = {t.hex()}")
 
        M_bytes = bytes(a ^ b for a, b in zip(C2, t))
 
        C3_input = x2.to_bytes(32, byteorder='big') + \
            M_bytes + y2.to_bytes(32, byteorder='big')
        C3_calculated = sm3_hash(C3_input)
 
        if C3 != C3_calculated:
            raise ValueError("解密失败，C3验证不通过")
 
        return M_bytes.decode('utf-8')
 
 
# 密钥已知
d = 0xc9b4281d041bf8c51a1d275209f92eba127a439fc20b0b0cbf41d3afbaf17209
print(f"私钥d：{d}")
 
# 从键盘输入密文
C_hex_with_spaces = input("请输入密文的十六进制表示: ")
# C  c6bfd950 146bd8be c5264ecf 85db11e7 1526a4fd b574252a 0a777362 b4e025af 35d17811 629b9055 2be2df87 a36891ef 4363456b 1a8314c8 e5326381 fc53401b caed0e6f 5759d193 501c4f73 bed9bab6 9ff21838 bc46202d cfb92c23 d034f18c be88a9ef 90322711 953ccdac 590e3051 c29ce38b
 
# 移除输入中的空格
C_hex = C_hex_with_spaces.replace(" ", "")
 
# 将输入的十六进制转换为字节
C = bytes.fromhex(C_hex)
 
# 调用解密函数
try:
    decrypted_text = dec(C, d, a, p, mul, KDF, is_all_zeros, sm3_hash)
    print(f"解密后的明文: {decrypted_text}")
except ValueError as e:
    print(e)
