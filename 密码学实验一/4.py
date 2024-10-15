import hashlib
import itertools
import datetime
import sys

hash1 = "67ae1a64661ac8b4494666f58c4822408dd0a3e4"
str2 = [['Q', 'q'], ['W', 'w'], ['%', '5'], ['8', '('], ['=', '0'], ['I', 'i'], ['*', '+'], ['n', 'N']]

def sha_encrypt(string):
    sha = hashlib.sha1(string.encode())
    return sha.hexdigest()

starttime = datetime.datetime.now()

for combination in itertools.product(*str2):
    for perm in itertools.permutations(combination):
        candidate = "".join(perm)
        if sha_encrypt(candidate) == hash1:
            print("ans:", candidate)
            endtime = datetime.datetime.now()
            print("t:", (endtime - starttime).seconds, "seconds")
            sys.exit(0)

print("Password not found.")