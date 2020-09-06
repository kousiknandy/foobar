def number(start = 1):
    while True:
        yield start
        start += 1

def post_order(d, s):
    if d > 1:
        post_order(d-1, s)
        post_order(d-1, s)
    r = next(s)
    print("{:3d} {:016b}".format(r, r), d)
    
def printpo(height):
    s = number(1)
    post_order(height, s)

#printpo(3)
#print("\n")
#printpo(4)
#print("\n")
#printpo(10)

height = 5
for h in range(height, 0, -1):
    for i in range(1,2**(height-h)+1):
        print " "*(2**h-1), (2**h-1)*i+(i-1)//2+(i-1)//4+(i-1)//8,
    print

def drop_msb(n):
    b = 1
    while 2**b <= n:
        b += 1
    return n - 2**(b-1)

print(drop_msb(100))
print(drop_msb(10))
print(drop_msb(64))
print(drop_msb(1024))
print(drop_msb(1))

def leftmost(n):  # 2^n-1
    return (n & (n+1)) == 0

def right_leftmost(n):  # 2^n-2
    return ((n+1) & (n+2)) == 0

def parent_po(n):
    p = c = n
    treesz = 0
    while not (leftmost(c) or right_leftmost(c)):
        # print c, treesz, " ",
        c = drop_msb(c)
        c += 1
        treesz += p - c
        p = c
    if leftmost(c):
        c *= 2
    c += 1
    c += treesz
    return c

def solution(h, q):
    sol = []
    for n in q:
        if n >= 2**h - 1:
            sol.append(-1)
        else:
            sol.append(parent_po(n))
    return sol

    

print(parent_po(10))
print(parent_po(14))
print(parent_po(5))
print(parent_po(8))
print(parent_po(19))
print(parent_po(14))
print(parent_po(28))
print(parent_po(7))

print(solution(3, [7,3,5,1]))
print(solution(5, [19,14,28]))
