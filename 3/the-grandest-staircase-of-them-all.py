
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

