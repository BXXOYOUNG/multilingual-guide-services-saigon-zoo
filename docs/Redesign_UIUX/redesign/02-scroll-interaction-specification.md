# TCV UX Redesign – 02. Scroll Interaction Specification

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Tài liệu**: Quy chuẩn tương tác cuộn (Scroll Interaction & Sticky Storytelling)  
> **Cam kết an toàn**: Không áp dụng mandatory scroll snapping toàn trang, không để animation cản trở người dùng, tôn trọng thiết bị di động.

---

## 1. Phân loại Cơ chế Cuộn theo Section

Để tạo sự cân bằng hoàn hảo giữa tính điện ảnh sống động (cinematic feel) và tính tiện dụng thực tế (usability), trang chủ kết hợp linh hoạt giữa 2 cơ chế cuộn:

| Thứ tự Section | Tên Section | Cơ chế cuộn áp dụng | Lý do thiết kế & Trải nghiệm mang lại |
| :---: | :--- | :--- | :--- |
| **01** | **Hero / Welcome** | **Normal Scrolling** | Giữ cảm giác tự nhiên, thoáng đãng khi vừa vào web; người dùng lướt nhẹ là bắt đầu trôi vào nội dung tiếp theo mà không bị giữ chân đột ngột. |
| **02** | **Animal Discovery** | **Sticky Storytelling (Pinned)** | Khối động vật tiêu biểu (Voi, Hổ, Hươu, Hà mã) áp dụng kỹ thuật ghim dính (`position: sticky; top: 80px`). Khi cuộn, cột ảnh và câu chuyện bên trái đứng yên tương đối, trong khi nội dung đặc tính và thẻ loài lướt qua mượt mà, tạo cảm giác như đọc tạp chí địa lý tự nhiên cao cấp. Sau đó chuyển tiếp sang lưới danh mục toàn bộ loài (Normal Grid). |
| **03** | **Audio Experience** | **Normal Scrolling + Fade In** | Trình diễn 3 thẻ phương thức nghe; cuộn bình thường để du khách nắm bắt thông tin nhanh chóng. |
| **04** | **Interactive Map** | **Normal Scrolling + Cooperative Gestures** | Bản đồ được nhúng trong khung nhìn cố định nhưng **không áp dụng scroll hijacking**. Thao tác cuộn trang tự do trôi qua bản đồ. Du khách tương tác với bản đồ bằng 2 ngón tay (Mobile) hoặc Ctrl+Scroll (Desktop). |
| **05** | **Suggested Routes** | **Horizontal Snap inside Normal Vertical** | Khung trang cuộn dọc bình thường; riêng 3 thẻ lộ trình (3/5/8 điểm) có thể lướt ngang mượt mà trên màn hình nhỏ với `scroll-snap-type: x mandatory` cục bộ trong container thẻ. |
| **06** | **Offline Preparation** | **Normal Scrolling** | Bố cục dạng lưới hiển thị các mã QR rõ ràng; cuộn tự do không cản trở. |
| **07** | **Getting Started** | **Normal Scrolling** | Đọc các câu hỏi thường gặp và thông tin trợ giúp theo dạng danh sách tự nhiên. |

---

## 2. Chỉ báo Tiến trình Cuộn (Scroll Progress Indicator)

### 2.1. Thanh tiến trình đỉnh đầu (Top Reading Line)
- Vị trí: Gắn sát mép đáy của Sticky Header.
- Kích thước: Chiều cao 2.5px.
- Màu sắc: Xanh lá cây tự nhiên (`var(--color-primary-green: #2d6a4f)`).
- Cơ chế tính toán: Dựa trên tỷ lệ phần trăm cuộn của trang `scrollY / (documentHeight - windowHeight) * 100%`, được cập nhật thông qua biến CSS `--scroll-percent` hoặc `transform: scaleX(...)` với `transform-origin: left` để tận dụng tăng tốc phần cứng GPU mà không kích hoạt layout reflow.

### 2.2. Điểm định vị cạnh sườn (Side Dot Navigator - Desktop Only)
- Trên màn hình máy tính (viewport >= 1024px), xuất hiện một dãy chấm tròn nhỏ tinh tế ở mép phải màn hình:
  - Gồm 7 chấm tương ứng với 7 section.
  - Chấm của section đang đọc sẽ nở lớn nhẹ nhàng và đổi màu xanh đậm.
  - Rê chuột vào hiện tooltip tên section; bấm vào sẽ cuộn mượt đến section đó.
- Ẩn hoàn toàn trên Mobile/Tablet để bảo toàn không gian hiển thị nội dung.

---

## 3. Hoạt Họa Kích Hoạt theo Cuộn (Scroll-Triggered Animations)

### 3.1. Nguyên tắc hoạt họa
- **Nhẹ nhàng, tinh tế (Subtle & Purposeful)**: Hoạt họa chỉ nhằm mục đích thu hút sự chú ý vào thông điệp chính, không lạm dụng hiệu ứng quá đà gây phân tâm hoặc kéo dài thời gian chờ đợi của du khách.
- **Không chặn tương tác (Non-blocking)**: Mọi nội dung text và nút bấm CTA phải có thể đọc và click được ngay lập tức, không phụ thuộc vào việc animation đã chạy xong hay chưa.

### 3.2. Danh mục hiệu ứng áp dụng
1. **Fade Up & Reveal (Chữ và Khối nội dung)**:
   - Các tiêu đề Section (`<h2>`) và đoạn giới thiệu trồi nhẹ lên 16px kèm độ mờ chuyển từ 0 lên 1 (`opacity: 1; transform: translateY(0)`), thời lượng 400ms easing `cubic-bezier(0.16, 1, 0.3, 1)`.
2. **Staggered Cards Entry (Danh sách thẻ)**:
   - 4 Thẻ động vật tiêu biểu và 3 Thẻ phương thức nghe xuất hiện so le nhau 80ms (`transition-delay: calc(index * 80ms)`), tạo nhịp điệu thị giác thanh thoát.
3. **Sticky Image Parallax**:
   - Hình ảnh động vật trong Section 02 trôi chậm hơn tốc độ cuộn chữ 15%, tạo chiều sâu thị giác (depth illusion) chân thực.

### 3.3. Tôn trọng tùy chọn Giảm Chuyển Động (`prefers-reduced-motion`)
Tuân thủ nghiêm ngặt chuẩn tiếp cận WCAG 2.1:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .animal-sticky-visual {
    position: static !important;
    transform: none !important;
  }
}
```
Khi người dùng kích hoạt Reduce Motion trên hệ điều hành, toàn bộ hiệu ứng di chuyển phức tạp lập tức tắt, trả về giao diện tĩnh rõ ràng và an toàn tuyệt đối.

---

## 4. Trải nghiệm Cuộn trên Thiết bị Di Động (Mobile Scrolling Strategy)

1. **Tuyệt đối không sử dụng Mandatory Scroll Snapping toàn trang**:
   - Scroll snapping trên toàn trang di động thường gây hiện tượng "cuộn nhảy cóc", giật cục và gây ức chế cho người dùng ngón tay cái. Toàn bộ thân trang chủ sử dụng cuộn tự nhiên (`overflow-y: auto; -webkit-overflow-scrolling: touch`).
2. **Kiểm soát cử chỉ trên Bản đồ (Cooperative Gestures)**:
   - Khi ngón tay chạm lướt 1 ngón qua khung bản đồ: trang tiếp tục cuộn xuống mượt mà, không bị khựng lại.
   - Để zoom/pan bản đồ: người dùng thao tác bằng 2 ngón tay. Nếu người dùng chạm 1 ngón giữ lâu vào bản đồ, hiển thị một overlay bán trong suốt với thông báo thân thiện: *"Dùng 2 ngón tay để di chuyển bản đồ"*.
3. **Sticky Element linh hoạt**:
   - Trên màn hình nhỏ (< 768px), cơ chế Sticky Storytelling của Section Động vật sẽ tự động chuyển đổi thành dạng Thẻ trượt ngang (Horizontal Carousel with peek preview) để tránh việc chiều cao màn hình di động bị chiếm dụng quá lâu.
