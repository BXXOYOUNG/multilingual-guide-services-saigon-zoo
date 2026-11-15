# TCV Visual Design System – 03. Component Visual Specification

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Tài liệu**: Quy chuẩn thị giác từng thành phần giao diện (Component Visual Specs)  
> **Nguyên tắc phân tách**: Phân định rạch ròi giữa Presentation Layer (UI Styling) và Functional Layer (Business Logic).

---

## 1. Sticky Navigation Header

- **Presentation Layer**:
  - Chiều cao cố định: `74px` trên Desktop, `62px` trên Mobile.
  - Hiệu ứng kính sương mờ: `background: rgba(255, 254, 250, 0.92); backdrop-filter: blur(16px)`.
  - Thanh tiến trình cuộn gắn liền đáy: Chiều cao `2.5px`, màu `--color-primary-base`, transform scaleX theo tỷ lệ cuộn trang.
  - Phân bổ 3 khối: Logo thương hiệu (trái) - Danh sách liên kết neo (giữa) - Nút chọn ngôn ngữ & Trạng thái mạng (phải).
- **Functional Layer (Bảo vệ)**:
  - Giữ nguyên `BrandLogo.jsx`, `LanguageContext.jsx`, `LanguageSelector.jsx`, `networkStatus.js`.
  - Giữ nguyên cơ chế gửi sự kiện `trackEvent({ event_type: 'heartbeat' })` định kỳ 60 giây.

---

## 2. Section 01 – Hero Welcome

- **Presentation Layer**:
  - Khung bao cong lớn bo tròn `border-radius: 28px`, nền gradient nhẹ từ xanh sương sang kem nhạt.
  - Cột trái: Nhãn Eyebrow `THẢO CẦM VIÊN 1864`, tiêu đề H1 lớn, đoạn giới thiệu và 2 nút hành động chính (Primary Pill CTA) và phụ (Ghost Pill CTA).
  - Cột phải: Hình ảnh chú voi Châu Á lớn cắt viền hữu cơ kèm huy hiệu nổi bật `1864 - Saigon Zoo & Botanical Gardens`.
  - Dưới cùng: Nốt chỉ dẫn cuộn xuống (`home.scrollHint`) kèm hoạt họa mũi tên trồi sụt nhẹ nhàng.
- **Functional Layer (Bảo vệ)**:
  - Liên kết CTA dẫn tới `/map` hoặc cuộn smooth xuống `#map`.

---

## 3. Section 02 – Animal Discovery Cards (Sticky Spotlight & Catalog)

- **Presentation Layer**:
  - **Tầng 1 (Sticky Spotlight)**:
    - Bố cục 2 cột: Cột trái ghim dính (`position: sticky; top: 100px`) hiển thị ảnh chân dung động vật đang chọn và tên khoa học.
    - Cột phải: Danh sách thẻ động vật tiêu biểu lướt qua. Khi một thẻ lướt vào giữa tầm nhìn, ảnh bên trái đổi tương ứng.
  - **Tầng 2 (Species Catalog Grid)**:
    - Lưới 3 cột trên desktop, 2 cột trên tablet, 1 cột trên mobile.
    - Card ảnh tỷ lệ 4:3, tên loài in đậm, tên khoa học in nghiêng, nhãn trạng thái `Có trên bản đồ` / `Chưa có bản đồ`.
- **Functional Layer (Bảo vệ)**:
  - Giữ nguyên fetch API `/api/pois/catalog?language=...`.
  - Giữ nguyên state `selectedAnimal` và component `AnimalImageCredit.jsx`.
  - Modal chi tiết động vật (`animal-detail-dialog`) giữ nguyên logic mở/đóng và link `/map?poi={id}`.

---

## 4. Section 03 – Audio Presentation (3 Phương Thức Nghe)

- **Presentation Layer**:
  - Lưới 3 cột gồm 3 thẻ cao cấp (`listening-card`), chiều cao tối thiểu 260px.
  - Thẻ 01: Nền xanh sẫm bóng bẩy (`#1d5039`) làm điểm nhấn thị giác cho trải nghiệm nghe trực tiếp.
  - Thẻ 02 & 03: Nền kem sáng tinh tươm.
  - Mỗi thẻ có số đếm lớn `01`, `02`, `03` ở góc trên, biểu tượng tai nghe / sóng âm, tiêu đề H3 và link mũi tên chuyển tiếp.
- **Functional Layer (Bảo vệ)**:
  - Các liên kết dẫn sang anchor `#map`, `#offline` hoặc route độc lập.

---

## 5. Section 04 – Interactive Map Container

- **Presentation Layer**:
  - Container bo góc 24px, đổ bóng sâu, chiều cao `620px` trên desktop.
  - Thanh trạng thái nổi trên đầu bản đồ (`map-status-bar`): Đèn GPS, số lượng POI, nút bật Thuyết minh tự động.
  - Khung overlay hướng dẫn cử chỉ: Hiện thông báo *"Dùng 2 ngón tay để di chuyển"* khi chạm 1 ngón trên di động.
  - Thẻ POI gần nhất (`nearest-poi-card`): Thẻ nổi góc dưới trái với viền cam hổ phách và khoảng cách mét.
  - Drawer chi tiết POI (`poi-detail-drawer`): Nằm cố định góc phải bản đồ trên desktop (chiều rộng 400px), dạng Bottom Sheet trên mobile.
- **Functional Layer (Bảo vệ Tuyệt Đối)**:
  - Giữ nguyên 100% logic bên trong `InteractiveMap.jsx`: Khởi tạo MapLibre GL, tải marker POI, watch vị trí GPS, thuật toán `findNearestPoi`, Geofencing engine, và HTML5 audio playback.

---

## 6. Section 05 – Suggested Routes Cards

- **Presentation Layer**:
  - Lưới 3 thẻ lộ trình tương ứng 3 gói (Khám phá nhanh 36p, Gia đình 60p, Trọn vẹn 96p).
  - Huy hiệu số phút ước tính màu xanh rêu (`36 phút`), tiêu đề H3, danh sách các trạm dừng đánh số `01`, `02` kèm vạch chấm nối.
  - Nút lớn toàn chiều rộng: *"Bắt đầu lộ trình này ↗"*.
- **Functional Layer (Bảo vệ)**:
  - Tái sử dụng logic chia mảng POI từ `ItineraryView.jsx`.
  - Nút bắt đầu kích hoạt chuyển bản đồ tới trạm đầu tiên (`firstPoiId`).

---

## 7. Section 06 – Offline QR Container

- **Presentation Layer**:
  - Nền dải màu chuyển nhẹ sang tông đất mộc mạc (`linear-gradient(135deg, #eaf1e7, #f8f7f0)`).
  - Khung track hiển thị 6 thẻ QR tương ứng 6 ngôn ngữ (Việt, Anh, Pháp, Trung, Nhật, Hàn).
  - Mỗi thẻ gồm mã QR SVG kích thước chuẩn 110px x 110px, nhãn ngôn ngữ in đậm và nút tải màu xanh rêu.
- **Functional Layer (Bảo vệ)**:
  - Giữ nguyên `QRCodeSVG` từ thư viện `qrcode.react` với payload `TCV-PACKAGE:{id}`.
  - Giữ nguyên cơ chế tải qua `downloadAudioPackage` và lưu trữ IndexedDB.

---

## 8. Section 07 – Getting Started & Visitor Guide

- **Presentation Layer**:
  - Bố cục 2 khối ngang trên desktop: Khối trái là FAQ dạng thẻ mở rộng (`<details>` và `<summary>`), khối phải là các mẹo hữu ích và cam kết bảo mật GPS.
  - Nút liên kết phụ chuyển sang trang Quản trị viên (`/admin`).
- **Functional Layer (Bảo vệ)**:
  - Sử dụng thẻ HTML5 ngữ nghĩa chuẩn tiếp cận.

---

## 9. Site Footer

- **Presentation Layer**:
  - Tông nền râm mát `#f0f3eb`, viền trên mỏng `1px solid #e2e8de`.
  - Phân chia 2 tầng: Tầng trên gồm Brand Logo di sản 1864, lời giới thiệu sứ mệnh và danh sách liên kết; Tầng dưới là dòng thông tin bản quyền và link chính sách riêng tư.
- **Functional Layer (Bảo vệ)**:
  - Giữ nguyên 100% các link điều hướng và link quản trị `/admin`.
