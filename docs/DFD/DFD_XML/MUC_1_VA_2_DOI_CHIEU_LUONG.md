# Đối chiếu DFD mức 1 và mức 2

10/11/2026. D1.1 — Dữ liệu dùng chung; D1.2 — Dữ liệu trên thiết bị. Cả hai thuộc D1 ở mức 0. Nhãn trên hình được rút gọn; cột cuối giữ dữ liệu đầy đủ. Các mũi tên trên hình ghi tên dữ liệu ngắn gọn; ID flow chỉ dùng tra cứu XML.

## 03_MUC_1_1_0_NGON_NGU.xml

**DFD MỨC 1 — PHÂN RÃ 1.0** — 4 tiến trình, 12 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | D1.2. Dữ liệu trên thiết bị | 1.1 Khôi phục lựa chọn | Ngôn ngữ đã lưu hoặc trạng thái chưa chọn | Ngôn ngữ đã lưu hoặc trạng thái chưa chọn |
| `flow_1` | E1. Khách tham quan | 1.2 Kiểm tra ngôn ngữ | Lựa chọn ngôn ngữ | Lựa chọn ngôn ngữ |
| `flow_2` | 1.2 Kiểm tra ngôn ngữ | E1. Khách tham quan | Kết quả cần chọn lại | Kết quả cần chọn lại |
| `flow_3` | 1.3 Lưu lựa chọn | D1.2. Dữ liệu trên thiết bị | Ngôn ngữ được chọn | Ngôn ngữ được chọn |
| `flow_4` | 1.3 Lưu lựa chọn | E1. Khách tham quan | Kết quả lưu lựa chọn | Kết quả lưu lựa chọn |
| `flow_5` | 1.4 Cung cấp ngữ cảnh ngôn ngữ | E1. Khách tham quan | Nhãn giao diện theo ngôn ngữ | Nhãn giao diện theo ngôn ngữ |
| `flow_6` | 1.4 Cung cấp ngữ cảnh ngôn ngữ | 2.0 Cung cấp POI, bản đồ, lộ trình | Mã ngôn ngữ hiện tại | Mã ngôn ngữ hiện tại |
| `flow_7` | 1.4 Cung cấp ngữ cảnh ngôn ngữ | 3.0 Xử lý nghe và tự phát | Mã ngôn ngữ hiện tại | Mã ngôn ngữ hiện tại |
| `flow_8` | 1.4 Cung cấp ngữ cảnh ngôn ngữ | 4.0 Quản lý audio ngoại tuyến | Mã ngôn ngữ hiện tại | Mã ngôn ngữ hiện tại |
| `flow_9` | 1.1 Khôi phục lựa chọn | 1.2 Kiểm tra ngôn ngữ | Mã ngôn ngữ khôi phục | Mã ngôn ngữ khôi phục |
| `flow_10` | 1.2 Kiểm tra ngôn ngữ | 1.3 Lưu lựa chọn | Mã ngôn ngữ hợp lệ | Mã ngôn ngữ hợp lệ |
| `flow_11` | 1.2 Kiểm tra ngôn ngữ | 1.4 Cung cấp ngữ cảnh ngôn ngữ | Ngôn ngữ hợp lệ | Ngôn ngữ hợp lệ |

## 04_MUC_1_2_0_POI_BAN_DO_LO_TRINH.xml

**DFD MỨC 1 — PHÂN RÃ 2.0** — 4 tiến trình, 24 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E1. Khách tham quan | 2.1 Tiếp nhận nhu cầu tra cứu | Yêu cầu xem POI, bản đồ, lộ trình, hướng dẫn | Yêu cầu xem POI, bản đồ, lộ trình, hướng dẫn |
| `flow_1` | 1.0 Quản lý ngôn ngữ | 2.1 Tiếp nhận nhu cầu tra cứu | Mã ngôn ngữ hiện tại | Mã ngôn ngữ hiện tại |
| `flow_2` | 4.0 Quản lý audio ngoại tuyến | 2.1 Tiếp nhận nhu cầu tra cứu | Yêu cầu metadata POI theo ngôn ngữ | Yêu cầu metadata POI theo ngôn ngữ |
| `flow_3` | D1.1. Dữ liệu dùng chung | 2.2 Tải và khôi phục POI | POI đang hiển thị và vị trí; Nội dung đúng ngôn ngữ | POI đang hiển thị và vị trí; Nội dung đúng ngôn ngữ |
| `flow_4` | D1.2. Dữ liệu trên thiết bị | 2.2 Tải và khôi phục POI | Snapshot POI theo ngôn ngữ | Snapshot POI theo ngôn ngữ |
| `flow_5` | 2.2 Tải và khôi phục POI | D1.2. Dữ liệu trên thiết bị | Snapshot POI cập nhật | Snapshot POI cập nhật |
| `flow_6` | 2.2 Tải và khôi phục POI | 4.0 Quản lý audio ngoại tuyến | Metadata POI theo ngôn ngữ | Metadata POI theo ngôn ngữ |
| `flow_7` | 2.2 Tải và khôi phục POI | E1. Khách tham quan | Lỗi không tải được POI | Lỗi không tải được POI |
| `flow_8` | D1.1. Dữ liệu dùng chung | 2.3 Cung cấp thông tin và bản đồ | Ảnh loài vật | Ảnh loài vật |
| `flow_9` | D1.2. Dữ liệu trên thiết bị | 2.3 Cung cấp thông tin và bản đồ | Ảnh đã cache | Ảnh đã cache |
| `flow_10` | 2.3 Cung cấp thông tin và bản đồ | D1.2. Dữ liệu trên thiết bị | Ảnh đã truy cập | Ảnh đã truy cập |
| `flow_11` | 2.3 Cung cấp thông tin và bản đồ | E4. Dịch vụ bản đồ | Thông số ô bản đồ | Thông số ô bản đồ |
| `flow_12` | E4. Dịch vụ bản đồ | 2.3 Cung cấp thông tin và bản đồ | Ảnh nền bản đồ | Ảnh nền bản đồ |
| `flow_13` | 2.3 Cung cấp thông tin và bản đồ | E5. Dịch vụ GPS | Yêu cầu lấy vị trí | Yêu cầu lấy vị trí |
| `flow_14` | E5. Dịch vụ GPS | 2.3 Cung cấp thông tin và bản đồ | Tọa độ, độ chính xác, trạng thái GPS | Tọa độ, độ chính xác, trạng thái GPS |
| `flow_15` | 2.3 Cung cấp thông tin và bản đồ | E1. Khách tham quan | Thông tin điểm, marker và điểm gần nhất | Thông tin điểm, marker và điểm gần nhất |
| `flow_16` | 2.3 Cung cấp thông tin và bản đồ | 3.0 Xử lý nghe và tự phát | POI được chọn và tọa độ hiện tại | POI được chọn và tọa độ hiện tại |
| `flow_17` | 2.3 Cung cấp thông tin và bản đồ | 6.0 Ghi nhận và thống kê | Sự kiện xem POI kèm ngôn ngữ | Sự kiện xem POI kèm ngôn ngữ |
| `flow_18` | 2.4 Cung cấp lộ trình và hướng dẫn | E1. Khách tham quan | Lộ trình gợi ý, liên kết bản đồ và hướng dẫn | Lộ trình gợi ý, liên kết bản đồ và hướng dẫn |
| `flow_19` | 2.1 Tiếp nhận nhu cầu tra cứu | 2.2 Tải và khôi phục POI | Tiêu chí POI và ngôn ngữ | Tiêu chí POI và ngôn ngữ |
| `flow_20` | 2.1 Tiếp nhận nhu cầu tra cứu | 2.3 Cung cấp thông tin và bản đồ | Nhu cầu xem thông tin và bản đồ | Nhu cầu xem thông tin và bản đồ |
| `flow_21` | 2.1 Tiếp nhận nhu cầu tra cứu | 2.4 Cung cấp lộ trình và hướng dẫn | Nhu cầu lộ trình hoặc hướng dẫn | Nhu cầu lộ trình hoặc hướng dẫn |
| `flow_22` | 2.2 Tải và khôi phục POI | 2.3 Cung cấp thông tin và bản đồ | Thông tin POI theo ngôn ngữ | Thông tin POI theo ngôn ngữ |
| `flow_23` | 2.2 Tải và khôi phục POI | 2.4 Cung cấp lộ trình và hướng dẫn | Danh sách POI có tọa độ | Danh sách POI có tọa độ |

## 05_MUC_1_3_0_NGHE_VA_TU_PHAT.xml

**DFD MỨC 1 — PHÂN RÃ 3.0** — 5 tiến trình, 21 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E1. Khách | 3.1 Tiếp nhận yêu cầu | Yêu cầu nghe, quét, tự phát hoặc mô phỏng | Yêu cầu nghe, quét, tự phát hoặc mô phỏng |
| `flow_1` | 2.0 Tiến trình tham chiếu | 3.1 Tiếp nhận yêu cầu | POI và tọa độ | POI và tọa độ |
| `flow_2` | 1.0 Tiến trình tham chiếu | 3.1 Tiếp nhận yêu cầu | Ngôn ngữ | Ngôn ngữ |
| `flow_3` | 3.1 Tiếp nhận yêu cầu | E5. Camera | Yêu cầu camera | Yêu cầu camera |
| `flow_4` | E5. Camera | 3.2 Giải mã QR | Khung hình và trạng thái | Khung hình và trạng thái |
| `flow_5` | 3.2 Giải mã QR | 4.0 Tiến trình tham chiếu | Gói ID hợp lệ | Gói ID hợp lệ |
| `flow_6` | 3.2 Giải mã QR | E1. Khách | Lỗi QR hoặc camera | Lỗi QR hoặc camera |
| `flow_7` | D1.1. Dữ liệu dùng chung | 3.3 Xác định vùng kích hoạt | POI và vùng tròn | POI và vùng tròn |
| `flow_8` | 3.3 Xác định vùng kích hoạt | E1. Khách | Kết quả xét vùng | Kết quả xét vùng |
| `flow_9` | 3.3 Xác định vùng kích hoạt | 6.0 Tiến trình tham chiếu | Sự kiện vào hoặc ra vùng | Sự kiện vào hoặc ra vùng |
| `flow_10` | D1.1. Dữ liệu dùng chung | 3.4 Xác định bản thu | Liên kết audio; Asset sẵn sàng; Dữ liệu audio online | Liên kết audio; Asset sẵn sàng; Dữ liệu audio online |
| `flow_11` | D1.2. Dữ liệu trên thiết bị | 3.4 Xác định bản thu | Bản thu đã tải; định danh ẩn danh | Bản thu đã tải; định danh ẩn danh |
| `flow_12` | 3.4 Xác định bản thu | E1. Khách | Lỗi thiếu bản thu | Lỗi thiếu bản thu |
| `flow_13` | 4.0 Tiến trình tham chiếu | 3.5 Phát và ghi nhận kết quả | Bản thu ngoại tuyến được chọn | Bản thu ngoại tuyến được chọn |
| `flow_14` | 3.5 Phát và ghi nhận kết quả | E1. Khách | Âm thanh và kết quả phát | Âm thanh và kết quả phát |
| `flow_15` | 3.5 Phát và ghi nhận kết quả | 6.0 Tiến trình tham chiếu | Sự kiện QR và audio kèm ngôn ngữ | Sự kiện QR và audio kèm ngôn ngữ |
| `flow_16` | 3.1 Tiếp nhận yêu cầu | 3.3 Xác định vùng kích hoạt | Yêu cầu xét vùng và tọa độ | Yêu cầu xét vùng và tọa độ |
| `flow_17` | 3.1 Tiếp nhận yêu cầu | 3.4 Xác định bản thu | POI và ngôn ngữ cần nghe | POI và ngôn ngữ cần nghe |
| `flow_18` | 3.2 Giải mã QR | 3.4 Xác định bản thu | POI ID hợp lệ | POI ID hợp lệ |
| `flow_19` | 3.3 Xác định vùng kích hoạt | 3.4 Xác định bản thu | POI và ngôn ngữ cần phát | POI và ngôn ngữ cần phát |
| `flow_20` | 3.4 Xác định bản thu | 3.5 Phát và ghi nhận kết quả | Blob hoặc URL và audio ID | Blob hoặc URL và audio ID |

## 06_MUC_1_4_0_AUDIO_NGOAI_TUYEN.xml

**DFD MỨC 1 — PHÂN RÃ 4.0** — 4 tiến trình, 21 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E1. Khách | 4.1 Xác định gói | Yêu cầu xem hoặc tải gói | Yêu cầu xem hoặc tải gói |
| `flow_1` | 1.0 Tiến trình tham chiếu | 4.1 Xác định gói | Ngôn ngữ | Ngôn ngữ |
| `flow_2` | 3.2 Tiến trình tham chiếu | 4.1 Xác định gói | Gói ID từ QR | Gói ID từ QR |
| `flow_3` | D1.1. Dữ liệu dùng chung | 4.1 Xác định gói | Danh sách gói | Danh sách gói |
| `flow_4` | 4.1 Xác định gói | E1. Khách | Danh sách và QR gói | Danh sách và QR gói |
| `flow_5` | D1.1. Dữ liệu dùng chung | 4.2 Đọc manifest | Manifest, checksum và size | Manifest, checksum và size |
| `flow_6` | 4.2 Đọc manifest | 2.0 Tiến trình tham chiếu | Yêu cầu metadata POI | Yêu cầu metadata POI |
| `flow_7` | 2.0 Tiến trình tham chiếu | 4.2 Đọc manifest | Metadata POI theo ngôn ngữ | Metadata POI theo ngôn ngữ |
| `flow_8` | 4.2 Đọc manifest | E1. Khách | Lỗi gói | Lỗi gói |
| `flow_9` | D1.1. Dữ liệu dùng chung | 4.3 Tải, kiểm tra, lưu | Bytes audio | Bytes audio |
| `flow_10` | D1.2. Dữ liệu trên thiết bị | 4.3 Tải, kiểm tra, lưu | Dữ liệu trước tải | Dữ liệu trước tải |
| `flow_11` | E1. Khách | 4.3 Tải, kiểm tra, lưu | Yêu cầu hủy tải | Yêu cầu hủy tải |
| `flow_12` | 4.3 Tải, kiểm tra, lưu | D1.2. Dữ liệu trên thiết bị | Blob, gói hoặc dữ liệu được khôi phục | Blob, gói hoặc dữ liệu được khôi phục |
| `flow_13` | 4.3 Tải, kiểm tra, lưu | E1. Khách | Tiến độ và kết quả tải | Tiến độ và kết quả tải |
| `flow_14` | E1. Khách | 4.4 Tra cứu và xóa | Yêu cầu xem, xóa hoặc chọn bản thu | Yêu cầu xem, xóa hoặc chọn bản thu |
| `flow_15` | D1.2. Dữ liệu trên thiết bị | 4.4 Tra cứu và xóa | Gói và bản thu đã lưu | Gói và bản thu đã lưu |
| `flow_16` | 4.4 Tra cứu và xóa | D1.2. Dữ liệu trên thiết bị | Dữ liệu sau xóa | Dữ liệu sau xóa |
| `flow_17` | 4.4 Tra cứu và xóa | E1. Khách | Danh sách và kết quả xóa | Danh sách và kết quả xóa |
| `flow_18` | 4.4 Tra cứu và xóa | 3.5 Tiến trình tham chiếu | Bản thu ngoại tuyến được chọn | Bản thu ngoại tuyến được chọn |
| `flow_19` | 4.1 Xác định gói | 4.2 Đọc manifest | Gói ID được chọn | Gói ID được chọn |
| `flow_20` | 4.2 Đọc manifest | 4.3 Tải, kiểm tra, lưu | Danh sách asset và tiêu chí kiểm tra | Danh sách asset và tiêu chí kiểm tra |

## 07_MUC_1_5_0_QUAN_TRI_NOI_DUNG.xml

**DFD MỨC 1 — PHÂN RÃ 5.0** — 7 tiến trình, 40 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E2. Admin | 5.1 Xác thực và quyền | Đăng nhập, phiên hoặc đổi mật khẩu | Đăng nhập, phiên hoặc đổi mật khẩu |
| `flow_1` | D1.1. Dữ liệu dùng chung | 5.1 Xác thực và quyền | Tài khoản và quyền; Phiên và bộ đếm | Tài khoản và quyền; Phiên và bộ đếm |
| `flow_2` | 5.1 Xác thực và quyền | D1.1. Dữ liệu dùng chung | Hash mật khẩu mới; Phiên và bộ đếm cập nhật | Hash mật khẩu mới; Phiên và bộ đếm cập nhật |
| `flow_3` | 5.1 Xác thực và quyền | E2. Admin | Kết quả xác thực | Kết quả xác thực |
| `flow_4` | E2. Admin | 5.2 Quản lý POI và geofence | Dữ liệu POI và vùng | Dữ liệu POI và vùng |
| `flow_5` | D1.1. Dữ liệu dùng chung | 5.2 Quản lý POI và geofence | Dữ liệu hiện có | Dữ liệu hiện có |
| `flow_6` | 5.2 Quản lý POI và geofence | D1.1. Dữ liệu dùng chung | POI và vùng cập nhật | POI và vùng cập nhật |
| `flow_7` | 5.2 Quản lý POI và geofence | E2. Admin | Kết quả lưu | Kết quả lưu |
| `flow_8` | E2. Admin | 5.3 Kiểm tra và lưu ảnh | Ảnh hoặc URL ảnh | Ảnh hoặc URL ảnh |
| `flow_9` | D1.1. Dữ liệu dùng chung | 5.3 Kiểm tra và lưu ảnh | POI cần gắn ảnh; Ảnh hiện có | POI cần gắn ảnh; Ảnh hiện có |
| `flow_10` | 5.3 Kiểm tra và lưu ảnh | D1.1. Dữ liệu dùng chung | Liên kết ảnh; Binary ảnh upload | Liên kết ảnh; Binary ảnh upload |
| `flow_11` | 5.3 Kiểm tra và lưu ảnh | E2. Admin | Ảnh xem trước và kết quả | Ảnh xem trước và kết quả |
| `flow_12` | E2. Admin | 5.4 Quản lý nội dung | Nội dung theo ngôn ngữ | Nội dung theo ngôn ngữ |
| `flow_13` | D1.1. Dữ liệu dùng chung | 5.4 Quản lý nội dung | POI hiện hữu; Bản hiện tại | POI hiện hữu; Bản hiện tại |
| `flow_14` | 5.4 Quản lý nội dung | D1.1. Dữ liệu dùng chung | Nội dung; vô hiệu audio khi lời đổi; đánh dấu bản phụ thuộc cần rà soát | Nội dung; vô hiệu audio khi lời đổi; đánh dấu bản phụ thuộc cần rà soát |
| `flow_15` | 5.4 Quản lý nội dung | E2. Admin | Kết quả lưu | Kết quả lưu |
| `flow_16` | E2. Admin | 5.5 Tạo và theo dõi TTS | Yêu cầu tạo, giọng, truy vấn trạng thái | Yêu cầu tạo, giọng, truy vấn trạng thái |
| `flow_17` | D1.1. Dữ liệu dùng chung | 5.5 Tạo và theo dõi TTS | Nội dung, dữ liệu audio và trạng thái tác vụ | POI hiện hữu; Văn bản và task hiện tại; Trạng thái tác vụ; Khóa hiện có; MP3 nghe thử; Asset nghe thử hiện tại |
| `flow_18` | 5.5 Tạo và theo dõi TTS | D1.1. Dữ liệu dùng chung | Dữ liệu audio và thông tin liên quan | Tác vụ và kết quả; Khóa có TTL hoặc dữ liệu sau giải phóng; MP3 mới; Metadata asset; Liên kết audio và trạng thái hiện tại |
| `flow_19` | 5.5 Tạo và theo dõi TTS | E3. Edge TTS | Văn bản và giọng | Văn bản và giọng |
| `flow_20` | E3. Edge TTS | 5.5 Tạo và theo dõi TTS | MP3 hoặc lỗi | MP3 hoặc lỗi |
| `flow_21` | 5.5 Tạo và theo dõi TTS | E2. Admin | ID, trạng thái, audio nghe thử hoặc lỗi | ID, trạng thái, audio nghe thử hoặc lỗi |
| `flow_22` | E2. Admin | 5.6 Phát hành gói và QR | Yêu cầu phát hành hoặc xem QR | Yêu cầu phát hành hoặc xem QR |
| `flow_23` | D1.1. Dữ liệu dùng chung | 5.6 Phát hành gói và QR | Thông tin POI, nội dung và tài nguyên liên quan | POI đang hiển thị; Liên kết audio đúng ngôn ngữ; Asset và gói hiện có; Size và checksum tệp |
| `flow_24` | 5.6 Phát hành gói và QR | D1.1. Dữ liệu dùng chung | Snapshot asset và gói mới | Snapshot asset và gói mới |
| `flow_25` | 5.6 Phát hành gói và QR | E2. Admin | QR và kết quả phát hành | QR và kết quả phát hành |
| `flow_26` | E2. Admin | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | Nguồn/đích đã lưu; thao tác dịch; bản chỉnh sửa; xác nhận thay thế/lưu | Nguồn/đích đã lưu; thao tác dịch; bản chỉnh sửa; xác nhận thay thế/lưu |
| `flow_27` | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | E2. Admin | Preview/đối chiếu; tiến độ; kết quả lưu hoặc lỗi/xung đột | Preview/đối chiếu; tiến độ; kết quả lưu hoặc lỗi/xung đột |
| `flow_28` | D1.1. Dữ liệu dùng chung | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | Nguồn, bản dịch và thông tin xác nhận | POI hiện hữu; Lời nguồn đã lưu; bản đích và revision hiện tại; Token, nguồn/revision và bộ đếm chuẩn bị preview |
| `flow_29` | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | D1.1. Dữ liệu dùng chung | Bản dịch đã xác nhận; trạng thái nội dung và audio | Token gắn admin/POI, nguồn và revision đích; TTL 30 phút; Transaction bản dịch đã xác nhận; metadata nguồn/review; vô hiệu audio khi lời đổi |
| `flow_30` | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | E6. Chrome Translator API tại máy | Cặp ngôn ngữ; văn bản nguồn; yêu cầu tạo translator | Cặp ngôn ngữ; văn bản nguồn; yêu cầu tạo translator |
| `flow_31` | E6. Chrome Translator API tại máy | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | Bản dịch; khả năng hỗ trợ; tiến độ mô hình hoặc lỗi | Bản dịch; khả năng hỗ trợ; tiến độ mô hình hoặc lỗi |
| `flow_32` | 5.1 Xác thực và quyền | 5.2 Quản lý POI và geofence | Thông tin quyền | Thông tin quyền |
| `flow_33` | 5.1 Xác thực và quyền | 5.3 Kiểm tra và lưu ảnh | Thông tin quyền | Thông tin quyền |
| `flow_34` | 5.1 Xác thực và quyền | 5.4 Quản lý nội dung | Thông tin quyền | Thông tin quyền |
| `flow_35` | 5.1 Xác thực và quyền | 5.5 Tạo và theo dõi TTS | Thông tin quyền | Thông tin quyền |
| `flow_36` | 5.1 Xác thực và quyền | 5.6 Phát hành gói và QR | Thông tin quyền | Thông tin quyền |
| `flow_37` | 5.2 Quản lý POI và geofence | 5.4 Quản lý nội dung | ID và nội dung đầu tiên | ID và nội dung đầu tiên |
| `flow_38` | 5.4 Quản lý nội dung | 5.5 Tạo và theo dõi TTS | Định danh nội dung đã lưu khi admin chọn tạo audio | Định danh nội dung đã lưu khi admin chọn tạo audio |
| `flow_39` | 5.1 Xác thực và quyền | 5.7 Dịch Chrome, đối chiếu và xác nhận lưu | Thông tin quyền content:write | Thông tin quyền content:write |

## 08_MUC_1_6_0_ANALYTICS.xml

**DFD MỨC 1 — PHÂN RÃ 6.0** — 4 tiến trình, 15 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E1. Khách tham quan | 6.1 Chuẩn bị định danh và sự kiện | Dữ liệu phiên, trang và hoạt động hiện diện | Dữ liệu phiên, trang và hoạt động hiện diện |
| `flow_1` | 2.0 Cung cấp POI và bản đồ | 6.1 Chuẩn bị định danh và sự kiện | Sự kiện xem POI kèm ngôn ngữ | Sự kiện xem POI kèm ngôn ngữ |
| `flow_2` | 3.0 Xử lý nghe và tự phát | 6.1 Chuẩn bị định danh và sự kiện | Sự kiện QR, audio và geofence kèm ngôn ngữ | Sự kiện QR, audio và geofence kèm ngôn ngữ |
| `flow_3` | D1.2. Dữ liệu trên thiết bị | 6.1 Chuẩn bị định danh và sự kiện | Định danh ẩn danh đã lưu | Định danh ẩn danh đã lưu |
| `flow_4` | 6.1 Chuẩn bị định danh và sự kiện | D1.2. Dữ liệu trên thiết bị | Định danh ẩn danh mới | Định danh ẩn danh mới |
| `flow_5` | D1.1. Dữ liệu dùng chung | 6.2 Kiểm tra và ghi hoạt động | Bộ đếm rate limit | Bộ đếm rate limit |
| `flow_6` | 6.2 Kiểm tra và ghi hoạt động | D1.1. Dữ liệu dùng chung | Bộ đếm cập nhật; Thiết bị, phiên, sự kiện, lịch sử nghe và vị trí | Bộ đếm cập nhật; Thiết bị, phiên, sự kiện, lịch sử nghe và vị trí |
| `flow_7` | E2. Quản trị viên | 6.3 Kiểm tra quyền phân tích | Yêu cầu dashboard kèm phiên | Yêu cầu dashboard kèm phiên |
| `flow_8` | D1.1. Dữ liệu dùng chung | 6.3 Kiểm tra quyền phân tích | Phiên quản trị; Tài khoản và quyền phân tích | Phiên quản trị; Tài khoản và quyền phân tích |
| `flow_9` | 6.3 Kiểm tra quyền phân tích | E2. Quản trị viên | Lỗi xác thực hoặc phân quyền | Lỗi xác thực hoặc phân quyền |
| `flow_10` | D1.1. Dữ liệu dùng chung | 6.4 Tổng hợp và cung cấp dashboard | Sự kiện và lịch sử phục vụ tổng hợp; Tên POI cho thống kê | Sự kiện và lịch sử phục vụ tổng hợp; Tên POI cho thống kê |
| `flow_11` | 6.4 Tổng hợp và cung cấp dashboard | E2. Quản trị viên | KPI, biểu đồ và bảng thống kê | KPI, biểu đồ và bảng thống kê |
| `flow_12` | 6.1 Chuẩn bị định danh và sự kiện | 6.2 Kiểm tra và ghi hoạt động | Payload định danh và sự kiện | Payload định danh và sự kiện |
| `flow_13` | 6.2 Kiểm tra và ghi hoạt động | 6.1 Chuẩn bị định danh và sự kiện | Kết quả tiếp nhận hoặc lỗi | Kết quả tiếp nhận hoặc lỗi |
| `flow_14` | 6.3 Kiểm tra quyền phân tích | 6.4 Tổng hợp và cung cấp dashboard | Yêu cầu dashboard hợp lệ | Yêu cầu dashboard hợp lệ |

## 09_MUC_2_5_5_TAO_AUDIO_TTS.xml

**DFD MỨC 2 — PHÂN RÃ 5.5** — 5 tiến trình, 21 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E2. Admin | 5.5.1 Kiểm tra nội dung | POI, ngôn ngữ, giọng và yêu cầu tạo | POI, ngôn ngữ, giọng và yêu cầu tạo |
| `flow_1` | 5.1 Tiến trình tham chiếu | 5.5.1 Kiểm tra nội dung | Thông tin quyền | Thông tin quyền |
| `flow_2` | 5.4 Tiến trình tham chiếu | 5.5.1 Kiểm tra nội dung | Định danh nội dung đã lưu | Định danh nội dung đã lưu |
| `flow_3` | D1.1. Dữ liệu dùng chung | 5.5.1 Kiểm tra nội dung | POI hiện hữu; Title, description và task hiện tại | POI hiện hữu; Title, description và task hiện tại |
| `flow_4` | 5.5.1 Kiểm tra nội dung | E2. Admin | Lỗi đầu vào | Lỗi đầu vào |
| `flow_5` | D1.1. Dữ liệu dùng chung | 5.5.2 Đăng ký tác vụ | Khóa hiện có | Khóa hiện có |
| `flow_6` | 5.5.2 Đăng ký tác vụ | D1.1. Dữ liệu dùng chung | Khóa mới có TTL; Task Pending; Task ID và trạng thái Pending | Khóa mới có TTL; Task Pending; Task ID và trạng thái Pending |
| `flow_7` | 5.5.2 Đăng ký tác vụ | E2. Admin | ID và trạng thái ban đầu hoặc lỗi trùng | ID và trạng thái ban đầu hoặc lỗi trùng |
| `flow_8` | 5.5.3 Tổng hợp giọng | D1.1. Dữ liệu dùng chung | Trạng thái Processing; Trạng thái Processing của bản hiện tại | Trạng thái Processing; Trạng thái Processing của bản hiện tại |
| `flow_9` | 5.5.3 Tổng hợp giọng | E3. Edge TTS | Văn bản và giọng | Văn bản và giọng |
| `flow_10` | E3. Edge TTS | 5.5.3 Tổng hợp giọng | MP3 hoặc lỗi | MP3 hoặc lỗi |
| `flow_11` | 5.5.4 Kiểm tra và lưu bản thu | D1.1. Dữ liệu dùng chung | MP3 và checksum; Metadata asset | MP3 và checksum; Metadata asset |
| `flow_12` | D1.1. Dữ liệu dùng chung | 5.5.5 Cập nhật và cung cấp kết quả | Nội dung, dữ liệu audio và trạng thái tác vụ | Nội dung và task hiện tại để đối chiếu; Tác vụ và thời điểm cập nhật; Metadata asset nghe thử; MP3 nghe thử |
| `flow_13` | E2. Admin | 5.5.5 Cập nhật và cung cấp kết quả | Yêu cầu trạng thái hoặc nghe thử | Yêu cầu trạng thái hoặc nghe thử |
| `flow_14` | 5.5.5 Cập nhật và cung cấp kết quả | D1.1. Dữ liệu dùng chung | Dữ liệu audio và thông tin liên quan | Liên kết audio và trạng thái phù hợp; Completed hoặc Failed và kết quả; Dữ liệu sau giải phóng lease |
| `flow_15` | 5.5.5 Cập nhật và cung cấp kết quả | E2. Admin | Trạng thái, audio nghe thử hoặc lỗi | Trạng thái, audio nghe thử hoặc lỗi |
| `flow_16` | 5.5.1 Kiểm tra nội dung | 5.5.2 Đăng ký tác vụ | Bản nguồn và giọng hợp lệ | Bản nguồn và giọng hợp lệ |
| `flow_17` | 5.5.2 Đăng ký tác vụ | 5.5.3 Tổng hợp giọng | Task và nội dung nguồn | Task và nội dung nguồn |
| `flow_18` | 5.5.3 Tổng hợp giọng | 5.5.4 Kiểm tra và lưu bản thu | Bytes và thông tin audio | Bytes và thông tin audio |
| `flow_19` | 5.5.4 Kiểm tra và lưu bản thu | 5.5.5 Cập nhật và cung cấp kết quả | Nội dung, dữ liệu audio và trạng thái tác vụ | Object key, checksum, size, duration và task ID; Thông tin lỗi lưu tệp hoặc metadata |
| `flow_20` | 5.5.3 Tổng hợp giọng | 5.5.5 Cập nhật và cung cấp kết quả | Thông tin lỗi tổng hợp | Thông tin lỗi tổng hợp |

## 10_MUC_2_5_7_DICH_CHROME.xml

**DFD MỨC 2 — PHÂN RÃ 5.7: DỊCH BẰNG CHROME** — 4 tiến trình, 20 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | E2. Quản trị viên | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | POI, ngôn ngữ nguồn/đích, title/description đã lưu; yêu cầu chuẩn bị | POI, ngôn ngữ nguồn/đích, title/description đã lưu; yêu cầu chuẩn bị |
| `flow_1` | 5.1 Xác thực và kiểm tra quyền | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | Thông tin quyền content:write | Thông tin quyền content:write |
| `flow_2` | D1.1. Dữ liệu dùng chung | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | Dữ liệu xác thực, phiên và thông tin xử lý | POI hiện hữu; Lời nguồn đã lưu; bản đích và revision; Bộ đếm chuẩn bị preview |
| `flow_3` | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | D1.1. Dữ liệu dùng chung | Token gắn admin/POI; nguồn/revision đích; TTL 30 phút; bộ đếm 3 giây | Token gắn admin/POI; nguồn/revision đích; TTL 30 phút; bộ đếm 3 giây |
| `flow_4` | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | E2. Quản trị viên | Preview sẵn sàng và nội dung đối chiếu hoặc lỗi đầu vào | Preview sẵn sàng và nội dung đối chiếu hoặc lỗi đầu vào |
| `flow_5` | E2. Quản trị viên | 5.7.2 Kiểm tra native API, tải mô hình và dịch | Thao tác bấm dịch hoặc thử lại/hủy | Thao tác bấm dịch hoặc thử lại/hủy |
| `flow_6` | 5.7.2 Kiểm tra native API, tải mô hình và dịch | E6. Chrome Translator API tại máy | Cặp ngôn ngữ; văn bản nguồn; yêu cầu tạo translator | Cặp ngôn ngữ; văn bản nguồn; yêu cầu tạo translator |
| `flow_7` | E6. Chrome Translator API tại máy | 5.7.2 Kiểm tra native API, tải mô hình và dịch | Bản dịch; khả năng hỗ trợ; tiến độ mô hình hoặc lỗi | Bản dịch; khả năng hỗ trợ; tiến độ mô hình hoặc lỗi |
| `flow_8` | 5.7.2 Kiểm tra native API, tải mô hình và dịch | E2. Quản trị viên | Tiến độ tải/dịch; lỗi từng ngôn ngữ hoặc trạng thái hủy | Tiến độ tải/dịch; lỗi từng ngôn ngữ hoặc trạng thái hủy |
| `flow_9` | E2. Quản trị viên | 5.7.3 Đối chiếu, chỉnh sửa và chọn bản lưu | Nội dung sửa; lựa chọn bản dịch; đồng ý thay thế | Nội dung sửa; lựa chọn bản dịch; đồng ý thay thế |
| `flow_10` | 5.7.3 Đối chiếu, chỉnh sửa và chọn bản lưu | E2. Quản trị viên | Các bản xem trước đã chỉnh; bản cũ để đối chiếu | Các bản xem trước đã chỉnh; bản cũ để đối chiếu |
| `flow_11` | E2. Quản trị viên | 5.7.4 Kiểm tra xung đột và lưu transaction | Yêu cầu xác nhận lưu | Yêu cầu xác nhận lưu |
| `flow_12` | 5.1 Xác thực và kiểm tra quyền | 5.7.4 Kiểm tra xung đột và lưu transaction | Thông tin quyền content:write | Thông tin quyền content:write |
| `flow_13` | D1.1. Dữ liệu dùng chung | 5.7.4 Kiểm tra xung đột và lưu transaction | Nguồn, bản dịch và thông tin xác nhận | Token còn hạn, admin/POI, nguồn và revision đích chuẩn bị; POI hiện hữu; Nguồn, bản đích, revision và audio hiện tại |
| `flow_14` | 5.7.4 Kiểm tra xung đột và lưu transaction | D1.1. Dữ liệu dùng chung | Bản dịch đã xác nhận; trạng thái nội dung và audio | Transaction bản dịch; guard nguồn; provenance/review; vô hiệu audio khi lời đổi |
| `flow_15` | 5.7.4 Kiểm tra xung đột và lưu transaction | E2. Quản trị viên | Ngôn ngữ đã lưu; nhắc tạo audio hoặc lỗi/xung đột 409 | Ngôn ngữ đã lưu; nhắc tạo audio hoặc lỗi/xung đột 409 |
| `flow_16` | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | 5.7.2 Kiểm tra native API, tải mô hình và dịch | Nguồn/đích và token chuẩn bị | Nguồn/đích và token chuẩn bị |
| `flow_17` | 5.7.2 Kiểm tra native API, tải mô hình và dịch | 5.7.3 Đối chiếu, chỉnh sửa và chọn bản lưu | Bản dịch mới trong bộ nhớ React; nguồn và token | Bản dịch mới trong bộ nhớ React; nguồn và token |
| `flow_18` | 5.7.1 Kiểm tra nguồn và chuẩn bị revision | 5.7.3 Đối chiếu, chỉnh sửa và chọn bản lưu | Nội dung đích hiện có để đối chiếu | Nội dung đích hiện có để đối chiếu |
| `flow_19` | 5.7.3 Đối chiếu, chỉnh sửa và chọn bản lưu | 5.7.4 Kiểm tra xung đột và lưu transaction | Token; các bản đã chọn/chỉnh; cờ replace_existing | Token; các bản đã chọn/chỉnh; cờ replace_existing |

## 11_MUC_2_3_3_VUNG_KICH_HOAT.xml

**DFD MỨC 2 — PHÂN RÃ 3.3: XÁC ĐỊNH VÙNG KÍCH HOẠT** — 3 tiến trình, 8 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | 3.1 Tiếp nhận yêu cầu | 3.3.1 Tiếp nhận ngữ cảnh xét vùng | Yêu cầu xét vùng và tọa độ | Yêu cầu xét vùng và tọa độ |
| `flow_1` | 3.3.1 Tiếp nhận ngữ cảnh xét vùng | 3.3.2 Tính khoảng cách và chọn vùng | Tọa độ, ngôn ngữ và trạng thái bật hoặc mô phỏng | Tọa độ, ngôn ngữ và trạng thái bật hoặc mô phỏng |
| `flow_2` | D1.1. Dữ liệu dùng chung | 3.3.2 Tính khoảng cách và chọn vùng | POI và vùng tròn | POI và vùng tròn |
| `flow_3` | 3.3.2 Tính khoảng cách và chọn vùng | 3.3.3 Đối chiếu trạng thái và đề nghị phát | Vùng gần nhất chứa vị trí hoặc kết quả ngoài vùng | Vùng gần nhất chứa vị trí hoặc kết quả ngoài vùng |
| `flow_4` | 3.3.1 Tiếp nhận ngữ cảnh xét vùng | 3.3.3 Đối chiếu trạng thái và đề nghị phát | Ngữ cảnh ngôn ngữ, bật hoặc mô phỏng | Ngữ cảnh ngôn ngữ, bật hoặc mô phỏng |
| `flow_5` | 3.3.3 Đối chiếu trạng thái và đề nghị phát | 3.4 Xác định bản thu | POI và ngôn ngữ cần phát | POI và ngôn ngữ cần phát |
| `flow_6` | 3.3.3 Đối chiếu trạng thái và đề nghị phát | E1. Khách | Kết quả xét vùng | Kết quả xét vùng |
| `flow_7` | 3.3.3 Đối chiếu trạng thái và đề nghị phát | 6.0 Ghi nhận và thống kê | Sự kiện vào hoặc ra vùng | Sự kiện vào hoặc ra vùng |

## 12_MUC_2_4_3_TAI_KIEM_TRA_LUU.xml

**DFD MỨC 2 — PHÂN RÃ 4.3: TẢI, KIỂM TRA VÀ LƯU GÓI** — 4 tiến trình, 17 dòng dữ liệu.

| ID XML | Nguồn | Đích | Nhãn hiển thị / mã luồng | Dữ liệu đầy đủ |
|---|---|---|---|---|
| `flow_0` | 4.2 Đọc manifest | 4.3.1 Kiểm tra khả năng lưu trữ | Danh sách asset và tiêu chí kiểm tra | Danh sách asset và tiêu chí kiểm tra |
| `flow_1` | 4.3.1 Kiểm tra khả năng lưu trữ | 4.3.2 Tải và kiểm tra bản thu | Danh sách bản thu và dung lượng dự kiến | Danh sách bản thu và dung lượng dự kiến |
| `flow_2` | D1.2. Dữ liệu trên thiết bị | 4.3.1 Kiểm tra khả năng lưu trữ | Dữ liệu trước tải | Dữ liệu trước tải |
| `flow_3` | D1.2. Dữ liệu trên thiết bị | 4.3.3 Lưu bản thu và hoàn tất gói | Dữ liệu trước tải | Dữ liệu trước tải |
| `flow_4` | 4.3.1 Kiểm tra khả năng lưu trữ | 4.3.3 Lưu bản thu và hoàn tất gói | Bản ghi gói và bản thu cũ được giữ để khôi phục | Bản ghi gói và bản thu cũ được giữ để khôi phục |
| `flow_5` | 4.3.1 Kiểm tra khả năng lưu trữ | 4.3.4 Khôi phục dữ liệu khi lỗi hoặc hủy | Lỗi chuẩn bị tải | Lỗi chuẩn bị tải |
| `flow_6` | D1.1. Dữ liệu dùng chung | 4.3.2 Tải và kiểm tra bản thu | Bytes audio | Bytes audio |
| `flow_7` | 4.3.2 Tải và kiểm tra bản thu | 4.3.3 Lưu bản thu và hoàn tất gói | Blob hợp lệ; định danh và metadata bản thu | Blob hợp lệ; định danh và metadata bản thu |
| `flow_8` | 4.3.2 Tải và kiểm tra bản thu | 4.3.4 Khôi phục dữ liệu khi lỗi hoặc hủy | Lỗi mạng, tệp rỗng, sai kích thước hoặc checksum | Lỗi mạng, tệp rỗng, sai kích thước hoặc checksum |
| `flow_9` | 4.3.3 Lưu bản thu và hoàn tất gói | 4.3.2 Tải và kiểm tra bản thu | Danh sách bản thu còn lại | Danh sách bản thu còn lại |
| `flow_10` | 4.3.3 Lưu bản thu và hoàn tất gói | D1.2. Dữ liệu trên thiết bị | Blob, gói hoặc dữ liệu được khôi phục | Blob, gói hoặc dữ liệu được khôi phục |
| `flow_11` | 4.3.3 Lưu bản thu và hoàn tất gói | 4.3.4 Khôi phục dữ liệu khi lỗi hoặc hủy | Lỗi lưu; bản ghi cũ và các bản thu đã ghi | Lỗi lưu; bản ghi cũ và các bản thu đã ghi |
| `flow_12` | E1. Khách | 4.3.4 Khôi phục dữ liệu khi lỗi hoặc hủy | Yêu cầu hủy tải | Yêu cầu hủy tải |
| `flow_13` | 4.3.4 Khôi phục dữ liệu khi lỗi hoặc hủy | D1.2. Dữ liệu trên thiết bị | Blob, gói hoặc dữ liệu được khôi phục | Blob, gói hoặc dữ liệu được khôi phục |
| `flow_14` | 4.3.1 Kiểm tra khả năng lưu trữ | E1. Khách | Tiến độ và kết quả tải | Tiến độ và kết quả tải |
| `flow_15` | 4.3.3 Lưu bản thu và hoàn tất gói | E1. Khách | Tiến độ và kết quả tải | Tiến độ và kết quả tải |
| `flow_16` | 4.3.4 Khôi phục dữ liệu khi lỗi hoặc hủy | E1. Khách | Tiến độ và kết quả tải | Tiến độ và kết quả tải |
