import time

class NQueens:
    def __init__(self, n):
        self.n = n
        self.solutions = []
        self.checks = 0  # đếm số lần kiểm tra is_safe

    def is_safe(self, queens, row, col):
        self.checks += 1
        for r, c in enumerate(queens):
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    # --- Chiến lược 1: Cơ bản ---
    def solve_basic(self, row=0, queens=[]):
        if row == self.n:
            self.solutions.append(queens[:])
            return
        for col in range(self.n):
            if self.is_safe(queens, row, col):
                queens.append(col)
                self.solve_basic(row + 1, queens)
                queens.pop()

    # --- Chiến lược 2: MRV (chọn hàng có ít lựa chọn hợp lệ nhất) ---
    def solve_mrv(self, queens=[]):
        row = len(queens)
        if row == self.n:
            self.solutions.append(queens[:])
            return

        # với hàng hiện tại, tính danh sách cột hợp lệ
        candidates = [c for c in range(self.n) if self.is_safe(queens, row, c)]

        # sắp xếp cột theo số lựa chọn còn lại cho hàng sau (MRV)
        candidates.sort(key=lambda c: self.future_moves(queens, row, c))

        for col in candidates:
            self.solve_mrv(queens + [col])

    def future_moves(self, queens, row, col):
        # tạm đặt hậu vào (row, col) và tính số cột hợp lệ cho hàng tiếp theo
        temp = queens + [col]
        next_row = row + 1
        return sum(1 for c in range(self.n) if self.is_safe(temp, next_row, c)) if next_row < self.n else 0


def test_strategies(n):
    print(f"\n--- N = {n} ---")

    # Basic
    nq = NQueens(n)
    start = time.time()
    nq.solve_basic()
    end = time.time()
    print(f"Basic Strategy: {len(nq.solutions)} solutions found in {end - start:.4f} seconds, checks={nq.checks}")

    # MRV
    nq = NQueens(n)
    start = time.time()
    nq.solve_mrv()
    end = time.time()
    print(f"MRV Strategy: {len(nq.solutions)} solutions found in {end - start:.4f} seconds, checks={nq.checks}")


if __name__ == "__main__":
    test_strategies(5)  # chạy thử với N=5
    test_strategies(8)  # chạy thử với N=8
