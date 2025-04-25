import random


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def findModReverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def divresult(m):
    Mj = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    for i in range(0, len(m)):
        for j in range(0, len(m)):
            if i == j:
                Mj[i] = Mj[i] * 1
            else:
                Mj[i] = Mj[i] * m[j]
    return Mj


def fun(d, t):
    N = 1
    M = 1
    for i in range(0, t):
        N = N * d[i]
    for i in range(len(d) - t + 1, len(d)):
        M = M * d[i]
    return N, M


def findk(d, k):
    k1 = [1, 1, 1, 1, 1, 1, 1]
    for i in range(0, len(d)):
        k1[i] = k % d[i]
    k1 = k1[0:len(d)]
    return k1


def ChineseSurplus(k, d, t):
    m = d[0:t]
    a = k[0:t]
    flag = 1

    m1 = 1
    for i in range(0, len(m)):
        m1 = m1 * m[i]

    Mj = divresult(m)
    Mj1 = [0, 0, 0, 0, 0, 0, 0]

    for i in range(0, len(m)):
        Mj1[i] = findModReverse(Mj[i], m[i])
    x = 0

    for i in range(0, len(m)):
        x = x + Mj[i] * Mj1[i] * a[i]

    result = x % m1
    return result


def judge_d(m, num):
    flag = 1
    for i in range(0, num):
        for j in range(0, num):
            if (gcd(m[i], m[j]) != 1) & (i != j):
                flag = 0
                break
    return flag


def find_d():
    d = [1, 1, 1, 1, 1]
    temp = random.randint(pow(10, 167), pow(10, 168))
    d[0] = temp
    i = 1
    while i < 5:
        temp = random.randint(pow(10, 167), pow(10, 168))
        d[i] = temp
        if judge_d(d, i + 1) == 1:
            i = i + 1
    return d


k = int(input("请输入秘密k:"))
d = find_d()
print("数组d为:")
print(d)
N, M = fun(d, 3)
print("N的值为：")
print(N)
print("M的值为：")
print(M)
k1 = findk(d, k)
result = ChineseSurplus(k1, d, 3)
print("最后恢复的明文为:")
print(result)
if result == k:
    print("恢复正确！")
else:
    print("恢复错误！")
