# AI Chess – Python & Pygame

Dự án này là một ứng dụng chơi cờ vua có tích hợp AI, được xây dựng bằng Python và Pygame.  
Người chơi có thể đấu với máy hoặc thiết lập để chơi 2 người trên cùng một máy.

---

##  Tính năng chính

- *Chơi cờ vua đầy đủ luật*:
  - Di chuyển hợp lệ cho tất cả quân: Vua, Hậu, Xe, Tượng, Mã, Tốt.
  - Phong cấp Tốt (cho phép chọn quân muốn phong).
  - Nhập thành (castle) hai bên.
  - Bắt tốt qua đường (en passant).
- *AI chơi cờ tích hợp*:
  - Sử dụng thuật toán *Negamax + Alpha–Beta Pruning* với hàm đánh giá vật chất cơ bản. :contentReference[oaicite:0]{index=0}  
- *Giao diện đồ họa với Pygame*:
  - Bàn cờ 8×8, hiển thị quân cờ bằng hình ảnh.
  - Highlight ô đang chọn và các nước đi hợp lệ. :contentReference[oaicite:1]{index=1}  
- *Undo / Reset ván đấu*:
  - Hoàn tác nước đi (kể cả khi chơi với AI).
  - Reset lại ván chơi mới nhanh chóng. :contentReference[oaicite:2]{index=2}  

---

##  Kiến trúc dự án

Dự án được tách thành ba mô-đun chính:

1. **chess_engine_final.py** – Logic luật cờ vua (Chess Engine) :contentReference[oaicite:3]{index=3}  
   - Lớp GameBoard quản lý:
     - Ma trận bàn cờ 8×8.
     - Lượt đi của bên trắng / bên đen.
     - Vị trí vua trắng / vua đen.
     - Các trạng thái: đang bị chiếu, chiếu hết, quân bị ghim (pin), các hướng chiếu (checks), v.v.
   - Sinh nước đi hợp lệ:
     - Các hàm như get_pawn_moves, get_rook_moves, get_bishop_moves, get_knight_moves, get_queen_moves, get_king_moves.
     - Xử lý đặc biệt: phong cấp tốt, bắt tốt qua đường (qd_sq), nhập thành (theo trạng thái vua/xe đã di chuyển chưa).
   - Kiểm tra chiếu / ghim:
     - Hàm check_for_pin_checks dùng để:
       - Xác định vua có đang bị chiếu.
       - Tìm các quân đang bị ghim.
       - Từ đó lọc lại danh sách nước đi hợp lệ.

   - Lớp Move:
     - Lưu thông tin một nước đi (tọa độ từ–đến, quân di chuyển, quân bị ăn…).
     - Hỗ trợ so sánh / hash để so sánh nước đi tạm với nước đi hợp lệ.
     - Cung cấp địa chỉ dạng cờ vua chuẩn (ví dụ: e2e4).

2. **AI_chess_final.py** – Bộ máy AI :contentReference[oaicite:4]{index=4}  
   - Bảng điểm quân cờ:
     
     pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
     
   - Các hằng số:
     - CHECKMATE = 1000
     - STALEMATE = 0
     - DEPTH = 2 (độ sâu tìm kiếm hiện tại).
   - Hàm chính:
     - findBestMove(board, valid_moves):
       - Duyệt qua các nước đi hợp lệ, dùng *Negamax + Alpha–Beta* để đánh giá.
     - negamax(...):
       - Gọi đệ quy, đổi dấu điểm số cho đối thủ.
       - Áp dụng cắt tỉa alpha–beta.
     - scoreb(board):
       - Tính điểm dựa trên tổng điểm quân trắng – quân đen, cộng/trừ mạnh khi chiếu hết.

3. **chess_final.py** – Giao diện & vòng lặp game (UI + Game Loop) :contentReference[oaicite:5]{index=5}  
   - Sử dụng pygame để:
     - Tạo cửa sổ game 512×512.
     - Vẽ bàn cờ, quân cờ, highlight ô chọn và nước đi hợp lệ.
   - Tạo và quản lý:
     - Đối tượng GameBoard.
     - Vòng lặp sự kiện (event loop) để xử lý:
       - Click chuột chọn và đi quân.
       - Phím *Z*: hoàn tác.
       - Phím *R*: restart ván mới.
   - Gọi AI:
     - Khi không phải lượt người chơi (tùy cấu hình), gọi findBestMove để máy tự đi.
   - Popup chọn phong cấp:
     - Hàm choose_promotion(...) hiển thị popup cho phép chọn quân phong: Hậu, Xe, Tượng, Mã.

---

##  Cấu trúc thư mục gợi ý

Bạn có thể tổ chức repo như sau để dễ quản lý:

```bash
AI-Chess/
├─ README.md
├─ chess_final.py           # Entry point – chạy file này để chơi
├─ chess_engine_final.py    # Logic luật cờ
├─ AI_chess_final.py        # AI (Negamax + Alpha–Beta)
└─  images/
      ├─ wP.png
      ├─ wR.png
      ├─ ...
      └─ bK.png