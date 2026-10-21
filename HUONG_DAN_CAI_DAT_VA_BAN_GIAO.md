# Hướng dẫn cài đặt, bàn giao và bật/tắt hệ thống Thảo Cầm Viên

Ngày viết: **21/10/2026**. Dành cho **Windows + PowerShell + Docker Desktop (Linux containers)**.

Tài liệu mô tả phiên bản đang có trên máy phát triển, gồm giao diện mới, quản trị, dashboard, POI đa ngôn ngữ, audio và tải ngoại tuyến. Đây là bản mô phỏng phục vụ kiểm chứng đồ án.

**Việc tạo tài liệu này chưa thực hiện backup, chuyển dữ liệu, cài máy mới, commit, push hay merge Git.** Các lệnh bên dưới là hướng dẫn để thực hiện sau. Quy trình chuyển máy chưa được chạy thử trên một máy Windows trắng.

## Đọc phần nào trước?

| Nhu cầu | Phần cần đọc |
|---|---|
| Máy mình đã có mọi thứ, chỉ muốn bật lại | 2 |
| Muốn biết MongoDB nằm ở đâu, mở như thế nào | 3 |
| Muốn bạn đăng nhập admin vào hệ thống mình đang chạy | 4 |
| Muốn bạn có một bản đầy đủ chạy trên máy riêng | 5 → 6 → 7 |
| Muốn chạy riêng backend/frontend/tunnel để biết từng bước | 8 |
| Tắt đúng cách hoặc cập nhật giao diện | 9 |
| Không chạy được, bad gateway, mất audio, lỗi admin | 10 |
| Kiểm tra bản bàn giao có đủ tính năng | 11 |

---

## 1. Hiểu hệ thống trước khi bật

### 1.1. Các thành phần

| Thành phần | Vai trò | Cách chạy hiện tại |
|---|---|---|
| MongoDB | POI, bản dịch, tài khoản admin, thông tin audio, gói offline, analytics | Docker |
| SeaweedFS | Lưu file MP3 thật; MongoDB chỉ giữ thông tin và đường dẫn | Docker |
| Redis | Lưu phiên đăng nhập admin và dữ liệu hỗ trợ | Docker |
| Backend FastAPI | Đọc/ghi dữ liệu, đăng nhập, phục vụ audio | Python trên Windows, cổng `8000` |
| Frontend React/Vite | Giao diện web | Node.js trên Windows, cổng `3000` |
| Cloudflare Tunnel | Cấp URL HTTPS tạm để điện thoại truy cập máy tính | Docker, chuyển tiếp về frontend |
| MongoDB Compass | Công cụ xem database bằng giao diện | Cài thêm nếu muốn; không phải máy chủ MongoDB |

Luồng truy cập:

```text
Điện thoại → URL HTTPS Cloudflare → frontend :3000
                                     ├─ /api và /audio → backend :8000
                                     │                    ├─ MongoDB :27018
                                     │                    ├─ Redis :6379
                                     │                    └─ SeaweedFS :8333
                                     └─ HTML, JS, CSS, ảnh và font
```

**Mở Compass không có nghĩa là đã bật database.** MongoDB chỉ chạy khi container MongoDB đã chạy trong Docker Desktop.

### 1.2. Tên và cổng phải dùng đúng

| Container | Cổng trên máy | Ghi chú |
|---|---|---|
| `saigon-zoo-t10-replset` | `127.0.0.1:27018` | MongoDB 6.0, replica set `rs0` |
| `saigon-zoo-t10-seaweedfs` | `127.0.0.1:8333` | Kho audio |
| `saigon-zoo-redis` | `127.0.0.1:6379` | Phiên đăng nhập |
| `saigon-zoo-demo-tunnel` | Không mở cổng MongoDB | URL HTTPS cho ứng dụng |

Database chính:

```text
saigon_zoo_tcv_dataset_dev
```

URI cho backend và Compass trên Windows:

```text
mongodb://127.0.0.1:27018/?replicaSet=rs0
```

**Compose cũ đã chuyển sang `docs/archive/pre-audit-2026-10-21/docker-compose.legacy.yml.txt`; không dùng để tái tạo bản này.** File đó dùng MongoDB `27017`, tên container khác, chưa có replica set và SeaweedFS. Chạy nó có thể tạo một database trống khác hoặc xung đột cổng Redis.

### 1.3. Quy ước lệnh trong hướng dẫn

- Mở **PowerShell** hoặc terminal PowerShell trong VS Code.
- Chạy các lệnh từ thư mục gốc dự án, nơi có `backend`, `frontend`, `scripts`.
- Đường dẫn ví dụ trên máy hiện tại:

```powershell
Set-Location 'E:\LUT\CNPM\multilingual-guide-services-saigon-zoo'
```

- Máy bạn có thể dùng `C:\Projects\saigon-zoo`. Nên chọn đường dẫn không có khoảng trắng để tương thích script launcher hiện tại.
- Chạy lần lượt từng khối. Nếu một lệnh báo lỗi, xử lý lỗi trước khi tiếp tục.
- Các biến `$env:...` chỉ tồn tại trong cửa sổ PowerShell hiện tại và các tiến trình được mở từ cửa sổ đó.
- Backend hiện đọc biến môi trường của tiến trình. **Chỉ tạo file `.env` là chưa đủ**, trừ khi bạn chủ động nạp nó.

---

## 2. Bật lại nhanh trên máy đã có đủ dữ liệu

Phần này dành cho máy hiện tại hoặc máy bạn đã hoàn tất phần 7. Không cần seed hay restore lại mỗi lần mở máy.

### Bước 1 — Mở Docker Desktop

Mở Start → Docker Desktop. Đợi Docker Engine hoạt động.

Trong PowerShell:

```powershell
docker info
docker ps -a
```

Nếu `docker info` không kết nối được Docker Engine, đừng chạy tiếp.

### Bước 2 — Bật database, kho audio và Redis

```powershell
docker start saigon-zoo-t10-replset saigon-zoo-t10-seaweedfs saigon-zoo-redis
```

Đợi vài giây rồi kiểm tra:

```powershell
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
docker exec saigon-zoo-t10-replset mongosh --port 27018 --quiet --eval 'db.hello().isWritablePrimary'
```

Lệnh MongoDB cần trả về `true`. Nếu báo `No such container`, máy này chưa được thiết lập theo bản hiện tại; xem phần 7.

### Bước 3 — Bật ứng dụng và HTTPS

Tại gốc dự án:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start_demo.ps1
```

Script sẽ:

1. Kiểm tra ba container và cấu hình kho audio.
2. Đặt biến môi trường cho backend.
3. Mở backend ở nền.
4. Build frontend nếu cần khởi động tiến trình frontend mới, rồi mở Vite preview ở nền.
5. Mở Cloudflare Tunnel.
6. Tạo URL và ảnh QR truy cập điện thoại.

**Script không tự tạo database, không tự bật ba container đang dừng, không tự phục hồi dữ liệu và không tự cài thư viện.**

Kết quả:

| Dùng ở đâu | Địa chỉ/file |
|---|---|
| Máy tính | `http://localhost:3000` |
| Điện thoại, đăng nhập admin qua HTTPS | URL in ở dòng `Phone URL` |
| Đọc lại URL | `.demo-run\phone-demo-url.txt` |
| Ảnh QR mở website | `.demo-run\phone-demo-qr.png` |
| Trang quản trị | Thêm `/admin` vào URL website |
| Dashboard | Thêm `/admin/analytics` |

Đọc URL:

```powershell
Get-Content .\.demo-run\phone-demo-url.txt
```

Mở ảnh QR bằng File Explorer hoặc Photos, không cần mở bằng trình soạn thảo.

### Chỉ dùng trên máy tính, không cần Cloudflare

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start_demo.ps1 -NoTunnel
```

Launcher đặt `ADMIN_COOKIE_SECURE=false` khi dùng `-NoTunnel` và `true` khi mở HTTPS tunnel. Khi đổi chế độ cần khởi động lại backend để nhận cấu hình cookie mới.

### Nếu chỉ Cloudflare bị dừng

Nếu backend và frontend vẫn chạy, chạy lại launcher sẽ giữ các tiến trình mà nó nhận diện đang chạy và mở lại tunnel:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start_demo.ps1
```

**URL HTTPS thường đổi khi tạo lại tunnel.** Gửi URL/QR mới cho bạn bè. URL trong tin nhắn cũ có thể hết hiệu lực.

---

## 3. Mở MongoDB bằng giao diện

### 3.1. Bật MongoDB trong Docker Desktop

1. Mở Docker Desktop.
2. Vào **Containers**.
3. Tìm `saigon-zoo-t10-replset`.
4. Nếu đang dừng, bấm nút **Start/Play**.
5. Chờ trạng thái Running.

Để ứng dụng chạy đầy đủ, bật thêm `saigon-zoo-t10-seaweedfs` và `saigon-zoo-redis`.

### 3.2. Cài và kết nối Compass

Tải [MongoDB Compass](https://www.mongodb.com/try/download/compass), cài rồi mở:

1. Chọn **Add new connection/New connection**.
2. Dán URI:

   ```text
   mongodb://127.0.0.1:27018/?replicaSet=rs0
   ```

3. Đặt tên kết nối, ví dụ `TCV - local dev`.
4. Bấm **Connect**.
5. Mở database `saigon_zoo_tcv_dataset_dev`.

Các collection đáng chú ý:

- `poi`: các điểm tham quan. Tên collection là `poi`, **không phải `pois`**.
- `poi_localizations`: nội dung theo ngôn ngữ.
- `audio_assets`: thông tin file audio và quan hệ với POI/gói.
- `admin_users`, `roles`: tài khoản và quyền quản trị.
- Các collection khác được giữ nguyên trong bản backup đầy đủ.

Không cần bấm “Create Database” nếu đã restore thành công. Nếu chỉ thấy `admin`, `config`, `local`, kiểm tra lại cổng `27018` và bước restore.

### 3.3. Những điều dễ nhầm

- Dữ liệu được lưu trong **Docker volume**, không nằm trong thư mục source Git.
- Dừng container hoặc tắt Docker Desktop thông thường không xóa volume.
- Xóa volume, Reset Docker Desktop hoặc chạy lệnh dọn volume có thể làm mất dữ liệu.
- Không cần cài thêm MongoDB Server trực tiếp trên Windows cho mô hình này.
- Compass trên máy bạn kết nối `127.0.0.1` là database **của máy bạn**, không phải database trên máy người gửi.
- Không đổi BSON `ObjectId` thành chuỗi khi chuyển dữ liệu; dùng `mongodump/mongorestore` ở dưới để giữ đúng kiểu và quan hệ.

---

## 4. Nếu bạn chỉ cần dùng quyền admin, không cần chạy một hệ thống riêng

Đây là cách nhanh nhất:

1. Chủ máy bật hệ thống như phần 2.
2. Chủ máy tạo một tài khoản riêng cho bạn theo phần 7.7.
3. Gửi URL HTTPS + tên tài khoản; chuyển mật khẩu qua kênh riêng.
4. Bạn mở `<URL-HTTPS>/admin` bằng trình duyệt.

Bạn không cần cài Docker, MongoDB, Node hay Python trong trường hợp này. Nhưng máy chủ phải đang chạy và tunnel phải còn hoạt động.

**Hai người cùng truy cập URL này sẽ sửa cùng một database.** Còn cài bản sao theo các phần sau thì mỗi máy có database riêng; dữ liệu không tự đồng bộ.

---

## 5. Cần bàn giao những gì để máy bạn giống máy hiện tại?

Không chỉ gửi bản Git cũ. Cần ba nhóm:

1. **Source hiện tại**, bao gồm các file đang sửa/chưa được Git theo dõi, ảnh và dữ liệu trong `data`.
2. **Bản sao MongoDB** để giữ POI, bản dịch, ObjectId, tài khoản, gói audio và các quan hệ.
3. **Kho SeaweedFS + đúng image đang dùng + cấu hình S3** để có các file MP3 thật.

Không cần mang Redis session sang; người dùng đăng nhập lại trên máy mới.

Thư mục bàn giao gợi ý:

```text
C:\TCV-handoff\
├─ source\                         Source hiện tại, chưa cần đẩy Git
├─ database.archive.gz             Backup MongoDB
├─ seaweed-data.tar.gz              Backup volume chứa audio
├─ seaweed-image.tar                Image SeaweedFS đang dùng
└─ seaweed.env                     Cấu hình S3, có khóa truy cập
```

Gói này có dữ liệu tài khoản, lịch sử analytics và khóa kho audio. Chỉ chuyển riêng cho người bạn được giao quyền admin; không đưa các file backup/`seaweed.env` lên Git công khai.

**Vì sao ưu tiên phục hồi thay vì seed lại?** Trang chủ hiện có ID gói offline cố định. Seed mới có thể tạo ID khác, làm QR/link hiện tại không khớp; seed nội dung cũng không thay thế một bản backup hoàn chỉnh gồm cả audio và gói offline.

---

## 6. Trên máy người gửi: chuẩn bị bản bàn giao

Các bước này **chưa được chạy khi viết tài liệu**. Thực hiện lúc không có ai đang sửa nội dung.

### 6.1. Chuẩn bị thư mục và sao chép source

Tại gốc dự án:

```powershell
$handoffDir = 'C:\TCV-handoff'
New-Item -ItemType Directory -Force -Path $handoffDir | Out-Null
```

Nếu thư mục này đã có bản bàn giao cũ, chọn một tên mới để không trộn hai bản.

Trong File Explorer:

1. Tạo `C:\TCV-handoff\source`.
2. Sao chép source hiện tại vào đó, gồm `backend`, `frontend`, `scripts`, `data`, `docs`, các file cấu hình và tài liệu gốc.
3. Đặc biệt giữ `frontend/public/images`, `frontend/src/assets/fonts`, `frontend/package-lock.json`.
4. Bỏ qua các thư mục/file sau:

   ```text
   .git
   .venv
   node_modules (ở mọi vị trí)
   frontend/dist
   .demo-run
   __pycache__
   .pytest_cache
   .env và các file chứa bí mật cá nhân
   ```

5. Giữ `.env.example` vì đây là mẫu, không phải cấu hình bí mật.

Không dùng `git archive` để lấy bản hiện tại: nó không mang theo các thay đổi chưa commit và file chưa được theo dõi.

### 6.2. Dừng ứng dụng trước khi chụp dữ liệu

Nếu các tiến trình được mở bằng launcher trong phiên làm việc hiện tại:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\stop_demo.ps1
```

Nếu chạy thủ công, bấm `Ctrl+C` trong các cửa sổ backend, frontend, tunnel. MongoDB vẫn phải chạy để dump.

Sau khi vừa khởi động lại Windows, không dùng mù quáng PID cũ trong `.demo-run`; xem phần 10.

### 6.3. Backup MongoDB

```powershell
docker start saigon-zoo-t10-replset
docker exec saigon-zoo-t10-replset mongodump --host 127.0.0.1 --port 27018 --db saigon_zoo_tcv_dataset_dev --archive=/tmp/tcv-database.archive.gz --gzip
if ($LASTEXITCODE -ne 0) { throw 'Backup MongoDB thất bại. Dừng tại đây.' }
docker cp saigon-zoo-t10-replset:/tmp/tcv-database.archive.gz "$handoffDir\database.archive.gz"
if ($LASTEXITCODE -ne 0) { throw 'Không sao chép được backup MongoDB.' }
```

Đây là bản sao toàn database, giữ tài liệu, kiểu BSON/ObjectId và metadata index. Không dùng export JSON từng collection thay cho bước này.

### 6.4. Lưu cấu hình S3 và đúng image SeaweedFS

Chạy trong cùng cửa sổ có `$handoffDir`:

```powershell
$seaweedConfig = (docker inspect saigon-zoo-t10-seaweedfs | ConvertFrom-Json)[0]
$s3Settings = @($seaweedConfig.Config.Env | Where-Object {
  $_ -match '^(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|S3_BUCKET)='
})
if ($s3Settings.Count -ne 3) { throw 'Thiếu cấu hình S3; chưa thể bàn giao.' }
$s3Settings | Set-Content -LiteralPath "$handoffDir\seaweed.env" -Encoding ascii

docker image tag $seaweedConfig.Image saigon-zoo-handoff/seaweedfs:20261021
if ($LASTEXITCODE -ne 0) { throw 'Không gắn được nhãn image SeaweedFS.' }
docker image save -o "$handoffDir\seaweed-image.tar" saigon-zoo-handoff/seaweedfs:20261021
if ($LASTEXITCODE -ne 0) { throw 'Không lưu được image SeaweedFS.' }
```

Khối trên không in khóa ra terminal. File `seaweed.env` vẫn chứa khóa thật, cần giữ riêng tư. Dùng đúng image nguồn để giảm rủi ro thay đổi định dạng dữ liệu giữa các phiên bản.

### 6.5. Backup volume SeaweedFS khi đã dừng

Volume đã đối chiếu trên máy hiện tại: `saigon_zoo_t10_seaweed_data`.

Tải công cụ sao lưu trước khi dừng storage:

```powershell
docker pull alpine:3.20
if ($LASTEXITCODE -ne 0) { throw 'Chưa tải được image sao lưu.' }
docker stop saigon-zoo-t10-seaweedfs
if ($LASTEXITCODE -ne 0) { throw 'Chưa dừng được SeaweedFS; không backup lúc đang ghi.' }
try {
  docker run --rm --mount "type=volume,source=saigon_zoo_t10_seaweed_data,target=/source,readonly" --mount "type=bind,source=$handoffDir,target=/backup" alpine:3.20 tar czf /backup/seaweed-data.tar.gz -C /source .
  if ($LASTEXITCODE -ne 0) { throw 'Backup SeaweedFS thất bại.' }
} finally {
  docker start saigon-zoo-t10-seaweedfs
}
```

Lệnh chỉ đọc volume nguồn. Không xóa database hay audio trên máy người gửi.

### 6.6. Kiểm tra và gửi

```powershell
Get-ChildItem -LiteralPath $handoffDir | Select-Object Name, Length
Get-FileHash "$handoffDir\database.archive.gz"
Get-FileHash "$handoffDir\seaweed-data.tar.gz"
Get-FileHash "$handoffDir\seaweed-image.tar"
```

Giữ các giá trị SHA-256 để đối chiếu file sau khi chuyển. Nén/chuyển cả thư mục qua USB hoặc kênh chia sẻ riêng.

Bật lại hệ thống người gửi bằng phần 2 khi đã sao lưu xong.

---

## 7. Trên máy bạn: cài lần đầu

### 7.1. Cài công cụ

| Công cụ | Mục đích / lựa chọn |
|---|---|
| Docker Desktop | Chọn WSL 2 và Linux containers; [hướng dẫn Windows chính thức](https://docs.docker.com/desktop/setup/install/windows-install/) |
| Python | Dùng Python **3.11.x** để gần môi trường hiện tại `3.11.6`; [trang tải](https://www.python.org/downloads/windows/) |
| Node.js | Dùng Node **24.x**, môi trường hiện tại `24.21.0`; [trang tải](https://nodejs.org/en/download) |
| VS Code | Đọc source/tài liệu và mở terminal, không bắt buộc để chạy |
| MongoDB Compass | Xem dữ liệu bằng giao diện, không bắt buộc |
| Git | Chỉ cần khi làm việc với repository; bàn giao qua thư mục không đòi hỏi push |

Nếu Docker yêu cầu WSL, mở PowerShell **Run as administrator**:

```powershell
wsl --install
```

Khởi động lại Windows nếu được yêu cầu, mở Docker Desktop và hoàn tất thiết lập. Máy cần bật virtualization theo yêu cầu Docker/WSL.

Mở cửa sổ PowerShell mới sau khi cài, kiểm tra:

```powershell
docker info
py -3.11 --version
node --version
npm.cmd --version
```

Nếu `npm` bị PowerShell chặn `npm.ps1`, dùng `npm.cmd` trong lệnh thủ công. Launcher được gọi bằng `-ExecutionPolicy Bypass` trong một tiến trình riêng, không cần đổi chính sách toàn máy.

### 7.2. Đặt source và cài thư viện

Giải nén gói bàn giao vào `C:\TCV-handoff`.

Sao chép `source` thành một thư mục mới, ví dụ `C:\Projects\saigon-zoo`. **Giữ riêng bản Git cũ**; không trộn file cũ/mới khi chưa biết file nào đã thay đổi.

```powershell
Set-Location 'C:\Projects\saigon-zoo'
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt
npm.cmd --prefix frontend ci
```

Nếu bước nào thất bại, chưa chạy launcher. Không cần copy `.venv`/`node_modules` từ máy người gửi.

### 7.3. Tạo MongoDB đúng cấu hình

Các lệnh tạo bên dưới chỉ chạy **một lần trên máy mới**. Nếu container hoặc volume cùng tên đã có dữ liệu, dừng lại để xác định nguồn; không restore chồng hay xóa cho hết lỗi.

```powershell
docker volume create saigon_zoo_t10_mongodb_data
docker volume create saigon_zoo_t10_mongodb_config
docker run -d --name saigon-zoo-t10-replset --restart unless-stopped -p 127.0.0.1:27018:27018 -v saigon_zoo_t10_mongodb_data:/data/db -v saigon_zoo_t10_mongodb_config:/data/configdb mongo:6.0 mongod --port 27018 --replSet rs0 --bind_ip_all
```

Đợi MongoDB khởi động:

```powershell
docker logs --tail 30 saigon-zoo-t10-replset
docker exec saigon-zoo-t10-replset mongosh --port 27018 --quiet --eval 'db.adminCommand({ping:1})'
```

Khởi tạo replica set **một lần**:

```powershell
docker exec saigon-zoo-t10-replset mongosh --port 27018
```

Trong cửa sổ `mongosh`, nhập:

```javascript
rs.initiate({_id: "rs0", members: [{_id: 0, host: "localhost:27018"}]})
```

Chờ vài giây rồi:

```javascript
db.hello().isWritablePrimary
```

Khi trả về `true`, nhập `exit`.

Địa chỉ `localhost:27018` phù hợp vì backend đang chạy trên Windows và cổng publish trùng cổng MongoDB trong container. Nếu sau này đưa backend vào Docker, cần thiết kế lại địa chỉ replica set; không áp dụng nguyên xi cấu hình này.

### 7.4. Phục hồi database

```powershell
$handoffDir = 'C:\TCV-handoff'
docker cp "$handoffDir\database.archive.gz" saigon-zoo-t10-replset:/tmp/tcv-database.archive.gz
if ($LASTEXITCODE -ne 0) { throw 'Không sao chép được archive vào MongoDB.' }
docker exec saigon-zoo-t10-replset mongorestore --host 127.0.0.1 --port 27018 --archive=/tmp/tcv-database.archive.gz --gzip --nsInclude='saigon_zoo_tcv_dataset_dev.*'
if ($LASTEXITCODE -ne 0) { throw 'Restore MongoDB thất bại; đọc lỗi trước khi tiếp tục.' }
```

Không thêm `--drop` để xử lý lỗi trùng dữ liệu. Các bước này dành cho database đích mới.

Kiểm tra:

```powershell
docker exec saigon-zoo-t10-replset mongosh --port 27018 saigon_zoo_tcv_dataset_dev --quiet --eval 'db.poi.countDocuments()'
docker exec saigon-zoo-t10-replset mongosh --port 27018 saigon_zoo_tcv_dataset_dev --quiet --eval 'db.audio_assets.countDocuments()'
```

Bản mô phỏng có 11 POI và 66 audio theo 6 ngôn ngữ; số thực tế có thể lớn hơn nếu chủ máy đã thêm nội dung. Đối chiếu với máy nguồn thay vì xóa phần dư.

### 7.5. Phục hồi kho audio

```powershell
docker image load -i "$handoffDir\seaweed-image.tar"
if ($LASTEXITCODE -ne 0) { throw 'Không nạp được image SeaweedFS.' }
docker volume create saigon_zoo_t10_seaweed_data
docker run --rm --mount "type=volume,source=saigon_zoo_t10_seaweed_data,target=/restore" --mount "type=bind,source=$handoffDir,target=/backup,readonly" alpine:3.20 tar xzf /backup/seaweed-data.tar.gz -C /restore
if ($LASTEXITCODE -ne 0) { throw 'Không giải nén được kho audio.' }
docker run -d --name saigon-zoo-t10-seaweedfs --restart unless-stopped -p 127.0.0.1:8333:8333 --env-file "$handoffDir\seaweed.env" -v saigon_zoo_t10_seaweed_data:/data saigon-zoo-handoff/seaweedfs:20261021 mini -dir=/data
```

Volume đích phải mới/trống trước khi giải nén, và không có SeaweedFS nào đang ghi vào volume đó.

Khởi động Redis:

```powershell
docker volume create saigon_zoo_redis_data
docker run -d --name saigon-zoo-redis --restart unless-stopped -p 127.0.0.1:6379:6379 -v saigon_zoo_redis_data:/data redis:7.0-alpine
```

### 7.6. Kiểm tra các dịch vụ và chạy app

```powershell
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_storage_access.ps1
```

Storage check cần hiện:

```text
s3_api_reachable=True
configured_bucket_exists=True
```

Kiểm tra này xác nhận API/bucket, **chưa chứng minh toàn bộ MP3 đều phát được**. Phần 11 hướng dẫn kiểm tra audio thực tế.

Sau đó:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start_demo.ps1
```

### 7.7. Tạo tài khoản admin riêng cho người bạn

Tại gốc dự án, trong cửa sổ PowerShell:

```powershell
$env:MONGODB_URI = 'mongodb://127.0.0.1:27018/?replicaSet=rs0'
$env:MONGODB_DATABASE = 'saigon_zoo_tcv_dataset_dev'
.\.venv\Scripts\python.exe -m scripts.create_admin
```

Nhập lần lượt:

1. Username mới, ví dụ `ban-quan-tri`.
2. Email của bạn.
3. Mật khẩu riêng, tối thiểu 12 ký tự. Khi nhập có thể không thấy ký tự hiện ra, đây là bình thường.

Kết quả thành công: `Admin account created.`

Tài khoản được cấp quyền quản lý POI, nội dung, audio và xem analytics. Script không gửi email kích hoạt.

Nếu báo username/email đã tồn tại, dùng tên/email khác hoặc đăng nhập tài khoản đã được bàn giao. Không sửa `password_hash` thủ công trong Compass.

Mở URL HTTPS của máy bạn + `/admin`, đăng nhập tài khoản mới. Bản restore cũng chứa các tài khoản từ máy nguồn; tài khoản riêng giúp phân biệt người sử dụng.

### 7.8. Những thứ không tự chuyển theo

- URL Cloudflare: tạo mới trên máy bạn.
- Phiên đăng nhập Redis: đăng nhập lại.
- Audio đã tải offline trong trình duyệt máy/điện thoại cũ: tải lại ở trình duyệt mới.
- Camera/GPS: trình duyệt hỏi cấp quyền lại theo URL.
- Các thay đổi sau thời điểm backup: không tự xuất hiện trên bản sao.

---

## 8. Chạy từng thành phần bằng tay

Dùng khi muốn hiểu cách chạy, xem log trực tiếp hoặc sửa code. **Không mở thêm các tiến trình này khi launcher đã dùng cổng `8000`/`3000`.**

### 8.1. Bật ba container

```powershell
docker start saigon-zoo-t10-replset saigon-zoo-t10-seaweedfs saigon-zoo-redis
```

### 8.2. Cửa sổ PowerShell A — backend

Tại gốc dự án:

```powershell
$env:MONGODB_URI = 'mongodb://127.0.0.1:27018/?replicaSet=rs0'
$env:MONGODB_DATABASE = 'saigon_zoo_tcv_dataset_dev'
$env:REDIS_URL = 'redis://127.0.0.1:6379/0'
$env:ADMIN_COOKIE_SECURE = 'false'

$storageConfig = (docker inspect saigon-zoo-t10-seaweedfs | ConvertFrom-Json)[0]
$storageValues = @{}
foreach ($entry in $storageConfig.Config.Env) {
  if ($entry -match '^(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|S3_BUCKET)=(.*)$') {
    $storageValues[$Matches[1]] = $Matches[2]
  }
}
$env:AUDIO_STORAGE_ENDPOINT_URL = 'http://127.0.0.1:8333'
$env:AUDIO_STORAGE_REGION = 'us-east-1'
$env:AUDIO_STORAGE_BUCKET = $storageValues['S3_BUCKET']
$env:AUDIO_STORAGE_ACCESS_KEY_ID = $storageValues['AWS_ACCESS_KEY_ID']
$env:AUDIO_STORAGE_SECRET_ACCESS_KEY = $storageValues['AWS_SECRET_ACCESS_KEY']

.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Giữ cửa sổ mở. `Ctrl+C` sẽ dừng backend.

- `ADMIN_COOKIE_SECURE=false`: dùng khi thử admin bằng HTTP local.
- Nếu dùng admin qua tunnel HTTPS, đặt `true` **trước khi khởi động backend**.
- Nếu đang sửa code backend, có thể thêm `--reload`; không cần khi demo.
- Mở `http://127.0.0.1:8000/health` chỉ kiểm tra API sống, không đủ kết luận database/audio đúng.

### 8.3. Cửa sổ PowerShell B — frontend demo có offline

Tại gốc dự án:

```powershell
npm.cmd --prefix frontend run build
npm.cmd --prefix frontend run preview -- --host 0.0.0.0 --port 3000
```

Mở `http://localhost:3000`. Giữ cửa sổ mở.

Khi đang lập trình giao diện, có thể dùng:

```powershell
npm.cmd --prefix frontend run dev -- --host 0.0.0.0 --port 3000
```

Chỉ chọn **một** trong `preview` hoặc `dev`. Để trình diễn ngoại tuyến, ưu tiên **build + preview** vì service worker của bản build lưu các asset đã đóng gói.

### 8.4. Cửa sổ PowerShell C — HTTPS cho điện thoại

Nếu container tunnel cũ còn chạy, dừng đúng container đó trước:

```powershell
docker stop saigon-zoo-demo-tunnel
```

Nếu báo không có container thì không cần dừng. Sau đó:

```powershell
docker run --rm --name saigon-zoo-demo-tunnel cloudflare/cloudflared:latest tunnel --no-autoupdate --url http://host.docker.internal:3000
```

Tìm dòng URL dạng:

```text
https://....trycloudflare.com
```

Mở URL này trên điện thoại. Không cần cùng Wi-Fi nếu cả hai thiết bị có Internet.

Chạy tunnel thủ công **không tự cập nhật** `.demo-run/phone-demo-url.txt` và ảnh QR cũ. Muốn tạo QR cho URL mới, mở một PowerShell khác ở gốc dự án:

```powershell
New-Item -ItemType Directory -Force -Path .demo-run | Out-Null
$phoneUrl = Read-Host 'Dán URL HTTPS vừa được tunnel cấp'
node .\scripts\write_demo_qr.mjs $phoneUrl .\.demo-run\phone-demo-qr.png
$phoneUrl | Set-Content .\.demo-run\phone-demo-url.txt -NoNewline
```

Không đưa cổng MongoDB/Redis/SeaweedFS lên tunnel. Tunnel này chỉ trỏ vào frontend; frontend proxy các đường API cần thiết về backend.

---

## 9. Tắt, bật lại và cập nhật code

### 9.1. Nếu đang chạy bằng launcher

Trong phiên máy hiện tại, dừng app/tunnel:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\stop_demo.ps1
```

Script để MongoDB/Redis/SeaweedFS tiếp tục chạy.

Nếu muốn tắt cả ba:

```powershell
docker stop saigon-zoo-t10-replset saigon-zoo-t10-seaweedfs saigon-zoo-redis
```

Sau đó có thể Quit Docker Desktop. Bật lại bằng phần 2, **không cần restore/seed**.

### 9.2. Nếu đang chạy thủ công

1. `Ctrl+C` trong cửa sổ tunnel.
2. `Ctrl+C` trong cửa sổ frontend.
3. `Ctrl+C` trong cửa sổ backend.
4. Dừng ba container bằng lệnh trên nếu muốn.

### 9.3. Sau khi sửa frontend/backend

- Frontend `dev`: thường tự cập nhật.
- Frontend `preview`: chạy lại `npm.cmd --prefix frontend run build`, sau đó tải lại trang.
- Backend không `--reload`: cần dừng/mở lại backend.
- Chỉ sửa frontend không bắt buộc tạo lại tunnel.
- Chỉ chạy lại launcher khi frontend còn sống **không đảm bảo nó build lại source mới**.
- Nếu thay dependency, chạy lại `npm.cmd --prefix frontend ci` hoặc pip theo requirements trước khi mở app.

### 9.4. Hiểu đúng về offline và tunnel

Cloudflare không tự làm website hoạt động ngoại tuyến. Website cần được mở và tải tài nguyên trước, còn audio cần tải gói vào trình duyệt.

1. Có mạng → mở URL HTTPS hiện tại.
2. Vào **Tải audio**, tải gói ngôn ngữ muốn dùng, đợi báo xong.
3. Mở các trang cần dùng ít nhất một lần.
4. Tắt mạng và thử phát audio đã tải trên **cùng trình duyệt, cùng URL**.

URL Cloudflare thay đổi là một origin mới: dữ liệu offline của URL cũ không tự chuyển sang. Ảnh/bản đồ nền chưa được cache cũng có thể thiếu khi offline. Không xóa dữ liệu website nếu muốn giữ gói đã tải.

QR mở website (`https://...`) khác với QR nội bộ `TCV-POI:...` hoặc `TCV-PACKAGE:...`. QR nội bộ dùng chức năng quét trong ứng dụng; camera điện thoại mặc định không nhất thiết hiểu các mã này.

---

## 10. Xử lý lỗi thường gặp

### Docker không chạy

- Mở Docker Desktop, chờ Engine ready.
- Kiểm tra `docker info`.
- Nếu lỗi WSL/virtualization, làm theo hướng dẫn Docker Desktop; chưa cần chỉnh code.

### `No such container`

Máy chưa có đúng container. Máy mới làm phần 7; máy cũ xem `docker ps -a`.

Không chạy compose cũ để “chữa nhanh”.

### Compass không kết nối / không thấy dữ liệu

- Đúng URI `27018`, không phải `27017`.
- Container `saigon-zoo-t10-replset` đang chạy.
- `db.hello().isWritablePrimary` trả `true`.
- Đã restore đúng database.
- Nếu Compass dùng kết nối cũ, tạo kết nối mới theo phần 3.

### `Address already in use` / cổng đang bận

```powershell
Get-NetTCPConnection -State Listen -LocalPort 3000,8000,27018,6379,8333 -ErrorAction SilentlyContinue |
  Select-Object LocalAddress, LocalPort, OwningProcess
```

Dùng Task Manager hoặc `Get-Process -Id <PID>` để xác định tiến trình. Đóng đúng cửa sổ/tiến trình đã chạy trước; không tắt hàng loạt Node/Python vì có thể ảnh hưởng ứng dụng khác.

### Launcher nhận nhầm PID cũ sau khi khởi động lại Windows

Launcher lưu PID trong `.demo-run`, nhưng PID có thể được Windows tái sử dụng. `stop_demo.ps1` đã kiểm tra command line thuộc dự án trước khi dừng PID; vẫn nên xác định đúng tiến trình nếu chạy thủ công.

1. Kiểm tra cổng `3000` và `8000` bằng lệnh trên.
2. Xác định các tiến trình thuộc dự án, nếu có, và dừng chúng đúng cách.
3. Khi đã chắc chắn app/tunnel cũ không còn chạy, xóa **chỉ** file PID, không xóa toàn thư mục:

```powershell
Remove-Item -LiteralPath .\.demo-run\backend.out.log.pid -ErrorAction SilentlyContinue
Remove-Item -LiteralPath .\.demo-run\frontend.out.log.pid -ErrorAction SilentlyContinue
Remove-Item -LiteralPath .\.demo-run\tunnel.out.log.pid -ErrorAction SilentlyContinue
```

4. Chạy launcher lại.

Không mang `.demo-run` của máy nguồn sang máy bạn.

### Cloudflare báo Bad Gateway / 502

Kiểm tra theo thứ tự:

```powershell
Invoke-WebRequest http://localhost:3000 -UseBasicParsing
Invoke-RestMethod http://127.0.0.1:8000/health
docker logs --tail 40 saigon-zoo-demo-tunnel
```

- `localhost:3000` không mở → frontend đang dừng hoặc sai cổng.
- Frontend mở nhưng API lỗi → kiểm tra backend và ba container.
- Local chạy, URL công khai lỗi → kiểm tra tunnel, đường Internet và URL mới nhất.
- Tunnel chạy Docker nên dùng `host.docker.internal:3000`, không dùng `localhost:3000` bên trong container.
- Máy tính ngủ/tắt, Docker tắt hoặc tunnel dừng thì URL công khai không phục vụ được nội dung mới.

### Đăng nhập xong lại quay về màn đăng nhập

- Bật Redis.
- Dùng đúng một URL nhất quán; `localhost`, `127.0.0.1` và URL tunnel có cookie riêng.
- Launcher đặt cookie Secure: ưu tiên HTTPS.
- Nếu cần HTTP local, chạy backend thủ công với `ADMIN_COOKIE_SECURE=false`.
- Restart Redis hoặc hết phiên có thể yêu cầu đăng nhập lại.

### Có POI nhưng không nghe được audio

- Chỉ restore MongoDB là chưa đủ; phải restore SeaweedFS.
- Chạy `check_storage_access.ps1`.
- Kiểm tra `configured_bucket_exists=True`.
- Nếu bucket đúng mà audio lỗi, đối chiếu backup volume/image/khóa S3 và xem backend log.
- Không vội tạo lại toàn bộ TTS: có thể làm thay đổi metadata/gói. Giữ bản audio đã backup trước.

### Camera điện thoại không bật

- Dùng HTTPS của tunnel, cấp quyền camera cho đúng website.
- `http://IP-máy-tính:3000` thường không đáp ứng yêu cầu secure context của camera.
- Nếu URL tunnel mới, cấp quyền lại.
- Thử trình duyệt đầy đủ thay vì trình duyệt nhúng trong ứng dụng nhắn tin.

### Dashboard lỗi hoặc không có số liệu

- Đăng nhập đúng tài khoản có quyền `analytics:read`.
- Kiểm tra backend/MongoDB/Redis.
- Máy bạn có database riêng: truy cập URL máy nguồn không tạo sự kiện ở máy bạn.
- Dashboard ghi rõ mốc thống kê hiện dùng UTC; không tự hiểu là ngày Việt Nam.

### Xem log

```powershell
Get-Content .\.demo-run\backend.out.log -Tail 60
Get-Content .\.demo-run\backend.out.log.err -Tail 60
Get-Content .\.demo-run\frontend.out.log -Tail 60
Get-Content .\.demo-run\frontend.out.log.err -Tail 60
Get-Content .\.demo-run\tunnel.out.log.err -Tail 60
docker logs --tail 60 saigon-zoo-t10-replset
docker logs --tail 60 saigon-zoo-t10-seaweedfs
```

Không phải lúc nào file `.err` có nội dung cũng là lỗi; một số công cụ ghi log bình thường vào stderr.

---

## 11. Checklist sau khi cài/bàn giao

Đây là các bước kiểm tra người nhận nên thực hiện sau khi cài, không phải kết quả đã kiểm thử trên máy mới.

- [ ] `docker ps` thấy MongoDB, SeaweedFS, Redis.
- [ ] MongoDB báo primary `true`, Compass thấy `saigon_zoo_tcv_dataset_dev`.
- [ ] Storage check báo API truy cập được và bucket tồn tại.
- [ ] `localhost:3000` mở được giao diện mới và logo.
- [ ] Trang chủ có danh sách loài và ảnh.
- [ ] Bấm loài → mở thông tin → xem trên bản đồ đúng POI.
- [ ] Chuyển ngôn ngữ, nội dung phù hợp.
- [ ] Phát thử audio của nhiều POI ở các ngôn ngữ.
- [ ] Tải gói offline, đợi xong rồi thử nghe khi mất mạng.
- [ ] Kiểm tra các QR gói hiện tại; restore đúng phải giữ nguyên ID.
- [ ] Điện thoại mở URL HTTPS mới, quét QR và cấp quyền camera.
- [ ] Bật mô phỏng trên bản đồ để kiểm chứng tự phát audio dù đang ở nhà.
- [ ] Tài khoản admin riêng đăng nhập được.
- [ ] Admin mở được POI/bản dịch, QR, khu audio và dashboard.
- [ ] Tắt đúng cách, bật lại bằng phần 2 vẫn thấy dữ liệu.

Nếu muốn thử sửa/lưu nội dung, chọn một POI thử nghiệm và ghi lại giá trị cũ để khôi phục sau.

---

## 12. Ghi chú về Git và phạm vi bàn giao

- Chưa commit, push, merge hoặc thay đổi nhánh chỉ để tạo hướng dẫn này.
- Bản source hiện tại có các thay đổi ngoài bản Git cũ; người nhận chỉ pull Git cũ sẽ chưa có giao diện/chức năng hiện tại.
- Thư mục source bàn giao và các backup nên được gắn cùng ngày để tránh lệch phiên bản.
- Dependency Python hiện khai báo khoảng phiên bản, chưa phải bản khóa môi trường tuyệt đối. Image SeaweedFS được xuất từ máy nguồn để giữ đúng bản đang chạy.
- Bản sao database chứa dữ liệu tới thời điểm backup; source và database giữa hai máy không tự đồng bộ.
- Đây là hướng dẫn môi trường demo/phát triển local. Không coi cấu hình này là triển khai production.

### Tài liệu tham khảo chính thức

- [Docker Desktop trên Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
- [MongoDB Compass](https://www.mongodb.com/try/download/compass)
- [mongodump](https://www.mongodb.com/docs/database-tools/mongodump/) và [mongorestore](https://www.mongodb.com/docs/database-tools/mongorestore/)
- [Cloudflare Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/)

Quick Tunnel cung cấp URL ngẫu nhiên để thử nghiệm; không cần tài khoản Cloudflare/tên miền cho luồng này. Nếu muốn URL cố định về sau, cần cấu hình tunnel/tên miền riêng.
