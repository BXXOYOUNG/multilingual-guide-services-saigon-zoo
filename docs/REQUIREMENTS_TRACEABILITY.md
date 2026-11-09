# Đối chiếu PRD / Use case / implementation

Audit nền 21/10/2026, cập nhật luồng admin/dịch 09/11/2026 theo bổ sung được người dùng chấp thuận. Bảng này chỉ ra implementation và khoảng cách; code bổ sung không thay thế kết quả nghiệm thu dịch vụ thật.

| Use case | Hiện có | Giới hạn / phần chưa đạt trọn vẹn PRD |
|---|---|---|
| UC-01 Ngôn ngữ | Chọn/lưu 6 ngôn ngữ, giao diện visitor và nội dung POI | Dashboard phân tích còn tiếng Việt; một số thông báo kỹ thuật fallback còn tiếng Việt |
| UC-02 Bản đồ | MapLibre, marker, GPS, gần nhất, POI cache theo ngôn ngữ | Raster OSM online, chưa có PMTiles offline; tọa độ mô phỏng |
| UC-03 Tự phát | Bật geofence, kiểm tra vòng tròn, phát audio, mô phỏng đến POI, sự kiện phát | Chưa có TTS fallback trực tiếp, chưa có cooldown thời gian đầy đủ; autoplay thật cần kiểm tra thiết bị, tab nền không được đảm bảo |
| UC-04 QR POI | Scanner, kiểm tra payload ObjectId, resolve audio đúng ngôn ngữ; ưu tiên bản tải sẵn khi offline | Audio thiếu báo lỗi; chưa tự tạo TTS/bản dịch; camera thật cần nghiệm thu điện thoại |
| UC-05 Tải gói | Bộ seed 6 gói, 11 bản/gói; admin phát hành thêm snapshot/QR từ audio hiện tại; SHA-256/size, hủy và rollback, lưu IndexedDB | Mỗi QR đại diện một gói/ngôn ngữ; không tự cập nhật gói đã tải khi tạo audio mới |
| UC-06 Nghe offline | Danh sách audio đã tải theo ngôn ngữ, phát lại, xóa gói; map dùng POI/recording đã lưu | Cần mở/tải trước cùng origin; URL tunnel mới không mang theo cache cũ; không hứa có nền bản đồ đầy đủ |
| UC-07 Admin | Cookie HTTP-only, Redis session, role/permission, đổi mật khẩu | Chưa có UI quản lý tài khoản/role; tạo admin bằng script |
| UC-08 POI | Tạo, sửa, ẩn; ảnh upload/URL và nghe thử; search/filter, QR; cấu hình geofence tròn, cập nhật tâm theo POI | Chưa có UI vẽ polygon; tọa độ demo cần admin kiểm tra; thêm POI không tự tạo 6 bản dịch |
| UC-09 Nội dung/dịch | Nhập thủ công hoặc Chrome Translator: lưu nguồn → chuẩn bị revision → admin bấm dịch tại máy → preview/sửa/đối chiếu → chọn/xác nhận lưu; chống ghi đè, nhắc rà soát nguồn; admin yêu cầu TTS và phát hành snapshot | Tự dịch cần Chrome desktop hỗ trợ từng cặp ngôn ngữ, localhost/HTTPS và tải mô hình lần đầu; điện thoại dùng nhập thủ công; không tự tạo audio đồng loạt; TTS chạy trong API; nội dung đã lưu của POI active có thể đọc ngay |
| UC-10 Analytics | Thu sự kiện, thiết bị 5 phút, visits, page/QR/audio, ngôn ngữ, xếp hạng POI | Không có heatmap/lịch sử tuyến đường; chưa có queue đồng bộ analytics offline hay consent UI; dashboard dùng UTC |

## Những mô tả không được dùng như “đã có”

- Backend đã đóng gói Docker; PMTiles đã tải offline; Redis là TTS queue; mọi trình duyệt đều hỗ trợ dịch hoặc mô hình đã sẵn sàng chỉ vì có mã nguồn.
- Khách thiếu audio sẽ luôn được TTS tạo ngay; sửa bản dịch là có audio mới tự động.
- Analytics ghi nhận đầy đủ hoạt động khi mất mạng; mọi khách đã bấm đồng ý tracking.
- Tất cả quan hệ thể hiện trong ảnh ERD cũ đã tồn tại đúng như ảnh.
- Tọa độ/hình minh họa/giọng tổng hợp là dữ liệu được Thảo Cầm Viên xác minh.

## Các bổ sung đã được người dùng yêu cầu sau PRD gốc

Homepage ảnh và chi tiết loài; logo; menu chữ; Tải audio; lộ trình gợi ý; hướng dẫn sử dụng và quyền riêng tư; dashboard quản trị riêng; giao diện responsive. Lộ trình là gợi ý theo danh sách điểm, không phải routing tìm đường tối ưu hoặc dữ liệu lối đi đã xác minh.

Ngày 09/11/2026: UC-09 bổ sung dịch tự động có xem trước và xác nhận lưu theo [ADMIN_AUTO_TRANSLATION.md](ADMIN_AUTO_TRANSLATION.md). TTS tiếp tục dùng lời đã lưu; luồng visitor/QR/offline không tự gọi dịch máy.

## Gate kết thúc

Unit/API/browser test thành công là bằng chứng cho ca đã chạy, không đồng nghĩa hoàn tất mọi mục tiêu trong PRD. Camera/GPS thực địa, Safari iOS và cài máy Windows mới vẫn cần nghiệm thu riêng. Xem `AUDIT_REPORT_2026-10-21.md` để biết kết quả và phạm vi thực tế.
