# Nhận bản bàn giao Thảo Cầm Viên — 21/10/2026

Đây là bản sao đã thử phục hồi: 11 POI, 66 audio, 6 gói ngôn ngữ. Không cần tạo thêm dự án ở ổ C. Bạn có thể dùng thư mục Git đang có ở bất kỳ ổ đĩa nào sau khi cập nhật đúng nhánh/commit.

## 1. Nhận đủ file và giải nén

Nếu nhận một ZIP hoàn chỉnh, giải nén bằng File Explorer/7-Zip. Nếu nhận các phần `.part001`, `.part002`…, tải tất cả vào cùng một thư mục, gồm cả `JOIN_BACKUP.ps1` và `TRANSFER_MANIFEST.json`, rồi mở PowerShell tại đó:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\JOIN_BACKUP.ps1
```

Script kiểm tra từng phần, ghép thành ZIP, kiểm tra SHA-256. Sau đó giải nén ZIP. Không giải nén riêng từng phần `.part...`.

## 2. Chọn source đúng phiên bản

- Nếu source đã được push: cập nhật nhánh `feature/dataset-six-language-seed`, hoặc `main` sau khi PR đã merge. Dùng luôn thư mục Git đang có.
- Nếu chưa có code mới trên Git: `source.zip` trong gói chứa toàn bộ source đã staging ở máy người gửi. Giải nén vào một thư mục riêng để không ghi đè bản Git cũ; không chứa `.git`, `.venv`, `node_modules` hay credential.
- `SOURCE_STATE.txt` ghi nhánh, commit nền và tree snapshot chính xác. Bản source này được chụp trước khi commit/push; không nhầm commit nền với toàn bộ bản bàn giao.

## 3. Cài và phục hồi

Trong source, mở `HUONG_DAN_CAI_DAT_VA_BAN_GIAO.md`, làm **phần 7**:

1. Cài Docker Desktop/WSL 2, Python 3.11 và Node.js 24.
2. Tạo venv, cài requirements, chạy `npm.cmd --prefix frontend ci`.
3. Tạo MongoDB replica set đúng cổng 27018, khởi tạo `rs0`.
4. Restore `database.archive.gz` vào database `saigon_zoo_tcv_dataset_dev`.
5. Load `seaweed-image.tar`, giải nén `seaweed-data.tar.gz` vào volume mới và tạo container với `seaweed.env`.
6. Tạo Redis và chạy launcher của source.

Thay `$handoffDir` trong hướng dẫn bằng đường dẫn thật tới thư mục chứa các file backup sau khi giải nén. Không bắt buộc `C:\TCV-handoff`.

Không restore đè lên database/volume đã có dữ liệu khác. Nếu báo trùng tên container, đọc phần xử lý lỗi trong hướng dẫn trước khi làm tiếp; không dùng lệnh xóa/prune để chữa nhanh.

## 4. Đăng nhập và sử dụng

Database backup giữ nguyên các tài khoản đang có. Nhận thông tin đăng nhập từ người gửi qua kênh riêng; file này không chứa mật khẩu. Có thể tự tạo tài khoản riêng bằng `scripts/create_admin.py` theo phần 7.7 của hướng dẫn.

Sau lần cài đầu, các lần sau chỉ cần mở Docker Desktop, bật ba container rồi chạy `scripts/start_demo.ps1`. Điện thoại dùng URL HTTPS mới do máy bạn tạo; URL cũ của máy người gửi không tự chuyển sang máy bạn.

## Nội dung gói

| File | Nội dung |
|---|---|
| `source.zip` | Source khớp staging, không có credential hay backup |
| `database.archive.gz` | Toàn database, gồm tài khoản/role, POI, bản dịch, audio metadata, package và analytics |
| `seaweed-data.tar.gz` | Volume SeaweedFS chứa MP3 thật |
| `seaweed-image.tar` | Đúng image SeaweedFS của máy người gửi |
| `seaweed.env` | Khóa/bucket S3 dùng với kho phục hồi |
| `RESTORE_VERIFICATION.json` | Kết quả phục hồi thử trên container/volume tạm |
| `backup-metadata.json` | Mốc backup, số bản ghi và phiên bản image |
| `SOURCE_STATE.txt` | Trạng thái source lúc chụp |
| `SHA256SUMS.txt` | SHA-256 của các file trong gói |

MongoDB backup chứa password hash và dữ liệu quản trị; `seaweed.env` có khóa storage. Chỉ gửi cho admin được bàn giao, không đưa gói này lên Git hoặc nhóm công khai.
