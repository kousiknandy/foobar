def ok_row(p, c):
    return p // 8 == c // 8

def ok_col(p, c):
    return c // 8 >= 0 and c // 8 <= 7

moves = [ ( -2, ok_row, -8, ok_col),
          ( -2, ok_row,  8, ok_col),
          (-16, ok_col, -1, ok_row),
          (-16, ok_col,  1, ok_row),
          (  2, ok_row, -8, ok_col),
          (  2, ok_row,  8, ok_col),
          ( 16, ok_col, -1, ok_row),
          ( 16, ok_col,  1, ok_row),
]

def next_move(c):
    for m in moves:
        p = c
        if m[1](p, p + m[0]):
            p += m[0]
        else:
            continue
        if m[3](p, p + m[2]):
            p += m[2]
        else:
            continue
        yield p

#for p in [0, 4, 7, 27, 47, 56, 63]:
#    print(p, list(next_move(p)))

visited = [False] * 64

def solution(src, dest):
    bfsqueue = [(src, 0)]
    while len(bfsqueue) > 0:
        nextsq = bfsqueue.pop(0)
        if nextsq[0] == dest:
            return nextsq[1]
        if visited[nextsq[0]]:
            continue
        else:
            visited[nextsq[0]] = True
        possible_moves = list(next_move(nextsq[0]))
        possible_moves = map(lambda x: (x, nextsq[1] + 1), possible_moves)
        # print(nextsq, possible_moves)
        bfsqueue.extend(possible_moves)


print(solution(0, 1))
print(solution(19, 36))
print(solution(56, 44))

