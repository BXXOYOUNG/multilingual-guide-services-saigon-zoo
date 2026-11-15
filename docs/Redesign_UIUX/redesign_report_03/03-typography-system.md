# TCV Visual Design System – 03. Typography System

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Tài liệu**: Quy chuẩn hệ thống kiểu chữ (Typography System & Hierarchy)  
> **Nguyên tắc**: Tối ưu hiển thị tiếng Việt có dấu, đa ngôn ngữ CJK (Trung - Nhật - Hàn) và đọc rõ ràng trên mọi thiết bị.

---

## 1. Font Family & Khả Năng Hỗ Trợ Đa Ngôn Ngữ

Hệ thống kế thừa và chuẩn hóa font chữ nhúng cục bộ sẵn có trong dự án:

```css
:root {
  --font-family-sans: 'Zoo Sans', 'Noto Sans CJK SC', 'Noto Sans CJK JP', 'Noto Sans CJK KR', 'Microsoft YaHei', 'Yu Gothic', 'Malgun Gothic', system-ui, -apple-system, sans-serif;
  --font-family-mono: ui-monospace, 'SFMono-Regular', Menlo, Monaco, Consolas, monospace;
}
```

- **`Zoo Sans`**: Font chữ Noto Sans tự host (`src/assets/fonts/NotoSans.ttf`) với giấy phép mã nguồn mở SIL OFL.
  - Hỗ trợ 100% tiếng Việt với đầy đủ dấu thanh, dấu mũ, móc không bao giờ bị lỗi vỡ font (tofu).
  - Khả năng scale mượt mà từ Font Weight 300 (Light), 400 (Regular), 500 (Medium), 600 (SemiBold), 700 (Bold) đến 800 (ExtraBold).
- **Bộ font CJK dự phòng**: Đảm bảo du khách quốc tế sử dụng tiếng Trung, tiếng Nhật và tiếng Hàn luôn nhìn thấy chữ sắc nét, tự nhiên.

---

## 2. Thang Đo Cỡ Chữ (Type Scale & Fluid Sizing)

Áp dụng phương pháp kích thước linh hoạt (`clamp()`) để chữ tự động điều chỉnh theo kích thước màn hình mà không cần viết quá nhiều media queries giật cục:

| Cấp bậc (Hierarchy) | Token Name | Mobile Size | Desktop Size | Weight | Line Height | Letter Spacing | Mục đích sử dụng |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Display Title (Hero)**| `--type-display-hero` | `2.8rem` (44.8px) | `clamp(3.2rem, 5.5vw, 4.8rem)` | 600 | 1.15 | `-0.035em` | Tiêu đề lớn tại Section 01 Hero ("Khám phá vườn thú lâu đời..."). |
| **Section Heading (H2)**| `--type-section-title` | `1.75rem` (28px) | `clamp(1.85rem, 3.2vw, 2.4rem)` | 600 | 1.25 | `-0.025em` | Tiêu đề chính mở đầu mỗi Section trong 7 Section. |
| **Card Heading (H3)** | `--type-card-title` | `1.15rem` (18.4px) | `1.3rem` (20.8px) | 600 | 1.35 | `-0.02em` | Tên các loài động vật, tiêu đề thẻ lộ trình, thẻ audio. |
| **Subheading / Lead** | `--type-text-lead` | `0.92rem` (14.7px) | `1.05rem` (16.8px) | 400 | 1.65 | `normal` | Đoạn văn mở đầu dưới tiêu đề Hero và Section. |
| **Body Regular** | `--type-text-body` | `0.85rem` (13.6px) | `0.92rem` (14.7px) | 400 | 1.6 | `normal` | Văn bản đọc nội dung chi tiết, mô tả thú, FAQ, chính sách. |
| **Body Small** | `--type-text-small` | `0.75rem` (12px) | `0.8rem` (12.8px) | 400 | 1.55 | `normal` | Ghi chú trạm dừng, hướng dẫn tải offline, chi tiết phụ. |
| **Eyebrow / Badge** | `--type-text-eyebrow` | `0.65rem` (10.4px) | `0.72rem` (11.5px) | 800 | 1.4 | `+0.14em` | Nhãn phân loại trên đầu tiêu đề (in hoa: `THẢO CẦM VIÊN 1864`). |
| **Navigation & Links** | `--type-text-nav` | `0.78rem` (12.5px) | `0.82rem` (13.1px) | 650 | 1.4 | `-0.01em` | Các liên kết trên Sticky Header, Footer links. |
| **Button Text** | `--type-text-btn` | `0.82rem` (13.1px) | `0.88rem` (14px) | 700 | 1 | `normal` | Chữ trên nút bấm hành động chính và phụ. |
| **Caption & Credit** | `--type-text-caption` | `0.62rem` (10px) | `0.68rem` (10.8px) | 400 | 1.5 | `normal` | Thông tin bản quyền ảnh `AnimalImageCredit`. |

---

## 3. Quy Tắc Sử Dụng Kiểu Chữ (Editorial Formatting Rules)

1. **Phân cấp Tiêu đề Chặt Chẽ (Heading Semantics)**:
   - Mỗi trang chủ chỉ có duy nhất một thẻ `<h1>` nằm tại Section 01 Hero.
   - Mỗi Section tiếp theo (02 đến 07) bắt buộc mở đầu bằng thẻ `<h2>`.
   - Các thẻ card con bên trong (thẻ thú, thẻ lộ trình) sử dụng thẻ `<h3>`.
2. **Quy tắc Font Weight**:
   - `400 (Regular)`: Dành riêng cho các đoạn văn bản dài cần độ thoáng mắt khi đọc.
   - `600 (SemiBold)`: Dành cho tiêu đề chính, tạo vẻ trang trọng, tin cậy của một cơ quan nghiên cứu bảo tồn.
   - `700 & 800 (Bold & ExtraBold)`: Dành cho nhãn Eyebrow và số đếm trạm dừng `01`, `02`...
3. **Độ Dài Dòng Văn Bản Tối Ưu (Line Length & Readability)**:
   - Đoạn văn mô tả không được trải dài toàn bộ chiều rộng màn hình lớn (gây mỏi mắt khi đọc). Bắt buộc giới hạn `max-width: 65ch` (khoảng 65 ký tự trên một dòng).
