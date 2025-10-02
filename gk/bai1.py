from simpleai.search import SearchProblem, backtrack
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -------------------------
# 1️⃣ Định nghĩa hàm mục tiêu
# -------------------------
def f(x, y):
    return abs((x + 1) * (x - 1) * (x - 2) + y * (y - 1))

# Miền giá trị của x và y (step = 0.5)
values = [i * 0.5 for i in range(-10, 11)]

# -------------------------
# 2️⃣ Xây dựng bài toán bằng simpleai
# -------------------------
class OptimizationProblem(SearchProblem):
    def actions(self, state):
        # Không sinh hành động tiếp theo vì ta duyệt toàn bộ miền giá trị
        return []

    def result(self, state, action):
        return state

    def is_goal(self, state):
        x, y = state
        # Kiểm tra điều kiện ràng buộc
        return (x >= 2 * y) and (round(x**2 + y**2, 2) == 1.0)

    def cost(self, state1, action, state2):
        # Giá trị cần tối ưu
        return f(state2[0], state2[1])


# -------------------------
# 3️⃣ Sinh toàn bộ trạng thái, lọc điểm hợp lệ
# -------------------------
all_states = [(x, y) for x in values for y in values]
valid_states = [s for s in all_states if (s[0] >= 2 * s[1]) and (round(s[0]**2 + s[1]**2, 2) == 1.0)]

# Gán trạng thái ban đầu (có thể chọn bất kỳ)
problem = OptimizationProblem(initial_state=valid_states[0] if valid_states else (0, 0))

# -------------------------
# 4️⃣ Duyệt toàn bộ để tìm cực tiểu
# -------------------------
best_state = None
best_val = float("inf")

for state in valid_states:
    cost = f(state[0], state[1])
    if cost < best_val:
        best_val = cost
        best_state = state

if best_state:
    print("✅ Cực tiểu tìm được:")
    print("x =", best_state[0], "y =", best_state[1])
    print("f(x, y) =", best_val)
else:
    print("❌ Không có điểm thỏa điều kiện!")

# -------------------------
# 5️⃣ Vẽ đồ thị mặt cong
# -------------------------
X, Y = np.meshgrid(values, values)
Z = f(X, Y)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Vẽ mặt cong
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)

# Vẽ điểm cực tiểu tìm được
if best_state:
    ax.scatter(best_state[0], best_state[1], best_val,
               color='red', s=100, label=f'Cực tiểu ({best_state[0]}, {best_state[1]})')

# Trang trí biểu đồ
ax.set_title("Biểu diễn mặt cong f(x, y) và điểm cực tiểu", fontsize=14)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("f(x, y)")
ax.legend()

plt.show()
