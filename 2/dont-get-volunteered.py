# in Bengali, a chessboard knight movement is called 2.5 moves
# because it takes 2 steps in one direction and 1 in perpendicular

# Since the chessboard is represented as 0-64 instead of (x,y) we
# need to check are we on the board or fell off the edges?
def ok_row(p, c):
    return p // 8 == c // 8

def ok_col(p, c):
    return c // 8 >= 0 and c // 8 <= 7

# there are 8 possible moves, each move is split into 2, and their
# offset to the previous positions. Also after each move we check
# if the move caused us to fall off the edge, and discard if so.
moves = [ ( -2, ok_row, -8, ok_col),
          ( -2, ok_row,  8, ok_col),
          (-16, ok_col, -1, ok_row),
          (-16, ok_col,  1, ok_row),
          (  2, ok_row, -8, ok_col),
          (  2, ok_row,  8, ok_col),
          ( 16, ok_col, -1, ok_row),
          ( 16, ok_col,  1, ok_row),
]

# generate the legal moves given a position
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

# the solution involves a BFS search for dest from the src: visit
# all unseen cells from the start, append <moves, depth++> to queue,
# since a Knight can tour a board we're sure we'll hit the dest
# sooner or later. 
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


# print(solution(0, 1))
# print(solution(19, 36))
# print(solution(56, 44))

