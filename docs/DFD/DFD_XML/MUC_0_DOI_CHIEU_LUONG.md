# Đối chiếu DFD mức 0

10/11/2026. Một kho logic D1 — Dữ liệu hệ thống. Các luồng cùng chiều giữa một tiến trình và kho được gộp; nội dung đầy đủ nằm dưới đây.

## 02_MUC_0_HE_THONG.xml

**DFD MỨC 0 — TOÀN HỆ THỐNG** — 6 tiến trình, 44 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E1. Khách tham quan | 1.0 Quản lý ngôn ngữ | Lựa chọn ngôn ngữ | Lựa chọn ngôn ngữ |
| `flow_1` | 1.0 Quản lý ngôn ngữ | E1. Khách tham quan | Giao diện và kết quả chọn | Nhãn giao diện và kết quả lựa chọn |
| `flow_2` | D1. Dữ liệu hệ thống | 1.0 Quản lý ngôn ngữ | Ngôn ngữ đã lưu | Ngôn ngữ đã lưu |
| `flow_3` | 1.0 Quản lý ngôn ngữ | D1. Dữ liệu hệ thống | Ngôn ngữ được chọn | Ngôn ngữ được chọn |
| `flow_4` | E1. Khách tham quan | 2.0 Cung cấp POI, bản đồ, lộ trình | Yêu cầu tra cứu | Yêu cầu xem điểm, bản đồ, lộ trình, hướng dẫn |
| `flow_5` | D1. Dữ liệu hệ thống | 2.0 Cung cấp POI, bản đồ, lộ trình | Dữ liệu POI và nội dung | POI và vị trí; Nội dung đúng ngôn ngữ; Ảnh loài vật; POI và ảnh đã cache |
| `flow_6` | 2.0 Cung cấp POI, bản đồ, lộ trình | D1. Dữ liệu hệ thống | POI và ảnh đã truy cập | Snapshot POI và ảnh đã truy cập |
| `flow_7` | 2.0 Cung cấp POI, bản đồ, lộ trình | E1. Khách tham quan | Thông tin tham quan | Thông tin điểm, bản đồ, lộ trình, hướng dẫn |
| `flow_8` | 2.0 Cung cấp POI, bản đồ, lộ trình | E4. Dịch vụ bản đồ | Thông số ô bản đồ | Thông số ô bản đồ |
| `flow_9` | E4. Dịch vụ bản đồ | 2.0 Cung cấp POI, bản đồ, lộ trình | Ảnh nền bản đồ | Ảnh nền bản đồ |
| `flow_10` | 2.0 Cung cấp POI, bản đồ, lộ trình | E5. GPS và camera | Yêu cầu vị trí | Yêu cầu lấy vị trí |
| `flow_11` | E5. GPS và camera | 2.0 Cung cấp POI, bản đồ, lộ trình | Vị trí và trạng thái GPS | Tọa độ, độ chính xác, trạng thái GPS |
| `flow_12` | E1. Khách tham quan | 3.0 Xử lý nghe và tự phát | Yêu cầu nghe hoặc quét | Yêu cầu nghe, quét QR, bật tự phát hoặc mô phỏng |
| `flow_13` | 3.0 Xử lý nghe và tự phát | E5. GPS và camera | Yêu cầu camera | Yêu cầu camera |
| `flow_14` | E5. GPS và camera | 3.0 Xử lý nghe và tự phát | Khung hình và trạng thái | Khung hình và trạng thái camera |
| `flow_15` | D1. Dữ liệu hệ thống | 3.0 Xử lý nghe và tự phát | Vùng, audio và định danh | Vùng kích hoạt và POI; Liên kết audio hiện tại; Thông tin asset sẵn sàng; Dữ liệu MP3; Bản thu đã tải và định danh thiết bị |
| `flow_16` | 3.0 Xử lý nghe và tự phát | E1. Khách tham quan | Audio và kết quả phát | Âm thanh, thông tin và lỗi phát |
| `flow_17` | E1. Khách tham quan | 4.0 Tải và quản lý audio ngoại tuyến | Yêu cầu quản lý gói | Yêu cầu xem, tải hoặc xóa gói |
| `flow_18` | D1. Dữ liệu hệ thống | 4.0 Tải và quản lý audio ngoại tuyến | Dữ liệu gói và audio | Danh sách gói, manifest và checksum; Các tệp MP3 của gói; Gói và bản thu đã lưu |
| `flow_19` | 4.0 Tải và quản lý audio ngoại tuyến | D1. Dữ liệu hệ thống | Gói và audio cập nhật | Gói, Blob audio và dữ liệu sau xóa hoặc rollback |
| `flow_20` | 4.0 Tải và quản lý audio ngoại tuyến | E1. Khách tham quan | Thông tin và kết quả gói | Danh sách, QR gói, tiến độ và kết quả tải hoặc xóa |
| `flow_21` | E2. Quản trị viên | 5.0 Quản trị nội dung và audio | Xác thực và yêu cầu quản trị | Xác thực; POI/nội dung; nguồn/đích; yêu cầu dịch; bản sửa và xác nhận lưu; TTS/phát hành |
| `flow_22` | D1. Dữ liệu hệ thống | 5.0 Quản trị nội dung và audio | Dữ liệu phục vụ quản trị | Tài khoản, vai trò, quyền; Phiên, bộ đếm, khóa TTS; token/nguồn/revision preview; POI và geofence hiện có; Nội dung và liên kết audio hiện có; Trạng thái tác vụ; Metadata audio và gói hiện có; Ảnh, audio nghe thử và metadata tệp |
| `flow_23` | 5.0 Quản trị nội dung và audio | D1. Dữ liệu hệ thống | Dữ liệu quản trị cập nhật | Password hash mới khi đổi mật khẩu; Phiên, bộ đếm, lease; token/nguồn/revision đích có TTL; POI và geofence cập nhật; Nội dung, trạng thái và liên kết audio mới; Tác vụ và kết quả xử lý; Asset và snapshot gói mới; Ảnh upload và MP3 tổng hợp |
| `flow_24` | 5.0 Quản trị nội dung và audio | E3. Edge TTS | Văn bản và giọng đọc | Văn bản và mã giọng |
| `flow_25` | E3. Edge TTS | 5.0 Quản trị nội dung và audio | MP3 hoặc lỗi TTS | MP3 hoặc kết quả lỗi |
| `flow_26` | 5.0 Quản trị nội dung và audio | E2. Quản trị viên | Kết quả quản trị | Kết quả quản trị; preview/bản đối chiếu; lỗi/xung đột; tác vụ/audio/QR |
| `flow_27` | 5.0 Quản trị nội dung và audio | E6. Chrome Translator API tại máy | Nguồn và yêu cầu dịch | Cặp ngôn ngữ; văn bản nguồn; yêu cầu tạo translator |
| `flow_28` | E6. Chrome Translator API tại máy | 5.0 Quản trị nội dung và audio | Bản dịch và trạng thái | Bản dịch; khả năng hỗ trợ; tiến độ mô hình hoặc lỗi |
| `flow_29` | E1. Khách tham quan | 6.0 Ghi nhận và thống kê | Hoạt động truy cập | Dữ liệu phiên, trang đang xem và hoạt động hiện diện |
| `flow_30` | D1. Dữ liệu hệ thống | 6.0 Ghi nhận và thống kê | Dữ liệu phục vụ phân tích | Định danh ẩn danh đã lưu; Phiên quản trị và bộ đếm sự kiện; Tài khoản, vai trò, quyền phân tích; Dữ liệu phục vụ tổng hợp; Tên POI cho thống kê |
| `flow_31` | 6.0 Ghi nhận và thống kê | D1. Dữ liệu hệ thống | Hoạt động và định danh mới | Định danh ẩn danh mới; Bộ đếm rate limit; Sự kiện và lịch sử sử dụng |
| `flow_32` | E2. Quản trị viên | 6.0 Ghi nhận và thống kê | Yêu cầu dashboard | Yêu cầu dashboard kèm phiên |
| `flow_33` | 6.0 Ghi nhận và thống kê | E2. Quản trị viên | Số liệu hoặc lỗi truy cập | Số liệu dashboard hoặc lỗi xác thực |
| `flow_34` | 1.0 Quản lý ngôn ngữ | 2.0 Cung cấp POI, bản đồ, lộ trình | Ngôn ngữ | Mã ngôn ngữ hiện tại |
| `flow_35` | 1.0 Quản lý ngôn ngữ | 3.0 Xử lý nghe và tự phát | Ngôn ngữ | Mã ngôn ngữ hiện tại |
| `flow_36` | 1.0 Quản lý ngôn ngữ | 4.0 Tải và quản lý audio ngoại tuyến | Ngôn ngữ | Mã ngôn ngữ hiện tại |
| `flow_37` | 2.0 Cung cấp POI, bản đồ, lộ trình | 3.0 Xử lý nghe và tự phát | POI và vị trí | POI được chọn và tọa độ hiện tại |
| `flow_38` | 3.0 Xử lý nghe và tự phát | 4.0 Tải và quản lý audio ngoại tuyến | Mã gói từ QR | ID gói từ QR hợp lệ |
| `flow_39` | 4.0 Tải và quản lý audio ngoại tuyến | 2.0 Cung cấp POI, bản đồ, lộ trình | Yêu cầu thông tin POI | Yêu cầu metadata POI theo ngôn ngữ |
| `flow_40` | 2.0 Cung cấp POI, bản đồ, lộ trình | 4.0 Tải và quản lý audio ngoại tuyến | Thông tin POI | Metadata POI theo ngôn ngữ |
| `flow_41` | 4.0 Tải và quản lý audio ngoại tuyến | 3.0 Xử lý nghe và tự phát | Bản thu ngoại tuyến | Bản thu ngoại tuyến được chọn |
| `flow_42` | 2.0 Cung cấp POI, bản đồ, lộ trình | 6.0 Ghi nhận và thống kê | Sự kiện xem POI | Sự kiện xem POI kèm ngôn ngữ |
| `flow_43` | 3.0 Xử lý nghe và tự phát | 6.0 Ghi nhận và thống kê | Sự kiện nghe và vùng | Sự kiện QR, audio và geofence kèm ngôn ngữ |
