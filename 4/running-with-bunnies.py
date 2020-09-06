# run all around to pick bunnies and drop them off to the bulkhead
# given a time limit (note that it is acceptable to temporarily
# exceed the time limit, because of negative edge cost can make it
# up later). The negative edge cost also allows for negative cycle
# allowing us to gain time as much needed (all bunnies are saved if
# there is a negative cycle)

class BunnyGraph:
    def __init__(self, mat):
        self.graph = mat
        self.shortest = None
        self.sz = len(mat[0]) 

    # textbook implementation of Floyd Warsall algorithm - calculate
    # all source shortest paths and detect negative cycle on the go.
    # Why I preferred this O(n^3) over Bellman Ford which is O(VE),
    # is given input seems to be a dense graph so running time is
    # same, but Floyd is simpler and negative cycle doesn't require
    # additional iteration
    def floyd_warsall(self):
        negative = False
        dist = map(lambda i : map(lambda j : j , i) , self.graph) 
        for k in range(self.sz):
            for i in range(self.sz):
                for j in range(self.sz):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
                    if dist[j][j] < 0:
                        negative = True
        self.shortest = dist
        return negative

    # Now we search brute forcing all the possible orders bunnies will
    # be picked up. First generate the powerset, and then generate all
    # permutations of them. Total number to search: Sum k!*(n k), k=0-n
    # which Wolfram Alpha computes to e*Gamma(n+1, 1). For 5 bunnies,
    # it is 326, but it is super fast growing function, 10 million for
    # 10 bunnies!
    
    # generate all possible powersets of bunnies -- from here we're
    # using generators all the way down, each layer adds a value to
    # previously yielded value
    def generate_powerset(self):
        len = self.sz - 2
        bunnies = [x for x in range(1, len+1)]
        masks = [1 << x for x in range(len)]
        for i in range(1 << len):
            yield [subset for mask, subset in zip(masks, bunnies) if i & mask]

    # implementation of Heap's algorithm for generating permutations:
    # keep the last element, generate other permulations, swap the
    # last with first or ith element (for even and odd i). The recursive
    # is easier to understand but we can keep auxiliarry array to loop
    def generate_bunnies(self):
        for buns in self.generate_powerset():
            l = len(buns)
            c = [0 for _ in range(l)]
            b = map(lambda i: i, buns)
            yield b[:]
            i = 0
            while i < l:
                if c[i] < i:
                    if i % 2 == 0:
                        b[0], b[i] = b[i], b[0]
                    else:
                        b[c[i]], b[i] = b[i], b[c[i]]
                    yield b[:]
                    c[i] += 1
                    i = 0
                else:
                    c[i] = 0
                    i += 1

    def generate_paths(self):
        bulkhead = self.sz - 1
        for buns in self.generate_bunnies():
            path = [0] + buns + [bulkhead]
            yield path

    # the key insight here is when we are visiting bunny to bunny we
    # take the cheapest path as pre-computed earlier by floyd_warsall
    # so if there is a need to visit a previously unvisited bunny, it
    # get automatically covered (but we still need to account for it)
    def path_time(self, path):
        if len(path) < 2:
            return 0
        cost = 0
        for i in range(len(path)-1):
            src = path[i]
            dst = path[i+1]
            cost += self.shortest[src][dst]
        return cost

    # Here we generate all bunny sequences that are possible to pick
    # by the deadline. Remember there maybe several with same length
    # we make the job of next step easier by sorting reverse on len()
    def gather_bunnies(self, times_limit):
        bunnies = []
        bulkhead = self.sz - 1
        for path in self.generate_paths():
            time_taken = self.path_time(path)
            if time_taken <= times_limit:
                buns = sorted(set(path))
                buns.remove(0)
                buns.remove(bulkhead)
                buns = frozenset(map(lambda x: x-1, buns))
                bunnies.append(buns)
        return sorted(set(bunnies), reverse=True, key=lambda x: len(x))

    # out of all solutions we need to pick the best set of bunnies,
    # first we keep the sets that has the max length (filter), then
    # make sure the bunny list sorted (map), and then pick the list
    # that is comprised of smaller bunny ids (reduce). The sequence
    # looks like a pseudo map reduce :-)
    def best_bunnies(self, times_limit):
        bunnies = self.gather_bunnies(times_limit)
        if not bunnies:
            return []
        max_buns = len(bunnies[0])
        bunnies = filter(lambda x: len(x) == max_buns, bunnies)
        bunnies = map(lambda x: sorted(list(x)), bunnies)
        bunnies = reduce(lambda x, y: x if cmp(x, y) < 0 else y, bunnies)
        return bunnies

def solution(times, times_limit):
    bunnygraph = BunnyGraph(times)
    if bunnygraph.sz < 3:
        return []
    if bunnygraph.floyd_warsall():
        # negative cycle means we can get unlimited time to save all
        return range(bunnygraph.sz - 2)
    # among all sequences that satisfy time limit, longest with least ids
    return bunnygraph.best_bunnies(times_limit)



# bunnies = [ [1, 2, 4], [1, 3, 4], [2, 3, 1], [3, 4]]
# max_buns = len(bunnies[0])
# print bunnies
# bunnies = filter(lambda x: len(x) == max_buns, bunnies)
# print bunnies
# bunnies = map(lambda x: sorted(list(x)), bunnies)
# print bunnies
# bunnies = reduce(lambda x, y: x if cmp(x, y) < 0 else y, bunnies)
# print bunnies
# exit()
    
# g = BunnyGraph([[0, 2, 2, 2, -1],
#            [9, 0, 2, 2, -1],
#            [9, 3, 0, 2, -1],
#            [9, 3, 2, 0, -1],
#            [9, 3, 2, 2, 0]]) # 1, [1,2]
# print g.gather_bunnies(1)
# print g.best_bunnies(1)

g = solution([[0,-1, 0, 9, 9, 9, 9, 9],  # Start
              [9, 0, 1, 9, 9, 9, 9, 9],  # 0
              [0, 9, 0, 0, 9, 9, 1, 1],  # 1
              [9, 9, 9, 0, 1, 9, 9, 9],  # 2
              [9, 9, 9, 9, 0,-1, 9, 9],  # 3 
              [9, 9, 0, 9, 9, 0, 9, 9],  # 4
              [9, 9,-1, 9, 9, 9, 0, 9],  # 5
              [9, 9, 9, 9, 9, 9, 9, 0]], 1) # bulkhead
print g, ">  [0, 1, 2, 3, 4, 5]"


#exit()

g = solution([[0, 2, 2, 2, -1],
           [9, 0, 2, 2, -1],
           [9, 3, 0, 2, -1],
           [9, 3, 2, 0, -1],
              [9, 3, 2, 2, 0]], 1) 
print g, ">  [1, 2]"


g = solution([[0,  1,  5,  5,  2],
              [10, 0,  2,  6,  10],
              [10, 10, 0,  1,  5],
              [10, 10, 10, 0,  1],
              [10, 10, 10, 10, 0]], 5)
print g, ">  [0, 1, 2]"



g = solution([[0, 1, 3, 4, 2],
          [10, 0, 2, 3, 4],
          [10, 10, 0, 1, 2],
          [10, 10, 10, 0, 1],
          [10, 10, 10, 10, 0]], 4)
print g, ">  []"    


g = solution([[0, 2, 2, 2, -1],
          [9, 0, 2, 2, -1],
          [9, 3, 0, 2, -1],
          [9, 3, 2, 0, -1],
              [9, 3, 2, 2, 0]],  1)
print g, ">  [1, 2]"



        
g = solution([[0,  1, 10, 10, 10],
              [10, 0,  1,  1,  2],
              [10, 1,  0, 10, 10],
              [10, 1,  10, 0, 10],
              [10, 10, 10, 10, 0]],  7)
print g, ">  [0, 1, 2]"

        
g = solution([[0, 1, 1, 1, 1],
          [1, 0, 1, 1, 1],
          [1, 1, 0, 1, 1],
          [1, 1, 1, 0, 1],
              [1, 1, 1, 1, 0]], 3)
print g, ">  [0, 1]"



        
g = solution([[0, 5, 11, 11, 1],
          [10, 0, 1, 5, 1],
          [10, 1, 0, 4, 0],
          [10, 1, 5, 0, 1],
              [10, 10, 10, 10, 0]], 10)
print g, ">  [0, 1]"



        
g = solution([[0, 20, 20, 20, -1],
          [90, 0, 20, 20, 0],
          [90, 30, 0, 20, 0],
          [90, 30, 20, 0, 0],
              [-1, 30, 20, 20, 0]], 0)
print g, ">  [0, 1, 2]"



        
g = solution([[0, 10, 10, 10, 1],
          [0, 0, 10, 10, 10],
          [0, 10, 0, 10, 10],
          [0, 10, 10, 0, 10],
              [1, 1, 1, 1, 0]], 5)
print g, ">  [0, 1]"

        
g = solution([[2, 2], [2, 2]], 5)
print g, ">  []"
    
        
g = solution([[0, 10, 10, 1, 10],
          [10, 0, 10, 10, 1],
          [10, 1, 0, 10, 10],
          [10, 10, 1, 0, 10],
              [1, 10, 10, 10, 0]], 6)
print g, ">  [0, 1, 2]"

        
g = solution([[1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1]] , 1)
print g, ">  []"



g = solution([[0, 0, 1, 1, 1],
          [0, 0, 0, 1, 1],
          [0, 0, 0, 0, 1],
          [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]], 0)
print g, ">  [0, 1, 2]"



g = solution([[1, 1, 1, 1, 1],
          [-1, 1, 1, 1, 1],
          [-1, 1, 1, 1, 1],
          [-1, 1, 1, 1, 1],
          [-1, 1, 1, 1, 1]]  , 1)
print g, ">  [0, 1, 2]"



g = solution([[0, 1, 5, 5, 5, 5],
          [5, 0, 1, 5, 5, 5],
          [5, 5, 0, 5, 5, -1],
          [5, 5, 1, 0, 5, 5],
          [5, 5, 1, 5, 0, 5],
              [5, 5, 1, 1, 1, 0]], 3)
print g, ">  [0, 1, 2, 3]"



g = solution([[0, 1, 5, 5, 5, 5, 5],
          [5, 0, 1, 5, 5, 5, 5],
          [5, 5, 0, 5, 5, 0, -1],
          [5, 5, 1, 0, 5, 5, 5],
          [5, 5, 1, 5, 0, 5, 5],
          [5, 5, 0, 5, 5, 0, 0],
              [5, 5, 1, 1, 1, 0, 0]], 3)
print g, ">  [0, 1, 2, 3, 4]"



g = solution([[0,-1, 0, 9, 9, 9, 9, 9],  # Start
          [9, 0, 1, 9, 9, 9, 9, 9],  # 0
          [0, 9, 0, 0, 9, 9, 1, 1],  # 1
          [9, 9, 9, 0, 1, 9, 9, 9],  # 2
          [9, 9, 9, 9, 0,-1, 9, 9],  # 3 
          [9, 9, 0, 9, 9, 0, 9, 9],  # 4
          [9, 9,-1, 9, 9, 9, 0, 9],  # 5
              [9, 9, 9, 9, 9, 9, 9, 0]], 1) # bulkhead
print g, ">  [0, 1, 2, 3, 4, 5]"



g = solution([[0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]], 0)
print g, ">  [0, 1, 2]"

exit()

g = solution([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 0)
print g, "> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]"



g = solution([[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
          [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 5)
print g, ">  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]"


# 1 [1,2]
# 2 [0, 1]
# 3 [0, 1, 2, 3, 4]
# 4 []
# 5 [0, 2, 3, 4]
# 6 [0, 1, 2]
# 7 [0, 1, 2, 3, 4]
# 8 [1, 2, 3]
# 9 [0, 2, 4]
# 10 [0, 1, 2, 3, 4]
