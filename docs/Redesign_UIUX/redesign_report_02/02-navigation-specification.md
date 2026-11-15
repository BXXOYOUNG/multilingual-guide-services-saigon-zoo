# TCV UX Redesign – 02. Navigation Specification

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Tài liệu**: Quy chuẩn thiết kế thanh điều hướng (Sticky Navigation & Section Anchors)  
> **Phương châm**: Linh hoạt, phản hồi thời gian thực, bảo tồn khả năng truy cập mọi route.

---

## 1. Cấu trúc Sticky Header

### 1.1. Trạng thái hiển thị (Header States)
Thanh Header được thiết kế dạng **Sticky Floating Header** gắn cố định trên cùng màn hình (`position: sticky; top: 0; z-index: 1000`), với 2 trạng thái thẩm mỹ:
1. **Trạng thái Hero (Top of Page)**:
   - Nền trong suốt mờ nhẹ (`background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px)`).
   - Tối giản, không viền để hòa cùng hình ảnh thiên nhiên của Hero section.
2. **Trạng thái Cuộn (Scrolled State)**:
   - Kích hoạt khi trang cuộn quá 80px.
   - Nền trắng đục hơn (`background: rgba(255, 255, 255, 0.96)`), viền đáy mỏng tinh tế (`border-bottom: 1px solid var(--border-color)`), đổ bóng nhẹ (`box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06)`).
   - Tích hợp một thanh mảnh hiển thị **tiến trình cuộn toàn trang (Scroll Progress Bar)** dày 2px nằm sát mép đáy của Header (`var(--primary-green)`).

### 1.2. Các phần tử trên Header (Header Items)
Từ trái sang phải:
- **Logo Thương Hiệu (Brand Logo)**: Biểu tượng Saigon Zoo & Botanical Gardens 1864 (`<BrandLogo />`), click luôn cuộn mượt về đầu trang Hero.
- **Thanh Điều Hướng Chính (Desktop Primary Nav)**:
  1. *Khám phá (Explore / Animals)* -> Anchor: `#animals`
  2. *Thuyết minh (Audio)* -> Anchor: `#audio`
  3. *Bản đồ (Map)* -> Anchor: `#map`
  4. *Lộ trình (Routes)* -> Anchor: `#routes`
  5. *Tải Offline (Offline)* -> Anchor: `#offline`
  6. *Cẩm nang (Guide / Help)* -> Anchor: `#guide`
- **Công cụ tiện ích (Header Tools)**:
  - Nút chọn ngôn ngữ (`LanguageChip`): Hiển thị cờ và tên bản địa (Tiếng Việt, English, Français...) kết nối với `LanguageContext` hiện hữu.
  - Đèn trạng thái mạng (`ConnectionState`): Chấm tròn xanh/cam báo hiệu Online / Offline kết nối `networkStatus.js`.
- **Nút Menu Di Động (Mobile Hamburger Toggle)**: Cho phép mở drawer điều hướng toàn màn hình trên thiết bị di động.

---

## 2. Chỉ báo Section Đang Hoạt Động (Active Section Indicator)

### 2.1. Cơ chế phát hiện (IntersectionObserver)
Không sử dụng sự kiện `window.addEventListener('scroll')` thô sơ vì dễ gây nghẽn render (jank). Thay vào đó, áp dụng **IntersectionObserver API** độc lập:
- Khởi tạo một observer với `rootMargin: "-20% 0px -60% 0px"` (vùng trọng tâm chiếm phần lớn tầm mắt người đọc).
- Khi một Section đi vào vùng trọng tâm, cập nhật trạng thái `activeSectionId`.

### 2.2. Phản hồi giao diện (Visual Active Feedback)
- Mục navigation tương ứng trên Header nhận class `.is-active`:
  - Chữ đổi sang màu xanh thương hiệu (`var(--color-primary-green)`).
  - Xuất hiện vạch chỉ báo mỏng hoặc hiệu ứng pill nền nổi nhẹ bên dưới mục đang active.
- Đồng thời, đồng bộ URL hash nhẹ nhàng bằng `window.history.replaceState(null, '', `#${sectionId}`)` (tuyệt đối không dùng `pushState` để tránh làm rác lịch sử nút Back của trình duyệt).

---

## 3. Hành vi khi nhấn Navigation & Xử lý Scroll Offset

### 3.1. Hành vi khi nhấn (Click Behavior)
- Khi du khách đang ở trang chủ (`/`) và nhấn vào mục navigation (ví dụ "Bản đồ"):
  - Sự kiện ngăn chặn nhảy trang tức thời (`event.preventDefault()`).
  - Gọi phương thức cuộn mượt:
    ```javascript
    const targetElement = document.getElementById(targetSectionId);
    if (targetElement) {
      const headerOffset = 72; // Chiều cao của Sticky Header
      const elementPosition = targetElement.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
    ```
- Khi du khách đang ở một trang độc lập khác (ví dụ `/admin` hoặc trang lỗi) và nhấn mục điều hướng:
  - React Router thực hiện điều hướng về `/#${targetSectionId}`, sau đó tự động cuộn đến vị trí section tương ứng.

### 3.2. Xử lý Scroll Offset chính xác
- Để tránh tiêu đề của Section bị che khuất dưới Sticky Header khi cuộn đến, cấu hình thuộc tính CSS chuẩn cho toàn bộ các Section:
  ```css
  .home-section,
  #hero, #animals, #audio, #map, #routes, #offline, #guide {
    scroll-margin-top: 76px; /* Bù trừ chính xác chiều cao Header + 4px khoảng thở */
  }
  ```

---

## 4. Duy trì Khả năng Truy cập các Route Độc Lập

Để bảo vệ 100% các liên kết sâu (Deep Links), mã QR vật lý và tính năng chuyên sâu:
1. **Các Route Độc Lập vẫn tồn tại nguyên vẹn trong `router.jsx`**:
   - `/map`: Dành cho khách muốn trải nghiệm bản đồ toàn màn hình chuyên biệt (Full-screen Map Explorer).
   - `/explore`: Dành cho khách muốn quét mã QR trực tiếp bằng camera hoặc quản lý kho file âm thanh IndexedDB.
   - `/itinerary`: Dành cho khách muốn xem chi tiết các gói tham quan.
   - `/guide`: Dành cho trang tài liệu hướng dẫn và điều khoản quyền riêng tư.
   - `/admin/*`: Dành cho đội ngũ biên tập viên quản lý nội dung đa ngôn ngữ.
2. **Liên kết chéo 2 chiều (Bi-directional Linking)**:
   - Trên mỗi Section của trang chủ, luôn có một nút phụ hoặc link góc mở sang route độc lập (ví dụ: góc Section Map có nút *"Mở bản đồ toàn màn hình ↗"* dẫn sang `/map`).
   - Trên các trang độc lập, thanh Header luôn có logo và nút *"Trang chủ"* để quay lại dòng cuộn tổng thể bất kỳ lúc nào.
