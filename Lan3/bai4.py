from simpleai.search import CspProblem, backtrack, SearchProblem, hill_climbing, simulated_annealing
import random
import time

#----------------------------------------
# Các hằng số chung
#----------------------------------------
N = 8  # kích thước bàn cờ
POP_SIZE = 100  # kích thước quần thể cho GA
GENERATIONS = 100  # số thế hệ cho GA
MUTATION_RATE = 0.2  # tỉ lệ đột biến
TOURNAMENT_SIZE = 3  # kích thước giải đấu cho GA

#----------------------------------------
# Phần 1: Backtracking với CSP
#----------------------------------------
def setup_csp():
    variables = list(range(N))
    domains = {var: list(range(N)) for var in variables}
    
    def queens_constraint(variables, values):
        row1, row2 = variables
        col1, col2 = values
        return col1 != col2 and abs(row1 - row2) != abs(col1 - col2)
    
    constraints = [((i, j), queens_constraint) 
                  for i in variables 
                  for j in variables if i < j]
    
    return variables, domains, constraints

def run_backtracking(use_ac3=False):
    print(f"\n=== Backtracking {'với' if use_ac3 else 'không dùng'} AC3 ===")
    variables, domains, constraints = setup_csp()
    problem = CspProblem(variables, domains, constraints)
    
    start_time = time.time()
    solution = backtrack(problem, inference='ac3' if use_ac3 else None)
    end_time = time.time()
    
    print(f"Thời gian chạy: {end_time - start_time:.4f} giây")
    if solution:
        print("Giải pháp tìm được:")
        print_solution(solution)
    else:
        print("Không tìm thấy giải pháp")

#----------------------------------------
# Phần 2: Hill Climbing
#----------------------------------------
class EightQueensProblem(SearchProblem):
    def actions(self, state):
        return [(row, col) for row in range(N) 
                for col in range(N) if state[row] != col]

    def result(self, state, action):
        row, col = action
        new_state = list(state)
        new_state[row] = col
        return tuple(new_state)

    def value(self, state):
        non_attacking = 0
        for i in range(N):
            for j in range(i + 1, N):
                if state[i] != state[j] and \
                   abs(state[i] - state[j]) != abs(i - j):
                    non_attacking += 1
        return non_attacking

def run_hill_climbing():
    print("\n=== Hill Climbing ===")
    best_result = None
    total_time = 0
    total_steps = 0
    attempts = 10
    
    for i in range(attempts):
        init_state = tuple(random.randint(0, N-1) for _ in range(N))
        start_time = time.time()
        result = hill_climbing(EightQueensProblem(init_state))
        end_time = time.time()
        
        total_time += end_time - start_time
        # Đếm số bước từ trạng thái ban đầu đến kết quả
        steps = sum(1 for x, y in zip(init_state, result.state) if x != y)
        total_steps += steps
        
        if not best_result or result.value > best_result.value:
            best_result = result
            best_time = end_time - start_time
            best_steps = steps
    
    print(f"Thống kê ({attempts} lần chạy):")
    print(f"- Thời gian trung bình: {total_time/attempts:.4f} giây")
    print(f"- Số bước trung bình: {total_steps/attempts:.1f}")
    print(f"\nKết quả tốt nhất:")
    print(f"- Value: {best_result.value}/{N*(N-1)//2}")
    print(f"- Thời gian: {best_time:.4f} giây")
    print(f"- Số bước: {best_steps}")
    print("\nBàn cờ:")
    print_solution_as_board(best_result.state)

#----------------------------------------
# Phần 3: Simulated Annealing
#----------------------------------------
def run_simulated_annealing():
    print("\n=== Simulated Annealing ===")
    best_result = None
    total_time = 0
    total_steps = 0
    attempts = 10
    iterations = 10000
    
    for i in range(attempts):
        init_state = tuple(random.randint(0, N-1) for _ in range(N))
        start_time = time.time()
        result = simulated_annealing(EightQueensProblem(init_state), 
                                   iterations_limit=iterations)
        end_time = time.time()
        
        total_time += end_time - start_time
        # Đếm số bước từ trạng thái ban đầu đến kết quả
        steps = sum(1 for x, y in zip(init_state, result.state) if x != y)
        total_steps += steps
        
        if not best_result or result.value > best_result.value:
            best_result = result
            best_time = end_time - start_time
            best_steps = steps
    
    print(f"Thống kê ({attempts} lần chạy):")
    print(f"- Thời gian trung bình: {total_time/attempts:.4f} giây")
    print(f"- Số bước trung bình: {total_steps/attempts:.1f}")
    print(f"\nKết quả tốt nhất:")
    print(f"- Value: {best_result.value}/{N*(N-1)//2}")
    print(f"- Thời gian: {best_time:.4f} giây")
    print(f"- Số bước: {best_steps}")
    print(f"- Số lần lặp tối đa: {iterations}")
    print("\nBàn cờ:")
    print_solution_as_board(best_result.state)

#----------------------------------------
# Phần 4: Genetic Algorithm
#----------------------------------------
def fitness(state):
    count = 0
    for i in range(N):
        for j in range(i + 1, N):
            if abs(state[i] - state[j]) != abs(i - j):
                count += 1
    return count

def generate_individual():
    state = list(range(N))
    random.shuffle(state)
    return tuple(state)

def tournament_selection(population):
    tournament = random.sample(population, TOURNAMENT_SIZE)
    return max(tournament, key=fitness)

def crossover(parent1, parent2):
    a, b = sorted(random.sample(range(N), 2))
    child = [None] * N
    child[a:b] = parent1[a:b]
    
    remaining = [x for x in parent2 if x not in child[a:b]]
    j = 0
    for i in range(N):
        if child[i] is None:
            child[i] = remaining[j]
            j += 1
    return tuple(child)

def mutate(state):
    i, j = random.sample(range(N), 2)
    new_state = list(state)
    new_state[i], new_state[j] = new_state[j], new_state[i]
    return tuple(new_state)

def run_genetic_algorithm():
    print("\n=== Genetic Algorithm ===")
    start_time = time.time()
    
    population = [generate_individual() for _ in range(POP_SIZE)]
    best_solution = max(population, key=fitness)
    best_fitness = fitness(best_solution)
    gen_found = 0
    
    for generation in range(GENERATIONS):
        new_population = [best_solution]  # elitism
        
        while len(new_population) < POP_SIZE:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = crossover(parent1, parent2)
            
            if random.random() < MUTATION_RATE:
                child = mutate(child)
            new_population.append(child)
        
        population = new_population
        current_best = max(population, key=fitness)
        current_fitness = fitness(current_best)
        
        if current_fitness > best_fitness:
            best_solution = current_best
            best_fitness = current_fitness
            gen_found = generation
    
    end_time = time.time()
    run_time = end_time - start_time
    
    print(f"Thống kê:")
    print(f"- Thời gian chạy: {run_time:.4f} giây")
    print(f"- Số thế hệ đã chạy: {GENERATIONS}")
    print(f"- Thế hệ tìm thấy giải pháp tốt nhất: {gen_found}")
    print(f"\nKết quả tốt nhất:")
    print(f"- Fitness: {best_fitness}/{N*(N-1)//2}")
    print(f"- Tỉ lệ đột biến: {MUTATION_RATE}")
    print(f"- Kích thước quần thể: {POP_SIZE}")
    print("\nBàn cờ:")
    print_solution_as_board(best_solution)

#----------------------------------------
# Hàm tiện ích
#----------------------------------------
def print_solution_as_board(solution):
    for row in range(N):
        line = ['Q' if col == solution[row] else '.' for col in range(N)]
        print(' '.join(line))

def print_solution(solution):
    if isinstance(solution, dict):
        # Convert dictionary solution to list/tuple
        state = [0] * N
        for row, col in solution.items():
            state[row] = col
        print_solution_as_board(state)
    else:
        print_solution_as_board(solution)

#----------------------------------------
# Main
#----------------------------------------
if _name_ == "_main_":
    print(f"Giải bài toán {N} quân hậu bằng các thuật toán:")
    
    # CSP với Backtracking
    run_backtracking(use_ac3=False)
    run_backtracking(use_ac3=True)
    
    # Hill Climbing
    run_hill_climbing()
    
    # Simulated Annealing
    run_simulated_annealing()
    
    # Genetic Algorithm
    run_genetic_algorithm()
