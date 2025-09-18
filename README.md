# Thông Báo Đề Bài

## Bài 1:CSP với bàn cờ hậu 5×5
   - Giải bài toán N-Queens (N=5) bằng mô hình CSP (Constraint Satisfaction Problem)
   - Đảm bảo các quân hậu được đặt sao cho không tấn công nhau theo hàng, cột, và đường chéo.

---

## Bài 2: Backtracking với các chiến lược heuristic
   - Sử dụng backtracking để giải bài toán N-Queens.
   - Thử nghiệm các chiến lược heuristic khác nhau (ví dụ: chọn biến, chọn giá trị).
   - So sánh hiệu quả của từng chiến lược trong việc tìm nghiệm.

---

## Bài 3: Backtracking với AC3 (Arc Consistency)
   - Mở rộng từ Bài 2, sử dụng backtracking + kiểm tra tính nhất quán cung (AC3).

   - Thực hiện thử nghiệm với hai cấu hình:

      - Arc Consistency = True (có kiểm tra AC3).
      - Arc Consistency = False (không kiểm tra AC3).

   - So sánh kết quả, tốc độ và số bước tìm kiếm giữa hai chế độ.

---

## Bài 4: Heuristic nâng cao (Value, Hill Climbing, SA, GA)
   - Mở rộng Bài 2 và Bài 3 ở Lần 2 bằng cách áp dụng thêm các kỹ thuật heuristic:

      - Value ordering function: sắp xếp giá trị theo hàm value.

      - Hill Climbing (leo đồi).

      - Simulated Annealing (SA) (tôi luyện mô phỏng).

      - Genetic Algorithm (GA) (thuật toán di truyền).

   - Thử nghiệm, so sánh hiệu quả của các thuật toán này với backtracking (có/không AC3).

---
