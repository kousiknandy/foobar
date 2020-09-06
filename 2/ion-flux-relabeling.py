# in a post-order traversal, the left subtree has the complete
# sequence of numbers, whereas the right subtree is complicated
# but the pattern to notice is all the elements in leftmost
# path are 2^n-1, and the node to their right is 2^n-2

def drop_msb(n):
    b = 1
    while 2**b <= n:
        b += 1
    return n - 2**(b-1)

# print(drop_msb(100))
# print(drop_msb(10))
# print(drop_msb(64))
# print(drop_msb(1024))
# print(drop_msb(1))

def leftmost(n):  # 2^n-1
    return (n & (n+1)) == 0

def right_leftmost(n):  # 2^n-2
    return ((n+1) & (n+2)) == 0

# given any arbitrary node the plan is to map it to the leftmost
# node or right node of the leftmost node. Then the parent of the
# node is either 2n+1 or n+1 respectively. However when we map a
# node to the left side, we need to compute treesize we lost
# because of mapping from right to the left side, those to be
# accumulated and added back to the final answer ...
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
    

# print(parent_po(10))
# print(parent_po(14))
# print(parent_po(5))
# print(parent_po(8))
# print(parent_po(19))
# print(parent_po(14))
# print(parent_po(28))
# print(parent_po(7))

# print(solution(3, [7,3,5,1]))
# print(solution(5, [19,14,28]))
