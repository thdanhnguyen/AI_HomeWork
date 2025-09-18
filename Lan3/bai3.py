import time
from collections import deque
import copy

# --- CSP model for N-Queens ---
class NQueensCSP:
    def __init__(self, n):
        self.n = n
        self.variables = list(range(n))  # mỗi biến là 1 hàng, giá trị là cột
        self.domains = {v: set(range(n)) for v in self.variables}
        self.constraints = {}
        for v1 in self.variables:
            for v2 in self.variables:
                if v1 != v2:
                    self.constraints[(v1, v2)] = self.queen_constraint

    def queen_constraint(self, row1, col1, row2, col2):
        # Không cùng cột, không cùng đường chéo
        return col1 != col2 and abs(row1 - row2) != abs(col1 - col2)

    def is_consistent(self, assignment, var, value):
        for v in assignment:
            if not self.queen_constraint(var, value, v, assignment[v]):
                return False
        return True

# --- AC3 algorithm ---
def ac3(csp, domains):
    queue = deque([(xi, xj) for xi in csp.variables for xj in csp.variables if xi != xj])
    while queue:
        xi, xj = queue.popleft()
        if revise(csp, domains, xi, xj):
            if not domains[xi]:
                return False
            for xk in csp.variables:
                if xk != xi and xk != xj:
                    queue.append((xk, xi))
    return True

def revise(csp, domains, xi, xj):
    revised = False
    to_remove = set()
    for x in domains[xi]:
        if not any(csp.queen_constraint(xi, x, xj, y) for y in domains[xj]):
            to_remove.add(x)
            revised = True
    domains[xi] -= to_remove
    return revised

# --- Backtracking search with/without AC3 ---
def backtrack(assignment, csp, domains, ac3_enabled, steps):
    if len(assignment) == csp.n:
        return assignment, steps
    var = select_unassigned_variable(assignment, csp, domains)
    for value in order_domain_values(var, assignment, csp, domains):
        steps[0] += 1
        if csp.is_consistent(assignment, var, value):
            assignment[var] = value
            local_domains = copy.deepcopy(domains)
            local_domains[var] = {value}
            if ac3_enabled:
                if not ac3(csp, local_domains):
                    assignment.pop(var)
                    continue
            result, steps = backtrack(assignment, csp, local_domains, ac3_enabled, steps)
            if result:
                return result, steps
            assignment.pop(var)
    return None, steps

def select_unassigned_variable(assignment, csp, domains):
    # MRV heuristic: chọn biến có miền giá trị nhỏ nhất
    unassigned = [v for v in csp.variables if v not in assignment]
    return min(unassigned, key=lambda var: len(domains[var]))

def order_domain_values(var, assignment, csp, domains):
    # Không dùng value ordering nâng cao, chỉ trả về miền hiện tại
    return list(domains[var])

# --- Main experiment ---
def run_experiment(n, ac3_enabled):
    csp = NQueensCSP(n)
    domains = {v: set(range(n)) for v in csp.variables}
    steps = [0]
    start = time.time()
    result, steps = backtrack({}, csp, domains, ac3_enabled, steps)
    end = time.time()
    print(f"N={n}, AC3={'ON' if ac3_enabled else 'OFF'}: {result}")
    print(f"Time: {end-start:.4f}s, Steps: {steps[0]}")

if __name__ == "__main__":
    print("--- Backtracking + AC3 cho N-Queens (N=5) ---")
    run_experiment(5, ac3_enabled=True)
    run_experiment(5, ac3_enabled=False)
