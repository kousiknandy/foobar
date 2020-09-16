# we'll implement Polya Enumeration theorem as computed in https://franklinvp.github.io/2020-06-05-PolyaFooBar/

# Too many computations of small factorials and gcd needs to be done so let's use some pre-computed tables
# the table sizes will be max(w,h), and as per given constraints 12 should be enough (we keep some margins)
factorial_table = [
    1,
    1,
    2,
    6,
    24,
    120,
    720,
    5040,
    40320,
    362880,
    3628800,
    39916800,
    479001600,
    6227020800,
    87178291200,
    1307674368000,
    20922789888000,
    355687428096000,
    6402373705728000,
    121645100408832000,
    2432902008176640000,
    51090942171709440000,
    1124000727777607680000,
    25852016738884976640000,
    620448401733239439360000,
    15511210043330985984000000,
]

def factorial(num):
    if num < len(factorial_table):
        return factorial_table[num]
    return num * factorial(num-1)

gcd_table = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] ,
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2] ,
    [1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3] ,
    [1, 2, 1, 4, 1, 2, 1, 4, 1, 2, 1, 4, 1, 2, 1, 4, 1, 2, 1, 4, 1, 2, 1, 4, 1, 2, 1, 4, 1, 2] ,
    [1, 1, 1, 1, 5, 1, 1, 1, 1, 5, 1, 1, 1, 1, 5, 1, 1, 1, 1, 5, 1, 1, 1, 1, 5, 1, 1, 1, 1, 5] ,
    [1, 2, 3, 2, 1, 6, 1, 2, 3, 2, 1, 6, 1, 2, 3, 2, 1, 6, 1, 2, 3, 2, 1, 6, 1, 2, 3, 2, 1, 6] ,
    [1, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 1, 1, 7, 1, 1] ,
    [1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2] ,
    [1, 1, 3, 1, 1, 3, 1, 1, 9, 1, 1, 3, 1, 1, 3, 1, 1, 9, 1, 1, 3, 1, 1, 3, 1, 1, 9, 1, 1, 3] ,
    [1, 2, 1, 2, 5, 2, 1, 2, 1, 10, 1, 2, 1, 2, 5, 2, 1, 2, 1, 10, 1, 2, 1, 2, 5, 2, 1, 2, 1, 10] ,
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 1, 1, 1, 1, 1, 1, 1, 1] ,
    [1, 2, 3, 4, 1, 6, 1, 4, 3, 2, 1, 12, 1, 2, 3, 4, 1, 6, 1, 4, 3, 2, 1, 12, 1, 2, 3, 4, 1, 6] ,
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13, 1, 1, 1, 1] ,
    [1, 2, 1, 2, 1, 2, 7, 2, 1, 2, 1, 2, 1, 14, 1, 2, 1, 2, 1, 2, 7, 2, 1, 2, 1, 2, 1, 14, 1, 2] ,
    [1, 1, 3, 1, 5, 3, 1, 1, 3, 5, 1, 3, 1, 1, 15, 1, 1, 3, 1, 5, 3, 1, 1, 3, 5, 1, 3, 1, 1, 15] ,
    [1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 16, 1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2] ,
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 17, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] ,
    [1, 2, 3, 2, 1, 6, 1, 2, 9, 2, 1, 6, 1, 2, 3, 2, 1, 18, 1, 2, 3, 2, 1, 6, 1, 2, 9, 2, 1, 6] ,
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 19, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] ,
    [1, 2, 1, 4, 5, 2, 1, 4, 1, 10, 1, 4, 1, 2, 5, 4, 1, 2, 1, 20, 1, 2, 1, 4, 5, 2, 1, 4, 1, 10] ,
    [1, 1, 3, 1, 1, 3, 7, 1, 3, 1, 1, 3, 1, 7, 3, 1, 1, 3, 1, 1, 21, 1, 1, 3, 1, 1, 3, 7, 1, 3] ,
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 11, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 22, 1, 2, 1, 2, 1, 2, 1, 2] ,
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 23, 1, 1, 1, 1, 1, 1, 1] ,
    [1, 2, 3, 4, 1, 6, 1, 8, 3, 2, 1, 12, 1, 2, 3, 8, 1, 6, 1, 4, 3, 2, 1, 24, 1, 2, 3, 4, 1, 6] ,
    [1, 1, 1, 1, 5, 1, 1, 1, 1, 5, 1, 1, 1, 1, 5, 1, 1, 1, 1, 5, 1, 1, 1, 1, 25, 1, 1, 1, 1, 5] ,
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 13, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 26, 1, 2, 1, 2] ,
    [1, 1, 3, 1, 1, 3, 1, 1, 9, 1, 1, 3, 1, 1, 3, 1, 1, 9, 1, 1, 3, 1, 1, 3, 1, 1, 27, 1, 1, 3] ,
    [1, 2, 1, 4, 1, 2, 7, 4, 1, 2, 1, 4, 1, 14, 1, 4, 1, 2, 1, 4, 7, 2, 1, 4, 1, 2, 1, 28, 1, 2] ,
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 29, 1] ,
    [1, 2, 3, 2, 5, 6, 1, 2, 3, 10, 1, 6, 1, 2, 15, 2, 1, 6, 1, 10, 3, 2, 1, 6, 5, 2, 3, 2, 1, 30] ,
]

def gcd(a, b):
    try:
        return gcd_table(a-1, b-1)
    except:
        while b:
            a, b = b, a % b
        return a

# integer partition as implemented by https://www.ics.uci.edu/~eppstein/PADS/IntegerPartitions.py
# The mckay is iterative but lex_partitions looks elegant and understandable. 
def lex_partitions(n):
    """Similar to revlex_partitions, but in lexicographic order."""
    if n == 0:
        yield []
    if n <= 0:
        return
    for p in lex_partitions(n-1):
        p.append(1)
        yield p
        p.pop()
        if len(p) == 1 or (len(p) > 1 and p[-1] < p[-2]):
            p[-1] += 1
            yield p
            p[-1] -= 1

# given a list, count the elements: [1,1,1,2,2,4,4,4,4,5] => [(1,3),(2,2),(4,4),(5,1)]
def list2pow2(l):
    l = sorted(l)
    res = []
    c = p = l[0]
    count = 0
    for x in l:
        if x == c:
            count += 1
        else:
            res.append((c, count))
            c = x
            count = 1
    res.append((c,count))
    return res

#count_cycle computes number of cycles are availble for the given n and pows sticker
def count_cycle(n, pows):
    coff = factorial(n)
    for v, p in pows:
        coff //= (v ** p) * factorial(p)
    return coff


def solution(w, h, s):
    grids = 0
    for c_w in lex_partitions(w):
        for c_h in lex_partitions(h):
            mult = count_cycle(w, list2pow2(c_w)) * count_cycle(h, list2pow2(c_h))
            gcdsum = 0
            for i in c_w:
                for j in c_h:
                    gcdsum += gcd(i, j)
            grids += mult * (s ** gcdsum)
    grids //= factorial(w) * factorial(h)
    return str(grids)


print(solution(2,2,2))
print(solution(2,3,4))
