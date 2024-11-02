from Crypto.Util.number import getPrime

def invmod(a, b):
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x1, y1 = egcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return g, x, y

    g, x, y = egcd(a, b)
    if g != 1:
        raise ValueError('模逆不存在')
    else:
        return x % b

def generate_rsa_keys(bits=1024):
    p = getPrime(bits)
    q = getPrime(bits)
    e = 3  
    n = p * q
    et = (p-1)*(q-1)
    if et % e == 0:
        raise ValueError("e和et不互素，需要重新生成p和q")
    d = invmod(e,et)
    return (e,n),(d,n)

def RSA_e(m,public_key):
    e,n = public_key
    c = pow(m,e,n)
    return c

def RSA_d(c,private_key):
    d,n = private_key
    m = pow(c,d,n)
    return m

def main():
    public_key, private_key = generate_rsa_keys(bits=1024)
    print("Public Key:", public_key)
    print("Private Key:", private_key)
    #m = 42
    message = "Happy Holloween!"
    m = int.from_bytes(message.encode('utf-8'), byteorder='big')
    c = RSA_e(m,public_key)
    print("Encrypted message:",c)
    m = RSA_d(c,private_key)
    message = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big').decode('utf-8')
    print("Decrypted message:",message)
    # print("Decrypted message:",m)

main()
