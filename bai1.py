from collections import deque
import heapq
def breath_fisrt_search(N,A, n0, DICH):
    fringe = deque([n0])
    closed = set()
    while fringe:
        n = fringe.popleft()
        closed.add(n)
        if n == DICH:
            return f"SOLUTION {n}"
        neighbors = A.get(n, [])
        if neighbors:
            for v in neighbors:
                if v not in closed and v not in fringe:
                    fringe.append(v)
    return "NO SOLUTION"
def uniform_cost_search(N, A, n0, DICH):
    fringe = [(0, n0, [n0])]
    closed = set()
    while fringe:
        cost, n, path = heapq.heappop(fringe)
        if n in closed:
            continue
        closed.add(n)
        if n in DICH:
            return f"SOLUTION {path} COST {cost}"
        for neighbor, step_cost in A.get(n, []):
            if neighbor not in closed:
                heapq.heappush(fringe, (cost + step_cost, neighbor, path + [neighbor]))
    return "NO SOLUTION"
def depth_first_search(N, A, n0, DICH):
    fringe = [(n0, [n0])]
    close = set()
    while fringe:
        n, path = fringe.pop()
        close.add(n)
        if n in DICH:
            return f"SOLUTION path: {path}"
        neighbors = A.get(n, [])
        if neighbors: 
            for v in reversed(neighbors):
                if v not in close:
                    fringe.append((v, path + [v]))
    return "NO SOLUTION"

def depth_limited_search(N, A, n0, DICH, limit):
    fringe = [(n0, [n0], 0)]
    closed = set()
    while fringe:
        n, path, depth = fringe.pop()
        closed.add(n)
        if n in DICH:
            return f"SOLUTION path: {path}"
        if depth < limit:
            neighbors = A.get(n, [])
            for v in reversed(neighbors):
                if v not in closed:
                    fringe.append((v, path + [v], depth + 1))
    return None

def iterative_deepening_search(N, A, n0, DICH, max_depth):
    for limit in range(max_depth + 1):
        result = depth_limited_search(N, A, n0, DICH, limit)
        if result:
            return f"IDS found at depth {limit}: {result}"
    return "NO SOLUTION"      

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": [],
    "D": [],
    "E": []
}
N = len(graph)
start = "A"
goal = {"E"} 

print("=== BFS ===")
print(breath_fisrt_search(N, graph, start, "E"))

print("\n=== DFS ===")
print(depth_first_search(N, graph, start, goal))

print("\n=== DLS (limit=2) ===")
print(depth_limited_search(N, graph, start, goal, limit=2))

print("\n=== IDS (max_depth=4) ===")
print(iterative_deepening_search(N, graph, start, goal, max_depth=4))

weighted_graph = {
    "A": [("B", 1), ("C", 5)],
    "B": [("D", 2), ("E", 1)],
    "C": [],
    "D": [],
    "E": []
}
print("\n=== UCS ===")
print(uniform_cost_search(N, weighted_graph, start, goal))
       
