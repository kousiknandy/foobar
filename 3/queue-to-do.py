# clever way or XORing all bits column-wise from 0 to n
# without computing any intermediate steps.  XOR of a 
# sequence depends on their reminder modulo 4
def xor_range(n):
    rem = n % 4
    if rem == 0:
        return n
    elif rem == 1:
        return 1
    elif rem == 2:
        return n+1
    return 0

# another clever way to make a slice [n1, n2] work, make
# xor_range(1-dest) then you can XOR with xor_range(1-src)
def xor_seq(start, len):
    x1 = xor_range(start-1) if start > 1 else 0
    x2 = xor_range(start+len-1)
    return x1 ^ x2

# print 17^18^19^20, xor_seq(17, 4)

def solution(start, length):
    cksum = 0
    for col in range(length):
        cksum = cksum ^ xor_seq(start + col * length, length - col)
    return cksum

# print(solution(0,3))
# print(solution(110,2))
# print(solution(17,4))
# print(solution(0,10))
