# Rà soát file và thành phần cần dọn

Ngày 21/10/2026. Việc dọn dựa trên đường import, tham chiếu trong tài liệu và runtime đang có, không dựa vào ngày sửa file hoặc trạng thái untracked của Git.

## Đã đưa khỏi luồng sử dụng hiện tại

Các file ở bảng dưới đã chuyển vào `docs/archive/pre-audit-2026-10-21/`. File script/config lịch sử mang đuôi `.txt` để tránh chạy nhầm. Chưa xóa vĩnh viễn các tài liệu thiết kế gốc.

| Vị trí cũ | Vấn đề |
|---|---|
| `docker/docker-compose.yml` | Trỏ MongoDB standalone 27017, tên container khác; thiếu storage đang dùng |
| `scripts/prepare_mvp_dataset.py` | Kịch bản 2 POI, xóa tọa độ mô phỏng và vô hiệu geofence; trái với bản demo 11 POI được chấp thuận |
| `scripts/bootstrap_demo_admin.py` | Bootstrap admin đời đầu; trùng mục đích với script tạo admin được dùng hiện nay |
| `Component_Diagram.png`, `Deployment_Diagram.png`, `Logical_ERD.png` | Không phản ánh đầy đủ as-built; ERD còn lỗi nhãn/quan hệ |
| `frontend/public/images/animals/tcv-an-006.jpg` | Ảnh sai loài; không còn được frontend/dataset/database tham chiếu |

## Cần cập nhật, không nên xóa

| File/nhóm | Cách xử lý |
|---|---|
| `README.md` | Giữ 10 use case gốc; thêm điểm vào tài liệu hiện hành và bảng khoảng cách yêu cầu |
| `IMPLEMENTATION_PLAN.md` | Giữ kế hoạch mục tiêu; ghi rõ không phải báo cáo đã hoàn tất mọi task |
| `docs/DATABASE_TASK_SCENARIOS.md` | Sửa thông tin Redis, `.env.example` và giới hạn thao tác database |
| `docs/DEVELOPMENT.md`, `DEMO_DATASET.md`, `ROADMAP_CURRENT_STATE.md` | Đồng bộ 6 gói offline, runtime Windows/Docker, cách khởi động và các giới hạn còn lại |
| `README_SEED_DATASET.md`, `README_SYNC_FRENCH.md` | Giữ để bảo trì dataset; không dùng như bước cài máy nhận mặc định |
| Test API/audio/POI và T06 | Cập nhật auth, `id` serialization, schema metadata và service worker được build sinh ra |
| `scripts/seed_demo_experience.py`, `download_demo_images.py` | Giữ công cụ tái tạo, tránh chọn ảnh ngẫu nhiên sai loài và ghi trạng thái audio không khớp |

## Phải giữ

- MongoDB `saigon_zoo_tcv_dataset_dev`, volume MongoDB và volume SeaweedFS: chứa dữ liệu thật của bản demo, không phải rác.
- Redis và container `saigon-zoo-redis`: session đăng nhập phụ thuộc nó.
- `data/dataset/*.csv`: dữ liệu ứng viên/nguồn, bản dịch và checklist. Các pin chưa xác minh trong CSV là hồ sơ nguồn; runtime mô phỏng nằm trong MongoDB. Không đồng nhất hai lớp dữ liệu.
- `data/dataset/demo_image_credits.json`, ảnh đang dùng và license font: cần cho attribution và tái tạo giao diện.
- `scripts/create_admin.py`, launcher, script kiểm tra storage, tạo QR, seed/sync và các test: phục vụ vận hành/bảo trì.
- `frontend/src/services/cacheStorage.js` và các hàm verify foundation: còn được bài kiểm tra T06 tham chiếu. Chưa có lý do cần xóa chỉ vì chưa dùng trong luồng audio chính.
- `.env.example`, `Rules.md`, tài liệu quy ước API: vẫn là cấu hình mẫu và quy tắc dự án.

## Có thể dọn khi không cần, nhưng không giải quyết xung đột nghiệp vụ

- `frontend/dist/`: build tạo lại được; cần build trước khi chạy preview. Không xóa lúc đang demo.
- `node_modules/`, `.venv/`: cài lại được; xóa sẽ phải cài thư viện lại.
- `__pycache__/`, `.pytest_cache/`: cache công cụ, không ảnh hưởng PRD.
- `.demo-run/`: có log/PID/QR URL tạm, ảnh kiểm thử và snapshot trước sửa dữ liệu. Giữ snapshot trước khi hoàn tất audit; dừng đúng tiến trình trước khi dọn PID. URL/QR cũ có thể hết hạn.

Không dọn Docker volume bằng `prune`, không drop database hoặc xóa tài khoản admin chỉ để làm thư mục gọn. Chưa có thao tác push/merge Git trong đợt rà soát này.

## Tài liệu nên dùng từ đây

1. [Kiến trúc hiện tại](CURRENT_ARCHITECTURE.md).
2. [Đối chiếu yêu cầu và phần đã có](REQUIREMENTS_TRACEABILITY.md).
3. [Hướng dẫn cài đặt/bàn giao](../HUONG_DAN_CAI_DAT_VA_BAN_GIAO.md).
4. [Báo cáo kiểm thử](AUDIT_REPORT_2026-10-21.md).
