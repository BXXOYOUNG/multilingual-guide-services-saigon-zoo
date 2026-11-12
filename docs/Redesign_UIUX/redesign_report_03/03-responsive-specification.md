# TCV Visual Design System – 03. Responsive Specification

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Tài liệu**: Quy chuẩn thiết kế thích ứng (Responsive Design Rules)  
> **Nguyên tắc**: Không chỉ thu nhỏ giao diện desktop; tái tổ chức bố cục phù hợp với từng thiết bị và ngữ cảnh sử dụng thực tế của du khách.

---

## 1. Hệ Thống Breakpoints Chuẩn Hóa

Hệ thống sử dụng 3 điểm ngắt chính xác (Clean Breakpoints):

| Tên Breakpoint | Dải Viewport Width | Thiết bị mục tiêu | Định hướng trải nghiệm |
| :--- | :--- | :--- | :--- |
| **Mobile (`sm`)** | `< 768px` | Smartphone (iPhone, Android) | Tối ưu thao tác 1 tay, nút bấm lớn dễ chạm, quẹt ngang (horizontal swipe) để duyệt nhanh. |
| **Tablet (`md`)** | `768px – 1023px` | iPad, máy tính bảng | Cân bằng giữa không gian đọc và khả năng tương tác cảm ứng, lưới 2 cột. |
| **Desktop (`lg`)** | `>= 1024px` | Laptop, Desktop màn hình lớn | Trải nghiệm điện ảnh hoành tráng, Sticky Storytelling đa cột, typography biên tập lớn. |

---

## 2. Quy Tắc Chuyển Đổi Bố Cục Từng Section Theo Thiết Bị

### 2.1. Header & Điều Hướng
- **Desktop (>= 1024px)**:
  - Hiển thị đầy đủ thanh Menu 6 mục nằm ngang giữa màn hình.
  - Hiển thị logo đầy đủ 174px.
  - Đèn trạng thái mạng hiển thị cả chấm màu và chữ (`Online` / `Offline`).
- **Tablet (768px - 1023px)**:
  - Menu rút gọn khoảng cách giữa các mục (gap 12px), ẩn chữ trạng thái mạng (chỉ giữ lại chấm tròn xanh/cam).
- **Mobile (< 768px)**:
  - Ẩn toàn bộ thanh menu ngang; chuyển sang nút bấm **Hamburger Menu** (`mobile-menu-toggle`).
  - Khi bấm mở menu: Bung một Drawer trượt xuống phủ toàn chiều rộng màn hình với các mục chạm lớn (chiều cao tối thiểu mỗi mục 48px).

### 2.2. Section 01 – Hero Welcome
- **Desktop**: Bố cục 2 cột ngang song song (Cột trái 58% là chữ, Cột phải 42% là hình ảnh Voi Châu Á lớn).
- **Mobile**:
  - Chuyển thành bố cục 1 cột dọc: Chữ tiêu đề xuất hiện đầu tiên, sau đó đến hình ảnh Voi Châu Á bo góc tròn mềm mại nằm ngay dưới, tiếp theo là 2 nút CTA toàn chiều rộng (`width: 100%`).
  - Nút *Khám phá bản đồ* nổi bật trên cùng để người dùng đang đứng ở cổng vào vườn thú có thể bấm xem ngay trong 1 giây.

### 2.3. Section 02 – Animal Discovery
- **Desktop**: Áp dụng đầy đủ hiệu ứng **Sticky Storytelling** (Cột ảnh ghim dính bên trái, các câu chuyện trôi qua bên phải).
- **Mobile**:
  - Không ghim dính chiếm dụng màn hình. Tự động chuyển thành **Thẻ trượt ngang (Horizontal Swipe Carousel)** kèm hiệu ứng lộ trước một phần thẻ tiếp theo (`peek preview` khoảng 20% chiều rộng thẻ bên cạnh) để báo hiệu cho người dùng biết có thể quẹt tiếp.
  - Lưới danh mục toàn bộ loài chuyển từ 3 cột (desktop) về 1 cột thẻ dọc lớn (mobile) với hình ảnh phía trên và chữ phía dưới.

### 2.4. Section 04 – Interactive Map
- **Desktop**:
  - Chiều cao bản đồ `620px`.
  - Drawer thông tin POI hiển thị dạng hộp nổi nằm cố định ở góc phải bên trong bản đồ.
- **Mobile**:
  - Chiều cao bản đồ đặt `420px`.
  - Kích hoạt cơ chế **Cooperative Gestures**: Cuộn 1 ngón trôi trang web, 2 ngón tay để pan bản đồ.
  - Khi bấm chọn một POI: Drawer hiển thị dạng **Bottom Sheet** trượt từ đáy màn hình lên với thanh kéo vuốt (drag handle) thân thiện.

### 2.5. Section 05 – Suggested Routes
- **Desktop**: Lưới 3 cột đặt song song, hiển thị trọn vẹn danh sách trạm dừng của cả 3 tuyến giúp người dùng dễ dàng so sánh.
- **Mobile**:
  - Dạng danh sách thẻ lướt ngang có `scroll-snap-type: x mandatory` hoặc các thẻ accordion có thể gập/mở danh sách trạm dừng để tiết kiệm chiều dọc màn hình.

### 2.6. Section 06 – Offline Audio Preparation
- **Desktop**: Hiển thị hàng ngang 6 mã QR kích thước đầy đủ cho khách quét bằng điện thoại khi đang xem trên máy tính.
- **Mobile**:
  - Vì người dùng đang trực tiếp cầm điện thoại, màn hình hiển thị ưu tiên nút bấm: *"TẢI GÓI ÂM THANH VỀ THIẾT BỊ NÀY"* (kèm nút chọn ngôn ngữ dạng tabs), mã QR thu nhỏ thành tùy chọn phụ cho người đi cùng quét chéo.

---

## 3. Quy Chuẩn Về Vùng Chạm Cảm Ứng (Touch Target Ergonomics)

Tuân thủ nghiêm ngặt chuẩn tiện dụng trên thiết bị di động (Mobile Usability):
- Mọi nút bấm, link điều hướng và icon có thể click trên mobile phải đạt kích thước tối thiểu **44px x 44px** (hoặc padding bù trừ tối thiểu 12px xung quanh).
- Khoảng cách giữa các phần tử có thể bấm chạm tối thiểu là **8px** để tránh bấm nhầm.
