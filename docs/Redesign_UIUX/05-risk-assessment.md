# TCV UI/UX Redesign – Comprehensive Risk Assessment & Mitigation Plan

> **Tài liệu**: Đánh giá rủi ro kỹ thuật và chiến lược kiểm soát cho dự án TCV UI/UX Redesign  
> **Thư mục lưu trữ**: `Redesign_UIUX/05-risk-assessment.md`  
> **Phiên bản**: 1.0 (Audit-First Baseline)  
> **Nguyên tắc cốt lõi**: Giữ nguyên 100% backend, giữ nguyên API contracts, không refactor tùy tiện, bảo toàn toàn bộ routes, query params, hash params và QR destinations.

---

## 1. Giới thiệu & Khung tiêu chuẩn phân loại rủi ro

Tài liệu này xác định và phân tích toàn diện 7 rủi ro kỹ thuật trọng yếu phát sinh khi chuyển đổi kiến trúc website TCV từ đa trang truyền thống sang mô hình **Hybrid Scrolling & Sticky Storytelling**.

Mỗi rủi ro được định lượng theo:
- **Likelihood (Khả năng xảy ra)**: Low | Medium | High | Critical
- **Severity (Mức độ nghiêm trọng)**: Low | Medium | High | Critical
- **Ranh giới can thiệp (Intervention Boundary)**:
  - `Frontend-Only`: Các kỹ thuật UI/CSS/DOM events an toàn tuyệt đối, không đụng chạm logic.
  - `Potential Functional Impact`: Các biện pháp can thiệp có rủi ro ảnh hưởng đến state hoặc nghiệp vụ, bắt buộc phải audit trước và thử nghiệm hồi quy nghiêm ngặt.

---

## 2. Chi tiết 7 Rủi ro Trọng yếu

---

### Rủi ro 01: MapLibre Scroll Conflict (Xung đột cử chỉ cuộn trang và bản đồ)

- **Root Cause**:
  Component `InteractiveMap` sử dụng thư viện MapLibre GL gắn vào một container DOM trên trang. Theo cơ chế mặc định của MapLibre GL, các cử chỉ lăn chuột (`wheel`), chạm một ngón (`touch`) và kéo chuột (`drag`) sẽ bị canvas bản đồ chặn và diễn giải thành thao tác zoom/pan bản đồ. Khi được nhúng vào dòng cuộn dọc tự nhiên của trang chủ, người dùng cuộn đến vị trí bản đồ sẽ bị "kẹt", không thể tiếp tục cuộn xuống các section phía dưới (Scroll Trap / Scroll Hijacking).
- **Impact**:
  Du khách trên điện thoại và desktop bị chặn dòng chảy cuộn trang, tạo cảm giác trang web bị đơ hoặc hỏng trải nghiệm người dùng; cản trở tiếp cận các section tiếp theo như Suggested Routes hay Offline Download.
- **Likelihood**: High.
- **Severity**: High.
- **Mitigation Strategy (Đã điều chỉnh theo hướng kiểm soát gesture)**:
  1. *Kiểm soát Gesture (Cooperative Gestures / Two-finger Pan)*:
     - **Không vô hiệu hóa tương tác bản đồ**. Thay vào đó, áp dụng cơ chế cuộn hợp tác tương tự Google Maps / MapLibre:
       - Trên Mobile: Chỉ cho phép pan bản đồ khi dùng **2 ngón tay**. Khi dùng 1 ngón tay, trình duyệt tiếp tục cuộn trang bình thường. Nếu người dùng chạm 1 ngón, hiển thị một overlay hướng dẫn nhẹ nhàng: *"Sử dụng 2 ngón tay để di chuyển bản đồ"*.
       - Trên Desktop: Vô hiệu hóa thao tác lăn chuột đơn thuần (`scrollZoom: false` hoặc yêu cầu nhấn giữ phím `Ctrl + Wheel` để phóng to/thu nhỏ).
     - Cung cấp nút chuyển đổi trạng thái rõ ràng trên góc bản đồ: *"Khóa / Mở khóa cuộn trang"* (Toggle Map Interaction Lock) để du khách chủ động kích hoạt trải nghiệm bản đồ toàn quyền khi cần.
     - Luôn duy trì nút bấm dẫn sang route độc lập `/map` để người dùng có không gian thao tác trọn vẹn màn hình.
  2. *Phân loại ranh giới giải pháp*:
     - `Frontend-Only`: Cấu hình options của MapLibre instance (`cooperativeGestures: true` hoặc listener xử lý touch/wheel event trên wrapper của section; CSS pointer-events overlay).
     - `Potential Functional Impact`: Không có, vì API của MapLibre hỗ trợ trực tiếp các flag tương tác (`dragPan`, `scrollZoom`) mà không làm thay đổi state dữ liệu POI hay GPS.
- **Affected Components**:
  - `frontend/src/features/map/InteractiveMap.jsx`
  - `frontend/src/components/views/MapView.jsx`
  - Section Map trên trang chủ mới.
- **Verification Method**:
  - Kiểm thử trên thiết bị di động thực tế (iOS Safari, Android Chrome): Lướt 1 ngón tay qua section bản đồ để xác nhận trang vẫn cuộn mượt mà; lướt 2 ngón tay để xác nhận bản đồ di chuyển.
  - Kiểm thử trên Desktop Chrome/Firefox/Edge: Lăn chuột qua bản đồ không bị zoom đột ngột.

---

### Rủi ro 02: DOM Performance và WebGL Memory Management (Hiệu năng DOM & Bộ nhớ WebGL)

- **Root Cause**:
  MapLibre GL sử dụng WebGL context (`HTMLCanvasElement`) để dựng bản đồ vector/raster. Khi trang chủ tích hợp nhiều section (Hero ảnh lớn, carousel nhiều con vật, card lộ trình, danh sách QR và bản đồ WebGL), việc render liên tục các tài nguyên nặng và giữ WebGL context có thể gây tràn bộ nhớ GPU trên các thiết bị di động đời cũ. Tuy nhiên, nếu tùy tiện unmount/destroy MapLibre mỗi khi người dùng cuộn ra khỏi section thì chi phí khởi tạo lại (tải tile, tạo worker, re-render DOM markers) rất lớn, gây giật lag (frame drop) và mất trạng thái người dùng.
- **Impact**:
  Trình duyệt bị tụt FPS (dưới 30fps), giật lag khi cuộn, hoặc thậm chí WebGL context bị mất đột ngột (`webglcontextlost`) dẫn đến màn hình bản đồ đen ngòm.
- **Likelihood**: Medium.
- **Severity**: High.
- **Mitigation Strategy (Phân biệt Component Visibility và Component Lifecycle)**:
  1. *Nguyên tắc cốt lõi: Không tự động destroy/recreate MapLibre*:
     - **Tách biệt rạch ròi giữa Component Visibility và Component Lifecycle**:
       - Map component vẫn được giữ nguyên trong vòng đời (`mounted`) ở DOM cây để duy trì kết nối worker, bộ nhớ đệm tile và các marker vị trí khách du lịch.
       - Khi section bản đồ cuộn ra ngoài khung nhìn (sử dụng `IntersectionObserver` với ngưỡng thích hợp): chỉ tạm dừng các tác vụ tính toán vòng lặp không cần thiết hoặc tạm ngưng render animation pulse của GPS marker.
       - Khi section quay lại khung nhìn (`isVisible: true`): gọi nhẹ `map.resize()` để đảm bảo canvas hiển thị đúng kích thước khung hình mà không phải tải lại dữ liệu từ đầu.
  2. *Tối ưu hóa các tài nguyên khác*:
     - Áp dụng `content-visibility: auto` và `contain-intrinsic-size` cho các section nằm xa viewport để trình duyệt bỏ qua chi phí layout ban đầu.
     - Đảm bảo toàn bộ hình ảnh động vật sử dụng `loading="lazy"` và `decoding="async"`.
  3. *Phân loại ranh giới giải pháp*:
     - `Frontend-Only`: CSS containment, IntersectionObserver để toggle trạng thái rendering animation, gắn `loading="lazy"`.
     - `Potential Functional Impact`: Không đụng chạm vòng đời mount/unmount của MapLibre, tuyệt đối không gọi `map.remove()` khi chỉ cuộn trang.
- **Affected Components**:
  - `frontend/src/features/map/InteractiveMap.jsx`
  - Các Section hình ảnh trên trang chủ (`Species index`, `Carousel`, `Hero`).
- **Verification Method**:
  - Đo đạc qua Chrome DevTools Performance & Memory tab: Kiểm tra heap snapshot và số lượng WebGL contexts (luôn duy trì đúng 1 context, không tăng lũy tiến khi cuộn lên/xuống).
  - Giám sát FPS đạt mức ổn định >= 55-60fps trên thiết bị mô phỏng cấu hình trung bình (Mobile throttling 4x CPU slowdown).

---

### Rủi ro 03: Deep Linking và QR Code Compatibility (Tương thích liên kết sâu & Mã QR vật lý)

- **Root Cause**:
  Trong hệ sinh thái thực tế của Thảo Cầm Viên Sài Gòn, các mã QR vật lý đã được in trên các biển báo chuồng thú, tờ gấp và tài liệu hướng dẫn. Các mã QR này trỏ trực tiếp đến các đường dẫn cụ thể, ví dụ:
  - Từng con vật / điểm dừng: `/map?poi=TCV-AN-001`, `/map?poi=TCV-AN-005`
  - Gói âm thanh tải offline: `/explore?package=tcv-audio-vi` hoặc định dạng payload `TCV-PACKAGE:...`
  - Chỉ mục hướng dẫn và quyền riêng tư: `/guide#offline`, `/guide#privacy`
  - Khu vực quản trị: `/admin`, `/admin/analytics`
  Nếu việc tái thiết kế trang chủ làm thay đổi cấu trúc URL, gộp trang mà xóa bỏ router con hoặc không xử lý các tham số tìm kiếm (`searchParams`), toàn bộ hệ thống mã QR vật lý ngoài đời thực sẽ bị vô hiệu hóa (trả về 404 hoặc không kích hoạt đúng chức năng).
- **Impact**:
  Khách tham quan quét mã QR tại Thảo Cầm Viên không nghe được thuyết minh tương ứng, hệ thống hướng dẫn du lịch bị gãy hoàn toàn ngoài thực địa.
- **Likelihood**: High (nếu can thiệp sai cấu trúc routing).
- **Severity**: Critical.
- **Mitigation Strategy (Bảo toàn 100% Routes và Parameters)**:
  1. *Duy trì đầy đủ Router hiện hữu trong `router.jsx`*:
     - Không xóa bỏ bất kỳ route con nào: `/map`, `/explore`, `/itinerary`, `/guide`, `/admin`, `/admin/analytics`.
     - Trang chủ (`/`) đóng vai trò là trải nghiệm khám phá tổng hợp, trong khi các trang con vẫn tồn tại độc lập để tiếp nhận lưu lượng truy cập từ mã QR.
  2. *Hỗ trợ Deep Linking trực tiếp trên Homepage (nếu người dùng vào trang chủ kèm params)*:
     - Đảm bảo logic đọc `searchParams` (`?poi=...`, `?package=...`) và hash (`#offline`, `#privacy`) vẫn hoạt động chính xác, tự động cuộn mượt (smooth scroll) đến đúng section tương ứng và mở đúng drawer/modal.
  3. *Phân loại ranh giới giải pháp*:
     - `Frontend-Only`: Giữ nguyên khai báo trong `router.jsx`, kiểm tra URL params trong các component hiện hành.
     - `Potential Functional Impact`: Bất kỳ đề xuất nào xóa bỏ route hoặc đổi tên param đều bị từ chối tuyệt đối.
- **Affected Components**:
  - `frontend/src/app/router.jsx`
  - `frontend/src/features/map/InteractiveMap.jsx` (`useSearchParams`)
  - `frontend/src/components/views/ExploreView.jsx` (`searchParams.get('package')`)
  - `frontend/src/components/views/GuideView.jsx` (Anchor links `#privacy`, `#offline`)
- **Verification Method**:
  - Lập bảng test case kiểm tra toàn bộ danh sách URL QR vật lý:
    - Truy cập `/map?poi=TCV-AN-005` -> Phải hiển thị bản đồ và mở đúng drawer của Voi Châu Á.
    - Truy cập `/explore?package=vi` -> Phải kích hoạt quá trình tải gói tiếng Việt.
    - Truy cập `/guide#privacy` -> Phải mở đúng phần chính sách riêng tư.

---

### Rủi ro 04: Audio Lifecycle Management (Quản lý vòng đời âm thanh & Tránh phát trùng lặp)

- **Root Cause**:
  Trong ứng dụng hiện tại, âm thanh có thể được phát từ nhiều nguồn khác nhau:
  1. Thao tác bấm nghe thủ công trên thẻ POI bản đồ (`manualAudioRef`).
  2. Kích hoạt tự động khi đi vào vùng Geofence (`geofenceAudioRef`).
  3. Phát file âm thanh offline đã tải trong `ExploreView` (`audioRef`).
  Theo kiến trúc gốc, các cơ chế này nằm rải rác trong `InteractiveMap.jsx` và `ExploreView.jsx`. Mỗi nơi tự tạo và quản lý instance `HTMLAudioElement` riêng. Nếu tự ý viết thêm một Audio Manager mới phức tạp hoặc gộp trang thiếu kiểm soát, các audio instance có thể phát đè lên nhau (nhiều giọng thuyết minh nói cùng lúc) hoặc không dừng lại khi người dùng chuyển section / đổi ngôn ngữ.
- **Impact**:
  Âm thanh phát chồng chéo gây ô nhiễm tiếng ồn, hỏng trải nghiệm người dùng, vi phạm chính sách autoplay của trình duyệt trên di động và gửi sai telemetry analytics (`playback_start` liên tục mà không có `playback_complete`).
- **Likelihood**: High.
- **Severity**: High.
- **Mitigation Strategy (Audit implementation hiện tại, không tự chế Audio Manager mới)**:
  1. *Tôn trọng cơ chế hiện hữu của hệ thống*:
     - Audit kỹ implementation trong `InteractiveMap.jsx`: Component đã có logic `geofenceAudioRef.current?.pause()` khi người dùng phát manual audio và ngược lại. Đồng thời đã có cơ chế dọn dẹp Object URL (`URL.revokeObjectURL`) khi đổi ngôn ngữ hoặc unmount.
     - **Không tự ý tạo một Audio Manager mới** làm xáo trộn kết nối tới IndexedDB và backend stream.
  2. *Bổ sung kiểm soát ngữ cảnh cuộn (Scroll Context Awareness)*:
     - Khi người dùng cuộn hoàn toàn ra khỏi khu vực bản đồ/âm thanh hoặc mở một phương tiện khác, kích hoạt sự kiện tạm dừng an toàn (`pause()`) cho audio đang chạy của section đó thông qua các handler đã có sẵn.
     - Đảm bảo khi người dùng chuyển đổi ngôn ngữ trên Header (`LanguageSelector`), mọi audio đang phát lập tức dừng lại và clear state phát hiện geofence (giữ đúng hành vi tại lines 117-122 trong `InteractiveMap.jsx`).
  3. *Phân loại ranh giới giải pháp*:
     - `Frontend-Only`: Kích hoạt hàm pause trên ref hiện có khi chuyển section.
     - `Potential Functional Impact`: Tránh can thiệp vào các API call `/audio/assets/resolve`, `resolvePlayableAudio`, hay sửa đổi sự kiện gửi về `/api/analytics/events`.
- **Affected Components**:
  - `frontend/src/features/map/InteractiveMap.jsx`
  - `frontend/src/components/views/ExploreView.jsx`
  - `frontend/src/features/offline/audioPackages.js`
- **Verification Method**:
  - Kiểm thử đồng thời: Đang nghe thuyết minh thủ công con Voi, bấm mô phỏng Geofence đến chuồng Hổ -> Thuyết minh Voi phải dừng ngay, phát thuyết minh Hổ.
  - Đổi ngôn ngữ từ `VI` sang `EN` trong lúc đang phát -> Audio lập tức dừng, không phát tiếng Việt tiếp.

---

### Rủi ro 05: Scroll Position và Navigation State (Trạng thái vị trí cuộn & Đồng bộ thanh điều hướng)

- **Root Cause**:
  Khi chuyển đổi sang giao diện cuộn dài một trang (Hybrid Long-page Scrolling), người dùng cuộn qua lại giữa 7 section. Nếu không quản lý tốt trạng thái vị trí cuộn:
  - Khi người dùng bấm vào các nút điều hướng trên Header (ví dụ bấm "Bản đồ", "Lộ trình", "Hướng dẫn"), trình duyệt có thể bị nhảy giật đột ngột thay vì cuộn mượt mà.
  - Khi người dùng chuyển sang route khác (ví dụ vào `/admin` hoặc bấm vào một trang con) rồi bấm nút "Back" trên trình duyệt, vị trí cuộn trước đó trên trang chủ có thể bị mất, quay ngược về đầu trang Hero (`scroll restoration` thất bại).
  - Thanh Navigation Header không đồng bộ: người dùng đang ở Section Map nhưng Header vẫn highlight tab "Trang chủ".
- **Impact**:
  Mất phương hướng điều hướng (navigation disorientation), gây khó chịu khi người dùng không biết mình đang ở đâu trong hành trình, hỏng lịch sử duyệt trang (`history stack`).
- **Likelihood**: High.
- **Severity**: Medium.
- **Mitigation Strategy (Đồng bộ Scroll State & History API an toàn)**:
  1. *Intersection Observer cho Navigation Indicator*:
     - Sử dụng `IntersectionObserver` để theo dõi section nào đang chiếm phần lớn viewport (threshold 0.5 - 0.6) và cập nhật visual active state trên thanh navigation một cách tự nhiên.
  2. *Hỗ trợ Smooth Scrolling với Fallback*:
     - Sử dụng CSS tiêu chuẩn `scroll-behavior: smooth` trên phần tử container và `element.scrollIntoView({ behavior: 'smooth' })` khi bấm vào các anchor link nội bộ.
  3. *Xử lý History và Scroll Restoration*:
     - Khi cuộn qua các section chính, sử dụng `history.replaceState` (không dùng `pushState` để tránh làm rác lịch sử trình duyệt khi cuộn liên tục) để cập nhật hash tương ứng (`#map`, `#routes`, `#offline`).
     - Tận dụng cơ chế `ScrollRestoration` mặc định của React Router v7 để giữ vị trí cuộn khi điều hướng sang trang khác và quay lại.
  4. *Phân loại ranh giới giải pháp*:
     - `Frontend-Only`: Hoàn toàn là xử lý giao diện qua CSS, Observer API và History State cục bộ của trình duyệt.
     - `Potential Functional Impact`: Không có tác động tới backend hay dữ liệu nghiệp vụ.
- **Affected Components**:
  - `frontend/src/components/layout/PublicLayout.jsx`
  - `frontend/src/app/router.jsx`
  - `frontend/src/components/views/HomeView.jsx`
- **Verification Method**:
  - Bấm lần lượt các mục trên Header: trang cuộn mượt đến đúng vị trí tương ứng.
  - Cuộn đến Section 05 (Lộ trình), bấm sang `/admin`, sau đó bấm nút Back của trình duyệt -> Trang chủ phải hiển thị lại đúng vị trí Section 05.

---

### Rủi ro 06: Frontend State và Component Lifecycle (Quản lý trạng thái & Xung đột Vòng đời Component)

- **Root Cause**:
  Trong kiến trúc cũ, các trang như `HomeView`, `MapView`, `ExploreView`, `ItineraryView` được gắn vào các route độc lập, do đó vòng đời component (mount, fetch dữ liệu, unmount) diễn ra riêng rẽ.
  Khi đưa các thành phần này cùng xuất hiện trên một trang chủ dài:
  - Nếu tất cả các section cùng kích hoạt các lời gọi API (`useEffect` tải catalog, tải geofences, tải packages, kiểm tra IndexedDB) ngay khi trang chủ vừa tải, sẽ tạo ra tình trạng tắc nghẽn tài nguyên (network bottleneck) và race conditions.
  - State của các component con nếu để rò rỉ hoặc chồng chéo (ví dụ state `selectedPoi` của bản đồ bị xung đột với state `selectedAnimal` của carousel động vật) sẽ dẫn đến lỗi logic hiển thị modal đè lên drawer.
- **Impact**:
  Tăng thời gian Time to Interactive (TTI), nghẽn mạng ban đầu, tiêu hao băng thông 4G của du khách không cần thiết và lỗi giao diện chồng chéo modal/drawer.
- **Likelihood**: Medium.
- **Severity**: Medium.
- **Mitigation Strategy (Độc lập State & Lazy Data Fetching theo Section)**:
  1. *Giữ nguyên tính độc lập của Local State*:
     - Không cố gắng gộp toàn bộ state của các view vào một monolithic state to lớn. Giữ nguyên ranh giới đóng gói dữ liệu của từng component.
     - Quản lý thứ tự z-index và backdrop rõ ràng: Modal chi tiết động vật (`animal-detail-dialog`) và Drawer bản đồ (`poi-detail-drawer`) phải có cơ chế đóng khi mở cái còn lại, tránh mở 2 lớp overlay cùng lúc.
  2. *Tải dữ liệu thông minh theo Section (Viewport-driven initialization)*:
     - Dữ liệu Hero và Động vật nổi bật (Section 01, 02) được tải ngay lập tức để người dùng xem được ngay (First Contentful Paint).
     - Dữ liệu Geofences và danh sách POI chi tiết của bản đồ chỉ kích hoạt fetch khi người dùng cuộn gần tới Section 04 (preload trước 200px viewport).
  3. *Phân loại ranh giới giải pháp*:
     - `Frontend-Only`: Phối hợp `Suspense`, lazy loading, và quản lý z-index modal.
     - `Potential Functional Impact`: Giữ nguyên các hàm `poiLoader.loadPoisWithFallback` và `audioPackages.listOfflineAudio` mà không thay đổi logic bên trong.
- **Affected Components**:
  - `frontend/src/components/views/HomeView.jsx`
  - `frontend/src/features/map/InteractiveMap.jsx`
  - `frontend/src/components/views/ExploreView.jsx`
- **Verification Method**:
  - Mở Chrome Network Tab: Xác nhận khi vừa vào trang chủ, không có 10 request bắn ra cùng lúc; các request của map chỉ phát sinh khi chuẩn bị cuộn tới.
  - Mở đồng thời modal thú và drawer bản đồ: Hệ thống xử lý đóng layer cũ mượt mà, không bị kẹt backdrop.

---

### Rủi ro 07: Accessibility và Reduced Motion (Khả năng tiếp cận & Tránh say chuyển động)

- **Root Cause**:
  Mô hình **Sticky Storytelling** và hiệu ứng cuộn Hybrid thường sử dụng nhiều hiệu ứng thị giác như: cố định khung hình (sticky pinning), chữ/ảnh phóng to thu nhỏ khi cuộn (zoom/scale scroll triggers), chuyển cảnh lướt ngang (horizontal parallax).
  Đối với nhóm du khách bị chứng rối loạn tiền đình (vestibular disorders) hoặc người dùng nhạy cảm với chuyển động, việc cuộn trang gây ra các chuyển động liên tục sẽ gây cảm giác chóng mặt, buồn nôn (motion sickness). Ngoài ra, các thành phần cuộn ngang và canvas bản đồ nếu không quản lý focus bàn phím sẽ gây khó khăn cho người dùng khiếm thị hoặc sử dụng bộ đọc màn hình (Screen Readers).
- **Impact**:
  Vi phạm tiêu chuẩn tiếp cận web (WCAG 2.1 Level AA), gây khó chịu cho người dùng khuyết tật hoặc người kích hoạt chế độ giảm chuyển động trong hệ điều hành.
- **Likelihood**: High.
- **Severity**: Medium.
- **Mitigation Strategy (Tôn trọng `prefers-reduced-motion` & Hỗ trợ Screen Reader)**:
  1. *Tôn trọng triệt để `prefers-reduced-motion`*:
     - Tích hợp media query CSS:
       ```css
       @media (prefers-reduced-motion: reduce) {
         * {
           animation-duration: 0.01ms !important;
           animation-iteration-count: 1 !important;
           transition-duration: 0.01ms !important;
           scroll-behavior: auto !important;
         }
       }
       ```
     - Khi phát hiện người dùng bật "Reduce Motion": vô hiệu hóa các hiệu ứng ghim dính phức tạp (sticky parallax), chuyển sang hiển thị các khối nội dung tĩnh tuần tự, dễ đọc.
  2. *Đảm bảo Thứ tự Focus và Semantic HTML*:
     - Mọi nút bấm tương tác (Next/Prev carousel, nút nghe audio, mở bản đồ) phải có nhãn `aria-label` đa ngôn ngữ đầy đủ (tận dụng `t('key')` hiện hữu).
     - Giữ nguyên cấu trúc các thẻ ngữ nghĩa: `<header>`, `<main>`, `<section>`, `<footer>`, `<nav>`, `<article>`, heading levels (`<h1>` -> `<h2>` -> `<h3>`) hợp lý.
  3. *Phân loại ranh giới giải pháp*:
     - `Frontend-Only`: 100% xử lý qua CSS media query và thuộc tính ARIA trên JSX.
     - `Potential Functional Impact`: Không có bất kỳ tác động nào tới logic nghiệp vụ.
- **Affected Components**:
  - Toàn bộ stylesheet (`frontend/src/app/index.css`)
  - Tất cả các section component trên trang chủ.
- **Verification Method**:
  - Bật tùy chọn "Emulate CSS media feature prefers-reduced-motion: reduce" trong Chrome DevTools -> Xác nhận toàn bộ animation phức tạp ngừng hoạt động, trang hiển thị nội dung tĩnh rõ ràng.
  - Sử dụng phím `Tab` để di chuyển xuyên suốt 7 section của trang chủ: Thấy rõ viền focus, không bị bẫy bàn phím (keyboard trap).

---

## 3. Ma trận Tổng hợp Rủi ro & Ranh giới Can thiệp

| ID | Tên Rủi ro | Likelihood | Severity | Ranh giới can thiệp chính | Nguy cơ ảnh hưởng nghiệp vụ | Biện pháp bảo vệ hàng đầu |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **R-01** | MapLibre Scroll Conflict | High | High | `Frontend-Only` (Gesture controls) | **Thấp** | Áp dụng 2-finger pan trên di động, cooperative gestures, giữ link sang `/map`. |
| **R-02** | DOM & WebGL Memory | Medium | High | `Frontend-Only` (Lifecycle containment) | **Thấp** | Giữ component mounted, chỉ pause animation khi ẩn; không `remove()` bản đồ khi cuộn. |
| **R-03** | Deep Linking & QR Broken | High | Critical | `Frontend-Only` (Routing preservation) | **Cực cao nếu vi phạm** | Giữ 100% routes con, query params và hash; cấm xóa bất kỳ path nào. |
| **R-04** | Audio Lifecycle Conflict | High | High | `Frontend-Only` (Trigger pause) | **Trung bình** | Tôn trọng implementation hiện tại, không tự chế Audio Manager mới; pause khi chuyển ngữ cảnh. |
| **R-05** | Scroll & Nav Disorientation | High | Medium | `Frontend-Only` (Observer & History) | **Thấp** | Dùng IntersectionObserver đồng bộ Nav; `history.replaceState` lưu vị trí an toàn. |
| **R-06** | State & Lifecycle Collision | Medium | Medium | `Frontend-Only` (State isolation) | **Thấp** | Giữ độc lập local state, lazy fetch theo viewport, quản lý z-index modal/drawer. |
| **R-07** | A11y & Reduced Motion | High | Medium | `Frontend-Only` (CSS & ARIA) | **Không có** | Hỗ trợ `@media (prefers-reduced-motion)`, ARIA labels và keyboard navigation đầy đủ. |

---

## 4. Kết luận & Khuyến nghị Tiếp theo

Bản đánh giá rủi ro này xác nhận rằng:
1. **Toàn bộ 7 rủi ro đều có thể được kiểm soát và giải quyết 100% ở tầng Frontend (CSS, Event Listener, Component Architecture)** mà không cần và **tuyệt đối không được phép** chỉnh sửa backend, database hay API contracts.
2. Trải nghiệm người dùng sẽ được nâng cấp vượt bậc thông qua kỹ thuật Hybrid Scrolling có kiểm soát (gesture-aware) mà không gây ảnh hưởng tiêu cực tới hệ thống mã QR vật lý và tính ổn định hiện có.

Tài liệu này được lưu trữ tại `Redesign_UIUX/05-risk-assessment.md` và đóng vai trò làm kim chỉ nam an toàn cho các Phase tiếp theo.
