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
