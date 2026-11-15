# TCV UX Redesign – 02. Information Architecture (IA)

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Tài liệu**: Kiến trúc thông tin (Information Architecture) cho Homepage Redesign  
> **Phương pháp tiếp cận**: Hybrid Scrolling + Sticky Storytelling  
> **Nguyên tắc bảo toàn**: 100% không đổi Backend, không đổi API contracts, bảo tồn tất cả functional behavior hiện hữu.

---

## 1. Mục tiêu kiến trúc thông tin

Chuyển đổi trải nghiệm từ mô hình **phân mảnh đa trang** (nơi người dùng phải tự bấm tìm từng trang riêng biệt trên thanh menu) sang mô hình **hành trình khám phá liên tục theo chiều dọc (Vertical Discovery Journey)**.

Du khách cuộn trang sẽ được dẫn dắt tự nhiên qua 7 Section chức năng cốt lõi của Thảo Cầm Viên:
1. **Hero / Welcome** (Ấn tượng đầu tiên & Lời mở đầu di sản 1864)
2. **Animal Discovery** (Gặp gỡ các loài động vật tiêu biểu & tra cứu toàn bộ danh mục)
3. **Audio Experience** (Khám phá 3 phương thức nghe thuyết minh đa ngôn ngữ)
4. **Interactive Map** (Trải nghiệm bản đồ số tích hợp định vị GPS & Geofencing)
5. **Suggested Routes** (Lựa chọn lộ trình tham quan phù hợp thời gian & gia đình)
6. **Offline Audio Preparation** (Chuẩn bị và quét QR tải trọn gói âm thanh trước chuyến đi)
7. **Getting Started / Visitor Guide** (Cẩm nang tham quan, FAQ & chính sách quyền riêng tư)

---

## 2. Chi tiết 7 Section trên Homepage

### Section 01 – Hero / Welcome (Lời Chào Di Sản & Điểm Xuất Phát)
- **Mục đích**: Chào đón du khách, truyền tải tinh thần di sản xanh thành lập từ 1864 của Thảo Cầm Viên, định vị dịch vụ thuyết minh âm thanh đa ngôn ngữ thông minh, và cung cấp lối tắt truy cập ngay cho người dùng vội.
- **Nội dung & Dữ liệu hiển thị**:
  - Eyebrow: `t('home.newEyebrow')` ("Chào mừng bạn đến với Thảo Cầm Viên Sài Gòn").
  - Tiêu đề chính: `t('home.newTitle')` ("Khám phá vườn thú lâu đời bằng âm thanh sống động").
  - Đoạn mô tả: `t('home.newDescription')` ("Hệ thống thuyết minh tự động theo định vị GPS...").
  - Điểm nhấn di sản: Badge "1864 – Saigon Zoo & Botanical Gardens".
  - Ảnh đại diện: Chú voi Châu Á ấn tượng (`/images/animals/tcv-an-005.jpg`) kèm credit tác giả.
  - Call to Action (CTA):
    - Primary CTA: *Khám phá bản đồ* (Link `/map` hoặc cuộn nhanh xuống `#map-section`).
    - Secondary CTA: *Lộ trình tham quan* (Link `/itinerary` hoặc cuộn nhanh xuống `#routes-section`).
  - Chỉ báo cuộn: *Cuộn để khám phá* (`home.scrollHint`) kèm mũi tên động nhẹ nhàng.
- **Mối quan hệ**: Là điểm xuất phát (Anchor Point), mở lối dẫn trực tiếp vào Section 02 (Động vật) hoặc nhảy cóc tới Section 04 (Bản đồ) / Section 05 (Lộ trình).
- **Chống trùng lặp**: Chỉ đóng vai trò giới thiệu tổng quan và điều hướng tắt; không nhúng trình phát nhạc hay danh sách chi tiết các trạm dừng tại đây.

---

### Section 02 – Animal Discovery (Thế Giới Động Vật & Sticky Storytelling)
- **Mục đích**: Kích thích sự tò mò và cảm xúc của du khách thông qua các câu chuyện sinh động về các loài thú biểu tượng tại Thảo Cầm Viên trước và trong chuyến đi.
- **Nội dung & Chức năng xuất hiện**:
  - **Tầng 1 - Sticky Spotlight (Featured Animals)**: Trình diễn 4 loài động vật tiêu biểu (Voi Châu Á, Hổ Bengal, Hươu cao cổ, Hà mã) kết hợp hình ảnh chất lượng cao và câu chuyện ngắn (`t('animal.*.note')`).
  - **Tầng 2 - Species Catalog (Danh mục toàn bộ loài)**: Lưới hiển thị các loài động vật tải từ API `/api/pois/catalog?language=...`.
  - **Chức năng tương tác**:
    - Khi bấm vào thẻ động vật: Mở modal chi tiết (`animal-detail-dialog`) hiển thị tên khoa học, mô tả đầy đủ, ảnh chụp, thông tin bản quyền ảnh (`AnimalImageCredit`).
    - Kiểm tra `map_available`: Nếu con vật có ghim trên bản đồ, hiển thị nút *Xem vị trí trên bản đồ* (điều hướng sang `/map?poi={id}` hoặc kích hoạt bản đồ tại Section 04 focus vào POI).
- **Mối quan hệ**: Tạo sự gắn kết cảm xúc với các cá thể sinh vật; sau khi xem xong loài thú yêu thích, du khách có nhu cầu tự nhiên: "Làm thế nào để nghe thuyết minh về loài này?" -> Dẫn dắt sang Section 03 (Audio).
- **Chống trùng lặp**: Tập trung vào hình ảnh, câu chuyện và nhận diện sinh thái; không tích hợp bản đồ phức tạp hay tải file nén ở section này.

---

### Section 03 – Audio Experience (Hệ Thống Thuyết Minh Đa Ngôn Ngữ)
- **Mục đích**: Giải thích rõ ràng 3 phương thức trải nghiệm thuyết minh độc đáo của Thảo Cầm Viên, giúp du khách hiểu cách công nghệ đồng hành cùng họ trong chuyến tham quan.
- **Nội dung & Chức năng xuất hiện**:
  - Trình bày 3 thẻ phương thức nghe trực quan (Cards):
    1. **Nghe trực tiếp trên Web (In-browser Streaming)**: Bấm vào bất kỳ điểm nào trên bản đồ để nghe thuyết minh bằng ngôn ngữ đã chọn (`t('home.listenWebTitle')`, `t('home.listenWebBody')`).
    2. **Tự động thuyết minh khi đến gần (GPS Geofence Auto-Play)**: Ứng dụng tự động phát hiện khi bạn bước vào vùng chuồng thú và cất giọng thuyết minh (`t('home.listenArrivalTitle')`, `t('home.listenArrivalBody')`).
    3. **Tải về nghe Offline không cần mạng (Offline Audio Package)**: Tải trọn gói âm thanh về máy khi còn ở cổng hoặc ở nhà, tiết kiệm dung lượng 4G (`t('home.listenOfflineTitle')`, `t('home.listenOfflineBody')`).
  - Nút chuyển tiếp nhanh: *Thử ngay trên bản đồ* (dẫn tới Section 04) và *Tải gói âm thanh ngay* (dẫn tới Section 06).
- **Mối quan hệ**: Đóng vai trò cầu nối logic giữa việc "Thấy con vật" (Section 02) và "Định vị vị trí để nghe" (Section 04) hoặc "Chuẩn bị tải offline" (Section 06).
- **Chống trùng lặp**: Section này làm nhiệm vụ giải thích phương thức và tính năng; không nhúng canvas bản đồ hay cơ chế quét QR camera phức tạp vào đây.

---

### Section 04 – Interactive Map (Bản Đồ Số Tương Tác & Định Vị Thông Minh)
- **Mục đích**: Cung cấp công cụ điều hướng không gian thực tế tại Thảo Cầm Viên, cho phép định vị vị trí hiện tại, tìm điểm thuyết minh gần nhất và nghe thuyết minh trực tiếp.
- **Nội dung & Chức năng xuất hiện**:
  - Nhúng trực tiếp component chức năng `InteractiveMap.jsx` (được bọc trong container an toàn cử chỉ).
  - Bản đồ MapLibre GL với lớp ngói OpenStreetMap.
  - Toàn bộ marker POI động vật với biểu tượng trực quan; marker sao vàng ⭐ cho điểm gần nhất.
  - Pulse định vị GPS du khách; nút "Định vị của tôi" và "Điểm gần nhất".
  - Thẻ thông báo POI gần nhất (`nearest-poi-card`).
  - Drawer chi tiết POI kèm audio player đa ngôn ngữ (`poi-audio-player`).
  - Nút bật/tắt chế độ thuyết minh tự động Geofencing và nút giả lập đến nơi (`simulateArrival`) cho mục đích demo/kiểm thử.
- **Mối quan hệ**: Là trung tâm hành động thực địa (Execution Core) của toàn bộ ứng dụng web.
- **Chống trùng lặp**: Bản đồ tập trung phục vụ tra cứu tức thời tại chỗ; các gợi ý tuyến đường dài theo chủ đề được tách riêng sang Section 05.

---

### Section 05 – Suggested Routes (Gợi Ý Lộ Trình Tham Quan)
- **Mục đích**: Hỗ trợ du khách lên kế hoạch tham quan theo quỹ thời gian và đối tượng đi cùng một cách khoa học, tránh đi lạc hoặc bỏ lỡ các điểm nổi bật.
- **Nội dung & Chức năng xuất hiện**:
  - Tải danh sách điểm dừng thực tế thông qua `poiLoader`.
  - 3 Thẻ hành trình thiết kế riêng biệt:
    1. **Tuyến Khám Phá Nhanh (Short Tour)**: 3 điểm dừng tiêu biểu (~36 phút) cho người có ít thời gian.
    2. **Tuyến Dành Cho Gia Đình & Trẻ Em (Family Tour)**: 5 điểm dừng thú vị, đường đi râm mát (~60 phút).
    3. **Tuyến Trọn Vẹn Thảo Cầm Viên (Full Tour)**: 8 điểm dừng bao quát toàn bộ vườn thú & thực vật (~96 phút).
  - Chi tiết từng tuyến: Danh sách các trạm dừng đánh số `01`, `02`... kèm liên kết thẳng tới trạm tương ứng trên bản đồ.
  - Nút hành động: *Bắt đầu lộ trình* -> Tự động focus bản đồ vào trạm dừng đầu tiên (`/map?poi={firstPoiId}`).
- **Mối quan hệ**: Kế thừa dữ liệu POI từ Section 04 nhưng tổ chức lại theo chiều kích thời gian và hành trình.
- **Chống trùng lặp**: Không hiển thị lại toàn bộ bản đồ; chỉ hiển thị thẻ lộ trình tóm lược và danh sách trạm dừng.

---

### Section 06 – Offline Audio Preparation (Chuẩn Bị Gói Âm Thanh Offline & QR Codes)
- **Mục đích**: Đảm bảo trải nghiệm nghe không bị gián đoạn ngay cả khi mạng 4G/Wifi chập chờn dưới tán cây rậm rạp của vườn thú; cung cấp mã QR tải nhanh cho 6 ngôn ngữ.
- **Nội dung & Chức năng xuất hiện**:
  - Danh sách mã QR SVG tương ứng các gói ngôn ngữ chính thức: Tiếng Việt, English, Français, 中文, 日本語, 한국어.
  - Mã QR dạng `TCV-PACKAGE:{id}` được vẽ bằng `QRCodeSVG`.
  - Nút *Tải gói trực tiếp trên thiết bị này* dẫn sang `/explore?package={id}`.
  - Hướng dẫn thao tác quét mã đơn giản bằng camera điện thoại.
- **Mối quan hệ**: Phục vụ giai đoạn chuẩn bị (Pre-visit hoặc tại cổng kiểm soát vé).
- **Chống trùng lặp**: Trưng bày trực quan các mã QR ngôn ngữ; thao tác quét camera thời gian thực (`QrScanner`) vẫn được giữ nguyên tại route `/explore` hoặc kích hoạt dạng overlay khi cần quét vé/chuồng thú.

---

### Section 07 – Getting Started & Visitor Guide (Cẩm Nang & Trợ Giúp)
- **Mục đích**: Cung cấp thông tin thực tế cần biết, câu hỏi thường gặp (FAQ) và cam kết minh bạch về quyền riêng tư dữ liệu GPS của du khách trước khi kết thúc hành trình trang chủ.
- **Nội dung & Chức năng xuất hiện**:
  - Các khối thông tin hữu ích: Mẹo nghe tai nghe, cách bật quyền GPS, hướng dẫn mở lại gói offline khi mất sóng.
  - Khối Hỏi & Đáp (FAQ Collapsible/Accordion): Giải đáp các thắc mắc phổ biến nhất.
  - Thông báo minh bạch quyền riêng tư (Privacy Notice): Giải thích rõ tọa độ GPS của khách chỉ được tính toán trên trình duyệt để kích hoạt âm thanh, hoàn toàn không lưu trữ vị trí cá nhân lên máy chủ.
  - Nút liên kết đến Cổng thông tin Quản lý Nội dung (`/admin`).
- **Mối quan hệ**: Đóng gói toàn bộ trải nghiệm khám phá, giải tỏa thắc mắc và dẫn tới Footer.

---

## 3. Ma trận Mối quan hệ và Dòng chảy Nội dung

| Thứ tự | Tên Section | Dữ liệu chính phụ thuộc | Trạng thái tương tác chính | Chuyển tiếp tiếp theo |
| :---: | :--- | :--- | :--- | :--- |
| **01** | **Hero / Welcome** | Static locales + Brand visual | CTAs cuộn trang hoặc nhảy sang Map/Route | Cuộn xuống Section 02 |
| **02** | **Animal Discovery** | `/api/pois/catalog` | Modal chi tiết động vật, liên kết Map POI | Dẫn sang Section 03 |
| **03** | **Audio Experience** | Locales 3 chế độ nghe | Chọn phương thức trải nghiệm | Dẫn sang Section 04 hoặc 06 |
| **04** | **Interactive Map** | `/api/pois`, `/api/geofences`, Audio assets | Thao tác 2 ngón tay, định vị, nghe POI audio | Dẫn sang Section 05 |
| **05** | **Suggested Routes** | POIs array qua `poiLoader` | Chọn tour, bấm mở bản đồ trạm đầu tiên | Dẫn sang Section 06 |
| **06** | **Offline Preparation** | `/audio/packages` | Quét QR hoặc click tải gói đa ngôn ngữ | Dẫn sang Section 07 |
| **07** | **Getting Started** | Locales FAQ & Privacy | Mở/đóng accordion FAQ, link Admin | Xuống Footer |

---

## 4. Kiểm tra Tuân thủ Ràng buộc Kỹ thuật

- Không sinh thêm API mới; mọi dữ liệu đều lấy từ `/api/pois/catalog`, `/api/pois`, `/api/geofences`, `/audio/packages`.
- Thứ tự 7 section phản ánh đúng tâm lý học hành vi du khách: **Tò mò (01, 02) -> Tìm hiểu cách dùng (03) -> Thực hành tương tác (04, 05) -> Chuẩn bị kỹ thuật (06) -> An tâm trải nghiệm (07)**.
- Đảm bảo tính tương thích tuyệt đối với tài liệu `Redesign_UIUX/05-risk-assessment.md`.
