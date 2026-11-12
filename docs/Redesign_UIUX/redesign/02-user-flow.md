# TCV UX Redesign – 02. User Flow Design

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Tài liệu**: Thiết kế luồng người dùng (User Flow Design)  
> **Mục tiêu**: Đảm bảo luồng khám phá tự nhiên theo chiều dọc, đồng thời bảo vệ 100% khả năng truy cập trực tiếp và phi tuyến tính.

---

## 1. Nguyên tắc thiết kế User Flow

1. **Khám phá liên tục (Continuous Scrolling Discovery)**: Du khách lần đầu truy cập có thể cuộn từ trên xuống dưới để tìm hiểu toàn bộ tiện ích mà không bị ép buộc chuyển trang liên tục.
2. **Không ép buộc tuần tự (Non-linear & Free Traversal)**: Du khách có thể nhảy ngay đến bất kỳ chức năng nào thông qua Sticky Navigation Header, các nút CTA tắt trên Hero, hoặc gõ trực tiếp URL.
3. **Bảo toàn khả năng truy cập trực tiếp (Direct Access Preservation)**: Giữ trọn vẹn toàn bộ các Route con (`/map`, `/explore`, `/itinerary`, `/guide`, `/admin`) phục vụ mã QR in thực tế tại Thảo Cầm Viên.

---

## 2. Chi tiết 5 Luồng Người Dùng Chính

---

### Luồng 1: Luồng Khám Phá Chính (Primary Discovery Flow)

Dành cho du khách mới, muốn tìm hiểu tổng quan về Thảo Cầm Viên trước khi quyết định đi đâu hoặc nghe gì.

```
[Du khách truy cập Trang Chủ "/"]
       │
       ▼
[Section 01: Hero Welcome]
       │ (Cuộn xuống tự nhiên)
       ▼
[Section 02: Animal Discovery] ──(Bấm vào con vật)──> [Mở Modal Chi Tiết Động Vật]
       │                                                         │
       │ (Tiếp tục cuộn)                               (Bấm "Xem trên bản đồ")
       ▼                                                         │
[Section 03: Audio Experience]                                   │
       │                                                         │
       │ (Tiếp tục cuộn)                                         │
       ▼                                                         ▼
[Section 04: Interactive Map] <──────────────────────────────────┘
       │ (Tương tác bản đồ bằng 2 ngón tay, nghe thử audio POI)
       │
       │ (Tiếp tục cuộn)
       ▼
[Section 05: Suggested Routes] ──(Chọn lộ trình 3/5/8 điểm)──> [Tự động cuộn/focus trạm 01 trên Map]
       │
       │ (Tiếp tục cuộn)
       ▼
[Section 06: Offline Audio Preparation] ──(Quét/Click QR ngôn ngữ)──> [Tải gói âm thanh về máy]
       │
       │ (Tiếp tục cuộn)
       ▼
[Section 07: Getting Started / Guide] ──(Xem FAQ, Mẹo, Quyền riêng tư)
       │
       ▼
[Footer & Bản quyền di sản]
```

---

### Luồng 2: Luồng Truy Cập Trực Tiếp Vào Map (Direct Map Access Flow)

Áp dụng cho du khách đang có mặt trực tiếp tại Thảo Cầm Viên, cần xem ngay bản đồ và định vị xem mình đang đứng ở đâu.

**Có 3 phương thức tiếp cận không cản trở:**
1. **Qua URL độc lập hoặc QR Code**:
   - Du khách quét mã QR tại chuồng voi dẫn tới `/map?poi=TCV-AN-005`.
   - Trình duyệt điều hướng thẳng đến `MapView` (với component `InteractiveMap` chiếm trọn màn hình).
   - Tự động zoom vào tọa độ Voi Châu Á và mở ngay Drawer chi tiết kèm nút phát audio.
2. **Qua Sticky Navigation Header**:
   - Ở bất kỳ vị trí nào trên trang chủ, du khách bấm vào mục **"Bản đồ" (Map)** trên Header.
   - Trang thực hiện smooth scroll ngay lập tức xuống Section 04 `#map-section` với offset header chuẩn xác.
3. **Qua Hero Quick CTA**:
   - Ngay tại màn hình đầu tiên, du khách bấm nút lớn **"Khám phá bản đồ ↗"** để cuộn thẳng tới bản đồ.

---

### Luồng 3: Luồng Nghe Audio Thuyết Minh (Audio Listening Flow)

Bảo toàn chính xác cả 3 phương thức nghe hiện hữu của hệ thống:

```
                      ┌────────────────────────────────────────┐
                      │ Du khách muốn nghe thuyết minh âm thanh │
                      └──────────────────┬─────────────────────┘
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         ▼                               ▼                               ▼
[Nghe thủ công trên Web]      [Tự động theo GPS Geofence]        [Nghe Offline đã tải]
         │                               │                               │
(Bấm POI trên bản đồ)         (Bật nút "Thuyết minh tự động")    (Vào mục gói Offline)
         │                               │                               │
(Drawer mở ra)                (Di chuyển trong vườn thú)         (Bấm nút "Phát" offline)
         │                               │                               │
(Bấm "Tải/Nghe âm thanh")     (GPS chạm bán kính Geofence)       (Đọc Blob từ IndexedDB)
         │                               │                               │
         ▼                               ▼                               ▼
[Tải stream API /audio/...]   [Phát hiện & Auto-play Audio]      [Phát qua URL.createObjectURL]
         │                               │                               │
         └───────────────────────────────┼───────────────────────────────┘
                                         │
                                         ▼
                     [Ghi nhận sự kiện Analytics an toàn]
                     - playback_start (poi_id, audio_id, lang)
                     - playback_complete (duration)
                     - geofence_enter / geofence_exit
```

*Lưu ý bảo vệ vòng đời âm thanh*: Khi một nguồn audio phát, các nguồn khác tự động dừng lại (`pause()`) để tránh tiếng ồn chồng lấn.

---

### Luồng 4: Luồng Tải Offline Audio (Offline Package Download Flow)

Phục vụ du khách trước khi đi hoặc du khách có sim 4G hạn chế dung lượng:

```
[Du khách cuộn đến Section 06 "Chuẩn bị Offline" hoặc truy cập "/explore"]
                                │
                                ▼
         [Hiển thị danh sách 6 gói ngôn ngữ kèm mã QR SVG]
                                │
          ┌─────────────────────┴─────────────────────┐
          ▼                                           ▼
[Dùng điện thoại quét mã QR]                [Bấm nút "Tải về trên máy này"]
          │                                           │
(Quét mã: "TCV-PACKAGE:tcv-audio-vi")        (Kích hoạt downloadAudioPackage)
          │                                           │
          ▼                                           ▼
[Mở link /explore?package=tcv-audio-vi]     [Hiển thị thanh tiến trình % hoàn thành]
          │                                           │
          └─────────────────────┬─────────────────────┘
                                │
                                ▼
          [Tải file nén/metadata & toàn bộ audio chunks]
                                │
                                ▼
          [Lưu trữ an toàn vào IndexedDB STORES.PACKAGES & OFFLINE_AUDIO]
                                │
                                ▼
          [Thông báo: "Đã tải xong gói thuyết minh! Sẵn sàng dùng khi mất mạng"]
```

---

### Luồng 5: Luồng Lựa Chọn Suggested Routes (Suggested Routes Flow)

Hỗ trợ du khách chọn tuyến tham quan phù hợp:

```
[Du khách tiếp cận Section 05: Suggested Routes]
                       │
                       ▼
    [So sánh 3 thẻ lộ trình trực quan]
    - Tour Ngắn: 3 trạm (~36 phút)
    - Tour Gia Đình: 5 trạm (~60 phút)
    - Tour Trọn Vẹn: 8 trạm (~96 phút)
                       │
                       ▼
    [Du khách bấm nút "Bắt đầu lộ trình" trên thẻ Tour Gia Đình]
                       │
                       ▼
    [Trang cuộn ngược nhẹ nhàng lên Section 04: Interactive Map]
                       │
                       ▼
    [Bản đồ tự động flyTo trạm dừng 01 (ví dụ: Chuồng Voi)]
                       │
                       ▼
    [Mở Drawer trạm dừng 01 kèm nút phát thuyết minh đầu tiên]
```

---

## 3. Đảm bảo Tính Tự Do và Phi Tuyến Tính (Non-Linear Freedom)

Để không ép người dùng đi theo trình tự cố định:
- **Floating Progress & Jump Navigator**: Ngoài thanh Menu chính, cạnh màn hình có các chấm chỉ báo tiến trình cuộn (Dot Navigation Indicator) kèm tooltip tên section, cho phép nhấn vào bất kỳ chấm nào để nhảy ngay tới section đó.
- **Back to Top Button**: Luôn xuất hiện khi du khách cuộn qua khỏi 50% trang chủ để quay về Hero chỉ với 1 click.
- **Deep Hash Restoration**: Khi người dùng chia sẻ link hoặc bookmark `https://.../#routes`, trình duyệt tự động cuộn mượt đến đúng Section 05 mà không phải lướt qua các section trước.
