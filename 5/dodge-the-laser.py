# We need to find a way to sum the Beatty sequence without
# computing all intermediary terms. So instead of n iterations
# we're looking for a formula that can reduce the n by a
# constant factor at every iteration ... so we can compute the
# result in O(log n) instead of O(n). We refer to the derivation
# at https://math.stackexchange.com/questions/2052179/how-to-find\
# -sum-i-1n-left-lfloor-i-sqrt2-right-rfloor-a001951-a-beatty-s

# Compute n * (sqrt(2) - 1)
# this is over precise, but thanks to python support of bignum
# note if you multiply 2 n-bit numbers, result is 2*n bits
def A097508():
    n = yield
    while True:
        n = yield long((n * 41421356237309504880168872420969807856967187537694807317667973799073247846210703885038753432764157273501384623091229702492483605585073721264412149709993583141322266592750559275579995050115278206057147)//(10**200))

# Compute n * (n + 1) / 2
# also known as triangular series (to confuse the innocents)
def A000217():
    n = yield
    while True:
        n = yield long((n * (n+1)) / 2)

# The recursive computation of Beatty sequence sum as
# S(n) = n*n' + n(n+1)/2 - n'(n'+1)/2 - S(n'), n' = n*(sqrt(2)-1)
# as derived in stackexchange answer. At every stage the input
# is divided by ~2.414, so we hit the answer in O(log n) steps.
# Since near the tail the sequence is compressed, it may make
# sense to build a pre-built lookup table of a rnage long enough
# to trap most of the input's reduction sequence, to avoid last
# couple of nesting regressions. In our case we just terminate
# by the base cases 0 and 1.
def A001951(n, a000217, a097508):
    if n in [0, 1]:
        return n
    # these following 3 numbers can be parallely computed
    n_prime = a097508.send(n)
    n_triangular = a000217.send(n)
    n_p_triangular = a000217.send(n_prime)
    return n * n_prime + n_triangular - n_p_triangular - \
        A001951(n_prime, a000217, a097508)

def solution(s):
    # setup our co-routines, actually since they are compute
    # only on our CPU, it is actually of no help, but if these
    # computations were sent off a GPU, we can parallely run 'em
    a000217 = A000217()
    a000217.send(None)
    a097508 = A097508()
    a097508.send(None)
    n = long(s)
    ans = A001951(n, a000217, a097508)
    return str(ans)

print(solution(5)) #19
print(solution(77)) #4208

    
