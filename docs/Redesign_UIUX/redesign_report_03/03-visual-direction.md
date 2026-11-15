# TCV Visual Design System – 03. Brand & Visual Direction

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Tài liệu**: Định hướng thẩm mỹ & Ngôn ngữ thị giác thương hiệu (Visual Direction)  
> **Phong cách chủ đạo**: Nature-inspired Editorial Design + Modern Interactive Experience  
> **Nguyên tắc**: Tôn vinh di sản thiên nhiên 1864, hiện đại hóa giao diện, không làm mất bản sắc văn hóa.

---

## 1. Audit Nhận Diện Thị Giác Hiện Tại (Current Visual Identity Audit)

Qua khảo sát toàn bộ mã nguồn CSS (`frontend/src/app/index.css`) và các tài nguyên đồ họa:
- **Di sản cốt lõi**: Thảo Cầm Viên Sài Gòn (thành lập năm 1864) là một trong 8 vườn thú lâu đời nhất thế giới. Giá trị cốt lõi nằm ở bề dày lịch sử, cây cổ thụ trăm tuổi và bảo tồn động thực vật quý hiếm.
- **Bảng màu gốc**:
  - Tông màu chủ đạo là xanh lục rừng nhiệt đới (`#176b4b`, `#2e7d32`, `#1c573a`) mang tính biểu tượng cao cho mảng xanh giữa lòng Sài Gòn.
  - Tông nền tự nhiên là màu kem giấy ngà (`#f6f5ef`, `#fffefa`, `#e9eee7`), mang cảm giác ấm áp, sinh thái thay vì màu trắng tinh công nghiệp chói mắt.
  - Tông màu bổ trợ gồm màu đất nung / cam hổ phách (`#e49d55`, `#f57c00`, `#da8a36`) biểu trưng cho động vật hoang dã và ánh nắng phương Nam.
- **Bộ nhận diện Typography**:
  - Sử dụng font chữ nhúng cục bộ `Zoo Sans` (dựa trên Noto Sans với đầy đủ ký tự tiếng Việt, dấu thanh điệu chuẩn xác, font weight từ 100 đến 900).
- **Hạn chế của thiết kế cũ**:
  - Bố cục trước đây mang nặng tính chất ứng dụng di động dạng container hẹp (`max-width: 480px` - `760px`), chưa tận dụng được không gian thoáng đãng của màn hình lớn desktop.
  - Các section chưa có tính phân tầng thị giác nhịp nhàng (visual pacing), card bo góc và shadow còn phân mảnh.

---

## 2. Đề Xuất Hướng Đi Thị Giác Mới: "Nature-inspired Editorial Design"

Kết hợp 2 tinh thần: **Tính Biên tập Cao cấp (Editorial Storytelling)** và **Trải nghiệm Tương tác Hiện đại (Modern Interactive)**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   NATURE-INSPIRED EDITORIAL DESIGN                     │
│                                                                        │
│   [ BÁO CHÍ ĐỊA LÝ CAO CẤP ]        +       [ GIAO DIỆN TƯƠNG TÁC SỐ ] │
│   - Typography tiêu đề lớn          │       - Cử chỉ 2 ngón tay mượt mà│
│   - Khoảng trắng (whitespace) rộng  │       - Micro-interactions 60fps │
│   - Màu sắc hữu cơ ấm áp (Organic)  │       - Sticky scrolling pinning │
│   - Nhiếp ảnh thiên nhiên chân thực │       - Phản hồi vị trí tức thời │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Tính Biên tập Sinh thái (Botanical Editorial)**:
   - Cách bố trí bất đối xứng có chủ đích (intentional asymmetry) giữa hình ảnh động vật hoang dã và đoạn trích dẫn câu chuyện.
   - Sử dụng các chi tiết đồ họa tinh tế như: số thứ tự dạng hai chữ số (`01`, `02`, `03`), nhãn phân loại nhỏ gọn in hoa (`EYEBROW`), đường kẻ ngăn cách thanh mảnh (fine rules `1px solid`).
2. **Chiều sâu Hữu cơ (Organic Depth)**:
   - Ánh sáng tự nhiên và đổ bóng nhiều lớp rất nhẹ (`soft diffused shadows`), mô phỏng bóng râm của vòm lá nhiệt đới.
   - Sử dụng hiệu ứng làm mờ nền như giọt sương trên lá (`backdrop-filter: blur(16px)` với độ mờ trắng 92-96%) trên Header và các thẻ điều khiển.
3. **Cảm giác Khám phá Tự nhiên (Sense of Wonder)**:
   - Các chuyển động mượt mà khi người dùng cuộn tới: chữ trồi nhẹ lên (`soft rise`), ảnh có độ trôi nhẹ (`subtle parallax`), các chấm chỉ báo phát sáng dịu dàng.

---

## 3. Quy Chuẩn Không Làm Mất Nhận Diện Thương Hiệu

- **Biểu tượng thương hiệu**: Giữ nguyên vẹn logo `Saigon Zoo & Botanical Gardens 1864` (`<BrandLogo />`).
- **Tên gọi & Tinh thần**: Giữ vững tinh thần di sản 1864, kết nối hài hòa giữa giá trị lịch sử và công nghệ dẫn đường thông minh.
- **Màu sắc nhận diện**: Giữ nguyên sắc xanh di sản `#176b4b` làm màu đại diện số 1 của thương hiệu, chỉ chuẩn hóa thành hệ thống CSS Tokens đồng nhất.
