# Đối chiếu kỹ thuật kho dữ liệu

Cập nhật 10/11/2026. **K1–K9 chỉ là mã tra cứu kỹ thuật, không phải ký hiệu kho trên DFD.** K1–K8 thuộc D1.1; K9 thuộc D1.2; cả hai thuộc D1 ở mức 0.

Đây là các nhóm dữ liệu để đối chiếu triển khai. Một kho logic có thể nhóm nhiều collection cùng mục đích; việc nhóm không thay đổi schema hoặc tạo database mới.

| Mã tra cứu kỹ thuật | Nhóm dữ liệu | Thành phần đang triển khai | Dữ liệu chủ yếu |
|---|---|---|---|
| K1 | Điểm tham quan và vùng kích hoạt | MongoDB `poi`, `geofence_zones` | Tên hệ thống, thông tin loài, tọa độ, GeoJSON, đường dẫn ảnh, trạng thái hiển thị; tâm/bán kính/trạng thái vùng tròn |
| K2 | Nội dung theo ngôn ngữ | MongoDB `poi_localizations` | `poi_id`, `language_code`, tiêu đề, lời thuyết minh, liên kết audio, trạng thái/task hiện tại; metadata nguồn/review của bản dịch |
| K3 | Tác vụ tạo audio | MongoDB `audio_tasks` | POI/ngôn ngữ, giọng, nội dung nguồn, trạng thái, file kết quả, thông báo lỗi, thời điểm |
| K4 | Metadata audio và gói | MongoDB `audio_assets`, `audio_packages` | Object key, checksum, duration, size, ngôn ngữ, POI, thành viên gói, cờ snapshot |
| K5 | Tệp hình ảnh và âm thanh | SeaweedFS qua adapter S3; ảnh seed trong `frontend/public/images` | Binary MP3 và ảnh; MongoDB giữ liên kết/metadata |
| K6 | Tài khoản và vai trò quản trị | MongoDB `admin_users`, `roles` | Tài khoản, password hash, vai trò, quyền, trạng thái |
| K7 | Phiên và dữ liệu tạm phía server | Redis | Phiên admin, bộ đếm rate limit, khóa chống tạo TTS trùng; token/nguồn/revision preview gắn admin/POI, TTL 30 phút |
| K8 | Hoạt động sử dụng | MongoDB `analytics_devices`, `analytics_sessions`, `analytics_events`, `playback_history`, `location_events` | Định danh ẩn danh, sự kiện trang/QR/audio/geofence, thời điểm, ngôn ngữ, lịch sử nghe |
| K9 | Bộ nhớ trên thiết bị | IndexedDB, localStorage, sessionStorage, Cache Storage | Ngôn ngữ; định danh ẩn danh; snapshot POI; gói và Blob audio; shell/ảnh/asset đã cache |

Các ảnh seed và ảnh upload có đường phục vụ khác nhau, cùng được nhóm vào K5 vì đều cung cấp nội dung hình ảnh. Cache của các nội dung đã truy cập nằm trong K9.

MongoDB dùng BSON ObjectId cho khóa và tham chiếu nội bộ; API truyền chuỗi hex 24 ký tự. Visitor ẩn danh có định danh riêng, không dùng tài khoản admin để ghi lịch sử nghe.
