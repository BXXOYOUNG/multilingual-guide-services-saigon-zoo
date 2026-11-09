# Đối chiếu DFD mức 1 và mức 2 hiện hành

09/11/2026 — fb1b0b8. Các file 03–10 dùng bố cục dọc; mã F đánh số riêng trong mỗi sơ đồ.

## 03_MUC_1_1_0_NGON_NGU.xml

**DFD MỨC 1 — PHÂN RÃ 1.0** — 4 tiến trình, 12 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | D9. Bộ nhớ thiết bị | 1.1 Khôi phục lựa chọn | Ngôn ngữ đã lưu hoặc trạng thái chưa chọn | Ngôn ngữ đã lưu hoặc trạng thái chưa chọn |
| `flow_1` | 1.1 Khôi phục lựa chọn | 1.2 Kiểm tra ngôn ngữ | F01 | Mã ngôn ngữ khôi phục |
| `flow_2` | E1. Khách tham quan | 1.2 Kiểm tra ngôn ngữ | Lựa chọn ngôn ngữ | Lựa chọn ngôn ngữ |
| `flow_3` | 1.2 Kiểm tra ngôn ngữ | E1. Khách tham quan | Kết quả cần chọn lại | Kết quả cần chọn lại |
| `flow_4` | 1.2 Kiểm tra ngôn ngữ | 1.3 Lưu lựa chọn | F02 | Mã ngôn ngữ hợp lệ |
| `flow_5` | 1.3 Lưu lựa chọn | D9. Bộ nhớ thiết bị | Ngôn ngữ được chọn | Ngôn ngữ được chọn |
| `flow_6` | 1.3 Lưu lựa chọn | E1. Khách tham quan | Kết quả lưu lựa chọn | Kết quả lưu lựa chọn |
| `flow_7` | 1.2 Kiểm tra ngôn ngữ | 1.4 Cung cấp ngữ cảnh ngôn ngữ | F03 | Ngôn ngữ hợp lệ |
| `flow_8` | 1.4 Cung cấp ngữ cảnh ngôn ngữ | E1. Khách tham quan | Nhãn giao diện theo ngôn ngữ | Nhãn giao diện theo ngôn ngữ |
| `flow_9` | 1.4 Cung cấp ngữ cảnh ngôn ngữ | 2.0 Cung cấp POI, bản đồ, lộ trình | Mã ngôn ngữ hiện tại | Mã ngôn ngữ hiện tại |
| `flow_10` | 1.4 Cung cấp ngữ cảnh ngôn ngữ | 3.0 Xử lý nghe và tự phát | Mã ngôn ngữ hiện tại | Mã ngôn ngữ hiện tại |
| `flow_11` | 1.4 Cung cấp ngữ cảnh ngôn ngữ | 4.0 Quản lý audio ngoại tuyến | Mã ngôn ngữ hiện tại | Mã ngôn ngữ hiện tại |

## 04_MUC_1_2_0_POI_BAN_DO_LO_TRINH.xml

**DFD MỨC 1 — PHÂN RÃ 2.0** — 4 tiến trình, 25 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E1. Khách tham quan | 2.1 Tiếp nhận nhu cầu tra cứu | Yêu cầu xem POI, bản đồ, lộ trình, hướng dẫn | Yêu cầu xem POI, bản đồ, lộ trình, hướng dẫn |
| `flow_1` | 1.0 Quản lý ngôn ngữ | 2.1 Tiếp nhận nhu cầu tra cứu | Mã ngôn ngữ hiện tại | Mã ngôn ngữ hiện tại |
| `flow_2` | 4.0 Quản lý audio ngoại tuyến | 2.1 Tiếp nhận nhu cầu tra cứu | Yêu cầu metadata POI theo ngôn ngữ | Yêu cầu metadata POI theo ngôn ngữ |
| `flow_3` | 2.1 Tiếp nhận nhu cầu tra cứu | 2.2 Tải và khôi phục POI | F01 | Tiêu chí POI và ngôn ngữ |
| `flow_4` | 2.1 Tiếp nhận nhu cầu tra cứu | 2.3 Cung cấp thông tin và bản đồ | F02 | Nhu cầu xem thông tin và bản đồ |
| `flow_5` | 2.1 Tiếp nhận nhu cầu tra cứu | 2.4 Cung cấp lộ trình và hướng dẫn | F03 | Nhu cầu lộ trình hoặc hướng dẫn |
| `flow_6` | D1. POI và geofence | 2.2 Tải và khôi phục POI | POI đang hiển thị và vị trí | POI đang hiển thị và vị trí |
| `flow_7` | D2. Nội dung ngôn ngữ | 2.2 Tải và khôi phục POI | Nội dung đúng ngôn ngữ | Nội dung đúng ngôn ngữ |
| `flow_8` | D9. Bộ nhớ thiết bị | 2.2 Tải và khôi phục POI | Snapshot POI theo ngôn ngữ | Snapshot POI theo ngôn ngữ |
| `flow_9` | 2.2 Tải và khôi phục POI | D9. Bộ nhớ thiết bị | Snapshot POI cập nhật | Snapshot POI cập nhật |
| `flow_10` | 2.2 Tải và khôi phục POI | 2.3 Cung cấp thông tin và bản đồ | F04 | Thông tin POI theo ngôn ngữ |
| `flow_11` | 2.2 Tải và khôi phục POI | 2.4 Cung cấp lộ trình và hướng dẫn | F05 | Danh sách POI có tọa độ |
| `flow_12` | 2.2 Tải và khôi phục POI | 4.0 Quản lý audio ngoại tuyến | Metadata POI theo ngôn ngữ | Metadata POI theo ngôn ngữ |
| `flow_13` | 2.2 Tải và khôi phục POI | E1. Khách tham quan | Lỗi không tải được POI | Lỗi không tải được POI |
| `flow_14` | D5. Tệp ảnh | 2.3 Cung cấp thông tin và bản đồ | Ảnh loài vật | Ảnh loài vật |
| `flow_15` | D9. Bộ nhớ thiết bị | 2.3 Cung cấp thông tin và bản đồ | Ảnh đã cache | Ảnh đã cache |
| `flow_16` | 2.3 Cung cấp thông tin và bản đồ | D9. Bộ nhớ thiết bị | Ảnh đã truy cập | Ảnh đã truy cập |
| `flow_17` | 2.3 Cung cấp thông tin và bản đồ | E4. Dịch vụ bản đồ | Thông số ô bản đồ | Thông số ô bản đồ |
| `flow_18` | E4. Dịch vụ bản đồ | 2.3 Cung cấp thông tin và bản đồ | Ảnh nền bản đồ | Ảnh nền bản đồ |
| `flow_19` | 2.3 Cung cấp thông tin và bản đồ | E5. Dịch vụ GPS | Yêu cầu lấy vị trí | Yêu cầu lấy vị trí |
| `flow_20` | E5. Dịch vụ GPS | 2.3 Cung cấp thông tin và bản đồ | Tọa độ, độ chính xác, trạng thái GPS | Tọa độ, độ chính xác, trạng thái GPS |
| `flow_21` | 2.3 Cung cấp thông tin và bản đồ | E1. Khách tham quan | Thông tin điểm, marker và điểm gần nhất | Thông tin điểm, marker và điểm gần nhất |
| `flow_22` | 2.3 Cung cấp thông tin và bản đồ | 3.0 Xử lý nghe và tự phát | POI được chọn và tọa độ hiện tại | POI được chọn và tọa độ hiện tại |
| `flow_23` | 2.3 Cung cấp thông tin và bản đồ | 6.0 Ghi nhận và thống kê | Sự kiện xem POI kèm ngôn ngữ | Sự kiện xem POI kèm ngôn ngữ |
| `flow_24` | 2.4 Cung cấp lộ trình và hướng dẫn | E1. Khách tham quan | Lộ trình gợi ý, liên kết bản đồ và hướng dẫn | Lộ trình gợi ý, liên kết bản đồ và hướng dẫn |

## 05_MUC_1_3_0_NGHE_VA_TU_PHAT.xml

**DFD MỨC 1 — PHÂN RÃ 3.0** — 5 tiến trình, 23 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E1. Khách | 3.1 Tiếp nhận yêu cầu | Yêu cầu nghe, quét, tự phát hoặc mô phỏng | Yêu cầu nghe, quét, tự phát hoặc mô phỏng |
| `flow_1` | 2.0 Tiến trình tham chiếu | 3.1 Tiếp nhận yêu cầu | POI và tọa độ | POI và tọa độ |
| `flow_2` | 1.0 Tiến trình tham chiếu | 3.1 Tiếp nhận yêu cầu | Ngôn ngữ | Ngôn ngữ |
| `flow_3` | 3.1 Tiếp nhận yêu cầu | E5. Camera | Yêu cầu camera | Yêu cầu camera |
| `flow_4` | E5. Camera | 3.2 Giải mã QR | Khung hình và trạng thái | Khung hình và trạng thái |
| `flow_5` | 3.1 Tiếp nhận yêu cầu | 3.3 Xác định vùng kích hoạt | F01 | Yêu cầu xét vùng và tọa độ |
| `flow_6` | D1. POI và geofence | 3.3 Xác định vùng kích hoạt | POI và vùng tròn | POI và vùng tròn |
| `flow_7` | 3.1 Tiếp nhận yêu cầu | 3.4 Xác định bản thu | F02 | POI và ngôn ngữ cần nghe |
| `flow_8` | 3.2 Giải mã QR | 3.4 Xác định bản thu | F03 | POI ID hợp lệ |
| `flow_9` | 3.2 Giải mã QR | 4.0 Tiến trình tham chiếu | Gói ID hợp lệ | Gói ID hợp lệ |
| `flow_10` | 3.2 Giải mã QR | E1. Khách | Lỗi QR hoặc camera | Lỗi QR hoặc camera |
| `flow_11` | 3.3 Xác định vùng kích hoạt | 3.4 Xác định bản thu | F04 | POI và ngôn ngữ cần phát |
| `flow_12` | 3.3 Xác định vùng kích hoạt | E1. Khách | Kết quả xét vùng | Kết quả xét vùng |
| `flow_13` | 3.3 Xác định vùng kích hoạt | 6.0 Tiến trình tham chiếu | Sự kiện vào hoặc ra vùng | Sự kiện vào hoặc ra vùng |
| `flow_14` | D2. Nội dung ngôn ngữ | 3.4 Xác định bản thu | Liên kết audio | Liên kết audio |
| `flow_15` | D4. Metadata audio | 3.4 Xác định bản thu | Asset sẵn sàng | Asset sẵn sàng |
| `flow_16` | D5. MP3 | 3.4 Xác định bản thu | Dữ liệu audio online | Dữ liệu audio online |
| `flow_17` | D9. Bộ nhớ thiết bị | 3.4 Xác định bản thu | Bản thu đã tải; định danh ẩn danh | Bản thu đã tải; định danh ẩn danh |
| `flow_18` | 3.4 Xác định bản thu | 3.5 Phát và ghi nhận kết quả | F05 | Blob hoặc URL và audio ID |
| `flow_19` | 4.0 Tiến trình tham chiếu | 3.5 Phát và ghi nhận kết quả | Bản thu ngoại tuyến được chọn | Bản thu ngoại tuyến được chọn |
| `flow_20` | 3.4 Xác định bản thu | E1. Khách | Lỗi thiếu bản thu | Lỗi thiếu bản thu |
| `flow_21` | 3.5 Phát và ghi nhận kết quả | E1. Khách | Âm thanh và kết quả phát | Âm thanh và kết quả phát |
| `flow_22` | 3.5 Phát và ghi nhận kết quả | 6.0 Tiến trình tham chiếu | Sự kiện QR và audio kèm ngôn ngữ | Sự kiện QR và audio kèm ngôn ngữ |

## 06_MUC_1_4_0_AUDIO_NGOAI_TUYEN.xml

**DFD MỨC 1 — PHÂN RÃ 4.0** — 4 tiến trình, 21 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E1. Khách | 4.1 Xác định gói | Yêu cầu xem hoặc tải gói | Yêu cầu xem hoặc tải gói |
| `flow_1` | 1.0 Tiến trình tham chiếu | 4.1 Xác định gói | Ngôn ngữ | Ngôn ngữ |
| `flow_2` | 3.2 Tiến trình tham chiếu | 4.1 Xác định gói | Gói ID từ QR | Gói ID từ QR |
| `flow_3` | D4. Metadata audio và gói | 4.1 Xác định gói | Danh sách gói | Danh sách gói |
| `flow_4` | 4.1 Xác định gói | E1. Khách | Danh sách và QR gói | Danh sách và QR gói |
| `flow_5` | 4.1 Xác định gói | 4.2 Đọc manifest | F01 | Gói ID được chọn |
| `flow_6` | D4. Metadata audio và gói | 4.2 Đọc manifest | Manifest, checksum và size | Manifest, checksum và size |
| `flow_7` | 4.2 Đọc manifest | 2.0 Tiến trình tham chiếu | Yêu cầu metadata POI | Yêu cầu metadata POI |
| `flow_8` | 2.0 Tiến trình tham chiếu | 4.2 Đọc manifest | Metadata POI theo ngôn ngữ | Metadata POI theo ngôn ngữ |
| `flow_9` | 4.2 Đọc manifest | 4.3 Tải, kiểm tra, lưu | F02 | Danh sách asset và tiêu chí kiểm tra |
| `flow_10` | D5. MP3 | 4.3 Tải, kiểm tra, lưu | Bytes audio | Bytes audio |
| `flow_11` | D9. Bộ nhớ thiết bị | 4.3 Tải, kiểm tra, lưu | Dữ liệu trước tải | Dữ liệu trước tải |
| `flow_12` | E1. Khách | 4.3 Tải, kiểm tra, lưu | Yêu cầu hủy tải | Yêu cầu hủy tải |
| `flow_13` | 4.3 Tải, kiểm tra, lưu | D9. Bộ nhớ thiết bị | Blob, gói hoặc dữ liệu được khôi phục | Blob, gói hoặc dữ liệu được khôi phục |
| `flow_14` | 4.2 Đọc manifest | E1. Khách | Lỗi gói | Lỗi gói |
| `flow_15` | 4.3 Tải, kiểm tra, lưu | E1. Khách | Tiến độ và kết quả tải | Tiến độ và kết quả tải |
| `flow_16` | E1. Khách | 4.4 Tra cứu và xóa | Yêu cầu xem, xóa hoặc chọn bản thu | Yêu cầu xem, xóa hoặc chọn bản thu |
| `flow_17` | D9. Bộ nhớ thiết bị | 4.4 Tra cứu và xóa | Gói và bản thu đã lưu | Gói và bản thu đã lưu |
| `flow_18` | 4.4 Tra cứu và xóa | D9. Bộ nhớ thiết bị | Dữ liệu sau xóa | Dữ liệu sau xóa |
| `flow_19` | 4.4 Tra cứu và xóa | E1. Khách | Danh sách và kết quả xóa | Danh sách và kết quả xóa |
| `flow_20` | 4.4 Tra cứu và xóa | 3.5 Tiến trình tham chiếu | Bản thu ngoại tuyến được chọn | Bản thu ngoại tuyến được chọn |

## 07_MUC_1_5_0_QUAN_TRI_NOI_DUNG.xml

**DFD MỨC 1 — PHÂN RÃ 5.0** — 7 tiến trình, 60 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E2. Admin | 5.1 Xác thực và quyền | Đăng nhập, phiên hoặc đổi mật khẩu | Đăng nhập, phiên hoặc đổi mật khẩu |
| `flow_1` | D6. Tài khoản và vai trò | 5.1 Xác thực và quyền | Tài khoản và quyền | Tài khoản và quyền |
| `flow_2` | 5.1 Xác thực và quyền | D6. Tài khoản và vai trò | Hash mật khẩu mới | Hash mật khẩu mới |
| `flow_3` | D7. Redis | 5.1 Xác thực và quyền | Phiên và bộ đếm | Phiên và bộ đếm |
| `flow_4` | 5.1 Xác thực và quyền | D7. Redis | Phiên và bộ đếm cập nhật | Phiên và bộ đếm cập nhật |
| `flow_5` | 5.1 Xác thực và quyền | E2. Admin | Kết quả xác thực | Kết quả xác thực |
| `flow_6` | E2. Admin | 5.2 Quản lý POI và geofence | Dữ liệu POI và vùng | Dữ liệu POI và vùng |
| `flow_7` | E2. Admin | 5.3 Kiểm tra và lưu ảnh | Ảnh hoặc URL ảnh | Ảnh hoặc URL ảnh |
| `flow_8` | E2. Admin | 5.4 Quản lý nội dung | Nội dung theo ngôn ngữ | Nội dung theo ngôn ngữ |
| `flow_9` | E2. Admin | 5.5 Tạo và theo dõi TTS | Yêu cầu tạo, giọng, truy vấn trạng thái | Yêu cầu tạo, giọng, truy vấn trạng thái |
| `flow_10` | E2. Admin | 5.6 Phát hành gói và QR | Yêu cầu phát hành hoặc xem QR | Yêu cầu phát hành hoặc xem QR |
| `flow_11` | 5.1 Xác thực và quyền | 5.2 Quản lý POI và geofence | F01 | Thông tin quyền |
| `flow_12` | 5.1 Xác thực và quyền | 5.3 Kiểm tra và lưu ảnh | F02 | Thông tin quyền |
| `flow_13` | 5.1 Xác thực và quyền | 5.4 Quản lý nội dung | F03 | Thông tin quyền |
| `flow_14` | 5.1 Xác thực và quyền | 5.5 Tạo và theo dõi TTS | F04 | Thông tin quyền |
| `flow_15` | 5.1 Xác thực và quyền | 5.6 Phát hành gói và QR | F05 | Thông tin quyền |
| `flow_16` | D1. POI và geofence | 5.2 Quản lý POI và geofence | Dữ liệu hiện có | Dữ liệu hiện có |
| `flow_17` | 5.2 Quản lý POI và geofence | D1. POI và geofence | POI và vùng cập nhật | POI và vùng cập nhật |
| `flow_18` | 5.2 Quản lý POI và geofence | 5.4 Quản lý nội dung | F06 | ID và nội dung đầu tiên |
| `flow_19` | 5.2 Quản lý POI và geofence | E2. Admin | Kết quả lưu | Kết quả lưu |
| `flow_20` | D1. POI và geofence | 5.3 Kiểm tra và lưu ảnh | POI cần gắn ảnh | POI cần gắn ảnh |
| `flow_21` | 5.3 Kiểm tra và lưu ảnh | D1. POI và geofence | Liên kết ảnh | Liên kết ảnh |
| `flow_22` | 5.3 Kiểm tra và lưu ảnh | D5. Tệp media | Binary ảnh upload | Binary ảnh upload |
| `flow_23` | D5. Tệp media | 5.3 Kiểm tra và lưu ảnh | Ảnh hiện có | Ảnh hiện có |
| `flow_24` | 5.3 Kiểm tra và lưu ảnh | E2. Admin | Ảnh xem trước và kết quả | Ảnh xem trước và kết quả |
| `flow_25` | D1. POI và geofence | 5.4 Quản lý nội dung | POI hiện hữu | POI hiện hữu |
| `flow_26` | D2. Nội dung ngôn ngữ | 5.4 Quản lý nội dung | Bản hiện tại | Bản hiện tại |
| `flow_27` | 5.4 Quản lý nội dung | D2. Nội dung ngôn ngữ | Nội dung; vô hiệu audio khi lời đổi; đánh dấu bản phụ thuộc cần rà soát | Nội dung; vô hiệu audio khi lời đổi; đánh dấu bản phụ thuộc cần rà soát |
| `flow_28` | 5.4 Quản lý nội dung | E2. Admin | Kết quả lưu | Kết quả lưu |
| `flow_29` | 5.4 Quản lý nội dung | 5.5 Tạo và theo dõi TTS | F07 | Định danh nội dung đã lưu khi admin chọn tạo audio |
| `flow_30` | D1. POI và geofence | 5.5 Tạo và theo dõi TTS | POI hiện hữu | POI hiện hữu |
| `flow_31` | D2. Nội dung ngôn ngữ | 5.5 Tạo và theo dõi TTS | Văn bản và task hiện tại | Văn bản và task hiện tại |
| `flow_32` | D3. Tác vụ audio | 5.5 Tạo và theo dõi TTS | Trạng thái tác vụ | Trạng thái tác vụ |
| `flow_33` | 5.5 Tạo và theo dõi TTS | D3. Tác vụ audio | Tác vụ và kết quả | Tác vụ và kết quả |
| `flow_34` | D7. Redis | 5.5 Tạo và theo dõi TTS | Khóa hiện có | Khóa hiện có |
| `flow_35` | 5.5 Tạo và theo dõi TTS | D7. Redis | Khóa có TTL hoặc dữ liệu sau giải phóng | Khóa có TTL hoặc dữ liệu sau giải phóng |
| `flow_36` | 5.5 Tạo và theo dõi TTS | E3. Edge TTS | Văn bản và giọng | Văn bản và giọng |
| `flow_37` | E3. Edge TTS | 5.5 Tạo và theo dõi TTS | MP3 hoặc lỗi | MP3 hoặc lỗi |
| `flow_38` | 5.5 Tạo và theo dõi TTS | D5. Tệp media | MP3 mới | MP3 mới |
| `flow_39` | D5. Tệp media | 5.5 Tạo và theo dõi TTS | MP3 nghe thử | MP3 nghe thử |
| `flow_40` | 5.5 Tạo và theo dõi TTS | D4. Audio và gói | Metadata asset | Metadata asset |
| `flow_41` | D4. Audio và gói | 5.5 Tạo và theo dõi TTS | Asset nghe thử hiện tại | Asset nghe thử hiện tại |
| `flow_42` | 5.5 Tạo và theo dõi TTS | D2. Nội dung ngôn ngữ | Liên kết audio và trạng thái hiện tại | Liên kết audio và trạng thái hiện tại |
| `flow_43` | 5.5 Tạo và theo dõi TTS | E2. Admin | ID, trạng thái, audio nghe thử hoặc lỗi | ID, trạng thái, audio nghe thử hoặc lỗi |
| `flow_44` | D1. POI và geofence | 5.6 Phát hành gói và QR | POI đang hiển thị | POI đang hiển thị |
| `flow_45` | D2. Nội dung ngôn ngữ | 5.6 Phát hành gói và QR | Liên kết audio đúng ngôn ngữ | Liên kết audio đúng ngôn ngữ |
| `flow_46` | D4. Audio và gói | 5.6 Phát hành gói và QR | Asset và gói hiện có | Asset và gói hiện có |
| `flow_47` | D5. Tệp media | 5.6 Phát hành gói và QR | Size và checksum tệp | Size và checksum tệp |
| `flow_48` | 5.6 Phát hành gói và QR | D4. Audio và gói | Snapshot asset và gói mới | Snapshot asset và gói mới |
| `flow_49` | 5.6 Phát hành gói và QR | E2. Admin | QR và kết quả phát hành | QR và kết quả phát hành |
| `flow_50` | E2. Admin | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | Nguồn/đích đã lưu; thao tác dịch; bản chỉnh sửa; xác nhận thay thế/lưu | Nguồn/đích đã lưu; thao tác dịch; bản chỉnh sửa; xác nhận thay thế/lưu |
| `flow_51` | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | E2. Admin | Preview/đối chiếu; tiến độ; kết quả lưu hoặc lỗi/xung đột | Preview/đối chiếu; tiến độ; kết quả lưu hoặc lỗi/xung đột |
| `flow_52` | 5.1 Xác thực và quyền | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | F08 | Thông tin quyền content:write |
| `flow_53` | D1. POI và geofence | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | POI hiện hữu | POI hiện hữu |
| `flow_54` | D2. Nội dung ngôn ngữ | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | Lời nguồn đã lưu; bản đích và revision hiện tại | Lời nguồn đã lưu; bản đích và revision hiện tại |
| `flow_55` | D7. Redis | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | Token, nguồn/revision và bộ đếm chuẩn bị preview | Token, nguồn/revision và bộ đếm chuẩn bị preview |
| `flow_56` | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | D7. Redis | Token gắn admin/POI, nguồn và revision đích; TTL 30 phút | Token gắn admin/POI, nguồn và revision đích; TTL 30 phút |
| `flow_57` | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | E6. Chrome Translator API tại máy | Cặp ngôn ngữ; văn bản nguồn; yêu cầu tạo translator | Cặp ngôn ngữ; văn bản nguồn; yêu cầu tạo translator |
| `flow_58` | E6. Chrome Translator API tại máy | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | Bản dịch; khả năng hỗ trợ; tiến độ mô hình hoặc lỗi | Bản dịch; khả năng hỗ trợ; tiến độ mô hình hoặc lỗi |
| `flow_59` | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | D2. Nội dung ngôn ngữ | Transaction bản dịch đã xác nhận; metadata nguồn/review; vô hiệu audio khi lời đổi | Transaction bản dịch đã xác nhận; metadata nguồn/review; vô hiệu audio khi lời đổi |

## 08_MUC_1_6_0_ANALYTICS.xml

**DFD MỨC 1 — PHÂN RÃ 6.0** — 4 tiến trình, 18 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E1. Khách tham quan | 6.1 Chuẩn bị định danh và sự kiện | Dữ liệu phiên, trang và hoạt động hiện diện | Dữ liệu phiên, trang và hoạt động hiện diện |
| `flow_1` | 2.0 Cung cấp POI và bản đồ | 6.1 Chuẩn bị định danh và sự kiện | Sự kiện xem POI kèm ngôn ngữ | Sự kiện xem POI kèm ngôn ngữ |
| `flow_2` | 3.0 Xử lý nghe và tự phát | 6.1 Chuẩn bị định danh và sự kiện | Sự kiện QR, audio và geofence kèm ngôn ngữ | Sự kiện QR, audio và geofence kèm ngôn ngữ |
| `flow_3` | D9. Bộ nhớ thiết bị | 6.1 Chuẩn bị định danh và sự kiện | Định danh ẩn danh đã lưu | Định danh ẩn danh đã lưu |
| `flow_4` | 6.1 Chuẩn bị định danh và sự kiện | D9. Bộ nhớ thiết bị | Định danh ẩn danh mới | Định danh ẩn danh mới |
| `flow_5` | 6.1 Chuẩn bị định danh và sự kiện | 6.2 Kiểm tra và ghi hoạt động | F01 | Payload định danh và sự kiện |
| `flow_6` | D7. Phiên và bộ đếm Redis | 6.2 Kiểm tra và ghi hoạt động | Bộ đếm rate limit | Bộ đếm rate limit |
| `flow_7` | 6.2 Kiểm tra và ghi hoạt động | D7. Phiên và bộ đếm Redis | Bộ đếm cập nhật | Bộ đếm cập nhật |
| `flow_8` | 6.2 Kiểm tra và ghi hoạt động | D8. Hoạt động sử dụng | Thiết bị, phiên, sự kiện, lịch sử nghe và vị trí | Thiết bị, phiên, sự kiện, lịch sử nghe và vị trí |
| `flow_9` | 6.2 Kiểm tra và ghi hoạt động | 6.1 Chuẩn bị định danh và sự kiện | F02 | Kết quả tiếp nhận hoặc lỗi |
| `flow_10` | E2. Quản trị viên | 6.3 Kiểm tra quyền phân tích | Yêu cầu dashboard kèm phiên | Yêu cầu dashboard kèm phiên |
| `flow_11` | D7. Phiên và bộ đếm Redis | 6.3 Kiểm tra quyền phân tích | Phiên quản trị | Phiên quản trị |
| `flow_12` | D6. Tài khoản và vai trò | 6.3 Kiểm tra quyền phân tích | Tài khoản và quyền phân tích | Tài khoản và quyền phân tích |
| `flow_13` | 6.3 Kiểm tra quyền phân tích | E2. Quản trị viên | Lỗi xác thực hoặc phân quyền | Lỗi xác thực hoặc phân quyền |
| `flow_14` | 6.3 Kiểm tra quyền phân tích | 6.4 Tổng hợp và cung cấp dashboard | F03 | Yêu cầu dashboard hợp lệ |
| `flow_15` | D8. Hoạt động sử dụng | 6.4 Tổng hợp và cung cấp dashboard | Sự kiện và lịch sử phục vụ tổng hợp | Sự kiện và lịch sử phục vụ tổng hợp |
| `flow_16` | D1. POI | 6.4 Tổng hợp và cung cấp dashboard | Tên POI cho thống kê | Tên POI cho thống kê |
| `flow_17` | 6.4 Tổng hợp và cung cấp dashboard | E2. Quản trị viên | KPI, biểu đồ và bảng thống kê | KPI, biểu đồ và bảng thống kê |

## 09_MUC_2_5_5_TAO_AUDIO_TTS.xml

**DFD MỨC 2 — PHÂN RÃ 5.5** — 5 tiến trình, 32 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E2. Admin | 5.5.1 Kiểm tra nội dung | POI, ngôn ngữ, giọng và yêu cầu tạo | POI, ngôn ngữ, giọng và yêu cầu tạo |
| `flow_1` | 5.1 Tiến trình tham chiếu | 5.5.1 Kiểm tra nội dung | Thông tin quyền | Thông tin quyền |
| `flow_2` | 5.4 Tiến trình tham chiếu | 5.5.1 Kiểm tra nội dung | Định danh nội dung đã lưu | Định danh nội dung đã lưu |
| `flow_3` | D1. POI | 5.5.1 Kiểm tra nội dung | POI hiện hữu | POI hiện hữu |
| `flow_4` | D2. Nội dung ngôn ngữ | 5.5.1 Kiểm tra nội dung | Title, description và task hiện tại | Title, description và task hiện tại |
| `flow_5` | 5.5.1 Kiểm tra nội dung | E2. Admin | Lỗi đầu vào | Lỗi đầu vào |
| `flow_6` | 5.5.1 Kiểm tra nội dung | 5.5.2 Đăng ký tác vụ | F01 | Bản nguồn và giọng hợp lệ |
| `flow_7` | D7. Lease Redis | 5.5.2 Đăng ký tác vụ | Khóa hiện có | Khóa hiện có |
| `flow_8` | 5.5.2 Đăng ký tác vụ | D7. Lease Redis | Khóa mới có TTL | Khóa mới có TTL |
| `flow_9` | 5.5.2 Đăng ký tác vụ | D3. Tác vụ audio | Task Pending | Task Pending |
| `flow_10` | 5.5.2 Đăng ký tác vụ | D2. Nội dung ngôn ngữ | Task ID và trạng thái Pending | Task ID và trạng thái Pending |
| `flow_11` | 5.5.2 Đăng ký tác vụ | E2. Admin | ID và trạng thái ban đầu hoặc lỗi trùng | ID và trạng thái ban đầu hoặc lỗi trùng |
| `flow_12` | 5.5.2 Đăng ký tác vụ | 5.5.3 Tổng hợp giọng | F02 | Task và nội dung nguồn |
| `flow_13` | 5.5.3 Tổng hợp giọng | D3. Tác vụ audio | Trạng thái Processing | Trạng thái Processing |
| `flow_14` | 5.5.3 Tổng hợp giọng | D2. Nội dung ngôn ngữ | Trạng thái Processing của bản hiện tại | Trạng thái Processing của bản hiện tại |
| `flow_15` | 5.5.3 Tổng hợp giọng | E3. Edge TTS | Văn bản và giọng | Văn bản và giọng |
| `flow_16` | E3. Edge TTS | 5.5.3 Tổng hợp giọng | MP3 hoặc lỗi | MP3 hoặc lỗi |
| `flow_17` | 5.5.3 Tổng hợp giọng | 5.5.4 Kiểm tra và lưu bản thu | F03 | Bytes và thông tin audio |
| `flow_18` | 5.5.4 Kiểm tra và lưu bản thu | D5. Kho media | MP3 và checksum | MP3 và checksum |
| `flow_19` | 5.5.4 Kiểm tra và lưu bản thu | D4. Asset | Metadata asset | Metadata asset |
| `flow_20` | 5.5.4 Kiểm tra và lưu bản thu | 5.5.5 Cập nhật và cung cấp kết quả | F04 | Object key, checksum, size, duration và task ID |
| `flow_21` | 5.5.3 Tổng hợp giọng | 5.5.5 Cập nhật và cung cấp kết quả | F05 | Thông tin lỗi tổng hợp |
| `flow_22` | 5.5.4 Kiểm tra và lưu bản thu | 5.5.5 Cập nhật và cung cấp kết quả | F06 | Thông tin lỗi lưu tệp hoặc metadata |
| `flow_23` | D2. Nội dung ngôn ngữ | 5.5.5 Cập nhật và cung cấp kết quả | Nội dung và task hiện tại để đối chiếu | Nội dung và task hiện tại để đối chiếu |
| `flow_24` | D3. Tác vụ audio | 5.5.5 Cập nhật và cung cấp kết quả | Tác vụ và thời điểm cập nhật | Tác vụ và thời điểm cập nhật |
| `flow_25` | E2. Admin | 5.5.5 Cập nhật và cung cấp kết quả | Yêu cầu trạng thái hoặc nghe thử | Yêu cầu trạng thái hoặc nghe thử |
| `flow_26` | D4. Asset | 5.5.5 Cập nhật và cung cấp kết quả | Metadata asset nghe thử | Metadata asset nghe thử |
| `flow_27` | D5. Kho media | 5.5.5 Cập nhật và cung cấp kết quả | MP3 nghe thử | MP3 nghe thử |
| `flow_28` | 5.5.5 Cập nhật và cung cấp kết quả | D2. Nội dung ngôn ngữ | Liên kết audio và trạng thái phù hợp | Liên kết audio và trạng thái phù hợp |
| `flow_29` | 5.5.5 Cập nhật và cung cấp kết quả | D3. Tác vụ audio | Completed hoặc Failed và kết quả | Completed hoặc Failed và kết quả |
| `flow_30` | 5.5.5 Cập nhật và cung cấp kết quả | D7. Lease Redis | Dữ liệu sau giải phóng lease | Dữ liệu sau giải phóng lease |
| `flow_31` | 5.5.5 Cập nhật và cung cấp kết quả | E2. Admin | Trạng thái, audio nghe thử hoặc lỗi | Trạng thái, audio nghe thử hoặc lỗi |

## 10_MUC_2_5_7_DICH_CHROME.xml

**DFD MỨC 2 — PHÂN RÃ 5.7: DỊCH BẰNG CHROME** — 4 tiến trình, 24 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E2. Quản trị viên | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | POI, ngôn ngữ nguồn/đích, title/description đã lưu; yêu cầu chuẩn bị | POI, ngôn ngữ nguồn/đích, title/description đã lưu; yêu cầu chuẩn bị |
| `flow_1` | 5.1 Xác thực và kiểm tra quyền | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | Thông tin quyền content:write | Thông tin quyền content:write |
| `flow_2` | D1. POI và geofence | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | POI hiện hữu | POI hiện hữu |
| `flow_3` | D2. Nội dung theo ngôn ngữ | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | Lời nguồn đã lưu; bản đích và revision | Lời nguồn đã lưu; bản đích và revision |
| `flow_4` | D7. Phiên và dữ liệu tạm Redis | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | Bộ đếm chuẩn bị preview | Bộ đếm chuẩn bị preview |
| `flow_5` | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | D7. Phiên và dữ liệu tạm Redis | Token gắn admin/POI; nguồn/revision đích; TTL 30 phút; bộ đếm 3 giây | Token gắn admin/POI; nguồn/revision đích; TTL 30 phút; bộ đếm 3 giây |
| `flow_6` | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | E2. Quản trị viên | Preview sẵn sàng và nội dung đối chiếu hoặc lỗi đầu vào | Preview sẵn sàng và nội dung đối chiếu hoặc lỗi đầu vào |
| `flow_7` | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | 5.7.2 Kiểm tra native API, tải mô hình và dịch | F01 | Nguồn/đích và token chuẩn bị |
| `flow_8` | E2. Quản trị viên | 5.7.2 Kiểm tra native API, tải mô hình và dịch | Thao tác bấm dịch hoặc thử lại/hủy | Thao tác bấm dịch hoặc thử lại/hủy |
| `flow_9` | 5.7.2 Kiểm tra native API, tải mô hình và dịch | E6. Chrome Translator API tại máy | Cặp ngôn ngữ; văn bản nguồn; yêu cầu tạo translator | Cặp ngôn ngữ; văn bản nguồn; yêu cầu tạo translator |
| `flow_10` | E6. Chrome Translator API tại máy | 5.7.2 Kiểm tra native API, tải mô hình và dịch | Bản dịch; khả năng hỗ trợ; tiến độ mô hình hoặc lỗi | Bản dịch; khả năng hỗ trợ; tiến độ mô hình hoặc lỗi |
| `flow_11` | 5.7.2 Kiểm tra native API, tải mô hình và dịch | E2. Quản trị viên | Tiến độ tải/dịch; lỗi từng ngôn ngữ hoặc trạng thái hủy | Tiến độ tải/dịch; lỗi từng ngôn ngữ hoặc trạng thái hủy |
| `flow_12` | 5.7.2 Kiểm tra native API, tải mô hình và dịch | 5.7.3 Đối chiếu, chỉnh sửa và chọn bản lưu | F02 | Bản dịch mới trong bộ nhớ React; nguồn và token |
| `flow_13` | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | 5.7.3 Đối chiếu, chỉnh sửa và chọn bản lưu | F03 | Nội dung đích hiện có để đối chiếu |
| `flow_14` | E2. Quản trị viên | 5.7.3 Đối chiếu, chỉnh sửa và chọn bản lưu | Nội dung sửa; lựa chọn bản dịch; đồng ý thay thế | Nội dung sửa; lựa chọn bản dịch; đồng ý thay thế |
| `flow_15` | 5.7.3 Đối chiếu, chỉnh sửa và chọn bản lưu | E2. Quản trị viên | Các bản xem trước đã chỉnh; bản cũ để đối chiếu | Các bản xem trước đã chỉnh; bản cũ để đối chiếu |
| `flow_16` | 5.7.3 Đối chiếu, chỉnh sửa và chọn bản lưu | 5.7.4 Kiểm tra xung đột và lưu transaction | F04 | Token; các bản đã chọn/chỉnh; cờ replace_existing |
| `flow_17` | E2. Quản trị viên | 5.7.4 Kiểm tra xung đột và lưu transaction | Yêu cầu xác nhận lưu | Yêu cầu xác nhận lưu |
| `flow_18` | 5.1 Xác thực và kiểm tra quyền | 5.7.4 Kiểm tra xung đột và lưu transaction | Thông tin quyền content:write | Thông tin quyền content:write |
| `flow_19` | D7. Phiên và dữ liệu tạm Redis | 5.7.4 Kiểm tra xung đột và lưu transaction | Token còn hạn, admin/POI, nguồn và revision đích chuẩn bị | Token còn hạn, admin/POI, nguồn và revision đích chuẩn bị |
| `flow_20` | D1. POI và geofence | 5.7.4 Kiểm tra xung đột và lưu transaction | POI hiện hữu | POI hiện hữu |
| `flow_21` | D2. Nội dung theo ngôn ngữ | 5.7.4 Kiểm tra xung đột và lưu transaction | Nguồn, bản đích, revision và audio hiện tại | Nguồn, bản đích, revision và audio hiện tại |
| `flow_22` | 5.7.4 Kiểm tra xung đột và lưu transaction | D2. Nội dung theo ngôn ngữ | Transaction bản dịch; guard nguồn; provenance/review; vô hiệu audio khi lời đổi | Transaction bản dịch; guard nguồn; provenance/review; vô hiệu audio khi lời đổi |
| `flow_23` | 5.7.4 Kiểm tra xung đột và lưu transaction | E2. Quản trị viên | Ngôn ngữ đã lưu; nhắc tạo audio hoặc lỗi/xung đột 409 | Ngôn ngữ đã lưu; nhắc tạo audio hoặc lỗi/xung đột 409 |
