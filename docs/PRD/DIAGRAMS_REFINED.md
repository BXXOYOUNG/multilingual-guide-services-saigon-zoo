# Hai sơ đồ kiến trúc tinh gọn

Cập nhật 13/11/2026. Đây là bản vẽ lại **kiến trúc đang có trong repository**, dựa trên hai ảnh và mã PlantUML trong PRD, đối chiếu tài liệu và mã nguồn. Không đề xuất thay đổi kiến trúc, chức năng, API hoặc ERD.

| Sơ đồ | Xem / đưa vào báo cáo | Phóng to, in | Chỉnh sửa từng đối tượng |
|---|---|---|---|
| Component | [PNG 3600 × 2620](Component_Diagram_Refined.png) | [SVG](Component_Diagram_Refined.svg) | [diagrams.net](Component_Diagram_Refined.drawio) |
| Deployment | [PNG 3600 × 2900](Deployment_Diagram_Refined.png) | [SVG](Deployment_Diagram_Refined.svg) | [diagrams.net](Deployment_Diagram_Refined.drawio) |

## Cách bố trí

Component trả lời câu hỏi **mã nguồn được tạo từ những thành phần nào và phụ thuộc vào đâu**. Các khối có biểu tượng component biểu diễn đơn vị mã nguồn hoặc nhóm module có cùng trách nhiệm. Khung lớn gom các component theo frontend, backend, hạ tầng và công cụ. Các component con cùng sử dụng API hoặc hạ tầng được biểu diễn bằng một mũi tên phụ thuộc ở biên package. Quan hệ chi tiết được ghi trong bảng dưới để tránh hàng chục đường nối trùng đích. Khung router là các FastAPI router thực tế, không phải một gateway mới. Các API có thể gọi service, repository hoặc database trực tiếp; sơ đồ không áp đặt mọi request đi qua một chuỗi tầng bắt buộc.

Deployment trả lời câu hỏi **phần mềm chạy ở đâu, artifact nào được nạp, dữ liệu lưu ở đâu và các runtime giao tiếp ra sao**. Máy khách, máy host, trình duyệt, môi trường Node/Python, container và volume được phân biệt bằng stereotype. Đường liền thể hiện bên khởi tạo kết nối; dữ liệu phản hồi đi theo chiều ngược lại. Vì cloudflared chủ động mở tunnel, mũi tên tunnel hướng từ connector đến Cloudflare, dù request của người dùng được chuyển từ Cloudflare về host.

Hai sơ đồ dùng đường gấp khúc vuông góc, làn nối riêng và vị trí cố định. Không lặp toàn bộ frontend cho máy local và máy từ xa ở component. Trong deployment, cả hai browser đều chạy cùng bản React PWA.

## Component: đối chiếu mã nguồn và các phụ thuộc

Đường dẫn trong bảng tính từ gốc repository. Tên nhóm là cách gom để trình bày, không khẳng định có một class riêng tương ứng mỗi khối.

| Khối | Mã nguồn tiêu biểu | Trách nhiệm / phụ thuộc |
|---|---|---|
| Ứng dụng và điều hướng | `frontend/src/app/App.jsx`, `app/router.jsx`, `components/layout/`, `components/views/` | Cùng frontend cho khách và admin; trang chủ, khám phá, hướng dẫn, bản đồ, lộ trình, quản trị, thống kê. Sử dụng các module frontend và API. |
| Ngôn ngữ | `frontend/src/features/localization/` | Chọn/lưu ngôn ngữ, thông điệp UI, nội dung theo ngôn ngữ; dùng IndexedDB. Hệ thống có vi, en, fr, zh-Hans, ja, ko. |
| Bản đồ, GPS, geofence, lộ trình | `frontend/src/features/map/`, `components/views/MapView.jsx`, `ItineraryView.jsx` | MapLibre, OpenStreetMap raster tiles, Geolocation; nhận POI/geofence từ API, fallback POI cache; xét vùng tròn tại client và kích hoạt phát audio. |
| QR và phát audio | `frontend/src/features/qr/QrScanner.jsx`, các view sử dụng HTML Audio | Camera qua ZXing; QR dẫn tới POI hoặc gói; phát bản thu từ API hoặc Blob đã lưu. Ghi sự kiện nghe. |
| Audio offline và lưu tại thiết bị | `frontend/src/features/offline/audioPackages.js`, `db/indexedDB.js`, `services/cacheStorage.js`, `services/poiRepository.js`, `sw/registerServiceWorker.js`, `frontend/vite.config.js` | Tải manifest và từng MP3, kiểm tra dung lượng/checksum, lưu POI và audio ở IndexedDB; Service Worker/Cache Storage giữ shell và asset. Theo dõi mạng qua `services/networkStatus.js`. |
| Quản trị và dịch tại máy | `frontend/src/components/views/AdminView.jsx`, `AdminPoiWorkflow.jsx`, `AdminTranslationPanel.jsx`, `services/adminApi.js`, `services/browserTranslation.js` | Quản lý POI/nội dung/ảnh/geofence/audio/gói; tạo QR. Gọi API chuẩn bị preview, Chrome Translator để dịch, API commit sau khi admin sửa/chọn/xác nhận. Hỗ trợ nhập tay. |
| Theo dõi và dashboard | `frontend/src/services/analytics.js`, `components/views/AnalyticsDashboard.jsx` | Thiết bị/phiên ẩn danh, sự kiện bản đồ/geofence/nghe; gửi visitor API và truy vấn thống kê dành cho admin. localStorage/sessionStorage giữ định danh. |
| Router / hợp đồng HTTP | `backend/main.py`, `backend/api/` | Đăng ký router, request/response và dependency; gồm POI, geofence, audio, visitor, health và các nhóm admin. |
| POI và geofence | `backend/api/pois.py`, `geofences.py`, `admin.py`, `admin_workflow.py`, `repositories/poi_repository.py` | Nội dung, localization, CRUD POI, cập nhật vùng tròn; MongoDB. Thao tác admin kiểm tra quyền; kiểm tra audio và upload ảnh dùng S3 adapter. |
| Auth và RBAC | `backend/api/admin_auth.py`, `backend/services/admin_auth.py` | Admin/role ở MongoDB; cookie HTTP-only và session/rate limit ở Redis; cung cấp kiểm tra permission cho các API quản trị. |
| Audio và gói tải | `backend/api/audio.py`, `admin_workflow.py`, `backend/services/audio.py`, `backend/repositories/audio.py` | Task/asset/package/manifest/snapshot; MongoDB lưu metadata, S3 adapter đọc/ghi file. Gói phát hành giữ snapshot audio. |
| Dịch: preview / commit | `backend/api/admin_translation.py`, `backend/services/admin_translation.py` | Kiểm tra quyền; đọc nguồn/revision từ MongoDB, giữ preview Redis 30 phút, xác nhận các bản admin chọn bằng transaction MongoDB rs0. Kết quả dịch chưa commit ở bộ nhớ React. |
| Visitor và analytics | `backend/api/visitor.py`, `backend/api/admin.py` | MongoDB ghi/tổng hợp thiết bị, phiên, sự kiện, vị trí theo sự kiện và lịch sử nghe; Redis giới hạn ghi sự kiện; truy vấn admin yêu cầu quyền. |
| Tạo giọng TTS | `backend/api/admin_workflow.py`, `backend/services/admin_narration.py` | Admin yêu cầu tạo giọng từ nội dung đã lưu; FastAPI BackgroundTasks gọi Edge TTS; Redis giữ lease 5 phút; ghi MP3 qua S3 adapter và task/asset/trạng thái vào MongoDB. |
| Truy cập dữ liệu và hạ tầng chung | `backend/repositories/`, `backend/database/mongodb.py`, `redis_client.py`, `schemas/`, `config.py`, `core/exception_handlers.py` | Repository, kết nối dữ liệu, schema/validation, cấu hình và xử lý lỗi dùng chung. Một số API trực tiếp dùng database client. |
| S3 media adapter | `backend/services/audio_storage.py` | `AudioStorageProvider` và provider tương thích S3, dùng SeaweedFS cho MP3/ảnh. Nội dung binary không nằm trong MongoDB. |
| Công cụ chủ động | `scripts/seed_dataset.py`, `seed_demo_experience.py`, `sync_french_dataset.py`, `create_admin.py`, `prepare_handoff_backup.py`, `verify_handoff_backup.py`, `start_demo.ps1`, `stop_demo.ps1`, `data/dataset/` | Seed/admin truy cập MongoDB; script chuẩn bị MP3 có thể gọi Edge TTS và S3; backup/kiểm tra phục hồi DB/media; launcher điều khiển process và tunnel. |

Các interface của ảnh cũ được giữ về **ý nghĩa hợp đồng**, thay bằng nhóm sau:

| Interface trong ảnh gốc | Vị trí trong bản tinh gọn |
|---|---|
| `ILocalization`, `IMap`, `IQRScanner` | Các component ngôn ngữ, bản đồ và QR của frontend |
| `IAudioPlayback`, `IOfflineData` | Component QR/phát audio và component audio offline |
| `IVisitorTracking`, `IAdminTranslationEditor` | Component theo dõi/dashboard và quản trị/dịch |
| `IPOIContentAPI`, `IGeofenceAPI`, `IAudioAPI` | HTTP API → router → module POI/geofence/audio |
| `IAdminSessionAPI`, `IAuthorization` | Auth/RBAC và dependency kiểm tra permission |
| `IEventIngestionAPI`, `IAnalyticsQueryAPI` | Visitor/analytics; nhóm API công khai và API quản trị tương ứng |
| `ITranslationPreviewCommitAPI` | Module dịch preview/commit |
| `IMediaStorage`, `IS3ObjectStorage` | S3 media adapter → SeaweedFS |
| `IMongoDataAccess`, `IRedisSessionAndRateLimit` | Truy cập MongoDB và Redis; Redis còn giữ lease TTS và preview dịch |
| `IGeolocation`, `ICameraStream`, `IRasterTiles`, `IOnDeviceTranslation` | Khung nền tảng client: browser APIs, OSM và native Chrome Translator |
| `ISpeechSynthesisProvider` | Edge TTS; bên gọi là AdminNarration hoặc script chuẩn bị |

## Deployment: kết nối và lưu trữ

| Bên khởi tạo | Đích / giao thức | Ý nghĩa |
|---|---|---|
| Browser từ xa | Cloudflare Quick Tunnel, HTTPS 443 | Lấy frontend/assets, gọi `/api` và `/audio` cùng origin |
| cloudflared trong Docker | Cloudflare, tunnel mã hóa đi ra | Nhận request qua tunnel đã mở; không cần public MongoDB/Redis/S3 |
| cloudflared | `http://host.docker.internal:3000` | Chuyển request sang Vite trên Windows host |
| Browser local | `http://localhost:3000` | Dùng cùng build React PWA |
| Vite preview | `http://127.0.0.1:8000` | Proxy `/api/*`, `/audio/*` sang Uvicorn/FastAPI; Vite trả build tĩnh và service worker |
| FastAPI | MongoDB TCP `127.0.0.1:27018` → container `27018` | Replica set `rs0`, DB `saigon_zoo_tcv_dataset_dev`; lưu nội dung và metadata |
| FastAPI | Redis TCP `127.0.0.1:6379` → container `6379` | Session, rate limit, lease và preview có TTL |
| FastAPI | S3 HTTP `127.0.0.1:8333` → container `8333` | SeaweedFS mini; lưu và phục vụ MP3/ảnh qua backend |
| FastAPI hoặc script | Edge TTS qua Internet | Tạo MP3 theo yêu cầu admin hoặc khi chuẩn bị dataset |
| Browser local / từ xa | `tile.openstreetmap.org`, HTTPS | Tải nền bản đồ trực tiếp, không qua FastAPI |
| React admin | Native Chrome Translator trên máy admin | Dịch tại máy khi API/cặp ngôn ngữ hỗ trợ; tải model lần đầu cần Internet |
| MongoDB / SeaweedFS | Docker volumes | DB: `/data/db`, `/data/configdb`; media: `/data` |
| Công cụ trên host | Process, MongoDB, S3, Edge TTS và bản backup | Điều khiển demo; chuẩn bị, sao lưu và kiểm tra phục hồi. Các đích chung được gom bằng chú thích để không chồng dây runtime |

Hai browser đều có IndexedDB, Cache Storage và localStorage/sessionStorage. Model native thuộc Chrome profile, tách khỏi dữ liệu ứng dụng. Sơ đồ chỉ thể hiện volume bền vững cho MongoDB/SeaweedFS theo tài liệu; không giả định Redis có volume hoặc queue bền vững.

## Những giới hạn được giữ đúng

- Chỉ một backend FastAPI và một frontend React; frontend/backend chạy trên Windows host, không nằm trong Docker trong cấu hình demo này.
- Geofence được xét ở browser; server cung cấp vùng. Không có dịch vụ theo dõi GPS liên tục ở backend.
- Dịch văn bản xảy ra ở Chrome admin. Backend chuẩn bị và kiểm soát việc lưu; không gọi Cloud Translation và không tự sinh TTS sau dịch.
- TTS runtime là BackgroundTasks trong process FastAPI, không phải worker/queue bền vững; khách thiếu audio không được tự sinh TTS fallback.
- Offline chỉ dùng dữ liệu đã tải trên cùng origin/browser. Chưa có nền OSM offline đầy đủ; URL Quick Tunnel thay đổi làm thay đổi origin.
- Backup dữ liệu/media tách khỏi Git và không bao gồm model Chrome. Các máy nhận bàn giao chạy bản riêng, không tự đồng bộ.

## Tài liệu đã đối chiếu

- [Hai ảnh và nguồn cũ trong PRD](README.md).
- [Kiến trúc hiện tại](../CURRENT_ARCHITECTURE.md), [đối chiếu yêu cầu](../REQUIREMENTS_TRACEABILITY.md).
- [Quy trình POI admin](../ADMIN_POI_WORKFLOW.md), [dịch bằng Chrome](../ADMIN_AUTO_TRANSLATION.md), [hướng dẫn phát triển](../DEVELOPMENT.md).
- [Cài đặt và bàn giao](../../HUONG_DAN_CAI_DAT_VA_BAN_GIAO.md), [README và các use case](../../README.md).
- `backend/main.py`, các API/service/repository, cấu hình Vite, router frontend và `scripts/start_demo.ps1`.

## Chỉnh sửa và xuất lại

Mở file `.drawio` bằng diagrams.net qua **File → Open from → Device**. Các khối, nhãn và đường gấp khúc đều chỉnh sửa được. File này là nguồn chỉnh sửa trực quan của bản mới; các `.md` PlantUML cũ vẫn thuộc bộ ảnh cũ.

Để tái tạo chính xác SVG, PNG và drawio từ tọa độ đã kiểm tra, dùng [render_refined_diagrams.py](render_refined_diagrams.py):

```powershell
python docs/PRD/render_refined_diagrams.py
```

Script cần Pillow, dùng Arial trên Windows, xuất PNG ở tỉ lệ 2×. Trước khi lưu, script kiểm tra chữ vượt chiều rộng, đường đi xuyên khối/chữ và các đoạn nối giao cắt/chồng lên nhau. SVG/drawio được ghi UTF-8. Thay đổi thủ công trong drawio không được đồng bộ ngược vào script; chỉ chạy lại script khi muốn xuất lại bản được định nghĩa bằng mã.

Bản cũ không bị ghi đè. Việc kiểm tra này xác nhận bố cục và đối chiếu tĩnh với repository, không phải kiểm thử lại dịch native, TTS online hoặc hạ tầng đang chạy.
