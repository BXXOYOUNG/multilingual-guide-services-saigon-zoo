# Đối chiếu PRD / Use case / implementation

Audit nền 21/10/2026, cập nhật luồng admin 04/11/2026. Không thay yêu cầu gốc để khiến code có vẻ hoàn tất. Bảng này chỉ ra phần đạt và khoảng cách cần ghi trong báo cáo/đợt triển khai tiếp theo.

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
| UC-09 Nội dung/dịch | Sửa theo ngôn ngữ; lưu và tạo TTS, chọn giọng, trạng thái/retry; lời mới vô hiệu hóa audio cũ; phát hành snapshot audio | Không dịch máy; TTS cần mạng, chạy trong process API, chưa có durable worker; draft không phải kho nháp tách khỏi nội dung visitor |
| UC-10 Analytics | Thu sự kiện, thiết bị 5 phút, visits, page/QR/audio, ngôn ngữ, xếp hạng POI | Không có heatmap/lịch sử tuyến đường; chưa có queue đồng bộ analytics offline hay consent UI; dashboard dùng UTC |

## Những mô tả không được dùng như “đã có”

- Backend đã đóng gói Docker; PMTiles đã tải offline; Redis là TTS queue; external translation adapter đang chạy.
- Khách thiếu audio sẽ luôn được TTS tạo ngay; sửa bản dịch là có audio mới tự động.
- Analytics ghi nhận đầy đủ hoạt động khi mất mạng; mọi khách đã bấm đồng ý tracking.
- Tất cả quan hệ thể hiện trong ảnh ERD cũ đã tồn tại đúng như ảnh.
- Tọa độ/hình minh họa/giọng tổng hợp là dữ liệu được Thảo Cầm Viên xác minh.

## Các bổ sung đã được người dùng yêu cầu sau PRD gốc

Homepage ảnh và chi tiết loài; logo; menu chữ; Tải audio; lộ trình gợi ý; hướng dẫn sử dụng và quyền riêng tư; dashboard quản trị riêng; giao diện responsive. Lộ trình là gợi ý theo danh sách điểm, không phải routing tìm đường tối ưu hoặc dữ liệu lối đi đã xác minh.

## Gate kết thúc

Unit/API/browser test thành công là bằng chứng cho ca đã chạy, không đồng nghĩa hoàn tất mọi mục tiêu trong PRD. Camera/GPS thực địa, Safari iOS và cài máy Windows mới vẫn cần nghiệm thu riêng. Xem `AUDIT_REPORT_2026-10-21.md` để biết kết quả và phạm vi thực tế.
