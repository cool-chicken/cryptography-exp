import random

def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
    
def exponentiation(a, b, n):
    c = 1
    d = a % n
    while b:
        if b % 2 == 1:
            c = c * d % n
        d = d * d % n
        b //= 2
    return c
# print(exponentiation(312,13,667))

def fermat(m,k):
    if m % 2 == 0 or m < 3:
        print("m必须是大于等于3的奇数")
        return False
    kk = k
    while k:
        a = random.randint(2, m - 2)
        g = gcd(a, m)
        if g != 1:
            print(f"m是合数")
            break
        else:
            r = exponentiation(a, m - 1, m)
            if r != 1:
                print(f"m是合数")
                break
        k -= 1
    if k == 0:
        print(f"m是素数的概率为{(1 - 1 / 2 ** kk) * 100}%")

if __name__ == "__main__":
    f = open("4.txt", "r")
    m = int(f.readline())
    f.close()
    k = 10
    fermat(m, k)
