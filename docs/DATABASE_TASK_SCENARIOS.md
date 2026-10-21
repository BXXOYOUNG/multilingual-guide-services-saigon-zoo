# Kịch bản tạo task khi database dev đã có

**Ngày đối chiếu:** 2026-10-21
**Database dev:** `saigon_zoo_tcv_dataset_dev`

Tài liệu này bổ sung điều kiện thực thi task cho coding agent. Nó không thay Use Case, Logical ERD, API contract hoặc Deployment Diagram đã duyệt.

## Runtime đã đối chiếu

| Thành phần | Runtime quan sát được | Quy tắc khi tạo task |
|---|---|---|
| MongoDB | Container `saigon-zoo-t10-replset`, MongoDB 6.0, host port `27018`, replica set `rs0` | Dùng URI `mongodb://127.0.0.1:27018/?replicaSet=rs0` từ host và database `saigon_zoo_tcv_dataset_dev`. |
| SeaweedFS | Container `saigon-zoo-t10-seaweedfs`, port `8333` | Đây là object/file storage, không phải MongoDB hay Redis. Chỉ task storage/audio được dùng nó qua adapter đã có. |
| Redis | `saigon-zoo-redis`, host port `6379` | Dùng `REDIS_URL=redis://127.0.0.1:6379/0` cho session/rate limit. |
| Compose lịch sử | Đã lưu tại `docs/archive/pre-audit-2026-10-21/docker-compose.legacy.yml.txt` | Không chạy; xem hướng dẫn bàn giao để tạo đúng runtime. |

Backend settings được đọc từ `backend/config.py`: `MONGODB_URI`, `MONGODB_DATABASE`, `REDIS_URL`. `.env.example` đã đồng bộ các tên này; backend không tự nạp file `.env`.

## Luồng bắt buộc trước task có dữ liệu

1. Đọc task, Use Case liên quan, ERD và repository/schema đang có.
2. Kiểm tra tên database trong cấu hình hiệu lực là `saigon_zoo_tcv_dataset_dev`; không in credential hoặc toàn bộ URI có thông tin xác thực vào log.
3. Kiểm tra MongoDB có phản hồi và đọc metadata cần thiết (database/collection/field/count mẫu) trước khi quyết định thao tác.
4. Nếu collection hoặc field thực tế khác với ERD/code, báo cáo chênh lệch và dừng phần phụ thuộc; không tự tạo collection/field mới để “làm cho chạy”.
5. Mặc định dùng fixture/fake database cho unit test. Chỉ kết nối database thật khi task yêu cầu tích hợp và phải ghi rõ thao tác đọc/ghi dự kiến.
6. Không drop database/collection, xóa dữ liệu, reseed toàn bộ, hay thay ID hiện hữu. Khi cần seed dataset cho task cụ thể: dry-run, xác nhận đúng database dev, dùng script có sẵn và tuân theo `README_SEED_DATASET.md`.

## Kịch bản theo loại task

### A. Kết nối backend

- Đọc `backend/config.py` và `backend/database/mongodb.py` trước khi sửa.
- Dùng `MONGODB_URI` + `MONGODB_DATABASE`; hai biến phải cùng tồn tại.
- Chỉ xác nhận ping/kết nối và chọn đúng database. Không khởi tạo dữ liệu mẫu hoặc xóa dữ liệu để kiểm tra.
- Kiểm tra Redis độc lập; nếu chưa có `REDIS_URL`/service đang chạy, ghi rõ phần Redis chưa tích hợp thay vì đánh dấu hoàn tất toàn bộ data layer.

### B. POI và bản dịch

- Dùng collection đúng như repository/ERD hiện hữu: `poi` và `poi_localizations`.
- Liên kết `poi_localizations.poi_id` bằng BSON ObjectId tương ứng, không đổi thành chuỗi hoặc tự tạo ID khác.
- Lọc trạng thái POI và `language_code` theo hợp đồng hiện có; không tự thêm fallback ngôn ngữ hoặc đổi mã ngôn ngữ.
- Đối chiếu các language code với manifest/dataset và frontend trước khi thêm lựa chọn mới.
- Với tọa độ minh họa/chưa xác minh, không dùng chúng để tuyên bố geofence đã đúng thực địa.

### C. Nội dung đa ngôn ngữ và audio

- Nội dung text được định danh theo POI + language như model hiện hành.
- Giữ đúng quan hệ đã ghi trong IMPLEMENTATION_PLAN: `audio_tasks` là trạng thái xử lý, `audio_assets` là audio sẵn sàng, `poi_localizations.audio_url` tham chiếu audio phát được và `audio_packages` gom asset offline.
- Không thay `audio_url` bằng URL task hoặc URL package; không thêm collection/field để né việc đọc ERD.
- Chỉ task storage/audio sử dụng SeaweedFS, thông qua adapter. Không suy ra API/credential/bucket từ việc container đang chạy; đọc cấu hình và adapter trước.

### D. Ghi dữ liệu quản trị hoặc cập nhật dataset

- Xác định rõ task đang sửa dữ liệu qua API quản trị hay qua script seed; không dùng lẫn hai luồng.
- Chỉ ghi vào database dev đã nêu, giới hạn bản ghi theo task và giữ nguyên trường không thuộc phạm vi cập nhật.
- Với seeder, dùng upsert có ID ổn định theo script. Không activate POI, nội dung draft hoặc tọa độ minh họa trừ khi task yêu cầu rõ và đủ cờ bảo vệ.
- Trước khi chạy thao tác ghi, trình bày collection, bộ lọc, trường thay đổi và số bản ghi dự kiến trong báo cáo task.

### E. Task không cần database

- Không thêm database connection/dependency chỉ vì task thuộc cùng đồ án.
- Dùng API contract hiện hữu hoặc fixture nếu cần mô phỏng kết quả.

## Mẫu prompt gắn với task

```text
DATABASE BASELINE
- Dev database đã tồn tại: saigon_zoo_tcv_dataset_dev.
- MongoDB replica set chạy tại host port 27018 (rs0); dùng MONGODB_URI và MONGODB_DATABASE.
- Không drop, recreate, reseed hoặc đổi schema/ERD.
- Redis chạy ở 127.0.0.1:6379; SeaweedFS là storage audio, không thay thế Redis.
- Trước khi sửa, đọc code/config hiện hữu và kiểm tra dữ liệu bằng thao tác chỉ đọc.
- Nêu rõ mọi thao tác ghi dự kiến và chỉ giới hạn vào dữ liệu cần cho task.
```

## Tài liệu hiện hành

Đọc [CURRENT_ARCHITECTURE.md](CURRENT_ARCHITECTURE.md) và [REQUIREMENTS_TRACEABILITY.md](REQUIREMENTS_TRACEABILITY.md) trước khi sinh task. Các script chuẩn bị giai đoạn 2 POI đã lưu trữ; không chạy lại để “sửa” dataset demo 11 POI. Seed/sync chỉ chạy khi có yêu cầu rõ vì có thể thay đổi nội dung và làm audio cũ không còn khớp.
