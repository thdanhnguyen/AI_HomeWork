from simpleai.search import SearchProblem, astar
import time

GOAL_STATE = ((1, 2, 3),
              (8, 0, 4),
              (7, 6, 5))

ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

class EightPuzzleProblem(SearchProblem):
    def __init__(self, initial_state, heuristic_func=None):
        super().__init__(initial_state)
        self.heuristic_func = heuristic_func

    def heuristic(self, state):
        if self.heuristic_func:
            return self.heuristic_func(state)
        return 0

    def actions(self, state):
        row, col = [(ix, iy) for ix, row in enumerate(state) for iy, i in enumerate(row) if i == 0][0]
        possible_actions = []
        if row > 0: possible_actions.append('UP')
        if row < 2: possible_actions.append('DOWN')
        if col > 0: possible_actions.append('LEFT')
        if col < 2: possible_actions.append('RIGHT')
        return possible_actions

    def heuristic(self, state):
        if self.heuristic_func:
            return self.heuristic_func(state)
        return 0

    def result(self, state, action):
        row, col = [(ix, iy) for ix, row in enumerate(state) for iy, i in enumerate(row) if i == 0][0]
        new_state = [list(r) for r in state]

        if action == 'UP': new_row, new_col = row - 1, col
        elif action == 'DOWN': new_row, new_col = row + 1, col
        elif action == 'LEFT': new_row, new_col = row, col - 1
        elif action == 'RIGHT': new_row, new_col = row, col + 1

        new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
        return tuple(tuple(r) for r in new_state)

    def is_goal(self, state):
        return state == GOAL_STATE

    def cost(self, state, action, state2):
        return 1


# === Heuristic 1: Số ô sai vị trí ===
def h1(state):
    misplaced = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != GOAL_STATE[i][j]:
                misplaced += 1
    return misplaced

# === Heuristic 2: Manhattan distance ===
def h2(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_i, goal_j = [(x, y) for x, row in enumerate(GOAL_STATE) for y, val in enumerate(row) if val == value][0]
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance


def print_state(state):
    for row in state:
        print(' '.join(str(i) if i != 0 else ' ' for i in row))
    print()


def main():
    # Trạng thái ví dụ
    initial_state = ((2, 8, 3),
                     (1, 6, 4),
                     (7, 0, 5))

    problem = EightPuzzleProblem(initial_state)

    # Chạy với heuristic h1 (Misplaced Tiles)
    print("=== A* với Heuristic h1 (Misplaced Tiles) ===")
    problem1 = EightPuzzleProblem(initial_state, h1)
    start = time.time()
    result1 = astar(problem1, graph_search=True)
    end = time.time()
    print("Steps:", len(result1.path()) - 1)
    print("Time:", round(end - start, 4), "s")

    # Chạy với heuristic h2 (Manhattan Distance)
    print("\n=== A* với Heuristic h2 (Manhattan Distance) ===")
    problem2 = EightPuzzleProblem(initial_state, h2)
    start = time.time()
    result2 = astar(problem2, graph_search=True)
    end = time.time()
    print("Steps:", len(result2.path()) - 1)
    print("Time:", round(end - start, 4), "s")

    # In đường đi với h2
    print("\n=== Đường đi với h2 ===")
    for action, state in result2.path():
        if action:  # bỏ qua trạng thái đầu tiên vì action=None
            print("Action:", action)
        print_state(state)
    print("Steps:", len(result2.path()) - 1)
    print("Time:", round(end - start, 4), "s")

    # In đường đi với h2
    print("\n=== Đường đi với h2 ===")
    for action, state in result2.path():
        if action:  # bỏ qua trạng thái đầu tiên vì action=None
            print("Action:", action)
        print_state(state)


if _name_ == '_main_':
    main()