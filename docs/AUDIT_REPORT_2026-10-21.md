# Báo cáo audit hệ thống và dọn tài liệu

Thực hiện ngày 21/10/2026 trên database dev `saigon_zoo_tcv_dataset_dev`. Phạm vi gồm source, tài liệu Markdown/sơ đồ, dữ liệu, API, file ảnh/audio, UI Chromium và các luồng online/offline có thể tự động kiểm chứng trên máy phát triển.

## Kết quả kiểm thử

| Kiểm tra | Kết quả |
|---|---|
| Python unit/API và hồi quy | 78 test + 12 subtest qua |
| JavaScript unit test | 8/8 qua |
| Vite production build | Thành công; còn cảnh báo kích thước chunk MapLibre/QR |
| T06 service worker/IndexedDB/cache foundation | Qua; test dùng `dist/sw.js` do Vite sinh ra |
| Audit runtime chỉ đọc | 326 kiểm tra qua: 11 POI, 66 audio, 6 gói; các tham chiếu, API, file ảnh, SHA-256/size audio và manifest |
| Chromium 390/768/1440 px | Các route chính mở được, không tràn ngang, không có JavaScript page error trong ca chạy |
| Admin | Login bằng tài khoản thử, tìm kiếm, mở/đóng dialog, dashboard; tạo bản dịch/sửa/ẩn POI thử qua API |
| Map | Marker có vùng bấm, bật mô phỏng và bắt đầu audio |
| Offline | Tải 6 gói/66 bản, ngắt mạng, chuyển 6 ngôn ngữ, phát bản thu, mở map với POI và audio đã lưu |

Lệnh tái chạy được ghi trong `docs/DEVELOPMENT.md`. Ảnh và JSON browser results nằm trong `.demo-run/audit/` và không đưa lên Git. `scripts/audit_runtime.py` chỉ đọc. `tests/e2e_audit.py` có tạo/xóa tài khoản và POI thử, chặn các analytics event của browser test để không tăng chỉ số sử dụng thật.

Không chạy runtime audit cùng lúc bài E2E tạo POI tạm: trong thời gian đó database có thể tạm có 12 POI. Chốt số liệu sau khi fixture được dọn.

## Lỗi đã sửa

1. **Test cũ không theo auth và contract mới:** thêm override quyền chỉ trong fixture, giữ test 401/403 riêng; đổi kỳ vọng response sang `id`, metadata POI và kiểm tra gói manifest thay ZIP.
2. **Cache POI ghi đè giữa ngôn ngữ:** lưu snapshot riêng theo ngôn ngữ trong IndexedDB. Tải gói cũng chuẩn bị metadata ngôn ngữ đó.
3. **Audio tải về chưa được client kiểm toàn vẹn:** đối chiếu byte size và SHA-256 trước khi lưu hoàn tất; giữ rollback khi tải thất bại/hủy.
4. **Map/QR còn gọi mạng dù có recording offline:** resolve ưu tiên Blob đã tải cho đúng POI và ngôn ngữ.
5. **Audio bản đồ có thể trả nhầm do request cũ:** chặn kết quả trễ khi chọn điểm/ngôn ngữ khác; pause khi tắt hoặc rời map, giữ audio ID trong sự kiện phát/hoàn tất.
6. **Marker nhìn thấy nhưng phần tử bấm có kích thước 0:** thêm kích thước, role, nhãn và bàn phím.
7. **Sửa text nhưng vẫn phát lời cũ:** invalidation liên kết audio của localization khi title/description đổi; API resolve chỉ lấy asset khớp đường audio hiện hành. Gói đã tải vẫn là snapshot được mô tả rõ.
8. **Sửa tọa độ POI nhưng geofence giữ tâm cũ:** cập nhật tâm circle cùng tọa độ POI.
9. **Visit chart dùng page view nhưng mô tả session:** chuyển biểu đồ sang session start, loại trùng theo phiên trong bucket. Backend session start được upsert; ngôn ngữ lấy theo event.
10. **Metadata dev thiếu và sai kiểu:** bổ sung tên/category/mô tả cho 11 POI, chuyển 10 `analytics_sessions.user_id` hợp lệ về ObjectId và đối chiếu trạng thái audio của 66 localization. Giữ ID POI/asset/package và file MP3.
11. **Script seed có thể phá trạng thái gói:** giữ `package_id` khi tái tạo asset; chỉ vô hiệu audio khi text thay đổi, bổ sung metadata POI và trạng thái TTS.
12. **Attribution/ảnh:** thay ảnh Great Argus bị gán cho Trĩ sao Việt Nam bằng Rheinardia ocellata, sửa URL nguồn ảnh báo gấm, hiển thị credit trong profile/map. Ảnh nguồn Trĩ sao được đối chiếu tại [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Argo_de_Rheinard_(Rheinardia_ocellata),_Zoo_de_Ciudad_Ho_Chi_Minh,_Vietnam,_2013-08-14,_DD_01.JPG); nguồn báo gấm tại [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Neofelis_nebulosa,_Clouded_leopard.jpg).
13. **Logo và điều hướng:** gắn logo thật vào header/footer public; thẻ ảnh hổ chưa có POI không dẫn ngầm sang một điểm loài khác.
14. **Vận hành:** `-NoTunnel` cấu hình cookie phù hợp HTTP; xác định process thuộc workspace trước khi dừng PID; sửa nhận diện frontend preview có đường dẫn đặt trong dấu nháy.

Snapshot trước sửa dữ liệu liên quan nằm ở `.demo-run/audit-data-before.json`. Đây không phải backup đầy đủ kho audio; để bàn giao vẫn phải làm quy trình MongoDB + SeaweedFS trong hướng dẫn.

## File được đưa ra khỏi luồng sử dụng

Xem [CLEANUP_REVIEW.md](CLEANUP_REVIEW.md) và [README của kho lịch sử](archive/pre-audit-2026-10-21/README.md). Ba sơ đồ PNG, compose cũ, hai script bootstrap/chuẩn bị cũ và ảnh sai loài đã được lưu trữ. Tài liệu hiện hành trỏ tới Mermaid as-built thay vì các ảnh thiết kế lỗi thời.

## Giới hạn và khoảng cách yêu cầu còn lại

Đọc [REQUIREMENTS_TRACEABILITY.md](REQUIREMENTS_TRACEABILITY.md) trước khi gọi hệ thống là hoàn tất toàn bộ PRD. Các phần chưa triển khai đầy đủ gồm TTS/dịch fallback runtime, PMTiles và nền bản đồ offline, cooldown geofence theo thời gian, quản lý geofence/tài khoản bằng UI, editorial version/publish workflow, queue analytics offline và một số màn quản trị chưa dịch đủ ngôn ngữ.

Chưa kiểm chứng camera thật/GPS thực địa, autoplay trên Safari iOS/Android thật, điều kiện browser chạy nền hoặc cài đặt/restore trên máy Windows trắng. Bài Chromium dùng viewport điện thoại không thay thế kiểm thử thiết bị thật. Các vị trí và giọng đọc vẫn là mô phỏng đã được chấp thuận.

Đây là kết quả các ca đã chạy, không phải cam kết hệ thống không còn bất kỳ lỗi nào. Chưa commit/push/merge Git hoặc thay đổi deployment production trong đợt audit này.
