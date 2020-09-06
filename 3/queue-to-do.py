def xor_ap(start, jump, iters):
    x = 0
    #print "{:032b}".format(start), 
    for i in range(iters):
        x = x ^ (start + i * jump)
        print start + i * jump, 
    #print "{:032b}".format(x)
    print ":", x
    return x

# xor_ap(17, 4, 4)
# xor_ap(10, 5, 3)
# xor_ap(2, 4, 1)
# xor_ap(170, 40, 40)
# xor_ap(15, 8, 5)
# xor_ap(31, 7, 2)

# xor_ap(1, 1, 10)
# xor_ap(1, 1, 11)
# xor_ap(1, 1, 12)
# xor_ap(1, 1, 13)
# xor_ap(1, 1, 14)
# xor_ap(1, 1, 15)
# xor_ap(1, 1, 16)
# xor_ap(1, 1, 17)


def xor_range(n):
    rem = n % 4
    if rem == 0:
        return n
    elif rem == 1:
        return 1
    elif rem == 2:
        return n+1
    return 0

def xor_seq(start, len):
    x1 = xor_range(start-1) if start > 1 else 0
    x2 = xor_range(start+len-1)
    return x1 ^ x2

print 17^18^19^20, xor_seq(17, 4)

def solution(start, length):
    cksum = 0
    for col in range(length):
        cksum = cksum ^ xor_seq(start + col * length, length - col)
    return cksum

print(solution(0,3))
print(solution(110,2))
print(solution(17,4))
print(solution(0,10))
