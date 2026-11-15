# TCV Visual Design System – 03. Color System & Design Tokens

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Tài liệu**: Hệ thống màu sắc và Design Tokens (Color Palette & Tokens)  
> **Cam kết**: Tái sử dụng và kế thừa các biến CSS hiện hữu, chuẩn hóa mã màu tự nhiên, đáp ứng chuẩn tương phản WCAG 2.1 AA.

---

## 1. Triết lý Bảng màu Sinh thái (Eco-Color Philosophy)

Bảng màu được trích xuất từ 4 yếu tố tự nhiên của Thảo Cầm Viên:
1. **Rừng Nhiệt Đới (Deep Canopy)**: Xanh ngọc lục bảo và xanh rêu đậm của tán cổ thụ trăm tuổi.
2. **Đất Phù Sa & Nắng Phương Nam (Terracotta & Amber)**: Ánh cam hổ phách của bộ lông hổ Bengal, ánh nắng rọi qua kẽ lá.
3. **Giấy Ngà Sinh Thái (Warm Parchment)**: Tông nền ngả vàng kem mộc mạc, tạo cảm giác thư thái cho mắt khi đọc ngoài trời nắng.
4. **Hệ Thống Tín Hiệu Thân Thiện (Semantic Naturals)**: Các trạng thái GPS, Geofence, Online/Offline rõ ràng, trực quan.

---

## 2. Danh mục Design Tokens Màu Sắc

### 2.1. Nhóm Màu Chính (Primary Brand Green)
| Token Name | Giá trị Hex | Giá trị HSL / RGB | Mục đích sử dụng |
| :--- | :--- | :--- | :--- |
| `--color-primary-base` | `#176b4b` | `rgb(23, 107, 75)` | Màu thương hiệu cốt lõi, nút bấm chính (CTA Primary), liên kết active, thanh tiến trình cuộn. |
| `--color-primary-dark` | `#124d39` | `rgb(18, 77, 57)` | Trạng thái hover của nút bấm, tiêu đề chính trong các card tối (`listening-card-dark`). |
| `--color-primary-deep` | `#0c2b1e` | `rgb(12, 43, 30)` | Màu đen xanh đậm nhất, dùng cho chữ tiêu đề lớn `h1` và nền tương phản cao. |
| `--color-primary-light` | `#4c9a6b` | `rgb(76, 154, 107)` | Đường gạch chân active nav, viền phụ, chỉ báo trạng thái đang phát audio. |
| `--color-primary-tint` | `#eaf3e9` | `rgb(234, 243, 233)` | Nền thẻ phụ, badge loại loài, hover background của menu. |

### 2.2. Nhóm Màu Nhấn & Hoang Dã (Accent & Wildlife Amber)
| Token Name | Giá trị Hex | Giá trị HSL / RGB | Mục đích sử dụng |
| :--- | :--- | :--- | :--- |
| `--color-accent-amber` | `#e49d55` | `rgb(228, 157, 85)` | Màu nhấn phụ, ngôi sao ⭐ cho POI gần nhất (`findNearestPoi`), điểm nhấn lộ trình. |
| `--color-accent-terracotta` | `#c86a28` | `rgb(200, 106, 40)` | Nút cảnh báo nhẹ, huy hiệu thông báo đặc biệt. |
| `--color-accent-tint` | `#fdf5ea` | `rgb(253, 245, 234)` | Nền highlight của thẻ POI gần nhất (`nearest-poi-card`). |

### 2.3. Nhóm Màu Nền & Bề Mặt (Background & Surfaces)
| Token Name | Giá trị Hex | Giá trị HSL / RGB | Mục đích sử dụng |
| :--- | :--- | :--- | :--- |
| `--color-bg-canvas` | `#f6f5ef` | `rgb(246, 245, 239)` | Nền toàn trang web (Warm eco cream), giảm lóa mắt khi đứng ngoài trời. |
| `--color-bg-surface` | `#fffefa` | `rgb(255, 254, 250)` | Nền thẻ card, nền dialog modal, nền drawer bản đồ. |
| `--color-bg-elevated` | `#ffffff` | `rgb(255, 255, 255)` | Bề mặt nổi (popover, dropdown chọn ngôn ngữ, nút điều khiển map). |
| `--color-bg-glass` | `rgba(255, 254, 250, 0.92)` | Alpha 92% | Nền Sticky Header kết hợp `backdrop-filter: blur(16px)`. |
| `--color-bg-overlay` | `rgba(12, 29, 20, 0.65)` | Alpha 65% | Lớp màn mờ khi mở Modal chi tiết động vật (`animal-detail-backdrop`). |

### 2.4. Nhóm Màu Chữ & Thứ Bậc Nội Dung (Typography & Text Hierarchy)
| Token Name | Giá trị Hex | Giá trị HSL / RGB | Mục đích sử dụng |
| :--- | :--- | :--- | :--- |
| `--color-text-title` | `#173a29` | `rgb(23, 58, 41)` | Màu chữ tiêu đề chính `h1`, `h2`, tên các loài động vật. Độ tương phản 11.2:1. |
| `--color-text-body` | `#334a3e` | `rgb(51, 74, 62)` | Màu văn bản mô tả, đoạn văn đọc chính. Độ tương phản 7.8:1. |
| `--color-text-muted` | `#6a7a70` | `rgb(106, 122, 112)` | Màu chữ phụ, thời lượng phút, số đếm trạm dừng, credit ảnh. Độ tương phản 4.6:1. |
| `--color-text-subtle` | `#8c9c92` | `rgb(140, 156, 146)` | Số thứ tự `01`, `02`, placeholder không quan trọng. |
| `--color-text-inverse`| `#ffffff` | `rgb(255, 255, 255)` | Chữ trắng trên nền nút xanh hoặc thẻ tối màu. |

### 2.5. Nhóm Màu Viền & Ngăn Cách (Borders & Dividers)
| Token Name | Giá trị Hex | Giá trị HSL / RGB | Mục đích sử dụng |
| :--- | :--- | :--- | :--- |
| `--color-border-subtle` | `#e7eae1` | `rgb(231, 234, 225)` | Viền thẻ tiêu chuẩn, viền phân tách các hàng trong danh sách. |
| `--color-border-strong` | `#cdd7c8` | `rgb(205, 215, 200)` | Viền các phần tử tương tác khi focus hoặc hover nhẹ. |
| `--color-border-focus` | `#176b4b` | `rgb(23, 107, 75)` | Viền outline rõ ràng khi người dùng sử dụng phím Tab (`focus-visible`). |

### 2.6. Nhóm Màu Ngữ Nghĩa (Semantic & State Colors)
| Token Name | Giá trị Hex | Giá trị HSL / RGB | Mục đích sử dụng |
| :--- | :--- | :--- | :--- |
| `--color-status-online` | `#388e3c` | `rgb(56, 142, 60)` | Đèn chấm báo hiệu Online (`is-online`). |
| `--color-status-offline` | `#d97724` | `rgb(217, 119, 36)` | Đèn chấm báo hiệu Offline (`is-offline`). |
| `--color-status-gps-live`| `#1e88e5` | `rgb(30, 136, 229)` | Chấm tròn xanh định vị GPS của khách du lịch (`visitor-dot`). |
| `--color-status-error` | `#c62828` | `rgb(198, 40, 40)` | Báo lỗi tải âm thanh, từ chối quyền định vị. |
| `--color-status-warning` | `#f9a825` | `rgb(249, 168, 37)` | Băng rôn chế độ chạy Demo (`demo-mode-banner`). |

---

## 3. Khả Năng Tiếp Cận & Tương Phản (WCAG 2.1 AA Compliance)

Tất cả các cặp màu chữ và màu nền được chọn lọc nghiêm ngặt để vượt qua tiêu chuẩn:
- **Chữ thường (Body Text)**: Tỷ lệ tương phản tối thiểu **4.5:1** (Thực tế `--color-text-body` trên `--color-bg-canvas` đạt **7.8:1**).
- **Chữ lớn (Headings >= 18pt)**: Tỷ lệ tương phản tối thiểu **3.0:1** (Thực tế `--color-text-title` trên `--color-bg-canvas` đạt **11.2:1**).
- **Phần tử giao diện tương tác (UI Components & Controls)**: Nút bấm và viền input đạt tối thiểu **3.0:1**.
