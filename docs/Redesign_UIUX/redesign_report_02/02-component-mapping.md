# TCV UX Redesign – 02. Component Mapping & Lifecycle Safety

> **Dự án**: TCV – Saigon Zoo Audio Guide  
> **Tài liệu**: Bảng ánh xạ linh kiện & phân tích an toàn vòng đời (Component Mapping)  
> **Cam kết**: Tuyệt đối không tạo component mới thay thế component chức năng đang hoạt động; phân tách rạch ròi giữa UI Presentation và Functional Logic.

---

## 1. Bảng Ánh xạ Toàn diện theo 7 Section

Dưới đây là ma trận ánh xạ từng thành phần hiện có trong source code vào 7 Section của giao diện mới:

| Section | Existing Component / Source | Phân loại | Vai trò mới trong Redesign | Functional Dependencies cần bảo vệ |
| :--- | :--- | :--- | :--- | :--- |
| **Header & Nav** | `PublicLayout.jsx`<br>`BrandLogo.jsx`<br>`LanguageSelector.jsx` | **RESTYLE** | Trở thành Sticky Navigation Header với hiệu ứng mờ nền, thanh tiến trình cuộn và active section indicator. | `useLanguage`, `useTranslation`, `networkStatus.subscribeNetworkStatus`, `trackEvent`. |
| **01. Hero** | `HomeView.jsx` (lines 57-64) | **RESTYLE & WRAP** | Tái cấu trúc thành Section Hero hiện đại, bổ sung typography phân cấp mạnh mẽ, 2 nút Quick CTAs và chỉ báo cuộn. | `useTranslation`, locales `home.newEyebrow`, `home.newTitle`, `home.newDescription`. |
| **02. Animals** | `HomeView.jsx` (lines 66-72, 91-96)<br>`AnimalImageCredit.jsx` | **RESTYLE & WRAP** | Tách làm 2 tầng: Tầng 1 Sticky Spotlight cho 4 con vật tiêu biểu; Tầng 2 Species Catalog lưới. Giữ nguyên modal chi tiết. | `fetch('/api/pois/catalog?language=...')`, state `selectedAnimal`, `AnimalImageCredit`. |
| **03. Audio** | `HomeView.jsx` (lines 74-81) | **RESTYLE** | Bố cục lại 3 thẻ trải nghiệm âm thanh (Web, GPS, Offline) với iconography cao cấp và CTA điều hướng tương ứng. | Locales `home.listen*`, liên kết anchor `#map` và `#offline`. |
| **04. Map** | `InteractiveMap.jsx`<br>(Lazy load qua `MapView.jsx`) | **WRAP & PROTECT** | Nhúng nguyên vẹn `InteractiveMap` vào một Section Container có kiểm soát gesture (2-finger scroll) và bảo vệ lifecycle. | **PROTECT TUYỆT ĐỐI**: MapLibre GL instance, `useGeolocation`, `calculateDistanceMeters`, `findNearestPoi`, Geofencing engine, HTML5 Audio player, telemetry `trackEvent`. |
| **05. Routes** | Logic trong `ItineraryView.jsx` (lines 10-33) | **REUSE & RESTYLE** | Tái sử dụng thuật toán tính toán chia lộ trình 3/5/8 điểm dừng; bọc trong các thẻ lộ trình lớn có số phút ước tính và nút bắt đầu. | `poiLoader.loadPoisWithFallback`, `useTranslation`, liên kết `/map?poi={firstPoiId}`. |
| **06. Offline** | `HomeView.jsx` (lines 83-85)<br>`ExploreView.jsx` (lines 18-24)<br>`qrcode.react` (`QRCodeSVG`) | **REUSE & RESTYLE** | Hiển thị 6 mã QR SVG gói ngôn ngữ tải từ IndexedDB/API `/audio/packages`; nút tải trực tiếp. | `getItem(STORES.APP_STATE, 'public_audio_packages')`, `/audio/packages`, `QRCodeSVG`. |
| **07. Guide** | Nội dung trong `GuideView.jsx` (lines 7-22) | **RESTYLE & WRAP** | Đưa các khối FAQ (accordion collapsible), Mẹo tham quan và Cam kết quyền riêng tư GPS vào cuối trang chủ. | Locales `guide.*`, thẻ HTML5 `<details>` và `<summary>` chuẩn tiếp cận. |
| **Footer** | `PublicLayout.jsx` (lines 56-59) | **RESTYLE** | Chuẩn hóa chân trang với logo di sản 1864, liên kết điều hướng đầy đủ, link trang Quản trị `/admin` và bản quyền. | Giữ 100% liên kết hiện hữu. |

---

## 2. Phân Tích An Toàn Vòng Đời (Lifecycle & State Safety)

### 2.1. Thành phần nhạy cảm cao: `InteractiveMap.jsx`
- **Nguy cơ tiềm ẩn**: Nếu unmount component mỗi khi người dùng cuộn ra khỏi Section 04, MapLibre GL sẽ phải hủy WebGL context và tải lại toàn bộ tile bản đồ khi người dùng cuộn ngược lại, gây giật lag và hao tổn dữ liệu mạng.
- **Biện pháp bảo vệ**:
  - `InteractiveMap` được giữ **mounted vĩnh viễn** trong cấu trúc DOM một khi đã được nạp.
  - Sử dụng một biến cờ trạng thái hiển thị `isSectionInView` (thông qua `IntersectionObserver` với ngưỡng 0.1).
  - Khi `isSectionInView === false`:
    - Tạm dừng animation nhấp nháy của chấm GPS visitor (`.visitor-pulse`).
    - Không chạy các vòng lặp tính toán Geofence khi không có sự thay đổi tọa độ.
  - Khi `isSectionInView === true`:
    - Gọi nhẹ hàm `mapRef.current?.resize()` để đảm bảo kích thước canvas khớp hoàn hảo với khung hình.

### 2.2. Thành phần phát âm thanh (Audio Lifecycle)
- **Nguy cơ tiềm ẩn**: Trùng lặp âm thanh nếu đang nghe ở Section Bản đồ mà người dùng cuộn sang mục khác.
- **Biện pháp bảo vệ**:
  - Không khởi tạo audio manager mới.
  - Tận dụng refs sẵn có trong `InteractiveMap.jsx`: Khi section bản đồ bị cuộn ra ngoài hoàn toàn, chỉ gọi lệnh `pause()` an toàn trên `manualAudioRef.current` và `geofenceAudioRef.current`, không reset state để du khách có thể bấm nghe tiếp khi cuộn lại.

### 2.3. Tải dữ liệu không đồng bộ (Data Fetching Bottleneck)
- **Nguy cơ tiềm ẩn**: Nạp đồng thời tất cả API khi trang chủ vừa khởi động.
- **Biện pháp bảo vệ**:
  - Section 01 & 02: Tải ngay dữ liệu catalog động vật (`/api/pois/catalog`).
  - Section 04 & 05: Sử dụng `React.lazy` và `IntersectionObserver` kích hoạt nạp trước dữ liệu POI khi người dùng cuộn tới gần Section 03 (preload trước 300px), đảm bảo trang mở lên cực nhanh (First Contentful Paint < 1.2s).
