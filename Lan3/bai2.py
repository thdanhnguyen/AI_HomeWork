from simpleai.search import CspProblem, backtrack
import time

def constraint(variables, values):
    row1, row2 = variables
    col1, col2 = values
    # Không cùng cột
    if col1 == col2:
        return False
    # Không cùng đường chéo
    if abs(row1 - row2) == abs(col1 - col2):
        return False
    return True

def solve_with_strategy(N, variable_heuristic=None, value_heuristic=None):
    variables = list(range(N))  # mỗi biến là 1 row
    domains = {v: list(range(N)) for v in variables}  # col từ 0..N-1

    constraints = []
    for i in range(N):
        for j in range(i + 1, N):
            constraints.append(((i, j), constraint))

    problem = CspProblem(variables, domains, constraints)

    start = time.time()
    result = backtrack(
        problem,
        variable_heuristic=variable_heuristic,
        value_heuristic=value_heuristic,
    )
    end = time.time()

    return result, end - start

if __name__ == "__main__":
    N = 5

    # Basic Strategy
    res_basic, t_basic = solve_with_strategy(N)
    print("--- Basic Strategy ---")
    print("Solution:", res_basic)
    print("Time:", t_basic)

    # MRV Strategy (Minimum Remaining Values)
    res_mrv, t_mrv = solve_with_strategy(N, variable_heuristic="mrv")
    print("\n--- MRV Strategy ---")
    print("Solution:", res_mrv)
    print("Time:", t_mrv)

    # Degree heuristic
    res_deg, t_deg = solve_with_strategy(N, variable_heuristic="degree")
    print("\n--- Degree Strategy ---")
    print("Solution:", res_deg)
    print("Time:", t_deg)
