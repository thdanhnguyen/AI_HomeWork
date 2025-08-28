from simpleai.search import SearchProblem, breadth_first, depth_first, uniform_cost, limited_depth_first, iterative_limited_depth_first
import random

GOAL_STATE = ((1, 2, 3),
              (4, 0, 5),
              (6, 7, 8))

ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

class EightPuzzleProblem(SearchProblem):
    def __init__(self, initial_state):
        super().__init__(initial_state)

    def actions(self, state):
        row, col = [(ix, iy) for ix, row in enumerate(state) for iy, i in enumerate(row) if i == 0][0]
        possible_actions = []
        if row > 0:
            possible_actions.append('UP')
        if row < 2:
            possible_actions.append('DOWN')
        if col > 0:
            possible_actions.append('LEFT')
        if col < 2:
            possible_actions.append('RIGHT')
        return possible_actions

    def result(self, state, action):
        row, col = [(ix, iy) for ix, row in enumerate(state) for iy, i in enumerate(row) if i == 0][0]
        new_state = [list(r) for r in state]
        if action == 'UP':
            new_row, new_col = row - 1, col
        elif action == 'DOWN':
            new_row, new_col = row + 1, col
        elif action == 'LEFT':
            new_row, new_col = row, col - 1
        elif action == 'RIGHT':
            new_row, new_col = row, col + 1
        new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
        return tuple(tuple(r) for r in new_state)

    def is_goal(self, state):
        return state == GOAL_STATE

    def cost(self, state, action, state2):
        return 1

def random_initial_state():
    nums = list(range(9))
    while True:
        random.shuffle(nums)
        state = tuple(tuple(nums[i*3:(i+1)*3]) for i in range(3))
        # Ensure solvable
        flat = sum(state, ())
        inv = 0
        for i in range(8):
            for j in range(i+1, 9):
                if flat[i] and flat[j] and flat[i] > flat[j]:
                    inv += 1
        if inv % 2 == 0:
            return state

def print_state(state):
    for row in state:
        print(' '.join(str(i) if i != 0 else ' ' for i in row))
    print()

def main():
    initial = random_initial_state()
    print('Initial State:')
    print_state(initial)
    problem = EightPuzzleProblem(initial)

    print('--- BFS ---')

    result = breadth_first(problem)
    print('Steps:', len(result.path())-1)
    for action, state in result.path():
        print('Action:', action)
        print_state(state)

    print('--- DFS ---')
    result = depth_first(problem)
    print('Steps:', len(result.path())-1)
    for action, state in result.path():
        print('Action:', action)
        print_state(state)

    print('--- UCS ---')
    result = uniform_cost(problem)
    print('Steps:', len(result.path())-1)
    for action, state in result.path():
        print('Action:', action)
        print_state(state)

    print('--- DLS (depth=20) ---')
    result = limited_depth_first(problem, 20)
    print('Steps:', len(result.path())-1)
    for action, state in result.path():
        print('Action:', action)
        print_state(state)

    print('--- IDS ---')
    result = iterative_limited_depth_first(problem)
    print('Steps:', len(result.path())-1)
    for action, state in result.path():
        print('Action:', action)
        print_state(state)

if __name__ == '__main__':
    main()
