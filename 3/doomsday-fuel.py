# we insist that we don't import anything and create the apple-pie from scratch

# basic math stuffs

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def lcm(x, y):
    return (x * y) // gcd(x, y)

# working in integer domain so multiplication
# and division are two distinct operations

def scalar_mult(m, n, mult=True):
    for i in range(len(m)):
        for j in range(len(m[0])):
            if mult:
                m[i][j] *= n
            else:
                m[i][j] /= n

# scale up or down all the matrices we have

def scale_mat(n, *m):
    for x in m:
        scalar_mult(x, n)

def divide_mat(n, *m):
    for x in m:
        scalar_mult(x, n, False)

# unnecessary optimization to scale down in
# the middle of things but let it remain

def scale_down(g_d, *m):
    n = []
    for x in m:
        for i in range(len(x)):
            for j in range(len(x[0])):
                if x[i][j]:
                    n.append(x[i][j])
    f = reduce(gcd, n)
    if f and g_d % f == 0:
        divide_mat(f, *m)
    return g_d / f

# the probability computation 

def normalize(m):
    row_sum = []
    for i in range(len(m)):
        denominator = sum(m[i])
        if denominator:
            row_sum.append(denominator)
    g_denominator = reduce(lcm, row_sum) if row_sum else 1
    scalar_mult(m, g_denominator)
    k = 0
    for i in range(len(m)):
        denominator = sum(m[i])
        if denominator:
            for j in range(len(m)):
                m[i][j] //= row_sum[k]
            k += 1
    return g_denominator

def is_terminal(r):
    return all(map(lambda x: x == 0, r))

# separate out terminal and non-terminal states

def q_r(m):
    q = []
    r = []
    for i in range(len(m)):
        if is_terminal(m[i]):
            r.append(i)
        else:
            q.append(i)
    return q, r

# collect the matrices under each terminal / non-terminal states

def qr_matrix(m, q, r):
    q_m = [[None for _1 in range(len(q))] for _2 in range(len(q))]
    r_m = [[None for _1 in range(len(r))] for _2 in range(len(q))]
    # print m, q, r
    for i in range(len(q)):
        for j in range(len(q)):
            q_m[i][j] = m[q[i]][q[j]]
    for i in range(len(q)):
        for j in range(len(r)):
            r_m[i][j] = m[q[i]][r[j]]
    return q_m, r_m

# the identity matrix - denominators are diagonal elements

def i_matrix(l, g_d = 1):
    m = [[None for _1 in range(l)] for _2 in range(l)]
    for i in range(l):
        for j in range(l):
            m[i][j] = g_d if i == j else 0
    return m

# ugh -- implement matrix operations from scratch ...

def i_minus_q(q, g_d):
    for i in range(len(q)):
        for j in range(len(q)):
            if i == j:
                q[i][j] = g_d - q[i][j]
            else:
                q[i][j] = -q[i][j]

def mat_mult(m1, m2):
    m = [[0 for _1 in range(len(m2[0]))] for _2 in range(len(m1))]
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m1[0])):
                m[i][j] += m1[i][k] * m2[k][j]
    return m

# ... but with a twist. We're limited to integer arithmatic, so
# every operation ensures we can do it in the integer domain. If
# division is necessary we scale up the global denominator to
# ensure the division goes it full. So if want to divide a number
# n by d, we scale down the system by multiplying n by a factor
# so that it can be lcm(n, d), and adjusting the global denominator
# by the same factor

# this follows the Gauss-Jordan process, but implemented in a hurry

def matx_invert(qm, im, g_d, rm):
    for row in range(len(qm)):
        if qm[row][row] == 0:
            qm[row], qm[row+1] = qm[row+1], qm[row]
            im[row], im[row+1] = im[row+1], im[row]            
        r2, r3 = g_d, qm[row][row]
        new_mult = lcm(r2, r3) / r2
        if r3 == 0:
            continue
        g_d *= new_mult
        scale_mat(new_mult, qm, rm, im)
        for col in range(len(qm)):
            qm[row][col] = (qm[row][col] * r2) / r3
            im[row][col] = (im[row][col] * r2) / r3
        #print "^v", g_d, qm, rm, im
        g_d = scale_down(g_d, qm, rm, im)
        for r4 in range(len(qm)):
            if r4 == row:
                continue
            r2, r3 = qm[r4][row], qm[row][row]
            if r2 == 0:
                continue
            new_mult = lcm(r2, r3) / r2
            g_d *= new_mult
            scale_mat(new_mult, qm, rm, im)
            for col in range(len(qm)):
                qm[r4][col] = qm[r4][col] - (qm[row][col] * r2 / r3)
                im[r4][col] = im[r4][col] - (im[row][col] * r2 / r3)
            #print "<>", g_d, qm, rm, im
            g_d = scale_down(g_d, qm, rm, im)
    return g_d

# the solution follows the method as per Markov's absorbing chains
# easiest to understand following ivanseed's steps

def solution(m):
    if len(m) <= 1:
        return [1, 1]
    
    g_d = normalize(m)
    q, r = q_r(m)
    qm, rm = qr_matrix(m, q, r)
    # print "0) ", g_d, q, qm, r, rm
    
    i_minus_q(qm, g_d)
    im = i_matrix(len(qm), g_d)
    # print "1) ", g_d, qm, im, rm
    g_d = matx_invert(qm, im, g_d, rm)
    f = im
    # print "2) ", g_d, qm, im, rm
    
    fr = mat_mult(f, rm)
    # print "3) ", g_d, fr
    d2 = reduce(gcd, fr[0])
    sol = map(lambda x: x / d2, fr[0])
    sol.append(g_d * g_d / d2)
    return sol


# # _qm = [[4, 5, 1], [3, 9, 4], [1, 3, 0]]
# # _im = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
# # _rm = [[0]]
# # _g_d= matx_invert(_qm, _im, 1, _rm)
# # print _g_d, _im
# # exit()

# print solution([[0]])

# print solution([
#   [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
#   [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
#   [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
#   [0,0,0,0,0,0],  # s3 is terminal
#   [0,0,0,0,0,0],  # s4 is terminal
#   [0,0,0,0,0,0],  # s5 is terminal
# ])

# print solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
# print solution([[1, 2, 3, 0, 0, 0], [4, 5, 6, 0, 0, 0], [7, 8, 9, 1, 0, 0], [0, 0, 0, 0, 1, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])

# print solution( [
#   [0,1,0,0,0,1,2,3,2,1],  
#   [4,0,0,3,2,0,9,2,2,3],  
#   [1,0,0,1,0,0,0,0,0,0],
#   [0,1,0,0,1,0,0,0,0,0],
#   [0,1,0,0,0,0,0,2,0,0],
#   [0,0,0,0,0,0,0,0,0,0],
#   [0,0,0,0,3,0,0,0,0,0],
#   [0,0,4,0,0,3,0,0,0,0],
#   [0,0,0,0,0,10,2,0,0,0],
#   [0,0,0,0,0,0,0,0,0,0],
# ])

# print solution([
#         [0, 86, 61, 189, 0, 18, 12, 33, 66, 39],
#         [0, 0, 2, 0, 0, 1, 0, 0, 0, 0],
#         [15, 187, 0, 0, 18, 23, 0, 0, 0, 0],
#         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     ])

# print solution([
#         [0, 0, 0, 0, 3, 5, 0, 0, 0, 2],
#         [0, 0, 4, 0, 0, 0, 1, 0, 0, 0],
#         [0, 0, 0, 4, 4, 0, 0, 0, 1, 1],
#         [13, 0, 0, 0, 0, 0, 2, 0, 0, 0],
#         [0, 1, 8, 7, 0, 0, 0, 1, 3, 0],
#         [1, 7, 0, 0, 0, 0, 0, 2, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ])


# assert (
#     solution([
#         [0, 2, 1, 0, 0],
#         [0, 0, 0, 3, 4],
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0]
#     ]) == [7, 6, 8, 21]
# )
 
# assert (
#     solution([
#         [0, 1, 0, 0, 0, 1],
#         [4, 0, 0, 3, 2, 0],
#         [0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0]
#     ]) == [0, 3, 2, 9, 14]
# )
 
# assert (
#     solution([
#         [1, 2, 3, 0, 0, 0],
#         [4, 5, 6, 0, 0, 0],
#         [7, 8, 9, 1, 0, 0],
#         [0, 0, 0, 0, 1, 2],
#         [0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0]
#     ]) == [1, 2, 3]
# )
# assert (
#     solution([
#         [0]
#     ]) == [1, 1]
# )
 
# assert (
#     solution([
#         [0, 0, 12, 0, 15, 0, 0, 0, 1, 8],
#         [0, 0, 60, 0, 0, 7, 13, 0, 0, 0],
#         [0, 15, 0, 8, 7, 0, 0, 1, 9, 0],
#         [23, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#         [37, 35, 0, 0, 0, 0, 3, 21, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     ]) == [1, 2, 3, 4, 5, 15]
# )
 
# assert (
#     solution([
#         [0, 7, 0, 17, 0, 1, 0, 5, 0, 2],
#         [0, 0, 29, 0, 28, 0, 3, 0, 16, 0],
#         [0, 3, 0, 0, 0, 1, 0, 0, 0, 0],
#         [48, 0, 3, 0, 0, 0, 17, 0, 0, 0],
#         [0, 6, 0, 0, 0, 1, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     ]) == [4, 5, 5, 4, 2, 20]
# )
 
# assert (
#     solution([
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     ]) == [1, 1, 1, 1, 1, 5]
# )
 
# assert (
#     solution([
#         [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     ]) == [2, 1, 1, 1, 1, 6]
# )
 
# assert (
#     solution([
#         [0, 86, 61, 189, 0, 18, 12, 33, 66, 39],
#         [0, 0, 2, 0, 0, 1, 0, 0, 0, 0],
#         [15, 187, 0, 0, 18, 23, 0, 0, 0, 0],
#         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     ]) == [6, 44, 4, 11, 22, 13, 100]
# )
 
# assert (
#     solution([
#         [0, 0, 0, 0, 3, 5, 0, 0, 0, 2],
#         [0, 0, 4, 0, 0, 0, 1, 0, 0, 0],
#         [0, 0, 0, 4, 4, 0, 0, 0, 1, 1],
#         [13, 0, 0, 0, 0, 0, 2, 0, 0, 0],
#         [0, 1, 8, 7, 0, 0, 0, 1, 3, 0],
#         [1, 7, 0, 0, 0, 0, 0, 2, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     ]) == [1, 1, 1, 2, 5])
