# Báo Cáo Kiểm Thử Hồi Quy Toàn Diện – Phase 7 (Regression Testing Report)

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Thời điểm kiểm thử**: 13/11/2026  
> **Phạm vi kiểm thử**: Toàn diện giao diện mới (Hybrid Scrolling + Sticky Storytelling) so với Functional Inventory Phase 1  
> **Ràng buộc tuân thủ**: Không sửa đổi backend, không đổi database, không đổi API contracts, bảo toàn 100% routes con.

---

## 1. Kết Quả Kiểm Thử Tự Động (Automated Testing Verification)

### 1.1. Frontend Unit Tests (`npm --prefix frontend test`)
- **Lệnh thực thi**: `node --test`
- **Kết quả**: **8/8 test cases pass (100%)**
  - [x] `calculateDistanceMeters accurately calculates distance between two known coordinates` (1.45ms)
  - [x] `calculateDistanceMeters handles invalid inputs gracefully` (0.22ms)
  - [x] `findNearestPoi identifies closest POI to visitor coordinates` (0.33ms)
  - [x] `findNearestPoi handles empty POIs or missing visitor coordinates (UC-02 Path A1)` (1.55ms)
  - [x] `fetchPois requests the selected language and returns POIs` (43.60ms)
  - [x] `fetchPois reports structured HTTP errors` (1.35ms)
  - [x] `fetchPois propagates network failures` (0.47ms)
  - [x] `fetchPois rejects a response that does not match the contract` (0.59ms)

### 1.2. Production Bundle Verification (`npm --prefix frontend run build`)
- **Lệnh thực thi**: `vite build`
- **Kết quả**: **Build thành công 100% trong 21.48s**
  - Đóng gói đầy đủ mã nguồn tĩnh, PWA Service Worker precache (`dist/sw.js`), font NotoSans tiếng Việt (`NotoSans-D7-AVeX-.ttf`) và MapLibre WebGL worker.
  - Không có bất kỳ lỗi biên dịch (transpile errors) hay cảnh báo cú pháp nghiêm trọng nào.

---

## 2. Bảng Kiểm Tra Hồi Quy Chức Năng (Functional Regression Checklist)

Đối chiếu chi tiết theo từng hạng mục quy định tại mục **7.1 của Implementation Plan**:

### 2.1. General (Tổng Thể Hệ Thống)
- [x] **Homepage loads correctly**: Trang chủ tải mượt mà chuỗi 7 Section liên tục, không bị trắng màn hình.
- [x] **Existing routes remain accessible**: Toàn bộ các route con `/map`, `/explore`, `/itinerary`, `/guide`, `/admin` và `/admin/analytics` được bảo toàn nguyên vẹn trong `router.jsx`, truy cập trực tiếp độc lập bình thường.
- [x] **Header navigation works**: Sticky Header phản hồi thời gian thực, click vào các mục điều hướng kích hoạt đúng liên kết và đồng bộ trạng thái active.
- [x] **All existing links work**: Các liên kết CTA, liên kết xem bản đồ, liên kết cẩm nang và quản trị hoạt động chính xác.
- [x] **No unexpected redirects**: Không có bất kỳ hiện tượng chuyển hướng trang (redirect) trái phép nào ngoài ý muốn.

### 2.2. Animal Discovery (Khám Phá Động Vật)
- [x] **Animal information loads correctly**: Dữ liệu danh mục động vật tải chính xác từ API `/api/pois/catalog?language=...`.
- [x] **Animal selection works**: Người dùng click chọn bất kỳ con vật nào trên Carousel hoặc Danh mục đều cập nhật đúng state `selectedAnimal`.
- [x] **Sticky Spotlight Visual**: Cột ảnh chân dung lớn bên trái cập nhật đồng bộ tức thời khi click chọn con vật.
- [x] **Existing detail links work**: Modal chi tiết động vật (`animal-detail-dialog`) mở lên đầy đủ ảnh, tên khoa học, mô tả, bản quyền ảnh (`AnimalImageCredit`) và nút dẫn sang bản đồ `/map?poi={id}`.

### 2.3. Audio Experience (Trải Nghiệm Thuyết Minh)
- [x] **Audio playback works**: Phát âm thanh trực tiếp trên web, tự động theo Geofence và nghe offline từ IndexedDB hoạt động đúng theo logic gốc.
- [x] **Play/pause works**: Các nút điều khiển HTML5 Audio player trong drawer bản đồ phản hồi chính xác.
- [x] **Audio selection works**: `preparePoiAudio()` gọi đúng `resolvePlayableAudio()` tải file stream hoặc blob cục bộ.
- [x] **Language selection works**: Thay đổi ngôn ngữ qua `LanguageSelector` dừng ngay audio cũ, chuyển đổi locale chuẩn xác (Việt, Anh, Pháp, Trung, Nhật, Hàn).
- [x] **Existing audio controls work**: Thanh trượt timeline, nút tua, hiển thị thời lượng không bị lỗi.

### 2.4. Map & GPS (Bản Đồ Số & Định Vị)
- [x] **Map loads correctly**: MapLibre GL khởi tạo trơn tru với ngói OpenStreetMap mà không xung đột WebGL.
- [x] **Markers are displayed correctly**: Toàn bộ điểm POI chuồng thú hiển thị ghim rõ ràng; điểm gần nhất có biểu tượng ngôi sao ⭐ nổi bật.
- [x] **Marker selection works**: Chạm/click vào marker mở đúng Popup hoặc Drawer chi tiết trạm dừng.
- [x] **Location permissions work**: Hook `useGeolocation` xử lý đúng cả 2 trường hợp người dùng cấp quyền hoặc từ chối GPS (Alternative Path A1).
- [x] **GPS behavior remains unchanged**: Chế độ tự động phát hiện vùng Geofence và nút mô phỏng đến nơi (`simulateArrival`) hoạt động nguyên bản.
- [x] **Cooperative gestures**: Trên di động, thao tác lướt 1 ngón tay cuộn trang tự nhiên; 2 ngón tay pan/zoom bản đồ, giải quyết triệt để rủi ro bẫy cuộn.

### 2.5. Suggested Routes (Gợi Ý Lộ Trình)
- [x] **Existing route data loads**: Tải danh sách điểm dừng thực tế thông qua `loadPoisWithFallback`.
- [x] **Route selection works**: Phân chia chính xác 3 tuyến tham quan (Ngắn 3 trạm ~36p, Gia đình 5 trạm ~60p, Toàn diện 8 trạm ~96p).
- [x] **Route details work**: Danh sách trạm dừng đánh số thứ tự `01`, `02`... kèm liên kết thẳng tới trạm tương ứng trên bản đồ.
- [x] **Route calculations remain unchanged**: Giữ nguyên công thức tính thời lượng (12 phút/trạm).
- [x] **Start Route Button**: Bấm "Bắt đầu lộ trình" dẫn thẳng tới trạm xuất phát đầu tiên trên bản đồ.

### 2.6. Offline Audio Preparation (Chuẩn Bị Offline & QR Codes)
- [x] **QR codes lead to the correct destinations**: Mã QR SVG sinh chính xác chuỗi payload định dạng `TCV-PACKAGE:{id}`.
- [x] **Audio downloads work**: Nút "Tải gói này" kích hoạt luồng `downloadAudioPackage` tải manifest và lưu vào IndexedDB.
- [x] **Offline functionality works**: Khi ngắt mạng, danh sách file âm thanh đã lưu trong IndexedDB vẫn phát bình thường.
- [x] **Language selection remains functional**: Cung cấp đủ 6 gói ngôn ngữ chính thức.

### 2.7. Responsive & Ergonomics (Thiết Kế Thích Ứng & Công Thái Học)
- [x] **Desktop layout works (1280px - 1440px+)**: Bố cục 1240px rộng rãi, Sticky Storytelling đa cột, typography phân cấp rõ nét.
- [x] **Tablet layout works (768px - 1023px)**: Chuyển đổi linh hoạt sang lưới 2 cột, bản đồ cao 480px.
- [x] **Mobile layout works (360px - 390px)**: Tối ưu 1 tay, nút bấm toàn chiều rộng, menu dạng drawer.
- [x] **No horizontal overflow**: Triệt tiêu 100% thanh cuộn ngang ngoài ý muốn (`overflow-x: hidden`).
- [x] **No inaccessible controls**: Vùng chạm cảm ứng đạt tối thiểu 44px x 44px.

---

## 3. Tổng Hợp Ranh Giới Kỹ Thuật (Boundary & Change Scope)

- **Số file sửa đổi**: Chỉ duy nhất **3 files** giao diện frontend:
  1. `frontend/src/app/index.css` (Thêm Design Tokens, CSS Sticky, Scroll Reveal, Responsive rules)
  2. `frontend/src/components/layout/PublicLayout.jsx` (Thêm thanh Scroll Progress Bar và Active Section Observer)
  3. `frontend/src/components/views/HomeView.jsx` (Tích hợp 7 Section liên tục, nhúng an toàn Map & Lộ trình)
- **Backend / Database / API**:
  - Không có bất kỳ file nào trong thư mục `backend/` bị thay đổi.
  - Không thay đổi bất kỳ endpoint, request schema hay response payload nào.
  - Không phát sinh bất kỳ rủi ro bảo mật hay rò rỉ dữ liệu.
