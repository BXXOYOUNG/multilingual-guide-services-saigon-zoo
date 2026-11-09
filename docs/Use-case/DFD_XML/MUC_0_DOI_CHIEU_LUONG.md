# Đối chiếu DFD mức 0 hiện hành

09/11/2026 — fb1b0b8. Sáu tiến trình, E1–E6 và D1–D9. E6 là dịch native của Chrome tại máy.

## 02_MUC_0_HE_THONG.xml

**DFD MỨC 0 — TOÀN HỆ THỐNG** — 6 tiến trình, 71 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E1. Khách tham quan | 1.0 Quản lý ngôn ngữ | Lựa chọn ngôn ngữ | Lựa chọn ngôn ngữ |
| `flow_1` | 1.0 Quản lý ngôn ngữ | E1. Khách tham quan | Nhãn giao diện và kết quả lựa chọn | Nhãn giao diện và kết quả lựa chọn |
| `flow_2` | D9. Bộ nhớ thiết bị | 1.0 Quản lý ngôn ngữ | Ngôn ngữ đã lưu | Ngôn ngữ đã lưu |
| `flow_3` | 1.0 Quản lý ngôn ngữ | D9. Bộ nhớ thiết bị | Ngôn ngữ được chọn | Ngôn ngữ được chọn |
| `flow_4` | 1.0 Quản lý ngôn ngữ | 2.0 Cung cấp POI, bản đồ, lộ trình | F01 | Mã ngôn ngữ hiện tại |
| `flow_5` | 1.0 Quản lý ngôn ngữ | 3.0 Xử lý nghe và tự phát | F02 | Mã ngôn ngữ hiện tại |
| `flow_6` | 1.0 Quản lý ngôn ngữ | 4.0 Tải và quản lý audio ngoại tuyến | F03 | Mã ngôn ngữ hiện tại |
| `flow_7` | E1. Khách tham quan | 2.0 Cung cấp POI, bản đồ, lộ trình | Yêu cầu xem điểm, bản đồ, lộ trình, hướng dẫn | Yêu cầu xem điểm, bản đồ, lộ trình, hướng dẫn |
| `flow_8` | D1. POI và geofence | 2.0 Cung cấp POI, bản đồ, lộ trình | POI và vị trí | POI và vị trí |
| `flow_9` | D2. Nội dung ngôn ngữ | 2.0 Cung cấp POI, bản đồ, lộ trình | Nội dung đúng ngôn ngữ | Nội dung đúng ngôn ngữ |
| `flow_10` | D5. Tệp ảnh và MP3 | 2.0 Cung cấp POI, bản đồ, lộ trình | Ảnh loài vật | Ảnh loài vật |
| `flow_11` | D9. Bộ nhớ thiết bị | 2.0 Cung cấp POI, bản đồ, lộ trình | POI và ảnh đã cache | POI và ảnh đã cache |
| `flow_12` | 2.0 Cung cấp POI, bản đồ, lộ trình | D9. Bộ nhớ thiết bị | Snapshot POI và ảnh đã truy cập | Snapshot POI và ảnh đã truy cập |
| `flow_13` | 2.0 Cung cấp POI, bản đồ, lộ trình | E1. Khách tham quan | Thông tin điểm, bản đồ, lộ trình, hướng dẫn | Thông tin điểm, bản đồ, lộ trình, hướng dẫn |
| `flow_14` | 2.0 Cung cấp POI, bản đồ, lộ trình | E4. Dịch vụ bản đồ | Thông số ô bản đồ | Thông số ô bản đồ |
| `flow_15` | E4. Dịch vụ bản đồ | 2.0 Cung cấp POI, bản đồ, lộ trình | Ảnh nền bản đồ | Ảnh nền bản đồ |
| `flow_16` | 2.0 Cung cấp POI, bản đồ, lộ trình | E5. GPS và camera | Yêu cầu lấy vị trí | Yêu cầu lấy vị trí |
| `flow_17` | E5. GPS và camera | 2.0 Cung cấp POI, bản đồ, lộ trình | Tọa độ, độ chính xác, trạng thái GPS | Tọa độ, độ chính xác, trạng thái GPS |
| `flow_18` | 2.0 Cung cấp POI, bản đồ, lộ trình | 3.0 Xử lý nghe và tự phát | F04 | POI được chọn và tọa độ hiện tại |
| `flow_19` | E1. Khách tham quan | 3.0 Xử lý nghe và tự phát | Yêu cầu nghe, quét QR, bật tự phát hoặc mô phỏng | Yêu cầu nghe, quét QR, bật tự phát hoặc mô phỏng |
| `flow_20` | 3.0 Xử lý nghe và tự phát | E5. GPS và camera | Yêu cầu camera | Yêu cầu camera |
| `flow_21` | E5. GPS và camera | 3.0 Xử lý nghe và tự phát | Khung hình và trạng thái camera | Khung hình và trạng thái camera |
| `flow_22` | D1. POI và geofence | 3.0 Xử lý nghe và tự phát | Vùng kích hoạt và POI | Vùng kích hoạt và POI |
| `flow_23` | D2. Nội dung ngôn ngữ | 3.0 Xử lý nghe và tự phát | Liên kết audio hiện tại | Liên kết audio hiện tại |
| `flow_24` | D4. Metadata audio và gói | 3.0 Xử lý nghe và tự phát | Thông tin asset sẵn sàng | Thông tin asset sẵn sàng |
| `flow_25` | D5. Tệp ảnh và MP3 | 3.0 Xử lý nghe và tự phát | Dữ liệu MP3 | Dữ liệu MP3 |
| `flow_26` | D9. Bộ nhớ thiết bị | 3.0 Xử lý nghe và tự phát | Bản thu đã tải và định danh thiết bị | Bản thu đã tải và định danh thiết bị |
| `flow_27` | 3.0 Xử lý nghe và tự phát | E1. Khách tham quan | Âm thanh, thông tin và lỗi phát | Âm thanh, thông tin và lỗi phát |
| `flow_28` | 3.0 Xử lý nghe và tự phát | 4.0 Tải và quản lý audio ngoại tuyến | F05 | ID gói từ QR hợp lệ |
| `flow_29` | E1. Khách tham quan | 4.0 Tải và quản lý audio ngoại tuyến | Yêu cầu xem, tải hoặc xóa gói | Yêu cầu xem, tải hoặc xóa gói |
| `flow_30` | D4. Metadata audio và gói | 4.0 Tải và quản lý audio ngoại tuyến | Danh sách gói, manifest và checksum | Danh sách gói, manifest và checksum |
| `flow_31` | D5. Tệp ảnh và MP3 | 4.0 Tải và quản lý audio ngoại tuyến | Các tệp MP3 của gói | Các tệp MP3 của gói |
| `flow_32` | 4.0 Tải và quản lý audio ngoại tuyến | 2.0 Cung cấp POI, bản đồ, lộ trình | F06 | Yêu cầu metadata POI theo ngôn ngữ |
| `flow_33` | 2.0 Cung cấp POI, bản đồ, lộ trình | 4.0 Tải và quản lý audio ngoại tuyến | F07 | Metadata POI theo ngôn ngữ |
| `flow_34` | D9. Bộ nhớ thiết bị | 4.0 Tải và quản lý audio ngoại tuyến | Gói và bản thu đã lưu | Gói và bản thu đã lưu |
| `flow_35` | 4.0 Tải và quản lý audio ngoại tuyến | D9. Bộ nhớ thiết bị | Gói, Blob audio và dữ liệu sau xóa hoặc rollback | Gói, Blob audio và dữ liệu sau xóa hoặc rollback |
| `flow_36` | 4.0 Tải và quản lý audio ngoại tuyến | 3.0 Xử lý nghe và tự phát | F08 | Bản thu ngoại tuyến được chọn |
| `flow_37` | 4.0 Tải và quản lý audio ngoại tuyến | E1. Khách tham quan | Danh sách, QR gói, tiến độ và kết quả tải hoặc xóa | Danh sách, QR gói, tiến độ và kết quả tải hoặc xóa |
| `flow_38` | E2. Quản trị viên | 5.0 Quản trị nội dung và audio | Xác thực; POI/nội dung; nguồn/đích; yêu cầu dịch; bản sửa và xác nhận lưu; TTS/phát hành | Xác thực; POI/nội dung; nguồn/đích; yêu cầu dịch; bản sửa và xác nhận lưu; TTS/phát hành |
| `flow_39` | D6. Tài khoản và vai trò | 5.0 Quản trị nội dung và audio | Tài khoản, vai trò, quyền | Tài khoản, vai trò, quyền |
| `flow_40` | 5.0 Quản trị nội dung và audio | D6. Tài khoản và vai trò | Password hash mới khi đổi mật khẩu | Password hash mới khi đổi mật khẩu |
| `flow_41` | D7. Phiên và dữ liệu tạm | 5.0 Quản trị nội dung và audio | Phiên, bộ đếm, khóa TTS; token/nguồn/revision preview | Phiên, bộ đếm, khóa TTS; token/nguồn/revision preview |
| `flow_42` | 5.0 Quản trị nội dung và audio | D7. Phiên và dữ liệu tạm | Phiên, bộ đếm, lease; token/nguồn/revision đích có TTL | Phiên, bộ đếm, lease; token/nguồn/revision đích có TTL |
| `flow_43` | D1. POI và geofence | 5.0 Quản trị nội dung và audio | POI và geofence hiện có | POI và geofence hiện có |
| `flow_44` | 5.0 Quản trị nội dung và audio | D1. POI và geofence | POI và geofence cập nhật | POI và geofence cập nhật |
| `flow_45` | D2. Nội dung ngôn ngữ | 5.0 Quản trị nội dung và audio | Nội dung và liên kết audio hiện có | Nội dung và liên kết audio hiện có |
| `flow_46` | 5.0 Quản trị nội dung và audio | D2. Nội dung ngôn ngữ | Nội dung, trạng thái và liên kết audio mới | Nội dung, trạng thái và liên kết audio mới |
| `flow_47` | D3. Tác vụ audio | 5.0 Quản trị nội dung và audio | Trạng thái tác vụ | Trạng thái tác vụ |
| `flow_48` | 5.0 Quản trị nội dung và audio | D3. Tác vụ audio | Tác vụ và kết quả xử lý | Tác vụ và kết quả xử lý |
| `flow_49` | D4. Metadata audio và gói | 5.0 Quản trị nội dung và audio | Metadata audio và gói hiện có | Metadata audio và gói hiện có |
| `flow_50` | 5.0 Quản trị nội dung và audio | D4. Metadata audio và gói | Asset và snapshot gói mới | Asset và snapshot gói mới |
| `flow_51` | D5. Tệp ảnh và MP3 | 5.0 Quản trị nội dung và audio | Ảnh, audio nghe thử và metadata tệp | Ảnh, audio nghe thử và metadata tệp |
| `flow_52` | 5.0 Quản trị nội dung và audio | D5. Tệp ảnh và MP3 | Ảnh upload và MP3 tổng hợp | Ảnh upload và MP3 tổng hợp |
| `flow_53` | 5.0 Quản trị nội dung và audio | E3. Edge TTS | Văn bản và mã giọng | Văn bản và mã giọng |
| `flow_54` | E3. Edge TTS | 5.0 Quản trị nội dung và audio | MP3 hoặc kết quả lỗi | MP3 hoặc kết quả lỗi |
| `flow_55` | 5.0 Quản trị nội dung và audio | E2. Quản trị viên | Kết quả quản trị; preview/bản đối chiếu; lỗi/xung đột; tác vụ/audio/QR | Kết quả quản trị; preview/bản đối chiếu; lỗi/xung đột; tác vụ/audio/QR |
| `flow_56` | E1. Khách tham quan | 6.0 Ghi nhận và thống kê | Dữ liệu phiên, trang đang xem và hoạt động hiện diện | Dữ liệu phiên, trang đang xem và hoạt động hiện diện |
| `flow_57` | 2.0 Cung cấp POI, bản đồ, lộ trình | 6.0 Ghi nhận và thống kê | F09 | Sự kiện xem POI kèm ngôn ngữ |
| `flow_58` | 3.0 Xử lý nghe và tự phát | 6.0 Ghi nhận và thống kê | F10 | Sự kiện QR, audio và geofence kèm ngôn ngữ |
| `flow_59` | D9. Bộ nhớ thiết bị | 6.0 Ghi nhận và thống kê | Định danh ẩn danh đã lưu | Định danh ẩn danh đã lưu |
| `flow_60` | 6.0 Ghi nhận và thống kê | D9. Bộ nhớ thiết bị | Định danh ẩn danh mới | Định danh ẩn danh mới |
| `flow_61` | D7. Phiên và dữ liệu tạm | 6.0 Ghi nhận và thống kê | Phiên quản trị và bộ đếm sự kiện | Phiên quản trị và bộ đếm sự kiện |
| `flow_62` | 6.0 Ghi nhận và thống kê | D7. Phiên và dữ liệu tạm | Bộ đếm rate limit | Bộ đếm rate limit |
| `flow_63` | D6. Tài khoản và vai trò | 6.0 Ghi nhận và thống kê | Tài khoản, vai trò, quyền phân tích | Tài khoản, vai trò, quyền phân tích |
| `flow_64` | 6.0 Ghi nhận và thống kê | D8. Hoạt động sử dụng | Sự kiện và lịch sử sử dụng | Sự kiện và lịch sử sử dụng |
| `flow_65` | D8. Hoạt động sử dụng | 6.0 Ghi nhận và thống kê | Dữ liệu phục vụ tổng hợp | Dữ liệu phục vụ tổng hợp |
| `flow_66` | D1. POI và geofence | 6.0 Ghi nhận và thống kê | Tên POI cho thống kê | Tên POI cho thống kê |
| `flow_67` | E2. Quản trị viên | 6.0 Ghi nhận và thống kê | Yêu cầu dashboard kèm phiên | Yêu cầu dashboard kèm phiên |
| `flow_68` | 6.0 Ghi nhận và thống kê | E2. Quản trị viên | Số liệu dashboard hoặc lỗi xác thực | Số liệu dashboard hoặc lỗi xác thực |
| `flow_69` | 5.0 Quản trị nội dung và audio | E6. Chrome Translator API tại máy | Cặp ngôn ngữ; văn bản nguồn; yêu cầu tạo translator | Cặp ngôn ngữ; văn bản nguồn; yêu cầu tạo translator |
| `flow_70` | E6. Chrome Translator API tại máy | 5.0 Quản trị nội dung và audio | Bản dịch; khả năng hỗ trợ; tiến độ mô hình hoặc lỗi | Bản dịch; khả năng hỗ trợ; tiến độ mô hình hoặc lỗi |
