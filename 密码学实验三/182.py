def gcd(a,b):
    if b ==0:
        return a
    else: 
        return gcd(b,a%b)


if __name__ == "__main__":
    p=1009
    q=3643
    phi = (p-1)*(q-1)
    e_state = {}
    for e in range(2,phi):
        if gcd(e,phi)==1:
            e_state[e]=(gcd(e-1,p-1)+1)*(gcd(e-1,q-1)+1)
    min_result = min(e_state.values())
    print(f"未加密信息的数目为最小值:",min_result)
    e_sum = sum([i for i in e_state if e_state[i] == min_result])
    print(f"e的和",e_sum)

# 未加密信息的数目为最小值: 9
# e的和 399788195976