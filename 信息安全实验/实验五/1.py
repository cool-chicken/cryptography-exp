import math
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3

a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498

b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A

gx= 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D

gy= 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

k = 0x4C62EEFD6ECFC2B95B92FD6C3D9575148AFA17425546D49018E5388D49DD7B4F


# def egcd(a, b):
#     if a == 0:
#         return b, 0, 1
#     else:
#         g, x, y = egcd(b % a, a)
#         return g, y - (b // a) * x, x
def ext_gcd(a, b):  
    
    if b == 0:          
        return 1, 0, a     
    else:         
        x, y, gcd = ext_gcd(b, a % b) 
        x, y = y, (x - (a // b) * y)          
        return x, y, gcd

# def invmod(a, m):
#     g, x, y = egcd(a, m)
#     if g == 1:
#         return x % m
#     else:
#         return None

def add(x1, y1, x2, y2):
    if x1 == math.inf:
        return x2,y2
    if x2 == math.inf:
        return x1,y1
    if x1 == x2 and y1 == -y2:
        return math.inf,math.inf
    if x1 == x2 and y1 == y2:
        l = (3 * x1 * x1 + a) * ext_gcd(2 * y1, p)[0] % p
    else:
        l = (y2 - y1) * ext_gcd(x2-x1,p)[0] % p
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


# def poly_points(k, point:list)->list:
#     k = bin(k)[2:]
#     Q = [math.inf, math.inf]
#     for i in k:
#         Q = point_add(Q, Q)
#         if int(i) == 1:
#             Q = point_add(Q, point)
#     return Q

# def point_add(P:list, Q:list)->list:
#     if P[0]==math.inf:
#         return Q
#     if Q[0]==math.inf:
#         return P
#     if P[0]==Q[0] and P[1]==Q[1]*(-1):
#         return [math.inf,math.inf]
#     if P==Q:
#         lam_1 = pow(3*P[0]*P[0] + a, 1, p)
#         lam_2 = 2*P[1]
#         lam_2 = ext_gcd(lam_2, p)[0] % p
#         lam = lam_1 * lam_2 % p
#     else:
#         lam_1 = Q[1] - P[1]
#         lam_2 = Q[0] - P[0]
#         lam_2 = ext_gcd(lam_2, p)[0] % p
#         lam = lam_1 * lam_2 % p
#     R = [0,0]
#     R[0] = (lam*lam - P[0] - Q[0]) % p
#     R[1] = (lam*(P[0]-R[0])-P[1]) % p
#     return R

# x1, x2 = poly_points(k,[gx,gy])
x1,x2 = mul(gx,gy,k)
print(hex(x1))
print(hex(x2))
