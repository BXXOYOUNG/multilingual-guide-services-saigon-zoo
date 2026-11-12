# TCV Visual Design System – 03. Spacing & Layout System

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Tài liệu**: Quy chuẩn khoảng cách, bố cục lưới và hình khối (Spacing & Layout Tokens)  
> **Phương pháp**: 8-Point Grid System + Fluid Container Widths

---

## 1. Thang Đo Khoảng Cách (8-Point Spacing Scale)

Toàn bộ khoảng cách lề (`margin`), khoảng đệm (`padding`) và khoảng cách giữa các phần tử (`gap`) được quy chuẩn theo bội số của 4px và 8px:

| Token Name | Giá trị Pixel | Giá trị REM | Trường hợp áp dụng |
| :--- | :--- | :--- | :--- |
| `--space-2xs` | 4px | 0.25rem | Khoảng cách icon và chữ nhỏ, vạch chỉ báo. |
| `--space-xs` | 8px | 0.5rem | Gap giữa các nút tag, padding trong badge. |
| `--space-sm` | 12px | 0.75rem | Khoảng đệm bên trong thẻ nhỏ, gap danh sách. |
| `--space-md` | 16px | 1.0rem | Padding chuẩn của card di động, khoảng cách form. |
| `--space-lg` | 24px | 1.5rem | Padding của card lớn trên desktop, khoảng cách cột. |
| `--space-xl` | 32px | 2.0rem | Lề phân tách giữa các khối con trong section. |
| `--space-2xl`| 48px | 3.0rem | Khoảng đệm section trên mobile / tablet. |
| `--space-3xl`| 72px | 4.5rem | Khoảng cách giữa các Section chính trên desktop. |
| `--space-4xl`| 96px | 6.0rem | Khoảng đệm Hero và khoảng thở lớn. |

---

## 2. Chiều Rộng Khung Chứa (Container Widths)

Không gò bó trong container hẹp của mobile, hệ thống mở rộng đa tầng:
- `--container-max-desktop`: `1240px` (Chiều rộng tối đa cho màn hình lớn desktop).
- `--container-content-narrow`: `880px` (Chiều rộng tối ưu cho văn bản đọc, species catalog và cẩm nang).
- `--container-padding-mobile`: `16px` (Khoảng đệm mép màn hình điện thoại).
- `--container-padding-desktop`: `clamp(24px, 4vw, 48px)` (Khoảng đệm thích ứng màn hình lớn).

---

## 3. Hệ Thống Lưới (Responsive Grid System)

- **Desktop (>= 1024px)**: Lưới 12 cột linh hoạt (`grid-template-columns: repeat(12, 1fr)`) với gap 24px:
  - Hero: 7 cột cho Text & CTA + 5 cột cho Hình ảnh lớn.
  - Section Động vật Sticky: 5 cột cho Khung Pinned Visual + 7 cột cho Thẻ lướt.
  - Section 3 Cách nghe Audio: 3 cột đều nhau (mỗi cột 4 span).
  - Section Lộ trình: 3 cột đều nhau (mỗi cột 4 span).
  - Section Mã QR Offline: 6 cột (mỗi cột 2 span) hoặc lưới ngang 6 thẻ.
- **Tablet (768px - 1023px)**: Lưới 2 cột hoặc 3 cột với gap 16px.
- **Mobile (< 768px)**: Lưới 1 cột dọc hoặc thẻ trượt ngang `scroll-snap-type: x mandatory` với gap 12px.

---

## 4. Tỷ Lệ Khung Hình Ảnh (Image Aspect Ratios)

Bảo đảm hình ảnh động vật và bản đồ luôn giữ tỷ lệ chuẩn mà không bị méo hình:
- **Hero Landscape**: `16 / 9` hoặc `48% 0 0 48%` bo góc hữu cơ bất đối xứng.
- **Animal Showcase Card**: `4 / 3` (Tỷ lệ tiêu chuẩn của nhiếp ảnh thiên nhiên).
- **Animal Square Avatar**: `1 / 1` (Dành cho thumbnail danh sách nhỏ).
- **Interactive Map Canvas**:
  - Desktop: Chiều cao tối thiểu `580px` đến `640px`.
  - Mobile: Chiều cao `420px` (Tỷ lệ cân đối giữa bản đồ và các nút điều khiển).

---

## 5. Bo Góc (Border Radius) & Đổ Bóng (Box Shadows)

### 5.1. Bo Góc Hữu Cơ (Organic Radii)
- `--radius-sm`: `8px` (Badge, tag, input).
- `--radius-md`: `14px` (Nút bấm, card nhỏ, ảnh thumbnail).
- `--radius-lg`: `20px` (Card lộ trình, card thuyết minh, card động vật).
- `--radius-xl`: `28px` (Khung container của từng Section lớn, Hero section).
- `--radius-pill`: `9999px` (Nút CTA hình con nhộng bo tròn thân thiện).

### 5.2. Đổ Bóng Sinh Thái Đa Tầng (Diffused Soft Shadows)
Mô phỏng ánh sáng mặt trời tự nhiên tán xạ qua vòm lá:
- `--shadow-subtle`: `0 2px 8px rgba(18, 45, 30, 0.04)` (Thẻ tĩnh trên nền giấy ngà).
- `--shadow-card`: `0 8px 24px rgba(23, 58, 41, 0.06)` (Thẻ mặc định khi hiển thị).
- `--shadow-hover`: `0 16px 36px rgba(23, 58, 41, 0.11)` (Khi rê chuột vào thẻ động vật, lộ trình).
- `--shadow-floating`: `0 20px 60px rgba(12, 35, 23, 0.16)` (Modal dialog chi tiết thú, Sticky Header khi cuộn).
