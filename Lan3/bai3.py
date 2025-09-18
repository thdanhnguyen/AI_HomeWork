# Bài 3: N-Queens (N=5) - Backtracking + AC3 (so sánh)

import time
from simpleai.search import CspProblem, backtrack
from collections import deque

constraint_calls = 0

def queens_constraint(variables, values):
    global constraint_calls
    constraint_calls += 1
    for i in range(len(values)):
        for j in range(i+1, len(values)):
            if values[i] == values[j] or abs(i-j) == abs(values[i]-values[j]):
                return False
    return True

# AC3 tự cài đặt cho simpleai
def ac3_simpleai(problem):
    queue = deque([(xi, xj) for xi in problem.variables for xj in problem.variables if xi != xj])
    while queue:
        xi, xj = queue.popleft()
        if revise(problem, xi, xj):
            if not problem.domains[xi]:
                return False
            for xk in problem.variables:
                if xk != xi and xk != xj:
                    queue.append((xk, xi))
    return True

def revise(problem, xi, xj):
    revised = False
    to_remove = set()
    for x in problem.domains[xi]:
        if not any(queens_constraint([xi, xj], [x, y]) for y in problem.domains[xj]):
            to_remove.add(x)
            revised = True
    problem.domains[xi] = [v for v in problem.domains[xi] if v not in to_remove]
    return revised

# Đếm số bước tìm kiếm bằng cách wrap lại hàm backtrack
def backtrack_count(problem):
    global search_steps
    search_steps = 0
    def callback(state):
        global search_steps
        search_steps += 1
    return backtrack(problem, callback=callback)

def solve_nqueens(n, use_ac3=False):
    global constraint_calls
    constraint_calls = 0
    variables = list(range(n))
    domains = {v: list(range(n)) for v in variables}
    constraints = [(variables, queens_constraint)]
    problem = CspProblem(variables, domains, constraints)
    if use_ac3:
        ac3_simpleai(problem)
    start = time.time()
    result = backtrack(problem)
    end = time.time()
    return result, end-start, constraint_calls

if __name__ == "__main__":
    print("--- N-Queens (N=5) CSP: So sánh Backtracking và Backtracking + AC3 ---")
    for ac3_flag in [False, True]:
        result, t, steps = solve_nqueens(5, use_ac3=ac3_flag)
        print(f"AC3 = {ac3_flag}: {result}")
        print(f"  Time: {t:.4f}s, Steps: {steps}\n")


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

    # Sử dụng simpleai cho giải bài toán N-Queens với backtracking và backtracking + AC3
    import time
    from simpleai.search import CspProblem, backtrack

    def queens_constraint(variables, values):
        for i in range(len(values)):
            for j in range(i+1, len(values)):
                if values[i] == values[j] or abs(i-j) == abs(values[i]-values[j]):
                    return False
        return True

    def solve_nqueens_simpleai(n, use_ac3=False):
        variables = list(range(n))
        domains = {v: list(range(n)) for v in variables}
        constraints = [(
            variables,
            queens_constraint
        )]
        problem = CspProblem(variables, domains, constraints)
        start = time.time()
        if use_ac3:
            ac3_simpleai(problem)
            result = backtrack(problem)
            method = "Backtracking + AC3 (simpleai)"
        else:
            result = backtrack(problem)
            method = "Backtracking (simpleai)"
        end = time.time()
        print(f"{method}: {result}")
        print(f"Time: {end-start:.4f}s")

    if __name__ == "__main__":
        print("--- N-Queens (N=5) với simpleai ---")
        solve_nqueens_simpleai(5, use_ac3=False)
        solve_nqueens_simpleai(5, use_ac3=True)
