from simpleai.search import CspProblem, backtrack

# Biến: mỗi hàng một quân hậu (x là hàng, y là cột)
variables = range(5)  # 5 hàng
domains = {}
for var in variables:
    domains[var] = list(range(5)) 

# Ràng buộc: 2 hậu không được tấn công nhau
def queens_constraint(variables, values):
    # variables là tuple chứa 2 hàng, values là tuple chứa cột tương ứng
    row1, row2 = variables
    col1, col2 = values
    
    return (col1 != col2 and row1 != row2 and abs(row1 - row2) != abs(col1 - col2)) 

# Tạo constraints giữa mọi cặp hàng
constraints = []
for i in range(5):
    for j in range(i + 1, 5):
        constraints.append(((i, j), queens_constraint))

problem = CspProblem(variables, domains, constraints)


solution = backtrack(problem)

if solution:
    print("\nGiải pháp tìm được:")
    board = [['.'] * 5 for _ in range(5)]
    for row, col in solution.items():
        board[row][col] = 'Q'
    for row in board:
        print(' '.join(row))
else:
    print("Không tìm thấy giải pháp")
