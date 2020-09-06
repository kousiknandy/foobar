# if we build stairs from the bottom then at every step we need to
# consume at least steps number of bricks. Then the problem reduces
# to bricks-steps bricks left, and one less steps to build. Also
# count the number of ways the Also like Fibonacchi we compute the
# lesser results multiple time so a memo can catch them and speed
# up.
def steps(bricks, start=1):
    global mem
    if bricks == 0:
        return 1
    if bricks < start:
        return 0
    if mem[start][bricks]:
        return mem[start][bricks]
    ways = steps(bricks - start, start + 1) + steps(bricks, start + 1)
    mem[start][bricks] = ways
    return ways

def solution(n):
    global mem
    mem = [[None for _1 in range(n+2)] for _2 in range(n+2)]
    return steps(n) - 1


print(solution(3))
print(solution(25))
print(solution(200))
print(solution(500))

