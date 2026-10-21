# Chuẩn bị push và gửi bản bàn giao

Ngày 21/10/2026. Nhánh source hiện tại: `feature/dataset-six-language-seed`.

## Phần đưa lên Git

Source frontend/backend, ảnh và font có license, dataset nguồn, test, script vận hành và tài liệu. File lỗi thời đã chuyển sang `docs/archive/pre-audit-2026-10-21/`, vì vậy Git sẽ có cả thay đổi xóa vị trí cũ và thêm vị trí lưu trữ; đây là thay đổi có chủ đích.

Các file đã được đưa vào staging để review. Xem lại trước khi commit:

```powershell
git status
git diff --cached --stat
git diff --cached --check
```

Khi đồng ý nội dung staged:

```powershell
git commit -m "Complete multilingual classroom demo and handoff documentation"
git push -u origin feature/dataset-six-language-seed
```

Sau đó mở Pull Request từ nhánh này vào `main`, review và merge theo quy trình nhóm. Không cần chuyển sang `main` rồi chép đè file thủ công. Máy nhận có thể checkout nhánh này ngay sau khi push, hoặc pull `main` sau khi PR đã merge.

Chưa có commit, push hay merge tự động trong bước chuẩn bị này. Không dùng `git add -f` với file backup/bí mật.

## Phần gửi riêng

Bộ dữ liệu được xuất ngoài repository, gồm `database.archive.gz`, `seaweed-data.tar.gz`, `seaweed-image.tar`, `seaweed.env`, metadata, kết quả thử phục hồi, hướng dẫn nhận và bản source ZIP khớp staging. ZIP source giúp đối chiếu phiên bản trong khi code chưa được push; nếu pull đúng commit sau này thì dùng thư mục Git đã có, không cần tạo dự án thứ hai.

- MongoDB backup chứa tài khoản, password hash và analytics tới thời điểm chụp.
- `seaweed.env` chứa khóa kho audio. Chỉ gửi gói này riêng cho admin được bàn giao, không đưa lên Git hoặc nhóm công khai.
- Redis session không được bàn giao; đăng nhập lại ở máy nhận.
- Thông tin đăng nhập được gửi riêng, không ghi mật khẩu vào source ZIP hoặc hướng dẫn.
- `SHA256SUMS.txt` dùng để kiểm tra file sau khi chuyển; `RESTORE_VERIFICATION.json` là kết quả restore thử vào Docker tạm.

Nếu gói lớn được chia thành nhiều phần `.part001`, `.part002`…, phải tải đủ các phần vào cùng một thư mục và chạy `JOIN_BACKUP.ps1` kèm gói trước khi giải nén. Script ghép chỉ đọc các phần và tạo ZIP hoàn chỉnh; không cài hay thay đổi database.

Hướng dẫn cài/restore chi tiết: [HUONG_DAN_CAI_DAT_VA_BAN_GIAO.md](../HUONG_DAN_CAI_DAT_VA_BAN_GIAO.md).

## Tái tạo backup lần sau

Chọn đường dẫn mới ngoài repository; dừng backend đang thuộc dự án trước khi chạy. MongoDB và SeaweedFS cần đang chạy. Script backup sẽ tạm dừng SeaweedFS để chụp volume rồi bật lại.

```powershell
.\.venv\Scripts\python.exe scripts/prepare_handoff_backup.py 'E:\TCV-handoff-new'
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start_demo.ps1 -NoTunnel
.\.venv\Scripts\python.exe scripts/verify_handoff_backup.py 'E:\TCV-handoff-new'
```

Thay đường dẫn theo máy; không bắt buộc ổ C hoặc E. Bước verify restore dùng container/volume tạm có tên ngẫu nhiên rồi dọn đúng các tài nguyên đó; không phục hồi đè database đang dùng. Các lệnh trên chưa tự đóng ZIP/chia file; giữ cấu trúc backup trong hướng dẫn gốc nếu làm thủ công.
