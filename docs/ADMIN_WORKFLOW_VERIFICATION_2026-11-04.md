# Kết quả kiểm tra luồng admin — 04/11/2026

Nhánh: `feature/admin-poi-content-workflow`. Phạm vi: POI/ảnh/geofence, tạo giọng theo bản ngôn ngữ, nghe thử, gói snapshot và QR. Không merge vào main.

## Đã kiểm tra

- Backend pytest: **95 ca và 12 subtest qua**; frontend: **8 ca qua**; production build thành công (còn cảnh báo bundle MapLibre lớn). Có thêm ca cho CAS khi sửa lời, chống tạo trùng, retry, ảnh không hợp lệ/quá lớn, phân quyền và snapshot.
- Browser hồi quy tại 390, 768, 1440 px: không tràn ngang; đăng nhập, tìm kiếm, form sửa, dashboard, CRUD POI tạm, mô phỏng tự phát và nghe offline ở cả sáu ngôn ngữ đều qua; không có lỗi JavaScript được ghi nhận.
- Runtime audit: **328 mục qua, 0 lỗi**, dữ liệu thật tại thời điểm kiểm tra có 12 POI, 66 asset, 6 gói. POI Cá sấu có bản tiếng Việt nhưng chưa có ảnh/audio; đây là nội dung admin đang chuẩn bị, không phải lỗi tham chiếu. Không xóa/sửa POI này.
- Browser luồng mới: thêm POI tạm ở trạng thái ẩn, upload ảnh thật vào SeaweedFS, lưu geofence 42 m, tạo MP3 tiếng Việt thật và đọc được duration, xem form mobile, bật hiển thị và thấy ở catalog, phát hành gói snapshot/QR mới, thấy QR trên trang chủ, tải gói và mở ảnh/audio khi offline đều qua.
- Lần browser cuối cùng **qua trọn luồng**, gồm sửa lời, tạo lại MP3 thật thành công, xác nhận file mới khác file trước và manifest gói cũ không đổi; không có lỗi JavaScript. Kết quả được lưu tại `.demo-run/admin-workflow-audit/results.json`.

## Giới hạn TTS quan sát được

Tạo giọng cho lời thử ban đầu đã thành công nhiều lần. Tuy nhiên, một số lần ở bước đổi lời và tạo lại, Edge TTS trả `NoAudioReceived`, kể cả sau khi retry; gọi trực tiếp provider cũng tái hiện được. Lần chạy cuối cùng đã tạo lại thành công với lời mới. Kết quả đó không bảo đảm dịch vụ luôn sẵn sàng hoặc mọi nội dung đều thành công. Không thay audio giả hoặc đánh dấu Completed để vượt kiểm thử.

Khi provider lỗi, backend ghi Failed, không gắn audio sai; Redis lease được giải phóng để admin thử lại. Gói đã phát hành vẫn giữ nguyên. Unit test còn kiểm tra có kiểm soát các tình huống lỗi và lời bị thay đổi trong khi đang tạo.

`tests/e2e_admin_workflow.py` giữ kiểm tra Completed bắt buộc ở bước tạo lại: nếu provider tiếp tục trả rỗng, script trả lỗi và ghi kết quả từng phần vào `.demo-run/admin-workflow-audit/results.json`. Không diễn giải lần chạy đó là toàn bộ kiểm thử đã qua. Ảnh chụp và log nằm trong `.demo-run/`, không đưa vào Git.

## Dữ liệu và phạm vi chưa nghiệm thu

Các ca browser dùng admin/POI/gói riêng và dọn các record, object storage do chính ca đó tạo. Analytics được chặn trong context kiểm thử. Dữ liệu trước đó được giữ lại. Chưa nghiệm thu lại camera/GPS thực địa, Safari iOS hay cài trên máy Windows mới; chưa có worker TTS bền vững hoặc tự dịch nội dung.
