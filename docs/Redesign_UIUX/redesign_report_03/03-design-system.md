# TCV Visual Design System – 03. Master Design System Document

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Tài liệu**: Tổng hợp toàn bộ quy chuẩn Hệ thống Thiết kế Giao diện (Master Design System)  
> **Phiên bản**: 1.0 (Hoàn thiện giai đoạn thiết kế chuẩn bị cho Phase 4)  
> **Phong cách**: Nature-inspired Editorial Design + Modern Interactive Experience  
> **Ràng buộc tuân thủ**: Giữ 100% backend, bảo vệ toàn bộ API và logic chức năng.

---

## 1. Bản Tóm Tắt Nguyên Tắc Thiết Kế (Design Principles)

1. **Tôn Vinh Di Sản Sinh Thái (Ecological Heritage 1864)**:
   Màu sắc, hình khối và ngôn từ đều phản chiếu không gian xanh cổ kính của Thảo Cầm Viên Sài Gòn — khu vườn bách thảo và bách thú hơn 160 năm tuổi giữa lòng đô thị.
2. **Biên Tập Sinh Động (Editorial Elegance)**:
   Bố cục phóng khoáng như một tạp chí địa lý tự nhiên cao cấp, kết hợp nhịp nhàng giữa hình ảnh động vật hoang dã sống động và kiểu chữ giàu tính biểu cảm.
3. **Trải Nghiệm Tương Tác Hiện Đại (Modern & Frictionless)**:
   Cuộn mượt mà không giật cục (60fps), tương tác cử chỉ hợp tác 2 ngón tay trên bản đồ, các hiệu ứng thị giác tinh tế nhưng không bao giờ cản trở tốc độ tiếp cận nội dung.
4. **Tiếp Cận Toàn Diện (Inclusivity & Accessibility)**:
   Tôn trọng tiêu chuẩn WCAG 2.1 AA về độ tương phản, hỗ trợ đầy đủ 6 ngôn ngữ (Việt, Anh, Pháp, Trung, Nhật, Hàn) và tự động tắt chuyển động phức tạp khi người dùng kích hoạt `prefers-reduced-motion`.

---

## 2. Hệ Thống CSS Design Tokens Tổng Hợp

Dưới đây là bộ Design Tokens hoàn chỉnh sẵn sàng tích hợp vào `:root` mà không gây xung đột với các biến cũ:

```css
:root {
  /* ==========================================================================
     1. COLOR SYSTEM (NATURE-INSPIRED ECO PALETTE)
     ========================================================================== */
  /* Primary Green (Canopy Heritage) */
  --color-primary-base: #176b4b;
  --color-primary-dark: #124d39;
  --color-primary-deep: #0c2b1e;
  --color-primary-light: #4c9a6b;
  --color-primary-tint: #eaf3e9;

  /* Accent Amber (Wildlife & Sunshine) */
  --color-accent-amber: #e49d55;
  --color-accent-terracotta: #c86a28;
  --color-accent-tint: #fdf5ea;

  /* Background & Surfaces (Warm Parchment) */
  --color-bg-canvas: #f6f5ef;
  --color-bg-surface: #fffefa;
  --color-bg-elevated: #ffffff;
  --color-bg-glass: rgba(255, 254, 250, 0.92);
  --color-bg-overlay: rgba(12, 29, 20, 0.65);

  /* Text Colors & Hierarchy */
  --color-text-title: #173a29;
  --color-text-body: #334a3e;
  --color-text-muted: #6a7a70;
  --color-text-subtle: #8c9c92;
  --color-text-inverse: #ffffff;

  /* Borders & Dividers */
  --color-border-subtle: #e7eae1;
  --color-border-strong: #cdd7c8;
  --color-border-focus: #176b4b;

  /* Semantic Status Indicators */
  --color-status-online: #388e3c;
  --color-status-offline: #d97724;
  --color-status-gps-live: #1e88e5;
  --color-status-error: #c62828;
  --color-status-warning: #f9a825;

  /* ==========================================================================
     2. TYPOGRAPHY SYSTEM
     ========================================================================== */
  --font-family-sans: 'Zoo Sans', 'Noto Sans CJK SC', 'Noto Sans CJK JP', 'Noto Sans CJK KR', system-ui, sans-serif;
  
  /* Fluid Heading & Text Sizing */
  --type-display-hero: clamp(2.8rem, 5.5vw, 4.8rem);
  --type-section-title: clamp(1.75rem, 3.2vw, 2.4rem);
  --type-card-title: clamp(1.15rem, 1.8vw, 1.35rem);
  --type-text-lead: clamp(0.92rem, 1.2vw, 1.05rem);
  --type-text-body: 0.92rem;
  --type-text-small: 0.8rem;
  --type-text-eyebrow: 0.68rem;
  --type-text-btn: 0.88rem;

  /* ==========================================================================
     3. SPACING & LAYOUT SYSTEM (8-PT SCALE)
     ========================================================================== */
  --space-2xs: 4px;
  --space-xs: 8px;
  --space-sm: 12px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 72px;

  --container-max-desktop: 1240px;
  --container-content-narrow: 880px;

  /* ==========================================================================
     4. RADII & SHADOWS (ORGANIC SHAPES)
     ========================================================================== */
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --radius-xl: 28px;
  --radius-pill: 9999px;

  --shadow-subtle: 0 2px 8px rgba(18, 45, 30, 0.04);
  --shadow-card: 0 8px 24px rgba(23, 58, 41, 0.06);
  --shadow-hover: 0 16px 36px rgba(23, 58, 41, 0.11);
  --shadow-floating: 0 20px 60px rgba(12, 35, 23, 0.16);

  /* Transitions */
  --transition-fast: 0.18s cubic-bezier(0.2, 0.8, 0.2, 1);
  --transition-normal: 0.28s cubic-bezier(0.2, 0.8, 0.2, 1);
  --transition-smooth: 0.45s cubic-bezier(0.16, 1, 0.3, 1);
}
```

---

## 3. Kiến Trúc 7 Section Đồng Nhất (Design Consistency Matrix)

| Section | Tiêu đề Visual | Bảng màu chủ đạo | Typography nổi bật | Điểm nhấn tương tác |
| :---: | :--- | :--- | :--- | :--- |
| **01. Hero** | Lời Chào Di Sản 1864 | Gradient Sương mù & Xanh ngọc | `--type-display-hero` (Lớn, đậm nét) | 2 Nút Quick Pill CTAs, chỉ báo cuộn nhẹ |
| **02. Animals** | Thế Giới Cư Dân | Nền kem ngà, card trắng nổi | Eyebrow + Tên thú H3 + Tên khoa học | **Sticky Storytelling** (Cột ảnh ghim) |
| **03. Audio** | 3 Phương Thức Nghe | 1 Thẻ Xanh đậm tương phản + 2 Thẻ kem | Số đếm lớn `01, 02, 03` in nổi | Hover card nhấc bổng 4px, icon phát sáng |
| **04. Map** | Bản Đồ Số & GPS | Khung canvas OSM + Nút nổi trắng/cam | Trạng thái Live GPS, Khoảng cách mét | Cử chỉ 2 ngón tay, Marker pulse sao vàng ⭐ |
| **05. Routes** | Gợi Ý Tuyến Đi | Thẻ kem ngà viền xanh nhạt | Huy hiệu thời lượng phút (`~36 phút`) | Danh sách trạm nối chấm, link mở trạm đầu |
| **06. Offline** | Chuẩn Bị Tải Gói | Dải chuyển màu tự nhiên ấm | Tên 6 ngôn ngữ in hoa trang trọng | 6 Mã QR SVG sắc nét, nút tải máy này |
| **07. Guide** | Cẩm Nang & Trợ Giúp | Nền trắng thẻ tối giản | Thẻ `<details>` tiêu chuẩn hỏi đáp | Mở/đóng accordion mượt mà, cam kết bảo mật |

---

## 4. Kiểm Toán Sự Đồng Nhất (Design Consistency Audit)

- **Tính liên kết màu sắc**: 100% các nút chính và trạng thái active đều quy về `--color-primary-base` (`#176b4b`), tạo sự nhận diện duy nhất và không bị phân mảnh như bản cũ.
- **Tính liên kết hình khối**: Toàn bộ các thẻ đều thống nhất bo góc `border-radius: 20px` (`--radius-lg`) và các nút bấm bo cong dạng con nhộng (`--radius-pill`), xóa bỏ hoàn toàn sự lộn xộn giữa nút vuông 6px và nút tròn 999px trước đây.
- **Tính nhất quán Typography**: Thống nhất dùng font nhúng `Zoo Sans` với phân cấp chặt chẽ: `H1` (duy nhất Hero) -> `H2` (7 Section) -> `H3` (Cards).

---

## 5. Những Điểm Cần Lưu Ý Khi Triển Khai (Key Implementation Cautions)

1. **Không ghi đè đột ngột CSS toàn cục**:
   - Khi áp dụng các token mới vào Phase 4, cần bổ sung có chọn lọc vào `frontend/src/app/index.css` dưới dạng các class mới có tiền tố rõ ràng (`.tcv-section`, `.tcv-card`...) hoặc cập nhật lại giá trị biến `:root`, đảm bảo không làm vỡ giao diện của trang Quản trị (`AdminView.jsx`, `AnalyticsDashboard.jsx`).
2. **Kiểm tra khả năng hiển thị tiếng Trung / Nhật / Hàn**:
   - Đảm bảo font-family luôn khai báo kèm các font CJK tiêu chuẩn để tên ngôn ngữ trên các mã QR hiển thị trang trọng, chính xác.
3. **Thao tác cử chỉ bản đồ**:
   - Khung chứa bản đồ phải có cơ chế hiển thị overlay chỉ dẫn cử chỉ hợp tác 2 ngón tay một cách nhẹ nhàng, không gây che khuất tầm nhìn của du khách.
