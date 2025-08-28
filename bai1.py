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
                    fringe.insert(0, (v, path + [v]))
    return "NO SOLUTION"
def depth_limited_search(A, n0, DICH, limit):
    fringe = [(n0, [n0], 0)]
    while fringe:
        n, path, depth = fringe.pop()
        if n in DICH:
            return f"SOLUTION path: {path}"
        if depth < limit:
            for v in reversed(A.get(n, [])):
                if v not in path:
                    fringe.append((v, path + [v], depth + 1))
    return "NO SOLUTION"