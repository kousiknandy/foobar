def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def infinite_loop(x, y):
    if x == y:  # give up
        return False
    
    if (x + y) % 2: # odd sum, can't reach equality
        return True
    
    g = gcd(x, y) # same fate when normalized
    if g > 1:
        return infinite_loop(x/g, y/g)

    if x > y:  
        x, y = y, x
    # hope we don't dig all the way down
    return infinite_loop(2 * x, y - x)    

class Graph:
    def __init__(self, size):
        self.graph = [[] for _ in range(size)] 
        self.maxnodes = size

    def add_edge(self, src, dst):
        self.graph[src].append(dst)
        self.graph[dst].append(src)

    # it is like a bipartite matching but undirected,
    # also source and destination comes from same set
    def bpm_match(self, u, matches, visited):
        for v in range(self.maxnodes):
            # weed out same, visited or unmatchable nodes
            if u == v:
                continue
            if v in visited:
                continue
            if v not in self.graph[u]:
                continue
            # funny part of the algorithm is its resemblence with cuckoo hashing
            visited.append(v)
            if matches[v] == None or self.bpm_match(matches[v], matches, visited):
                matches[v] = u
                matches[u] = v
                return True
        return False

    # the max number of pairs that can be made out of this graph
    def max_cover(self):
        matches = [None] * self.maxnodes
        pairs = 0
        for g in range(self.maxnodes): 
            if matches[g] is not None:
                continue
            visited = [g]
            if self.bpm_match(g, matches, visited):
                pairs += 1
        return pairs

def solution(banana_list):
    guardcount = len(banana_list)
    if guardcount in [0, 1]:
        return guardcount
    # we create a graph where 2 guards with potential loops are
    # represented by an edge
    g = Graph(guardcount)
    banana_list = sorted(banana_list)
    for i in range(guardcount):
        for j in range(i, guardcount):
            if infinite_loop(banana_list[i], banana_list[j]):
                g.add_edge(i, j)
    # find number of edges that covers maximum vertices with
    # no edge adjacency
    pairs = g.max_cover() 
    return guardcount - 2 * pairs


# print solution([1, 1]) #2
# print solution([1, 7, 3, 21, 13, 19]) #0
# #exit()
# print solution([1]) #1
# print solution([1, 7, 1, 1]) #4
    
# print solution([1,4]) #0
# print solution([(2**30)-1, 2,1,6]) #0
# print solution([3,5,1,4]) #0
# print solution([1,1,2,5]) #0

# print solution([3,5]) #2
# print solution([1,1]) #2
# print solution([9,15]) #2
# print solution([1,1,1,6]) #2

# print solution([3, 3, 2, 6, 6]) #1
# print solution([1,7, 21]) #1
# print solution([0]) #1

