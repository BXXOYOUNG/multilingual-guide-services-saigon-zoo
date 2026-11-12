# TCV UX Redesign – 02. Wireframes Specification (Desktop, Tablet & Mobile)

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Tài liệu**: Bản vẽ khung giao diện (Wireframes) cho Desktop, Tablet và Mobile  
> **Mục tiêu**: Thể hiện trực quan bố cục section, thứ bậc nội dung, vị trí hình ảnh, CTAs, sticky storytelling và hành vi cuộn.

---

## 1. Wireframe Desktop (Màn hình lớn >= 1024px)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [LOGO 1864]   Khám phá   Thuyết minh   Bản đồ   Lộ trình   Tải Offline   [VI ▾] [● Online] │ <-- Sticky Header (72px)
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [Top Scroll Progress Bar 2.5px ══════════════════════════════════════════════════════] │
│                                                                                        │
│ SECTION 01: HERO WELCOME                                                               │
│ ┌───────────────────────────────────────┐ ┌──────────────────────────────────────────┐ │
│ │ [Eyebrow] THẢO CẦM VIÊN SÀI GÒN       │ │                                          │ │
│ │ # KHÁM PHÁ VƯỜN THÚ LÂU ĐỜI           │ │         [ẢNH LỚN CHÚ VOI CHÂU Á]         │ │
│ │   BẰNG ÂM THANH SỐNG ĐỘNG             │ │         (Wild Photography 1864)          │ │
│ │                                       │ │                                          │ │
│ │ Thuyết minh tự động bằng GPS...       │ │ ┌──────────────────────────────────────┐ │ │
│ │                                       │ │ │ "1864 - Saigon Zoo & Botanical Gard" │ │ │
│ │ [Khám phá bản đồ ↗] [Lộ trình xem ▾]  │ │ └──────────────────────────────────────┘ │ │
│ │                                       │ │                                          │ │
│ │ ↓ Cuộn để khám phá                    │ │ Credit: Charles J. Sharp (CC BY-SA 4.0)  │ │
│ └───────────────────────────────────────┘ └──────────────────────────────────────────┘ │
│                                                                                        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 02: ANIMAL DISCOVERY (STICKY STORYTELLING + CATALOG)                           │
│ ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ [Tiêu đề Section] GẶP GỠ CÁC CƯ DÂN RỪNG XANH                                      │ │
│ └────────────────────────────────────────────────────────────────────────────────────┘ │
│ ┌────────────────────────────────────────┐ ┌─────────────────────────────────────────┐ │
│ │ [PINNED / STICKY VIEWPORT]             │ │ [SCROLLING ANIMAL CARDS]                │ │
│ │                                        │ │                                         │ │
│ │   [ẢNH ĐỘNG VẬT TIÊU BIỂU FOCUS]       │ │ ┌─────────────────────────────────────┐ │ │
│ │   (Lướt qua Voi, Hổ, Hươu, Hà mã)      │ │ │ 01. Voi Châu Á (Asian Elephant)     │ │ │
│ │                                        │ │ │ "Loài động vật có vú trên cạn lớn..."│ │ │
│ │   Tên khoa học: Elephas maximus        │ │ │ [Xem chi tiết ↗] [Vị trí bản đồ]    │ │ │
│ │   Năm sinh / Nguồn gốc                 │ │ └─────────────────────────────────────┘ │ │
│ │                                        │ │ ┌─────────────────────────────────────┐ │ │
│ │                                        │ │ │ 02. Hổ Bengal (Bengal Tiger)        │ │ │
│ │                                        │ │ │ "Chúa sơn lâm dũng mãnh..."         │ │ │
│ │                                        │ │ │ [Xem chi tiết ↗] [Vị trí bản đồ]    │ │ │
│ │                                        │ │ └─────────────────────────────────────┘ │ │
│ │                                        │ │ (Tiếp tục cuộn: 03. Hươu, 04. Hà mã)   │ │ │
│ └────────────────────────────────────────┘ └─────────────────────────────────────────┘ │
│ ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ [SPECIES CATALOG GRID] - Toàn bộ các loài động vật trong hệ sinh thái (API Catalog)│ │
│ │ [Card Thú 1]    [Card Thú 2]    [Card Thú 3]    [Card Thú 4]    [Card Thú 5]...    │ │
│ └────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 03: AUDIO EXPERIENCE (3 CHẾ ĐỘ THUYẾT MINH)                                    │
│ ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ [Eyebrow] CÔNG NGHỆ THUYẾT MINH      ## 3 CÁCH ĐỂ LẮNG NGHE CÂU CHUYỆN RỪNG XANH   │ │
│ └────────────────────────────────────────────────────────────────────────────────────┘ │
│ ┌───────────────────────────┐ ┌───────────────────────────┐ ┌───────────────────────────┐ │
│ │ [01] TRỰC TIẾP TRÊN WEB   │ │ [02] TỰ ĐỘNG THEO GPS     │ │ [03] TẢI GÓI OFFLINE     │ │
│ │ Nghe ngay trên trình duyệt│ │ Tự động phát khi bạn đi   │ │ Tải trước về máy, không │ │
│ │ khi bấm vào từng điểm.    │ │ vào vùng gần chuồng thú.  │ │ tốn dung lượng 4G.       │ │
│ │ [Nghe thử trên bản đồ ↗]  │ │ [Bật định vị & nghe ↗]    │ │ [Xem các gói tải ↗]     │ │
│ └───────────────────────────┘ └───────────────────────────┘ └───────────────────────────┘ │
│                                                                                        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 04: INTERACTIVE MAP (BẢN ĐỒ SỐ TÍCH HỢP GEOFENCE)                              │
│ ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ [Thanh trạng thái: ● GPS Hoạt động | 32 Điểm thuyết minh | [Bật Thuyết Minh Tự Động]│ │
│ ├────────────────────────────────────────────────────────┬───────────────────────────┤ │
│ │                                                        │ [POI DRAWER CHI TIẾT]     │ │
│ │              [KHUNG BẢN ĐỒ MAPLIBRE GL]                │ Chuồng Voi Châu Á         │ │
│ │                                                        │                           │ │
│ │       📍 Hổ Bengal          📍 Voi (⭐ Gần nhất)       │ [► 00:00 ───●─── 02:45]   │ │
│ │                                                        │ Ngôn ngữ: TIẾNG VIỆT      │ │
│ │                 🔵 (Vị trí bạn)                        │                           │ │
│ │                                     📍 Hươu Cao Cổ     │ [Mô phỏng đến nơi (Demo)] │ │
│ │                                                        │ [Xem chi tiết loài này ↗] │ │
│ ├────────────────────────────────────────────────────────┴───────────────────────────┤ │
│ │ [Cử chỉ: Dùng Ctrl + Lăn chuột để Zoom]               [Mở bản đồ toàn màn hình ↗]  │ │
│ └────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 05: SUGGESTED ROUTES (GỢI Ý LỘ TRÌNH THAM QUAN)                                │
│ ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ [Eyebrow] KHÁM PHÁ THÔNG MINH        ## LỘ TRÌNH THAM QUAN ĐỀ XUẤT                │ │
│ └────────────────────────────────────────────────────────────────────────────────────┘ │
│ ┌───────────────────────────┐ ┌───────────────────────────┐ ┌───────────────────────────┐ │
│ │ [Lộ trình 01] KHÁM PHÁ NHANH│ │ [Lộ trình 02] CHO GIA ĐÌNH│ │ [Lộ trình 03] TRỌN VẸN   │ │
│ │ 3 Điểm dừng · ~36 phút    │ │ 5 Điểm dừng · ~60 phút    │ │ 8 Điểm dừng · ~96 phút    │ │
│ │ Phù hợp du khách ít giờ   │ │ Đường đi râm mát, thú hiền│ │ Trải nghiệm đầy đủ nhất   │ │
│ │ 01. Voi -> 02. Hổ -> 03...│ │ 01. Voi -> 02. Hươu -> ...│ │ 01. Voi -> 02. Hà mã...   │ │
│ │ [Bắt đầu lộ trình này ↗]  │ │ [Bắt đầu lộ trình này ↗]  │ │ [Bắt đầu lộ trình này ↗]  │ │
│ └───────────────────────────┘ └───────────────────────────┘ └───────────────────────────┘ │
│                                                                                        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 06: OFFLINE AUDIO PREPARATION (QUÉT QR TẢI GÓI ÂM THANH)                       │
│ ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ [Eyebrow] CHUẨN BỊ TRƯỚC CHUYẾN ĐI   ## TẢI GÓI ÂM THANH OFFLINE 6 NGÔN NGỮ       │ │
│ └────────────────────────────────────────────────────────────────────────────────────┘ │
│ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐  │
│ │  [QR SVG VI]  │ │  [QR SVG EN]  │ │  [QR SVG FR]  │ │ [QR SVG ZH]   │ │ [QR JA / KO]  │  │
│ │   Tiếng Việt  │ │    English    │ │    Français   │ │    简体中文    │ │  日本語/한국어 │  │
│ │ [Tải gói này] │ │ [Tải gói này] │ │ [Tải gói này] │ │ [Tải gói này] │ │ [Tải gói này] │  │
│ └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘  │
│                                                                                        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ SECTION 07: GETTING STARTED & VISITOR GUIDE (CẨM NANG & FAQ)                           │
│ ┌───────────────────────────────────────────────┬────────────────────────────────────┐ │
│ │ ## CÂU HỎI THƯỜNG GẶP (FAQ)                   │ ## MẸO & QUYỀN RIÊNG TƯ            │ │
│ │ [▸] Ứng dụng có cần kết nối mạng liên tục?    │ 🎧 Mang theo tai nghe để nghe rõ   │ │
│ │ [▸] Làm sao để tự động phát thuyết minh?      │ 📍 Bật GPS khi vào cổng            │ │
│ │ [▸] Tôi có thể nghe lại khi đã rời khỏi vườn? │ 🔒 Quyền riêng tư: Tọa độ chỉ xử lý│ │
│ │                                               │    trên máy, không lưu máy chủ     │ │
│ │ [Đến trang Cẩm nang đầy đủ ↗]                 │ [Cổng quản trị nội dung /admin ↗]  │ │
│ └───────────────────────────────────────────────┴────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ FOOTER: Saigon Zoo & Botanical Gardens (Est. 1864) · All rights reserved · Privacy     │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Wireframe Tablet (Màn hình 768px - 1023px)

- **Header**: Logo rút gọn, Menu chính hiển thị các icon kèm chữ ngắn; Nút chọn ngôn ngữ giữ nguyên.
- **Section 01 (Hero)**: Khối hình ảnh Voi Châu Á chuyển xuống nằm dưới khối chữ tiêu đề và CTAs (1 cột dọc lớn).
- **Section 02 (Animals)**: Khối Sticky Storytelling hiển thị dạng 2 cột tỷ lệ 50/50: Cột trái ảnh lớn, cột phải nội dung mô tả có thể cuộn.
- **Section 03 (Audio)**: 3 Thẻ phương thức nghe dàn trải thành 2 dòng (Thẻ 1 & 2 ở dòng trên, Thẻ 3 chiếm trọn chiều rộng dòng dưới).
- **Section 04 (Map)**: Chiều cao bản đồ đặt 500px, Drawer thông tin POI hiển thị dạng Bottom Sheet trượt từ đáy lên khi người dùng chạm vào marker.
- **Section 05 (Routes)**: Các thẻ lộ trình hiển thị dạng lưới 2 cột.
- **Section 06 (Offline)**: 6 Mã QR chia thành 2 hàng, mỗi hàng 3 mã QR rõ ràng.

---

## 3. Wireframe Mobile (Màn hình < 768px)

```
┌──────────────────────────────────────────┐
│ [LOGO]               [VI ▾]  [●]  [☰ Menu]│ <-- Mobile Sticky Header (60px)
├──────────────────────────────────────────┤
│ [Scroll Progress 2px ══════════════════] │
│                                          │
│ SECTION 01: HERO                         │
│ [Eyebrow] THẢO CẦM VIÊN 1864             │
│ # KHÁM PHÁ VƯỜN THÚ                      │
│   BẰNG ÂM THANH SỐNG ĐỘNG                │
│                                          │
│ [ẢNH CHÚ VOI 100% WIDTH BO GÓC ĐẸP]      │
│                                          │
│ [Khám phá bản đồ ↗] (Button Full Width)  │
│ [Lộ trình tham quan] (Button Thứ cấp)    │
│                                          │
│ ↓ Cuộn để khám phá                       │
├──────────────────────────────────────────┤
│ SECTION 02: GẶP GỠ CÁC CƯ DÂN            │
│ (Horizontal Swipeable Carousel Cards)    │
│ ┌──────────────────────────────────────┐ │
│ │ [ẢNH VOI] 01. Voi Châu Á             │ │
│ │ "Loài thú ăn cỏ lớn nhất vườn..."    │ │
│ │ [Nghe thử ♫] [Xem vị trí map ↗]      │ │
│ └──────────────────────────────────────┘ │
│ ◀ Quẹt ngang để xem tiếp các con vật ▶   │
│                                          │
│ [Danh mục tất cả các loài (Grid 2 cột)]  │
├──────────────────────────────────────────┤
│ SECTION 03: 3 CÁCH NGHE THUYẾT MINH      │
│ ┌──────────────────────────────────────┐ │
│ │ 01. Trực tiếp trên Web               │ │
│ ├──────────────────────────────────────┤ │
│ │ 02. Tự động phát khi đến gần (GPS)   │ │
│ ├──────────────────────────────────────┤ │
│ │ 03. Tải về nghe Offline              │ │
│ └──────────────────────────────────────┘ │
├──────────────────────────────────────────┤
│ SECTION 04: BẢN ĐỒ SỐ                    │
│ [● GPS Sẵn sàng]  [Bật Thuyết Minh Tự Động]│
│ ┌──────────────────────────────────────┐ │
│ │                                      │ │
│ │      [BẢN ĐỒ MAPLIBRE GL 420PX]      │ │
│ │                                      │ │
│ │   (Dùng 2 ngón tay để di chuyển)     │ │
│ └──────────────────────────────────────┘ │
│ [Thẻ POI Gần Bạn Nhất Nổi Trên Bản Đồ]   │
│ [Mở Bản Đồ Toàn Màn Hình ↗]             │
├──────────────────────────────────────────┤
│ SECTION 05: GỢI Ý LỘ TRÌNH               │
│ (Horizontal Card Snap hoặc List Dọc)     │
│ ┌──────────────────────────────────────┐ │
│ │ [Tour 01] KHÁM PHÁ NHANH (36 Phút)   │ │
│ │ 3 Điểm dừng · Voi -> Hổ -> Hươu      │ │
│ │ [Bắt đầu lộ trình này ↗]             │ │
│ └──────────────────────────────────────┘ │
├──────────────────────────────────────────┤
│ SECTION 06: TẢI OFFLINE                  │
│ [Mã QR Tiếng Việt / English Lớn]         │
│ [Nút Tải gói âm thanh về máy này 💾]     │
├──────────────────────────────────────────┤
│ SECTION 07: CẨM NANG & HỎI ĐÁP           │
│ [▸ Câu hỏi thường gặp 1]                 │
│ [▸ Câu hỏi thường gặp 2]                 │
│ 🔒 Tọa độ GPS an toàn, bảo mật           │
├──────────────────────────────────────────┤
│ FOOTER: TCV Saigon Zoo · 1864 · Admin    │
└──────────────────────────────────────────┘
```

---

## 4. Bảng So Sánh và Đảm Bảo Đáp Ứng Ràng Buộc

| Tiêu chí | Desktop Wireframe | Mobile Wireframe | Đảm bảo an toàn kỹ thuật |
| :--- | :--- | :--- | :--- |
| **Cử chỉ Bản đồ** | Ctrl + Wheel để zoom, Drag bình thường | **2-finger pan**, cuộn 1 ngón trôi trang tự nhiên | Không xung đột cử chỉ (Giải quyết triệt để R-01). |
| **Bản đồ Canvas** | Chiều cao 620px, Drawer nằm cạnh phải | Chiều cao 420px, Drawer dạng Bottom Sheet | Không destroy/recreate MapLibre khi cuộn (Giải quyết R-02). |
| **Audio Player** | Player thanh lịch trong Drawer | Player gọn gàng với nút Play lớn | Sử dụng đúng HTML5 Audio refs sẵn có (Giải quyết R-04). |
| **QR Packages** | Lưới 6 ngôn ngữ nằm ngang | Thẻ vuốt ngang hoặc chọn gói kèm nút tải trực tiếp | Giữ nguyên payload format `TCV-PACKAGE:...` (Giải quyết R-03). |
| **Khả năng tiếp cận** | Navigation Indicator cạnh sườn | Sticky Header + Hamburger Menu | Đảm bảo focus bàn phím & semantic HTML (Giải quyết R-07). |
