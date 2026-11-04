# Quản lý POI, ảnh, giọng đọc và gói ngoại tuyến

Cập nhật 04/11/2026. Dùng cho bản mô phỏng phục vụ kiểm chứng chức năng của đồ án.

## 1. Chuẩn bị và chạy

1. Cài dependencies mới: tại thư mục dự án chạy `.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt`.
2. Mở Docker Desktop; bật MongoDB, Redis, SeaweedFS theo [hướng dẫn bàn giao](../HUONG_DAN_CAI_DAT_VA_BAN_GIAO.md).
3. Nếu backend/frontend đang chạy bản cũ: dùng `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\stop_demo.ps1`, sau đó chạy `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start_demo.ps1`. Launcher build frontend khi khởi động mới. Tunnel mới có thể đổi URL; cache ngoại tuyến gắn với URL cũ không chuyển theo.
4. Vào `/admin`, đăng nhập tài khoản có `poi:write`, `content:write`, `audio:write`. Tạo tài khoản bằng `python -m scripts.create_admin` nếu chưa có; không commit mật khẩu vào Git.

Không phải seed lại hoặc xóa database hiện có. Định danh nội bộ vẫn là BSON ObjectId. Hãy backup MongoDB **và** kho SeaweedFS khi chuyển máy: ảnh upload mới cũng nằm trong kho này.

## 2. Thêm POI mới

1. Chọn ngôn ngữ nội dung trong trang quản trị, bấm **Thêm POI**.
2. Nhập tên hệ thống, tiêu đề hiển thị theo ngôn ngữ, loại điểm, tên khoa học (tùy chọn), lời thuyết minh và tọa độ.
3. Chọn ảnh từ máy hoặc nhập URL HTTPS. Ảnh upload chỉ nhận JPEG, PNG, WebP, tối đa 5 MB và 16 megapixel; ảnh được lưu vào SeaweedFS, có thể xem trước. Nên dùng ảnh có quyền sử dụng; hệ thống không tự xác minh bản quyền/độ chính xác.
4. Giữ POI ẩn trong lúc chuẩn bị. Nhập bán kính geofence (5–500 m), bật vùng khi muốn kiểm tra tự phát. Vùng tròn lấy tâm từ tọa độ POI.
5. Bấm **Lưu** để lưu dữ liệu hoặc **Lưu và tạo audio** để tạo giọng từ nội dung vừa nhập. Sau lần lưu đầu, form giữ ID POI; nếu upload hoặc geofence lỗi, sửa lỗi và lưu lại ngay trong form để tiếp tục POI đó.
6. Chờ Completed, nghe thử bằng thanh audio. Bật trạng thái hiển thị và lưu khi nội dung sẵn sàng. POI có bản ngôn ngữ tương ứng sẽ xuất hiện trong danh sách loài trang chủ và trên bản đồ; không cần sửa mã nguồn.

Việc lưu POI, upload ảnh và lưu geofence là các bước API riêng. Nếu có lỗi một phần, thông báo không có nghĩa mọi bước trước đó đã rollback. Đóng form rồi mở danh sách để tìm POI đã tạo trước khi bấm thêm mới lần nữa.

## 3. Sửa ảnh, thêm bản dịch và tạo lại audio

- **Sửa POI**: đổi ảnh/tọa độ/thông tin chung/trạng thái và bán kính geofence. Sửa mô tả hệ thống tại đây không tự thay lời thuyết minh của từng ngôn ngữ.
- **Sửa nội dung**: chọn ngôn ngữ, nhập tiêu đề và lời thuyết minh, chọn giọng rồi **Lưu và tạo audio**. Có thể chỉ lưu nháp trước. Hệ thống hỗ trợ Việt, Anh, Pháp, Trung giản thể, Nhật, Hàn; mỗi ngôn ngữ có hai lựa chọn giọng.
- Admin phải cung cấp nội dung cho từng ngôn ngữ; chức năng này **không tự dịch**. Chưa có bản dịch thì POI không xuất hiện ở ngôn ngữ đó.
- Lưu nguyên lời không làm mất audio đang có. Thay tiêu đề/lời sẽ bỏ liên kết audio hiện tại để tránh phát sai nội dung; cần tạo lại audio. Nội dung đã lưu của POI đang hiển thị có thể được khách đọc ngay, không có kho nháp riêng.
- Mỗi POI/ngôn ngữ chỉ có một lượt tạo đang chạy. Có thể đóng form; mở lại để xem trạng thái. Đổi lời lúc đang tạo sẽ khiến kết quả từ lời cũ không được gắn vào bản hiện tại.
- Tạo giọng cần Internet tới Edge TTS. Khi Failed, kiểm tra mạng, tải lại form rồi thử lại. Tác vụ chạy trong backend hiện tại, không có worker bền vững: tắt backend giữa chừng cần chờ khoảng 5 phút, mở lại trạng thái và yêu cầu tạo lại. Không sửa thủ công status trong MongoDB để giả lập thành công.

## 4. Phát hành QR và tải ngoại tuyến

1. Kiểm tra POI đã hiển thị và audio đã nghe thử, đúng ngôn ngữ.
2. Trong phần **Gói audio ngoại tuyến**, bấm nút phát hành. Gói mới chỉ lấy audio sẵn sàng của POI đang hiển thị ở ngôn ngữ đang chọn; POI chưa có audio không được đưa vào.
3. Giao diện hiển thị QR `TCV-PACKAGE:<ObjectId>`. Đây là mã quét **trong app**, không phải URL mở trực tiếp bằng camera hệ thống. QR POI dùng `TCV-POI:<ObjectId>` để nghe một điểm.
4. Trang chủ lấy gói mới nhất của từng ngôn ngữ từ API. Khách mở **Tải audio** rồi quét/nhập mã, hoặc bấm liên kết tải gói trên trang chủ.
5. Chờ tải hoàn tất; mở bản đồ/điểm cần xem một lần khi còn mạng để cache ảnh, rồi tắt mạng và thử nghe trên cùng URL/trình duyệt. Nền bản đồ online không được bảo đảm khi mất mạng.

Gói mới là snapshot danh sách bản thu: tạo lại TTS không làm thay đổi gói cũ hoặc bản đã tải trên điện thoại. Phát hành gói mới để đưa audio mới cho khách; trên máy khách xóa gói cũ trước khi tải bản thay thế nếu muốn bảo đảm nghe bản mới. Snapshot audio không đóng băng tên/mô tả/ảnh POI. Ảnh URL ngoài có thể không sẵn sàng ngoại tuyến.

## 5. Giới hạn và vận hành

- Đây là luồng quản lý dữ liệu mô phỏng; không tự sinh bộ dữ liệu động vật hay tự xác nhận thông tin thực địa.
- Không xóa MP3 cũ trực tiếp trong SeaweedFS: snapshot cũ có thể còn tham chiếu. File ảnh/giọng cũ được giữ lại; chưa có chức năng dọn file không còn tham chiếu.
- Sau khi code cập nhật trên máy khác, cài lại requirements và build frontend; backup cũ tương thích nhưng không chứa ảnh/audio mới phát sinh sau thời điểm backup.
- Camera/GPS trên điện thoại cần HTTPS và quyền của trình duyệt; tự phát phải bật trong bản đồ, còn phụ thuộc chính sách audio/tab nền của thiết bị.
