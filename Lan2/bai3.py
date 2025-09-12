from simpleai.search import SearchProblem, hill_climbing, simulated_annealing
import random

SIZE = 8

class EightQueensProblem(SearchProblem):
    def actions(self, state):
        actions = []
        for row in range(SIZE):
            for col in range(SIZE):
                if state[row] != col:
                    actions.append((row, col))
        return actions

    def result(self, state, action):
        row, col = action
        new_state = list(state)
        new_state[row] = col
        return tuple(new_state)

    def value(self, state):
        # Số cặp quân hậu không tấn công nhau
        non_attacking = 0
        for i in range(SIZE):
            for j in range(i + 1, SIZE):
                if state[i] != state[j] and abs(state[i] - state[j]) != abs(i - j):
                    non_attacking += 1
        return non_attacking

def random_state():
    return tuple(random.randint(0, SIZE - 1) for _ in range(SIZE))

if __name__ == "__main__":
    best_hc = None
    best_sa = None
    for _ in range(10):
        initial = random_state()
        hc_result = hill_climbing(EightQueensProblem(initial))
        sa_result = simulated_annealing(EightQueensProblem(initial), iterations_limit=10000)
        if not best_hc or hc_result.value > best_hc.value:
            best_hc = hc_result
        if not best_sa or sa_result.value > best_sa.value:
            best_sa = sa_result
    print("Best Hill Climbing:", best_hc.state, "Value:", best_hc.value)
    print("Best Simulated Annealing:", best_sa.state, "Value:", best_sa.value)