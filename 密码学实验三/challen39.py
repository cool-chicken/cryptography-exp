def gcd(a,b):
    if b ==0:
        return a
    else: 
        return gcd(b,a%b)
    
def invmod(a,b):
    for i in range(b):
        if (a*i)%b == 1:
            return i
e = 3     
def RSA_e(p,q,m):
    n = p*q
    et = (p-1)*(q-1)
    if gcd(e,et) != 1:
        print("e与et不互质")
        return
    c = pow(m,e,n)
    print("加密后的信息为:{}\n公钥[e,n]:[{},{}]".format(c,e,n))

def RSA_d(p,q,c):
    n = p*q
    et = (p-1)*(q-1)
    d = invmod(e,et)
    if d is None:
        print("没有找到模逆")
        return
    m = pow(c,d,n)
    print("加密后的信息为:{}\n私钥[d,n]:[{},{}]".format(m,d,n))

if __name__ == "__main__":
    RSA_e(29,17,42)
    RSA_d(29,17,138)
# 加密后的信息为:138
# 公钥[e,n]:[3,493]
# 加密后的信息为:42
# 私钥[d,n]:[299,493]
    RSA_e(1019,2027,42)
    RSA_d(1019,2027,74088)
# 加密后的信息为:74088
# 公钥[e,n]:[3,2065513]
# 加密后的信息为:42
# 私钥[d,n]:[1374979,2065513]
