# Compute integer square root by Newton's method:
# we aysmptotically approach the answer from below
# using integer division instead over and under
# shooting the exact solution
def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

# keep subtracting perfect squares from n till 0
def prev_square(n):
    while n:
        p = isqrt(n)
        n -= p*p
        yield p*p

def solution(area):
    return list(prev_square(area))


# print(solution(12))
# print(solution(15324))
# print(solution(100))
# print(solution(90))
# print(solution(40))
# print(solution(0))


