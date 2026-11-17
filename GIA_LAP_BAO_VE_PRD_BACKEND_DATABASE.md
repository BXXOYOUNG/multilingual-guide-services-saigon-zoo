# Giả lập bảo vệ 1:1 — PRD, backend và database

Đối chiếu mã nguồn ngày **16/11/2026**, commit **`1c998a1266ce`**, thư mục `multilingual-guide-services-saigon-zoo`. Đây là tài liệu ôn tập và đối chiếu tĩnh, không phải biên bản nghiệm thu. Không sửa mã nguồn, database, PRD hoặc ERD khi soạn tài liệu.

Tài liệu đặt cạnh thư mục dự án theo yêu cầu. Các liên kết code là đường dẫn cục bộ tuyệt đối kèm dòng tại thời điểm đối chiếu; sau khi code đổi, tìm lại bằng tên hàm đi kèm. Số record thực tế, quyền MongoDB, cấu hình container và khả năng Chrome/điện thoại phải được kiểm tra trên môi trường bảo vệ; không suy ra từ số liệu seed.

**Quy mô:** 102 câu hỏi có trả lời mẫu và vị trí code; kèm ma trận PRD, kịch bản tập và các điểm dễ trả lời sai.

## Cách dùng khi luyện với một người hỏi nhanh

1. Che phần trả lời, trả lời mỗi câu trong 20–40 giây, rồi mở đúng code để chứng minh.
2. Nói kết luận trước; sau đó chỉ endpoint/hàm, collection và điều kiện quan trọng. Không đọc nguyên file.
3. Luôn tách **PRD yêu cầu**, **code hiện có**, **phần chưa đạt/giới hạn**. Không dùng từ “đã đầy đủ” nếu chưa có bằng chứng.
4. Các câu test là kịch bản đề xuất, chưa được chạy trong lần soạn này. Các thử nghiệm sửa dữ liệu chỉ thực hiện trên DB thử, có dữ liệu dùng một lần; không xóa collection hay file demo gốc để chứng minh.
5. Nếu chưa chắc: “Em xin mở hàm ... để đối chiếu điều kiện thực tế.” Tránh đoán tên collection hoặc bịa một ràng buộc chưa có.

## Mục lục theo nhóm câu hỏi

| Nhóm | Câu |
|---|---|
| [A. Thầy kiểm tra nhóm có bám PRD không](#phan-a) | 01–10 |
| [B. Kiến trúc và khả năng lần theo code backend](#phan-b) | 11–17 |
| [C. MongoDB, POI, ERD và toàn vẹn dữ liệu](#phan-c) | 18–31 |
| [D. Audio: truy vấn, storage, manifest và snapshot](#phan-d) | 32–41 |
| [E. Offline, QR, GPS — chỉ học ranh giới cần thiết](#phan-e) | 42–49 |
| [F. Đăng nhập, session và phân quyền backend](#phan-f) | 50–59 |
| [G. Nội dung và dịch: xác nhận, revision, transaction](#phan-g) | 60–68 |
| [H. TTS: chạy nền, cạnh tranh và thất bại](#phan-h) | 69–76 |
| [I. Analytics: phải hiểu công thức, không chỉ đọc dashboard](#phan-i) | 77–84 |
| [J. Vận hành, lỗi, kiểm thử và giới hạn kỹ thuật](#phan-j) | 85–92 |
| [K. Hỏi sâu để xem em thật sự đọc code hay chỉ thuộc slide](#phan-k) | 93–98 |
| [L. Bốn màn bảo vệ tổng hợp](#phan-l) | 99–102 |
| [M. Kịch bản tập dượt và bảng mở code nhanh](#phan-m) | Kịch bản và từ điển |

## Bản đồ PRD → nơi chứng minh

PRD/use case gốc ở `README.md`; `docs/PRD` hiện chủ yếu chứa sơ đồ. Tài liệu đối chiếu giải thích hiện trạng nhưng không tự thay thế yêu cầu gốc hoặc chứng minh thầy đã chấp thuận thay đổi.

| UC | Yêu cầu / mục tiêu | Hiện trạng cần nói đúng | Điểm mở code |
|---|---|---|---|
| 01 | Thiết lập ngôn ngữ | Lưu ở thiết bị, POI trả theo ngôn ngữ; không đồng nghĩa dịch máy | `LanguageContext.jsx`, `languageStorage.js`, `poi_repository.py` |
| 02 | Bản đồ, vị trí, POI | Có GPS/POI cache; nền OSM vẫn phụ thuộc mạng | `pois.py`, `poi_repository.py`, `InteractiveMap.jsx` |
| 03 | Tự phát theo vị trí | Client xét vòng tròn; chưa có visitor TTS fallback và cooldown thời gian đầy đủ | `geofences.py`, `InteractiveMap.jsx` |
| 04 | QR mở thuyết minh | QR chứa loại/ID; tìm bản thu đúng ngôn ngữ, thiếu thì báo lỗi | `audioPackages.js`, `api/audio.py`, `repositories/audio.py` |
| 05 | Tải gói offline | Manifest + từng MP3, kiểm tra size/SHA-256, lưu tại thiết bị | `services/audio.py`, `audioPackages.js` |
| 06 | Chọn đối tượng, nghe offline | Tích hợp danh sách audio đã tải trong trang Audio; không cần tab riêng để có hành vi | `ExploreView.jsx`, `audioPackages.js` |
| 07 | Đăng nhập admin | Cookie token ngẫu nhiên + Redis session + role/permission MongoDB | `api/admin_auth.py`, `services/admin_auth.py` |
| 08 | Quản lý POI | Tạo/sửa/ẩn, ảnh, vùng tròn; chưa có ràng buộc khóa ngoại chặn xóa cứng | `api/admin.py`, `admin_workflow.py` |
| 09 | Nội dung, bản dịch/audio | Nhập tay hoặc Chrome dịch; preview/revision/commit; TTS riêng, snapshot riêng | `admin_translation.py`, `admin_narration.py` |
| 10 | Phân tích hoạt động | Events, visits, active 5 phút, POI/ngôn ngữ; chưa có heatmap, tuyến và nghe trung bình như mục tiêu gốc | `visitor.py`, `api/admin.py` |

> Ưu tiên học: PRD và sai lệch → POI/database → audio/snapshot → auth → dịch/TTS → analytics → vận hành. Frontend chỉ học ranh giới trách nhiệm cần thiết.

<a id="phan-a"></a>

## A. Thầy kiểm tra nhóm có bám PRD không

### Câu 01. Thầy: “PRD của nhóm nằm ở đâu? Đừng đưa tôi xem mỗi ảnh giao diện.”

**Trả lời mẫu:** Các yêu cầu/use case gốc được lưu trong README gốc, từ UC-01 đến UC-10. Em dùng nó làm mốc đối chiếu; bảng REQUIREMENTS_TRACEABILITY mô tả phần hiện có và khoảng cách. Thư mục docs/PRD hiện có các sơ đồ, không phải bằng chứng rằng mọi yêu cầu đã hoàn thành.

**Mở để chứng minh:** [README.md:15](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/README.md:15>); [docs/REQUIREMENTS_TRACEABILITY.md:7](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/docs/REQUIREMENTS_TRACEABILITY.md:7>).

**Thầy có thể hỏi tiếp / yêu cầu thử:** Mở một yêu cầu gốc, chỉ endpoint và test tương ứng; đánh dấu phần chưa đạt thay vì đổi yêu cầu để khớp code.

### Câu 02. Thầy: “Em nói đã hoàn thành. UC-03 ghi thiếu audio thì dùng TTS, code ở đâu?”

**Trả lời mẫu:** Nhánh visitor TTS fallback trong PRD chưa được triển khai. Geofence hiện resolve bản thu sẵn có; không có thì báo không có audio. TTS hiện có là admin chủ động yêu cầu từ lời đã lưu, không phải khách đi vào vùng là sinh giọng mới.

**Mở để chứng minh:** [README.md:204](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/README.md:204>); [frontend/src/features/map/InteractiveMap.jsx:195](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/map/InteractiveMap.jsx:195>); [backend/api/admin_workflow.py:119](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:119>).

**Không trả lời:** “Có Edge TTS nên UC-03 đã hoàn thành toàn bộ.”

### Câu 03. Thầy: “UC-10 yêu cầu heatmap, tuyến di chuyển, thời gian nghe trung bình. Nhóm làm đến đâu?”

**Trả lời mẫu:** Dashboard hiện trả số phiên, sự kiện, thiết bị active 5 phút, số lượt bắt đầu/hoàn tất audio, POI nổi bật và phân bố ngôn ngữ/thời gian UTC. Chưa trả heatmap, lịch sử tuyến liên tục hoặc KPI thời gian nghe trung bình như Summary gốc. Việc có playback_history và location_events chưa đồng nghĩa các phân tích đó đã được xây dựng.

**Mở để chứng minh:** [README.md:984](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/README.md:984>); [backend/api/admin.py:172](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:172>); [backend/api/visitor.py:96](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/visitor.py:96>).

### Câu 04. Thầy: “UC-08 ghi xóa POI. Sao API DELETE chỉ đổi một cờ?”

**Trả lời mẫu:** Implementation chọn ẩn/xóa mềm: cập nhật is_active=false để giữ POI và tham chiếu. Đó là khác biệt cần thuyết minh với yêu cầu xóa trong PRD; code không có cơ chế kiểm tra hết các collection rồi cấm xóa cứng. Em không gọi xóa mềm là khóa ngoại.

**Mở để chứng minh:** [README.md:733](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/README.md:733>); [backend/api/admin.py:130](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:130>).

```text
 733 | ### A3 — Xóa POI
 734 | 1. Quản trị viên chọn một POI trong danh sách.
 735 | 2. Quản trị viên thực hiện thao tác xóa.
 736 | 3. Hệ thống thực hiện xóa POI.
```

### Câu 05. Thầy: “UC-06 có thật hay em vẽ thêm cho đủ mười use case?”

**Trả lời mẫu:** Có hành vi nghe audio đã lưu: ExploreView đọc danh sách offline, cho chọn bản thu và phát Blob tại thiết bị. UC-05 là tải/chuẩn bị; UC-06 là sử dụng sau khi tải. Hai mục tiêu có thể cùng một trang; phần khám phá chi tiết từng con cần đối chiếu phạm vi thực tế, không khẳng định đã có tab khám phá độc lập.

**Mở để chứng minh:** [README.md:506](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/README.md:506>); [frontend/src/components/views/ExploreView.jsx:98](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/components/views/ExploreView.jsx:98>); [frontend/src/features/offline/audioPackages.js:85](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:85>).

### Câu 06. Thầy: “Đây là hệ thống triển khai thật tại Thảo Cầm Viên hay demo?”

**Trả lời mẫu:** Bản đang đối chiếu là demo mô phỏng lớp học. Seed gắn tọa độ gần đúng, nội dung/giọng tổng hợp và metadata demo. Mô phỏng chứng minh được luồng phần mềm, không chứng minh vị trí chuồng chính xác, chất lượng dịch hay GPS/autoplay ngoài thực địa.

**Mở để chứng minh:** [scripts/seed_demo_experience.py:121](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/seed_demo_experience.py:121>); [backend/api/admin.py:103](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:103>); [docs/ROADMAP_CURRENT_STATE.md:39](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/docs/ROADMAP_CURRENT_STATE.md:39>).

### Câu 07. Thầy: “Em nói 11 POI, 66 audio, 6 gói. Đó là số code hay số thật hiện nay?”

**Trả lời mẫu:** Đó là baseline demo ghi trong tài liệu, không phải số cố định hệ thống buộc phải có. Admin thêm POI, tạo giọng và snapshot sẽ tăng số bản ghi; số asset cũng không luôn bằng POI nhân ngôn ngữ vì có phiên bản và bản sao metadata snapshot. Khi bảo vệ phải lấy thống kê DB thử hiện tại, không đọc số seed thành số live.

**Mở để chứng minh:** [docs/ROADMAP_CURRENT_STATE.md:20](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/docs/ROADMAP_CURRENT_STATE.md:20>); [backend/api/admin_workflow.py:151](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:151>); [scripts/seed_demo_experience.py:44](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/seed_demo_experience.py:44>).

### Câu 08. Thầy: “PRD, sơ đồ và code mâu thuẫn thì em lấy cái nào để chấm đạt?”

**Trả lời mẫu:** PRD là mốc yêu cầu; code là bằng chứng hành vi đã xây dựng. Em lập bảng sai lệch, đưa test và nêu thay đổi cần được nhóm/thầy chấp thuận. Không tự sửa ERD/PRD chỉ để hợp thức hóa code, cũng không lấy sơ đồ cũ để khẳng định runtime đang chạy đúng như vậy.

**Mở để chứng minh:** [Rules.md:18](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/Rules.md:18>); [docs/REQUIREMENTS_TRACEABILITY.md:18](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/docs/REQUIREMENTS_TRACEABILITY.md:18>); [backend/main.py:37](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/main.py:37>).

### Câu 09. Thầy: “Hai mũi tên liền vào Xác định ngôn ngữ có phải hai bước chạy tiếp nhau không?”

**Trả lời mẫu:** Không. Trong XML UC-01 chúng dùng tam giác rỗng, hướng từ use case chuyên biệt về khái quát, tức Generalization. Nó không tự diễn tả if/else hoặc thứ tự. Với chọn mới/dùng lựa chọn đã lưu, có thể giải thích như hai biến thể nhưng Activity Diagram hoặc luồng thay thế rõ hơn nếu mục đích là mô tả điều kiện thực thi. Việc dọn chú thích ngoài hình vừa rồi không tự đổi các quan hệ UML bên trong.

**Mở để chứng minh:** [docs/Use-case/USE_CASE_DIAGRAMS/UC_01_USE_CASE_CHI_TIET.xml:61](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/docs/Use-case/USE_CASE_DIAGRAMS/UC_01_USE_CASE_CHI_TIET.xml:61>); [docs/Use-case/USE_CASE_DIAGRAMS/README.md:24](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/docs/Use-case/USE_CASE_DIAGRAMS/README.md:24>); [frontend/src/features/localization/languageStorage.js:16](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/localization/languageStorage.js:16>).

### Câu 10. Thầy: “Use case, component và deployment khác nhau thế nào, em đối chiếu code bằng gì?”

**Trả lời mẫu:** Use case nói mục tiêu actor và chức năng; component nói thành phần mã nguồn/phụ thuộc; deployment nói process, node, artifact và đường kết nối thực thi. Không dùng use case để mô tả tuần tự từng câu lệnh. Đối chiếu component bằng router/service/repository thật, deployment bằng launcher và Vite proxy, không chỉ đọc công nghệ trên hình.

**Mở để chứng minh:** [backend/main.py:37](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/main.py:37>); [frontend/vite.config.js:4](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/vite.config.js:4>); [scripts/start_demo.ps1:17](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/start_demo.ps1:17>); [docs/PRD/DIAGRAMS_REFINED.md:10](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/docs/PRD/DIAGRAMS_REFINED.md:10>).

<a id="phan-b"></a>

## B. Kiến trúc và khả năng lần theo code backend

### Câu 11. Thầy: “Một request từ điện thoại đi đến backend như thế nào?”

**Trả lời mẫu:** Điện thoại vào HTTPS URL của Cloudflare; connector cloudflared trong Docker chuyển request về Vite trên host qua host.docker.internal:3000. Vite trả frontend và proxy /api, /audio về Uvicorn 127.0.0.1:8000. MongoDB, Redis và S3 không được publish ra URL tunnel bằng các proxy này.

**Mở để chứng minh:** [frontend/vite.config.js:4](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/vite.config.js:4>); [scripts/start_demo.ps1:85](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/start_demo.ps1:85>); [scripts/start_demo.ps1:50](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/start_demo.ps1:50>).

### Câu 12. Thầy: “Backend là microservice hay monolith? Có thư mục services thì có phải microservice?”

**Trả lời mẫu:** Đây là modular monolith: main.py đăng ký nhiều router vào cùng app FastAPI. AudioService/AdminNarration là module/class gọi nội bộ, không phải process hay server độc lập. Gọi SeaweedFS và Edge TTS là giao tiếp mạng với dịch vụ khác; MongoDB/Redis là dependency dữ liệu.

**Mở để chứng minh:** [backend/main.py:34](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/main.py:34>); [backend/api/audio.py:115](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/audio.py:115>); [backend/services/audio_storage.py:44](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio_storage.py:44>).

```python
  34 | app = FastAPI(lifespan=lifespan)
  35 | register_exception_handlers(app)
  36 | 
  37 | app.include_router(health_router)
```

### Câu 13. Thầy: “Chỉ đường đi của GET POI, không đọc tên folder.”

**Trả lời mẫu:** main.py đăng ký pois_router. api/pois.py nhận language và inject POIRepository; repository truy vấn POI active, lấy localization cùng ngôn ngữ và dựng POIResponse. Khách chỉ nhận POI có localization phù hợp trong luồng này.

**Mở để chứng minh:** [backend/main.py:38](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/main.py:38>); [backend/api/pois.py:17](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/pois.py:17>); [backend/repositories/poi_repository.py:12](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/repositories/poi_repository.py:12>).

### Câu 14. Thầy: “Schema, router, service, repository khác nhau thế nào trong chính code này?”

**Trả lời mẫu:** Schema mô tả/kiểm tra request-response; router khai báo HTTP và dependency; service xử lý quy tắc như trạng thái task, kiểm tra gói; repository chứa truy vấn dữ liệu. Chưa phải toàn bộ backend đều theo đủ bốn tầng: admin.py và admin_workflow.py còn nhiều nghiệp vụ/truy vấn trực tiếp. Em không vẽ một kiến trúc phân tầng hoàn hảo rồi nhận là code đã đạt.

**Mở để chứng minh:** [backend/schemas/audio.py:40](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/schemas/audio.py:40>); [backend/api/audio.py:145](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/audio.py:145>); [backend/services/audio.py:104](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:104>); [backend/repositories/audio.py:18](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/repositories/audio.py:18>).

### Câu 15. Thầy: “Kết nối MongoDB/Redis có được tạo lại mỗi request không?”

**Trả lời mẫu:** Hai client được khởi tạo trong lifespan và giữ dùng chung qua get_database/get_redis_client; shutdown đóng client. S3 provider cũng được cache theo cấu hình. Điều này tránh tự tạo kết nối mới cho từng câu query, nhưng vẫn phải theo dõi pool khi tăng tải.

**Mở để chứng minh:** [backend/main.py:22](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/main.py:22>); [backend/database/mongodb.py:12](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/database/mongodb.py:12>); [backend/database/redis_client.py:10](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/database/redis_client.py:10>); [backend/api/audio.py:45](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/audio.py:45>).

### Câu 16. Thầy: “GET /health trả healthy có chứng minh DB và S3 đều khỏe không?”

**Trả lời mẫu:** Không. Hàm health_check chỉ trả một dictionary tĩnh. Lifespan có ping MongoDB/Redis nếu được cấu hình lúc khởi động; health hiện tại không kiểm tra liên tục dependency và không đọc thử S3. Đây là liveness đơn giản, chưa phải readiness đầy đủ.

**Mở để chứng minh:** [backend/api/health.py:9](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/health.py:9>); [backend/main.py:25](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/main.py:25>); [backend/config.py:49](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/config.py:49>).

```python
   9 | def health_check() -> Dict[str, str]:
  10 |     return {"status": "healthy"}
```

### Câu 17. Thầy: “Code có async là tự động không chặn server phải không?”

**Trả lời mẫu:** Không. Phải xem bên trong có I/O đồng bộ hoặc xử lý CPU không. Storage adapter dùng asyncio.to_thread cho boto3; kiểm tra ảnh cũng chạy qua to_thread. verify_password dùng scrypt đồng bộ trong luồng login, nên khi tải lớn đó là điểm cần đo và cân nhắc xử lý, không thể nói toàn bộ đã non-blocking.

**Mở để chứng minh:** [backend/services/audio_storage.py:114](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio_storage.py:114>); [backend/api/admin_workflow.py:75](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:75>); [backend/services/admin_auth.py:29](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:29>).

<a id="phan-c"></a>

## C. MongoDB, POI, ERD và toàn vẹn dữ liệu

### Câu 18. Thầy: “ERD có 9 trường POI, document có 22, POI mới khoảng 15. Em giải thích thế nào?”

**Trả lời mẫu:** Có nhiều đường ghi: admin model_dump bổ sung metadata và geometry; seed bổ sung thông tin nguồn, ảnh, giấy phép, tọa độ mô phỏng. Số 9/22/15 là quan sát cần đối chiếu từng field, không phải đặc tả được chứng nhận trong tài liệu này. MongoDB cho phép khác field nhưng điều đó không chứng minh thiết kế đã thống nhất. Cần chốt field bắt buộc/tùy chọn và cập nhật code, seed, ERD theo quyết định đã duyệt.

**Mở để chứng minh:** [backend/api/admin.py:19](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:19>); [backend/api/admin.py:102](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:102>); [scripts/seed_demo_experience.py:121](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/seed_demo_experience.py:121>).

**Không trả lời:** “MongoDB NoSQL nên cấu trúc nào cũng hợp lệ với plan.”

### Câu 19. Thầy: “coordinate_source dùng làm gì, tại sao admin không nhập?”

**Trả lời mẫu:** Seed dùng nó để ghi nguồn tọa độ mô phỏng lớp học. Nó không nằm trong PoiInput hiện tại; endpoint create lại có coordinate_status. Đây là metadata theo đường nhập dữ liệu, cần ghi rõ tùy chọn và mục đích. Nếu bỏ phải tìm các nơi đọc trước; không bắt admin điền thêm chỉ để đủ số field.

**Mở để chứng minh:** [scripts/seed_demo_experience.py:121](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/seed_demo_experience.py:121>); [backend/api/admin.py:19](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:19>); [backend/api/admin.py:103](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:103>).

### Câu 20. Thầy: “name/description trong poi khác title/description trong poi_localizations ra sao?”

**Trả lời mẫu:** POI giữ thông tin hệ thống/chung như phân loại, tọa độ, tên/mô tả hệ thống. Localization giữ tiêu đề và lời thuyết minh cho từng ngôn ngữ, cùng liên kết audio. Public repository lấy title/description từ localization theo ngôn ngữ; admin list còn có fallback mô tả chung để biên tập nên hai API không hoàn toàn giống nhau.

**Mở để chứng minh:** [backend/repositories/poi_repository.py:42](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/repositories/poi_repository.py:42>); [backend/api/admin.py:81](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:81>); [backend/api/admin.py:40](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:40>).

### Câu 21. Thầy: “MongoDB _id là string hay ObjectId? Vì sao JSON lại là string?”

**Trả lời mẫu:** Các _id/tham chiếu chính ở MongoDB dùng BSON ObjectId. JSON response chuyển sang chuỗi hex 24 ký tự; request được validate và đổi lại ObjectId trước truy vấn. Không phải cứ hai chuỗi trông giống nhau là MongoDB sẽ tự match với ObjectId.

**Mở để chứng minh:** [backend/services/audio.py:65](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:65>); [backend/api/admin.py:122](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:122>); [backend/repositories/audio.py:63](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/repositories/audio.py:63>).

**Thầy có thể hỏi tiếp / yêu cầu thử:** Chỉ ra nơi chuyển kiểu trong một endpoint; giải thích 400 khi ID sai định dạng và 404 khi ID đúng nhưng không tồn tại.

### Câu 22. Thầy: “Tại sao một POI không trả về khi chọn ngôn ngữ khác?”

**Trả lời mẫu:** list_for_language chỉ dựng response cho POI có localization của language được yêu cầu. Nó không tự dịch hoặc tự lấy tiếng Việt thay thế. Vì vậy POI active nhưng thiếu localization tiếng Anh có thể không xuất hiện trong danh sách POI tiếng Anh.

**Mở để chứng minh:** [backend/repositories/poi_repository.py:24](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/repositories/poi_repository.py:24>); [backend/repositories/poi_repository.py:54](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/repositories/poi_repository.py:54>).

```python
  24 |                 "language_code": language,
  25 |             },
  26 |             {
  27 |                 "_id": 0,
```

### Câu 23. Thầy: “Tạo POI có tự tạo đủ 6 bản dịch, geofence và audio không?”

**Trả lời mẫu:** Không. Endpoint tạo POI và có thể thêm một initial_localization; không tự tạo sáu ngôn ngữ, vùng hay MP3. Các thao tác geofence/dịch/TTS/phát hành gói là request riêng. is_active=false là giá trị mặc định của PoiCreateInput, không phải lệnh cưỡng chế mọi payload luôn false nếu client chủ động gửi true.

**Mở để chứng minh:** [backend/api/admin.py:59](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:59>); [backend/api/admin.py:98](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:98>); [backend/api/admin_workflow.py:99](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:99>).

**Thầy có thể hỏi tiếp / yêu cầu thử:** Nếu chỉ có poi:write mà gửi initial_localization, endpoint cần kiểm tra thêm quyền gì?

### Câu 24. Thầy: “Tạo POI thành công nhưng thêm bản dịch ban đầu lỗi thì sao?”

**Trả lời mẫu:** Code hiện tạo POI trước, rồi try insert localization; nếu insert lỗi sẽ delete_one POI vừa tạo để bù. Đây là compensation chứ không phải một transaction nguyên tử; nếu process chết hoặc xóa bù lỗi, vẫn có thể còn dữ liệu từng phần. Không nên khẳng định mọi đường ghi đều có transaction.

**Mở để chứng minh:** [backend/api/admin.py:106](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:106>); [backend/api/admin.py:112](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:112>); [tests/test_admin_workflow.py:199](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/tests/test_admin_workflow.py:199>).

### Câu 25. Thầy: “Ràng buộc không cho xóa POI còn phụ thuộc nằm chính xác ở đâu?”

**Trả lời mẫu:** Chưa có ràng buộc RESTRICT đó. deactivate_poi kiểm tra quyền, ID, tồn tại rồi đặt is_active=false. Tham chiếu còn nguyên vì document chưa bị xóa, không phải vì đã quét các collection để chặn xóa. Xóa trực tiếp bằng quyền DB vượt qua code này.

**Mở để chứng minh:** [backend/api/admin.py:130](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:130>); [backend/repositories/poi_repository.py:14](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/repositories/poi_repository.py:14>).

```python
 130 | async def deactivate_poi(poi_id: str, _=Depends(require_permission("poi:write")), db: AsyncDatabase = Depends(get_database)):
 131 |     if not ObjectId.is_valid(poi_id):
 132 |         raise HTTPException(status_code=400, detail="Invalid POI ID")
 133 |     result = await db["poi"].update_one({"_id": ObjectId(poi_id)}, {"$set": {"is_active": False, "updated_at": datetime.now(timezone.utc)}})
```

**Không trả lời:** “Backend có khóa ngoại tự chặn xóa rồi.”

### Câu 26. Thầy: “Ẩn POI có thu hồi được mọi audio, ảnh và bản offline đã phát hành không?”

**Trả lời mẫu:** Không. Public POI list lọc active, nhưng endpoint đọc audio theo asset_id không kiểm tra POI active; ảnh được đọc theo key hợp lệ cũng không kiểm tra trạng thái POI. File offline đã tải ở thiết bị không bị thu hồi bởi việc đổi cờ trên server. Đây là giới hạn cần nói rõ, không coi ẩn POI là xóa/thu hồi toàn bộ tài nguyên.

**Mở để chứng minh:** [backend/services/audio.py:465](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:465>); [backend/api/admin_workflow.py:86](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:86>); [frontend/src/features/offline/audioPackages.js:90](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:90>).

### Câu 27. Thầy: “Cập nhật tọa độ POI có làm lệch tâm geofence không?”

**Trả lời mẫu:** update_poi cập nhật latitude/longitude và GeoJSON rồi update_many các geofence circle để đổi tâm theo. Thứ tự GeoJSON là longitude trước latitude. Hai bước đang là hai lệnh riêng nên không được nói là đã nguyên tử trong một transaction.

**Mở để chứng minh:** [backend/api/admin.py:118](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:118>); [backend/api/admin.py:125](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:125>); [tests/test_audit_regressions.py:54](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/tests/test_audit_regressions.py:54>).

```python
 118 | async def update_poi(poi_id: str, data: PoiInput, _=Depends(require_permission("poi:write")), db: AsyncDatabase = Depends(get_database)):
 119 |     if not ObjectId.is_valid(poi_id):
 120 |         raise HTTPException(status_code=400, detail="Invalid POI ID")
 121 |     values = data.model_dump() | {"updated_at": datetime.now(timezone.utc), "geometry": {"type": "Point", "coordinates": [data.longitude, data.latitude]}}
```

### Câu 28. Thầy: “Tạo vùng geofence có cho gửi tâm tùy ý hoặc bán kính âm không?”

**Trả lời mẫu:** GeofenceInput chỉ nhận radius 5–500 m và is_active; tâm lấy từ tọa độ POI đã lưu. save_geofence kiểm tra POI tồn tại/có tọa độ số rồi upsert circle và cập nhật geofence_enabled. Public geofences hiện chỉ lọc trạng thái vùng và loại circle, chưa tự join để lọc active của POI.

**Mở để chứng minh:** [backend/api/admin_workflow.py:28](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:28>); [backend/api/admin_workflow.py:99](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:99>); [backend/api/geofences.py:10](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/geofences.py:10>).

### Câu 29. Thầy: “unique index có bảo đảm toàn vẹn mọi quan hệ trong database không?”

**Trả lời mẫu:** Không. Commit dịch bảo đảm unique cặp poi_id/language_code để ngăn hai localization trùng khóa nghiệp vụ; nó không kiểm tra tồn tại POI như foreign key. Pydantic chỉ kiểm tra request đi qua model. Code có một số kiểm tra tồn tại/quy tắc ở từng endpoint nhưng không phải bộ khóa ngoại toàn DB.

**Mở để chứng minh:** [backend/api/admin_translation.py:133](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:133>); [backend/schemas/audio.py:27](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/schemas/audio.py:27>); [backend/api/admin.py:146](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:146>).

### Câu 30. Thầy: “Vì sao cần replica set rs0? Một node thì có phải HA không?”

**Trả lời mẫu:** Luồng commit bản dịch dùng transaction và môi trường demo cấu hình rs0. Một replica set chỉ có một member có thể phục vụ transaction nhưng không tạo được khả năng chịu mất máy như nhiều replica trên hạ tầng độc lập. Không nên gọi một container MongoDB là kiến trúc HA.

**Mở để chứng minh:** [backend/api/admin_translation.py:138](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:138>); [scripts/start_demo.ps1:29](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/start_demo.ps1:29>); [docs/CURRENT_ARCHITECTURE.md:72](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/docs/CURRENT_ARCHITECTURE.md:72>).

### Câu 31. Thầy: “Muốn sửa sai lệch ERD mà không phá dữ liệu thì em làm gì?”

**Trả lời mẫu:** Trước hết kiểm kê field theo từng đường ghi và loại document; chốt schema với nhóm/thầy; phân biệt optional/default và dữ liệu lịch sử. Sau đó mới thiết kế migration có backup, dry-run, kiểm tra trước/sau và khả năng phục hồi. Script seed có các guard DB dev/test, nhưng nó không tự là migration chuẩn hóa toàn bộ dữ liệu sản xuất.

**Mở để chứng minh:** [backend/api/admin.py:98](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:98>); [scripts/seed_demo_experience.py:92](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/seed_demo_experience.py:92>); [scripts/seed_dataset.py:252](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/seed_dataset.py:252>); [Rules.md:5](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/Rules.md:5>).

<a id="phan-d"></a>

## D. Audio: truy vấn, storage, manifest và snapshot

### Câu 32. Thầy: “Khách yêu cầu audio POI A tiếng Anh. Em đọc SeaweedFS bằng poi_id ngay à?”

**Trả lời mẫu:** Không. /audio/assets/resolve gọi service/repository tìm localization của POI và ngôn ngữ, đọc audio_url, rồi tìm asset cùng POI/ngôn ngữ/file_url. Sau khi có asset_id, /content lấy metadata và storage.read(file_url). MongoDB xác định đúng bản thu, SeaweedFS giữ bytes MP3.

**Mở để chứng minh:** [backend/api/audio.py:224](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/audio.py:224>); [backend/repositories/audio.py:54](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/repositories/audio.py:54>); [backend/services/audio.py:465](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:465>).

```python
 224 | async def resolve_ready_audio_asset(
 225 |     poi_id: str = Query(...),
 226 |     language_code: str = Query(..., min_length=1),
 227 |     service: AudioService = Depends(get_audio_service),
```

### Câu 33. Thầy: “Task, asset và package khác nhau thế nào? Task Completed là đã nghe được chưa?”

**Trả lời mẫu:** Task mô tả quá trình/trạng thái; asset mô tả bản thu và file; package mô tả nhóm bản thu/ngôn ngữ. Đổi status task sang Completed qua API trạng thái không tự sinh MP3 hoặc asset. Khả năng nghe cần localization liên kết tới asset và file storage thực sự tồn tại.

**Mở để chứng minh:** [backend/services/audio.py:104](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:104>); [backend/schemas/audio.py:89](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/schemas/audio.py:89>); [backend/schemas/audio.py:132](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/schemas/audio.py:132>); [tests/test_audio_api.py:302](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/tests/test_audio_api.py:302>).

### Câu 34. Thầy: “Task có được chuyển từ Completed về Processing không?”

**Trả lời mẫu:** API trạng thái generic dùng TASK_TRANSITIONS: Pending sang Processing/Failed, Processing sang Completed/Failed, hai trạng thái cuối không chuyển sang trạng thái khác. Update có filter trạng thái cũ để phát hiện request đồng thời. Tuy nhiên AdminNarration có luồng cập nhật riêng, không gọi trực tiếp state machine này; phải chỉ đúng đường đang hỏi.

**Mở để chứng minh:** [backend/services/audio.py:28](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:28>); [backend/services/audio.py:104](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:104>); [backend/repositories/audio.py:25](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/repositories/audio.py:25>).

```python
  28 | TASK_TRANSITIONS = {
  29 |     AudioTaskStatus.PENDING: {
  30 |         AudioTaskStatus.PROCESSING,
  31 |         AudioTaskStatus.FAILED,
```

### Câu 35. Thầy: “file_url trong DB có phải URL HTTPS công khai không?”

**Trả lời mẫu:** Trong luồng storage này nó là object key, ví dụ narration/...mp3. Provider từ chối absolute URL/đường dẫn bắt đầu bằng slash khi xử lý key, có thể tạo presigned URL. Visitor hiện thường phát/tải qua endpoint content cùng origin, nên không cần trực tiếp kết nối S3 từ điện thoại.

**Mở để chứng minh:** [backend/services/audio_storage.py:97](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio_storage.py:97>); [backend/services/audio_storage.py:17](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio_storage.py:17>); [frontend/src/features/offline/audioPackages.js:97](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:97>).

### Câu 36. Thầy: “Manifest là file ZIP à? Package file_url trỏ .manifest.json có chắc có object thật?”

**Trả lời mẫu:** Không. get_package_manifest đọc package và các asset thành viên để dựng JSON gồm package/assets/trạng thái toàn vẹn. Với snapshot admin, file_url chỉ là tên metadata manifest; publish_package không upload ZIP hay một object manifest tương ứng. Nơi tải thực tế của client là endpoint manifest rồi content từng asset.

**Mở để chứng minh:** [backend/services/audio.py:162](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:162>); [backend/api/admin_workflow.py:158](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:158>); [frontend/src/features/offline/audioPackages.js:14](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:14>).

### Câu 37. Thầy: “Checksum và size kiểm tra ở đâu, có dùng ETag thay SHA-256 không?”

**Trả lời mẫu:** Provider inspect lấy ContentLength và checksum/sha256 trong metadata, không mặc định coi ETag là SHA-256. Service so metadata với manifest asset; client tính SHA-256 của bytes tải xuống và so kích thước khi có. SHA-256 ở đây phục vụ toàn vẹn nội dung, không phải hash mật khẩu hoặc bằng chứng nguồn file đáng tin tuyệt đối.

**Mở để chứng minh:** [backend/services/audio_storage.py:20](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio_storage.py:20>); [backend/services/audio.py:191](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:191>); [frontend/src/features/offline/audioPackages.js:44](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:44>).

### Câu 38. Thầy: “Manifest unverified có bị chặn tải hoàn toàn không?”

**Trả lời mẫu:** Không. Backend phân biệt invalid, unverified, verified. Client từ chối invalid; unverified hỏi xác nhận tiếp tục bản demo. Client chỉ tính/so SHA-256 khi checksum đúng định dạng 64 hex. Không được nói mọi gói thiếu checksum đều bị chặn tuyệt đối.

**Mở để chứng minh:** [backend/schemas/audio.py:21](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/schemas/audio.py:21>); [backend/services/audio.py:199](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:199>); [frontend/src/features/offline/audioPackages.js:20](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:20>).

### Câu 39. Thầy: “Phát hành snapshot có copy tất cả file MP3 không?”

**Trả lời mẫu:** Không. publish_package lấy các POI active có audio đúng ngôn ngữ, kiểm tra storage rồi copy metadata asset với _id mới, package_id mới, is_snapshot=true. Các metadata có thể cùng tham chiếu một file MP3 bất biến. Sau đó mới tạo package record; lỗi ghi thì có bước xóa metadata snapshot vừa tạo để bù, không phải transaction bao phủ cả S3.

**Mở để chứng minh:** [backend/api/admin_workflow.py:134](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:134>); [backend/api/admin_workflow.py:151](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:151>); [backend/api/admin_workflow.py:161](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:161>).

```python
 134 | async def publish_package(data: PackageInput, _=Depends(require_permission('audio:write')), db=Depends(get_database), storage=Depends(get_audio_storage_provider)):
 135 |     if data.language_code not in VOICES:
 136 |         raise HTTPException(422, 'Unsupported language')
 137 |     pois = await db['poi'].find({'is_active': True}).to_list(length=None)
```

### Câu 40. Thầy: “Sinh giọng mới hoặc tạo QR có sửa gói snapshot cũ không?”

**Trả lời mẫu:** Không theo luồng phát hành mới. TTS tạo key riêng theo task_id; gói cũ giữ metadata tham chiếu key cũ. Snapshot package/asset bị chặn gán lại membership trong assign_asset. QR chỉ định danh POI hoặc package; phát hành gói mới sinh snapshot mới, không nâng cấp âm thầm gói khách đã tải.

**Mở để chứng minh:** [backend/services/admin_narration.py:102](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:102>); [backend/services/audio.py:485](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:485>); [backend/api/admin_workflow.py:139](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:139>); [tests/test_admin_workflow.py:136](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/tests/test_admin_workflow.py:136>).

### Câu 41. Thầy: “Em có thể xóa MP3 cũ sau khi đổi bản dịch để tiết kiệm dung lượng không?”

**Trả lời mẫu:** Không xóa tùy ý vì snapshot khác có thể còn tham chiếu cùng key. Code hiện giữ file/asset cũ; chưa có garbage collector hoàn chỉnh. Muốn dọn cần kiểm tra tất cả tham chiếu và chính sách giữ lịch sử, xử lý lỗi từng bước vì MongoDB và SeaweedFS không cùng transaction.

**Mở để chứng minh:** [backend/services/admin_narration.py:101](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:101>); [backend/api/admin.py:152](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:152>); [docs/ADMIN_POI_WORKFLOW.md:48](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/docs/ADMIN_POI_WORKFLOW.md:48>).

<a id="phan-e"></a>

## E. Offline, QR, GPS — chỉ học ranh giới cần thiết

### Câu 42. Thầy: “Quét QR có nghĩa QR chứa cả nội dung audio và ngôn ngữ không?”

**Trả lời mẫu:** Không. Parser nhận TCV-POI:ObjectId hoặc TCV-PACKAGE:ObjectId. POI QR dùng ngôn ngữ đang chọn để resolve bản thu; package QR định danh gói mà bản thân package có ngôn ngữ. Trang Audio cũng nhận link query package để bắt đầu tải.

**Mở để chứng minh:** [frontend/src/features/offline/audioPackages.js:6](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:6>); [frontend/src/components/views/ExploreView.jsx:68](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/components/views/ExploreView.jsx:68>); [frontend/src/components/views/ExploreView.jsx:16](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/components/views/ExploreView.jsx:16>).

```javascript
   6 | export function parseQrPayload(payload) {
   7 |   const match = /^TCV-(PACKAGE|POI):([a-f\d]{24})$/i.exec(String(payload || '').trim());
   8 |   if (!match) throw new Error('Mã QR không đúng định dạng gói audio/POI Thảo Cầm Viên.');
   9 |   return { type: match[1].toUpperCase(), id: match[2].toLowerCase() };
```

### Câu 43. Thầy: “QR có ObjectId đúng định dạng thì chắc POI/package tồn tại chứ?”

**Trả lời mẫu:** Không. Parser chỉ xác nhận cấu trúc payload và 24 hex; backend còn phải tìm document, asset và file. QR giả hợp lệ về cú pháp vẫn có thể trả 404. Một số endpoint kiểm tra tài nguyên khác nhau nên không suy ra toàn bộ referential integrity chỉ từ validation ID.

**Mở để chứng minh:** [frontend/src/features/offline/audioPackages.js:7](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:7>); [backend/services/audio.py:162](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:162>); [backend/services/audio.py:452](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:452>).

### Câu 44. Thầy: “Offline lưu trong MongoDB, Redis hay điện thoại?”

**Trả lời mẫu:** Dữ liệu offline nằm tại thiết bị: IndexedDB giữ gói, Blob audio và metadata/POI snapshot; Service Worker/Cache Storage giữ shell và asset tĩnh. Redis phía server không phải bộ nhớ offline của khách. Server cần online lúc tải, nhưng file đã lưu có thể phát cục bộ.

**Mở để chứng minh:** [frontend/src/db/indexedDB.js:10](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/db/indexedDB.js:10>); [frontend/src/features/offline/audioPackages.js:50](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:50>); [frontend/vite.config.js:24](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/vite.config.js:24>).

### Câu 45. Thầy: “Tải được 8/11 file rồi mất mạng thì có báo gói đã hoàn tất không?”

**Trả lời mẫu:** Client chỉ lưu record package sau vòng tải thành công. Nó nhớ các entry cũ; lỗi/hủy sẽ cố khôi phục entry cũ hoặc xóa entry vừa thêm. Đây là rollback ở logic client với các thao tác khôi phục có catch, không phải cam kết transaction liên store hoàn hảo trong mọi lỗi mất điện/dung lượng.

**Mở để chứng minh:** [frontend/src/features/offline/audioPackages.js:32](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:32>); [frontend/src/features/offline/audioPackages.js:73](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:73>); [frontend/src/features/offline/audioPackages.js:78](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:78>).

### Câu 46. Thầy: “Đổi URL tunnel có mang dữ liệu offline sang không?”

**Trả lời mẫu:** Không tự mang sang. URL host mới tạo origin khác; IndexedDB/Cache Storage của origin cũ có thể vẫn còn nhưng trang origin mới không truy cập như dữ liệu của nó. Phải tải lại ở origin mới hoặc có cơ chế chuyển dữ liệu riêng; hệ thống chưa có cơ chế đó.

**Mở để chứng minh:** [frontend/src/db/indexedDB.js:7](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/db/indexedDB.js:7>); [scripts/start_demo.ps1:91](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/start_demo.ps1:91>); [docs/CURRENT_ARCHITECTURE.md:156](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/docs/CURRENT_ARCHITECTURE.md:156>).

### Câu 47. Thầy: “Mất Internet có còn toàn bộ bản đồ, tự phát GPS, QR, analytics không?”

**Trả lời mẫu:** Chỉ cam kết ở mức đã lưu và đã thử: shell/POI/audio tải trước có thể dùng; OSM tile cần mạng, GPS thật tự phát đang gọi geofence và resolve online. QR POI có thể ưu tiên audio local; analytics không có queue offline bền vững. Việc phát offline không chứng minh toàn bộ hệ thống offline.

**Mở để chứng minh:** [frontend/src/features/map/InteractiveMap.jsx:97](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/map/InteractiveMap.jsx:97>); [frontend/src/features/map/InteractiveMap.jsx:193](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/map/InteractiveMap.jsx:193>); [frontend/src/services/analytics.js:16](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/services/analytics.js:16>); [frontend/src/features/offline/audioPackages.js:90](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:90>).

### Câu 48. Thầy: “Ai xét geofence? Nút mô phỏng chứng minh GPS thật hoạt động không?”

**Trả lời mẫu:** Browser lấy GPS bằng Geolocation và xét khoảng cách Haversine với tâm/bán kính server cung cấp. simulateArrival tự đặt tọa độ giả, phát trong click để phù hợp quyền autoplay; nó chỉ chứng minh đường mô phỏng. GPS thật phụ thuộc thiết bị/quyền/chất lượng vị trí và cần nghiệm thu riêng.

**Mở để chứng minh:** [frontend/src/features/map/useGeolocation.js:68](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/map/useGeolocation.js:68>); [frontend/src/features/map/InteractiveMap.jsx:146](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/map/InteractiveMap.jsx:146>); [frontend/src/features/map/InteractiveMap.jsx:181](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/map/InteractiveMap.jsx:181>); [backend/api/geofences.py:10](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/geofences.py:10>).

### Câu 49. Thầy: “PRD có chống phát lại gần đây. Set POI đã phát có phải cooldown thời gian không?”

**Trả lời mẫu:** Không tương đương. Client dùng triggeredPoisRef và activeGeofenceRef để tránh trigger lặp trong ngữ cảnh hiện tại; đó không phải kiểm tra timestamp đã qua X phút đầy đủ theo PRD. Phải xem các chỗ reset Set khi đổi ngữ cảnh và không báo đã đạt cooldown chỉ vì có Set.

**Mở để chứng minh:** [README.md:234](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/README.md:234>); [frontend/src/features/map/InteractiveMap.jsx:188](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/map/InteractiveMap.jsx:188>); [docs/REQUIREMENTS_TRACEABILITY.md:9](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/docs/REQUIREMENTS_TRACEABILITY.md:9>).

<a id="phan-f"></a>

## F. Đăng nhập, session và phân quyền backend

### Câu 50. Thầy: “Đăng nhập đang dùng JWT hay cookie session? Trình bày toàn luồng.”

**Trả lời mẫu:** Username/password qua auth/login; MongoDB lấy tài khoản active và role; scrypt xác minh hash. Backend tạo token ngẫu nhiên, Redis giữ admin-session:token → user_id 8 giờ, gửi cookie HTTP-only cho browser. Token này là session ID opaque, không phải JWT chứa claims tự xác minh.

**Mở để chứng minh:** [backend/api/admin_auth.py:26](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_auth.py:26>); [backend/services/admin_auth.py:39](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:39>); [backend/services/admin_auth.py:13](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:13>).

```python
  26 | async def login(request: LoginRequest, response: Response):
  27 |     return await login_admin(request.username, request.password, response)
  28 | 
  29 | 
```

### Câu 51. Thầy: “Mật khẩu có lưu plaintext hoặc mã hóa giải ngược không?”

**Trả lời mẫu:** Không theo luồng tạo admin này. hash_password dùng scrypt với salt ngẫu nhiên và lưu chuỗi thuật toán/salt/digest. verify_password tính lại và compare_digest. Không trả password_hash trong response session. Không đọc mật khẩu hoặc secret ra màn hình khi bảo vệ.

**Mở để chứng minh:** [backend/services/admin_auth.py:16](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:16>); [backend/services/admin_auth.py:24](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:24>); [scripts/create_admin.py:19](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/create_admin.py:19>).

```python
  16 | def hash_password(password: str, salt: bytes | None = None) -> str:
  17 |     if len(password) < 12:
  18 |         raise ValueError("Password must contain at least 12 characters")
  19 |     salt = salt or secrets.token_bytes(16)
```

### Câu 52. Thầy: “Đã login thì sao mỗi request vẫn tra Redis và MongoDB?”

**Trả lời mẫu:** require_admin đọc cookie, kiểm tra key Redis còn hạn, lấy lại admin active và role/permissions từ MongoDB. Sau đó require_permission kiểm tra quyền endpoint. Vì vậy xóa session hoặc khóa account phải có tác động ở request sau; việc giao diện còn mở không làm request được quyền tự động.

**Mở để chứng minh:** [backend/services/admin_auth.py:67](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:67>); [backend/services/admin_auth.py:85](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:85>).

**Thầy có thể hỏi tiếp / yêu cầu thử:** Dùng DB thử và tài khoản thử: thu hồi session/quyền rồi gửi lại request, quan sát 401/403; không chỉ nhìn nút trên UI.

### Câu 53. Thầy: “401 và 403 khác nhau thế nào trong dự án?”

**Trả lời mẫu:** 401 thường là chưa có cookie, session hết hạn hoặc account không còn hoạt động. 403 là request đã đi tới kiểm tra quyền nhưng không có permission cần thiết; login cũng có thể 403 khi account chưa được gán role. Các lỗi được handler đưa vào envelope error.code/message/details.

**Mở để chứng minh:** [backend/services/admin_auth.py:69](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:69>); [backend/services/admin_auth.py:87](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:87>); [backend/core/exception_handlers.py:17](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/core/exception_handlers.py:17>).

### Câu 54. Thầy: “Những quyền nào được cấp, đâu kiểm tra thêm quyền khi tạo POI?”

**Trả lời mẫu:** Role administrator do script cấp poi:write, content:write, audio:write, analytics:read. Endpoint tạo POI cần poi:write; nếu kèm initial_localization thì còn cần content:write. Đọc dashboard cần analytics:read, tạo giọng/gói cần audio:write. Đây là permission ứng dụng, khác role của tài khoản MongoDB.

**Mở để chứng minh:** [scripts/create_admin.py:35](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/create_admin.py:35>); [backend/api/admin.py:99](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:99>); [backend/api/admin.py:172](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:172>).

### Câu 55. Thầy: “Cookie HTTP-only đã đủ bảo mật chưa? Secure có luôn bật không?”

**Trả lời mẫu:** HTTP-only ngăn JavaScript đọc cookie, không tự loại bỏ mọi XSS/CSRF. Cookie có SameSite=Lax và Secure phụ thuộc ADMIN_COOKIE_SECURE; launcher đặt theo chế độ tunnel/local. Code chưa có bộ CSRF token riêng để em khẳng định đã hoàn thiện mọi bảo vệ. HTTPS, origin, quyền và kiểm tra request vẫn quan trọng.

**Mở để chứng minh:** [backend/services/admin_auth.py:59](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:59>); [backend/services/admin_auth.py:35](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:35>); [scripts/start_demo.ps1:37](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/start_demo.ps1:37>).

### Câu 56. Thầy: “Logout làm gì? Đóng tab có xóa session server không?”

**Trả lời mẫu:** Logout xóa key session hiện tại ở Redis và xóa cookie. Session có TTL 8 giờ; code không triển khai tự logout server ngay khi đóng tab. require_admin chỉ get key, không gia hạn TTL trong mỗi request, nên đây không phải sliding session mặc định.

**Mở để chứng minh:** [backend/api/admin_auth.py:36](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_auth.py:36>); [backend/services/admin_auth.py:57](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:57>); [backend/services/admin_auth.py:72](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:72>).

### Câu 57. Thầy: “Đổi mật khẩu có làm tất cả phiên cũ bị vô hiệu ngay không?”

**Trả lời mẫu:** Chưa. change_password xác minh mật khẩu hiện tại, hash mật khẩu mới và update admin_users. Không có bước quét/thu hồi mọi admin-session của user. Vì vậy không được khẳng định đổi mật khẩu tự đăng xuất tất cả thiết bị.

**Mở để chứng minh:** [backend/api/admin_auth.py:45](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_auth.py:45>); [backend/services/admin_auth.py:67](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:67>).

### Câu 58. Thầy: “Chống thử mật khẩu đặt ở đâu, nó giới hạn theo IP không?”

**Trả lời mẫu:** login_admin dùng Redis counter theo hash username chuẩn hóa, cửa sổ 60 giây và ngưỡng hơn 10 lần. Đăng nhập thành công xóa counter. Không phải IP-based limiter hoàn chỉnh; nhiều user khác nhau vẫn là các key khác nhau và cần đánh giá chống abuse riêng.

**Mở để chứng minh:** [backend/services/admin_auth.py:41](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:41>); [backend/services/admin_auth.py:45](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:45>).

```python
  41 |     login_key = "admin-login-limit:" + hashlib.sha256(username.strip().lower().encode()).hexdigest()
  42 |     attempts = await redis.incr(login_key)
  43 |     if attempts == 1:
  44 |         await redis.expire(login_key, 60)
```

### Câu 59. Thầy: “Nếu Redis mất dữ liệu thì tài khoản MongoDB có bị mất theo không?”

**Trả lời mẫu:** Không. User/role ở MongoDB vẫn còn, nhưng session Redis bị mất làm cookie cũ không tra được và cần đăng nhập lại. Preview dịch cũng mất, lease và limiter thay đổi. Nếu Redis không kết nối được thì code có thể trả lỗi dependency/500, không luôn là lỗi 401 như trường hợp key không tồn tại.

**Mở để chứng minh:** [backend/services/admin_auth.py:72](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:72>); [backend/api/admin_translation.py:113](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:113>); [backend/database/redis_client.py:26](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/database/redis_client.py:26>).

<a id="phan-g"></a>

## G. Nội dung và dịch: xác nhận, revision, transaction

### Câu 60. Thầy: “Backend có gọi Google Translate không? Nút dịch tất cả làm gì hiện nay?”

**Trả lời mẫu:** Không có lời gọi Cloud Translation trong luồng này. Browser gọi Chrome Translator cho các đích từ click; frontend đồng thời lấy preview nguồn/revision từ backend. Bản hiện tại có nút dịch tất cả và chọn tất cả; vẫn có hàm save/endpoint commit riêng để xác nhận lưu. Tên commit Git chứa one-click không thay thế việc đọc code thực tế.

**Mở để chứng minh:** [frontend/src/components/views/AdminTranslationPanel.jsx:67](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/components/views/AdminTranslationPanel.jsx:67>); [frontend/src/components/views/AdminTranslationPanel.jsx:123](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/components/views/AdminTranslationPanel.jsx:123>); [frontend/src/services/browserTranslation.js:54](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/services/browserTranslation.js:54>); [backend/api/admin_translation.py:76](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:76>).

### Câu 61. Thầy: “Nếu dịch ở browser thì backend còn vai trò gì?”

**Trả lời mẫu:** Backend kiểm tra quyền, POI và nguồn đã lưu; chuẩn bị revision đích, gắn token với admin/POI trong Redis 30 phút. Commit kiểm tra nguồn/revision/xác nhận thay thế và ghi các đích trong transaction. Nó kiểm soát việc lưu nhưng không chứng minh văn bản gửi lên chắc chắn do Chrome sinh ra hoặc dịch đúng nghĩa.

**Mở để chứng minh:** [backend/api/admin_translation.py:65](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:65>); [backend/api/admin_translation.py:82](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:82>); [backend/api/admin_translation.py:109](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:109>).

### Câu 62. Thầy: “Preview chứa bản dịch mới trong Redis chưa?”

**Trả lời mẫu:** Không. Nó giữ nguồn và baseline/revision của các bản đích đã có, cùng user_id/poi_id/provider. Kết quả mới và chỉnh sửa ở state React trước commit. Đóng form/reload có thể mất phần chưa lưu; mô hình Chrome ở profile, không nằm trong Redis hoặc gói audio.

**Mở để chứng minh:** [backend/api/admin_translation.py:102](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:102>); [frontend/src/components/views/AdminTranslationPanel.jsx:12](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/components/views/AdminTranslationPanel.jsx:12>); [backend/api/admin_translation.py:104](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:104>).

### Câu 63. Thầy: “Hai admin cùng dịch một POI, người lưu sau có ghi đè người trước không?”

**Trả lời mẫu:** Luồng commit so revision hiện tại với baseline; khác thì 409. Nguồn được kiểm tra lại trong transaction và ghi translation_guard để gây write conflict khi nguồn đồng thời bị sửa. Unique cặp POI/ngôn ngữ chống tạo hai đích giống khóa. Đây là bảo vệ của luồng commit, không phải mọi thao tác DB ngoài luồng đều tuân thủ tự động.

**Mở để chứng minh:** [backend/services/admin_translation.py:14](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_translation.py:14>); [backend/api/admin_translation.py:147](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:147>); [backend/api/admin_translation.py:142](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:142>).

```python
  14 | def revision(document: dict | None) -> str | None:
  15 |     if document is None:
  16 |         return None
  17 |     return hashlib.sha256(json.dumps([
```

### Câu 64. Thầy: “Có unique index mà dữ liệu đang trùng thì code tự xóa bản trùng không?”

**Trả lời mẫu:** Không. Commit tìm index phù hợp và tạo nếu chưa có; nếu dữ liệu trùng/không đủ quyền/lỗi transaction sẽ trả lỗi không xác nhận lưu. Code yêu cầu kiểm tra dữ liệu và không xóa record để bỏ qua lỗi. Không lấy lỗi index làm lý do dọn DB tùy ý.

**Mở để chứng minh:** [backend/api/admin_translation.py:129](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:129>); [backend/api/admin_translation.py:133](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:133>); [backend/api/admin_translation.py:167](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:167>).

### Câu 65. Thầy: “Một trong năm ngôn ngữ commit lỗi thì bốn ngôn ngữ kia có lưu không?”

**Trả lời mẫu:** Trong cùng request commit, các đích nằm trong một transaction nên lỗi trước khi commit thành công sẽ không lưu riêng bốn đích. Có thể chọn lưu nhóm thành công trước bằng request khác. Nếu mất kết nối lúc xác nhận commit, kết quả có thể chưa biết chắc; code không tự retry mù mà yêu cầu tải lại kiểm tra.

**Mở để chứng minh:** [backend/api/admin_translation.py:138](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:138>); [backend/api/admin_translation.py:168](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:168>); [frontend/src/components/views/AdminTranslationPanel.jsx:125](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/components/views/AdminTranslationPanel.jsx:125>).

### Câu 66. Thầy: “Preview hết hạn hoặc admin B dùng token admin A thì sao?”

**Trả lời mẫu:** Hết key preview trả 409 yêu cầu chuẩn bị lại. Token gắn user và POI; không khớp trả 403. Đích trùng hoặc ngoài danh sách preview trả 422. Retry dịch từng ngôn ngữ không làm backend tự gia hạn preview cũ.

**Mở để chứng minh:** [backend/api/admin_translation.py:114](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:114>); [backend/api/admin_translation.py:119](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:119>); [backend/api/admin_translation.py:121](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_translation.py:121>).

### Câu 67. Thầy: “Sửa lời thuyết minh mà audio cũ vẫn còn thì khách nghe lời nào?”

**Trả lời mẫu:** Khi title/description đổi, save_localization hoặc commit dịch bỏ audio_url/tts_task_id hiện tại, đặt trạng thái stale/draft. Resolve audio dựa liên kết hiện tại nên không tự lấy bản thu cũ bất kỳ. File cũ và snapshot cũ vẫn tồn tại; thay lời không tự tạo TTS mới.

**Mở để chứng minh:** [backend/api/admin.py:150](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:150>); [backend/api/admin.py:152](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:152>); [backend/repositories/audio.py:54](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/repositories/audio.py:54>).

### Câu 68. Thầy: “Lưu nháp là chưa ai thấy phải không? Sửa nguồn có tự sửa bản dịch phụ thuộc không?”

**Trả lời mẫu:** Không có publication state độc lập hoàn chỉnh cho từng localization trong public repository. Nếu POI active và có bản dịch, nội dung đã lưu có thể được đọc ngay, dù response gọi là draft. Sửa nguồn đánh dấu needs_review cho bản dịch phụ thuộc; không tự thay lời hoặc audio đích. Nên giữ POI ẩn trong lúc chuẩn bị.

**Mở để chứng minh:** [backend/api/admin.py:168](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:168>); [backend/repositories/poi_repository.py:12](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/repositories/poi_repository.py:12>); [backend/api/admin.py:166](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:166>).

<a id="phan-h"></a>

## H. TTS: chạy nền, cạnh tranh và thất bại

### Câu 69. Thầy: “Tạo TTS trả 202 nghĩa là file đã có chưa?”

**Trả lời mẫu:** Chưa. Endpoint enqueue tạo task Pending, gắn task vào localization rồi đăng ký BackgroundTasks và trả ID/status. HTTP 202 là nhận xử lý, không phải sinh MP3 thành công. Admin phải theo dõi job status, chờ Completed và nghe thử.

**Mở để chứng minh:** [backend/api/admin_workflow.py:119](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:119>); [backend/services/admin_narration.py:56](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:56>); [backend/api/admin_workflow.py:124](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:124>).

```python
 119 | async def generate_narration(poi_id: str, language: str, data: NarrationInput, background_tasks: BackgroundTasks,
 120 |                              _=Depends(require_permission('audio:write')), db=Depends(get_database),
 121 |                              storage=Depends(get_audio_storage_provider), redis=Depends(get_redis_client)):
 122 |     service = AdminNarration(db, storage, redis)
```

### Câu 70. Thầy: “TTS lấy lời từ request hay lời đã lưu? Tại sao?”

**Trả lời mẫu:** Request NarrationInput chỉ nhận voice tùy chọn. enqueue đọc title/description của localization đã lưu trong MongoDB và snapshot thành source_title/source_text trong task. Điều đó giúp biết tác vụ sinh từ phiên bản nội dung nào, không âm thầm tạo giọng cho văn bản chưa lưu trên UI.

**Mở để chứng minh:** [backend/api/admin_workflow.py:33](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:33>); [backend/services/admin_narration.py:62](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:62>); [backend/services/admin_narration.py:70](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:70>).

### Câu 71. Thầy: “Bấm tạo giọng hai lần liên tiếp thì sao?”

**Trả lời mẫu:** Redis SET NX EX 300 giữ lease theo POI/ngôn ngữ, trùng thì 409. Lease là khóa tạm, không phải job queue bền vững. Unlock dùng Lua so task_id trước khi xóa, tránh một task cũ xóa khóa của task mới. Những ngôn ngữ khác nhau có key khác nhau.

**Mở để chứng minh:** [backend/services/admin_narration.py:66](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:66>); [backend/services/admin_narration.py:67](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:67>); [backend/services/admin_narration.py:85](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:85>).

```python
  66 |         key = f'admin-tts:{poi_id}:{language}'
  67 |         if not await self.redis.set(key, str(task_id), nx=True, ex=300):
  68 |             raise HTTPException(409, 'An audio generation is already running for this language. Retry after it completes.')
  69 |         task = {'_id': task_id, 'poi_id': poi_id, 'language_code': language, 'type': 'TTS', 'status': 'Pending', 'file_url': None,
```

### Câu 72. Thầy: “Đang tạo giọng mà admin sửa lời thì bản giọng cũ có gắn vào lời mới không?”

**Trả lời mẫu:** Generate cập nhật localization với filter gồm POI/ngôn ngữ/task ID/title/description gốc. Nếu nội dung/task hiện tại đổi, matched_count=0 và tác vụ bị đánh lỗi thay vì ghi đè liên kết mới. Nhưng MP3/asset có thể đã được tạo trước khi phát hiện mismatch; code không bảo đảm không còn file dư.

**Mở để chứng minh:** [backend/services/admin_narration.py:94](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:94>); [backend/services/admin_narration.py:77](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:77>); [tests/test_admin_workflow.py:120](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/tests/test_admin_workflow.py:120>).

### Câu 73. Thầy: “Uvicorn bị tắt giữa chừng, mở lại có tự chạy tiếp task không?”

**Trả lời mẫu:** Không có cơ chế resume bền vững. Task chạy trong process FastAPI; dừng cưỡng bức có thể gián đoạn, dừng mềm có thể chờ tùy môi trường. Khi admin truy vấn status, task Pending/Processing cũ hơn 5 phút được đánh Failed để yêu cầu tạo lại; không phải có scheduler tự quét và khôi phục ngay khi restart.

**Mở để chứng minh:** [backend/api/admin_workflow.py:124](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:124>); [backend/services/admin_narration.py:123](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:123>); [backend/services/admin_narration.py:130](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:130>).

### Câu 74. Thầy: “Edge TTS lỗi mạng có treo vô hạn hoặc retry mãi không?”

**Trả lời mẫu:** synthesize thử tối đa hai lần cho một số lỗi tạm, giữa hai lần chờ 1 giây. generate bọc tổng hợp trong wait_for 180 giây; stream có connect/receive timeout, chặn audio quá 20 MiB và file quá nhỏ. Thất bại ghi trạng thái Failed rồi giải phóng lease trong finally, nhưng DB/Redis cũng lỗi thì vẫn cần kiểm tra trạng thái thực tế.

**Mở để chứng minh:** [backend/services/admin_narration.py:23](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:23>); [backend/services/admin_narration.py:99](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:99>); [backend/services/admin_narration.py:42](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:42>).

### Câu 75. Thầy: “Upload S3 thành công rồi MongoDB lỗi thì rollback cả hai được không?”

**Trả lời mẫu:** Không có distributed transaction MongoDB–S3. Generate upload MP3, insert asset rồi cập nhật localization/task; lỗi giữa các bước có thể để lại file/metadata chưa gắn vào nội dung hiện tại. Cần quan sát, retry và cơ chế dọn có kiểm tra tham chiếu; code hiện không chứng minh atomicity xuyên hai hệ lưu trữ.

**Mở để chứng minh:** [backend/services/admin_narration.py:103](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:103>); [backend/services/admin_narration.py:108](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:108>); [backend/services/admin_narration.py:79](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:79>).

### Câu 76. Thầy: “Sao không dùng task generic /audio/tasks là đủ để tạo TTS?”

**Trả lời mẫu:** create_task generic chỉ tạo metadata task Pending; không gọi edge_tts hay BackgroundTasks. Endpoint admin generate-audio mới enqueue nội dung đã lưu và đăng ký thực thi. Hai đường cùng collection nhưng mục đích khác nhau; khi demo phải gọi đúng đường sinh giọng thật.

**Mở để chứng minh:** [backend/services/audio.py:80](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:80>); [backend/api/admin_workflow.py:119](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:119>); [backend/services/admin_narration.py:35](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:35>).

<a id="phan-i"></a>

## I. Analytics: phải hiểu công thức, không chỉ đọc dashboard

### Câu 77. Thầy: “Sự kiện ghi ở admin.py đúng không?”

**Trả lời mẫu:** Không. POST /api/analytics/events trong visitor.py ghi/upsert devices, sessions, events và một số lịch sử. admin.py chỉ có endpoint đọc/tổng hợp dashboard theo quyền analytics:read. Frontend analytics.js phát ID ẩn danh và gửi request.

**Mở để chứng minh:** [backend/api/visitor.py:29](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/visitor.py:29>); [backend/api/admin.py:172](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:172>); [frontend/src/services/analytics.js:16](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/services/analytics.js:16>).

### Câu 78. Thầy: “device_id, session_id, visitor_id có phải cùng một thứ hoặc tài khoản admin không?”

**Trả lời mẫu:** Không. Frontend lưu device_id và visitor_id trong localStorage, session_id trong sessionStorage. Backend chuyển thành ObjectId; session trỏ device và user_id ẩn danh. Không có visitor account đăng nhập tương ứng admin_users; đổi browser/profile/xóa storage có thể sinh định danh khác, nên không đồng nhất với một người thật hoặc một điện thoại vật lý.

**Mở để chứng minh:** [frontend/src/services/analytics.js:19](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/services/analytics.js:19>); [backend/api/visitor.py:48](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/visitor.py:48>); [backend/api/visitor.py:54](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/visitor.py:54>).

```javascript
  19 |       device_id: storedId(localStorage, 'tcv_device_id'),
  20 |       visitor_id: storedId(localStorage, 'tcv_visitor_id'),
  21 |       session_id: storedId(sessionStorage, 'tcv_session_id'),
  22 |       ...event,
```

### Câu 79. Thầy: “Refresh trang có tăng lượt truy cập liên tục không? Visits đếm thế nào?”

**Trả lời mẫu:** Frontend có gửi session_start khi route/ngôn ngữ đổi, nhưng backend upsert theo session_id/event_type cho sự kiện này. Dashboard đếm session_start theo session ID thay vì mọi page_view. sessionStorage thường giữ ID qua reload cùng tab; tab/ngữ cảnh khác có thể là phiên khác. Không gọi visits là số người duy nhất.

**Mở để chứng minh:** [frontend/src/components/layout/PublicLayout.jsx:28](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/components/layout/PublicLayout.jsx:28>); [backend/api/visitor.py:76](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/visitor.py:76>); [backend/api/admin.py:184](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:184>).

### Câu 80. Thầy: “Active được tính bằng heartbeat hay bằng số account đang đăng nhập?”

**Trả lời mẫu:** Aggregation lọc bất kỳ event trong 5 phút gần nhất, lookup session rồi group device_id. Heartbeat ở PublicLayout mỗi phút khi tab visible là một nguồn event, không phải điều kiện duy nhất. Không liên quan trực tiếp số admin session Redis đang còn hạn.

**Mở để chứng minh:** [backend/api/admin.py:177](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:177>); [backend/api/admin.py:193](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:193>); [frontend/src/components/layout/PublicLayout.jsx:33](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/components/layout/PublicLayout.jsx:33>).

```python
 177 |     active_match = {"timestamp": {"$gte": now - timedelta(minutes=5)}}
 178 | 
 179 |     async def aggregate_rows(pipeline: list[dict], limit: int) -> list[dict]:
 180 |         cursor = await events.aggregate(pipeline)
```

### Câu 81. Thầy: “Mở web khách rồi vào admin thì tăng 2 thiết bị không? Vào thẳng admin thì sao?”

**Trả lời mẫu:** Cùng định danh browser thì vẫn một device, không phải hai trang là hai thiết bị. AdminLayout không gửi visitor heartbeat; vào thẳng admin không tự cộng active nếu không có event cũ/nguồn khác. Chuyển từ public sang admin vẫn còn được tính trong cửa sổ 5 phút; dashboard refresh mới phản ánh hết hạn.

**Mở để chứng minh:** [frontend/src/components/layout/PublicLayout.jsx:35](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/components/layout/PublicLayout.jsx:35>); [frontend/src/components/layout/AdminLayout.jsx:7](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/components/layout/AdminLayout.jsx:7>); [backend/api/admin.py:177](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:177>).

### Câu 82. Thầy: “Thống kê ngôn ngữ lấy ngôn ngữ khởi tạo session hay từng sự kiện?”

**Trả lời mẫu:** Biểu đồ ngôn ngữ group data.language_code của một nhóm event trong ngày. Session có ngôn ngữ ban đầu nhưng không dùng nó thay cho mọi hoạt động sau khi người dùng đổi ngôn ngữ. Tên field visits trong kết quả nhóm ngôn ngữ thực chất đang đếm số event đã chọn, không nhất thiết unique session.

**Mở để chứng minh:** [backend/api/visitor.py:61](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/visitor.py:61>); [backend/api/admin.py:210](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:210>); [backend/api/admin.py:212](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:212>).

### Câu 83. Thầy: “Audio completion rate có chắc luôn trong 0–100% và là tỷ lệ người nghe xong không?”

**Trả lời mẫu:** Code lấy số event playback_complete hôm nay chia playback_start hôm nay. Không join từng lượt nghe hoặc cohort; nghe bắt đầu hôm trước, event trùng hoặc client gửi không đầy đủ có thể làm tỷ lệ lệch, thậm chí vượt 100%. Dữ liệu thời gian được nhóm theo UTC, không tự thành ngày Việt Nam.

**Mở để chứng minh:** [backend/api/admin.py:227](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:227>); [backend/api/admin.py:233](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:233>); [backend/api/admin.py:217](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:217>).

### Câu 84. Thầy: “Events có đáng tin như log kiểm toán không? Offline có đồng bộ lại không?”

**Trả lời mẫu:** Không. Endpoint chấp nhận các ID/loại event theo payload, validate cú pháp và giới hạn 120 event/phút theo visitor ID; không chứng thực mỗi lần nghe/GPS thật hay kiểm tra mọi tài nguyên được tham chiếu. Client catch lỗi để không ngắt trải nghiệm, không có hàng đợi đồng bộ offline bền vững. Đây là analytics demo có thiếu/sai số, không phải audit trail chống giả mạo.

**Mở để chứng minh:** [backend/api/visitor.py:15](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/visitor.py:15>); [backend/api/visitor.py:37](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/visitor.py:37>); [frontend/src/services/analytics.js:28](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/services/analytics.js:28>).

<a id="phan-j"></a>

## J. Vận hành, lỗi, kiểm thử và giới hạn kỹ thuật

### Câu 85. Thầy: “Tắt Internet, tắt backend, tắt Redis khác nhau thế nào?”

**Trả lời mẫu:** Mất Internet có thể vẫn truy cập host local nhưng Edge TTS/OSM/tunnel bên ngoài bị ảnh hưởng. Tắt backend làm API ngừng, audio offline đã tải vẫn có thể phát nếu app shell còn mở/cache. Redis lỗi tác động login/session, limiter, preview và lease dù MongoDB còn; không nên gom mọi lỗi thành mất mạng.

**Mở để chứng minh:** [backend/database/redis_client.py:26](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/database/redis_client.py:26>); [backend/services/admin_auth.py:67](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_auth.py:67>); [frontend/src/features/offline/audioPackages.js:90](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:90>); [scripts/start_demo.ps1:37](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/start_demo.ps1:37>).

### Câu 86. Thầy: “Docker chứa gì? Vite/Uvicorn có nằm trong container không?”

**Trả lời mẫu:** Launcher demo mở Vite preview và Uvicorn bằng process trên Windows, còn MongoDB/Redis/SeaweedFS và cloudflared dùng Docker. Frontend build tạo trước khi preview. Port 3000 public qua connector; backend bind loopback 8000. Đây là mô hình demo, chưa có cấu hình production đầy đủ chỉ vì có Docker Desktop.

**Mở để chứng minh:** [scripts/start_demo.ps1:17](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/start_demo.ps1:17>); [scripts/start_demo.ps1:67](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/start_demo.ps1:67>); [scripts/start_demo.ps1:85](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/start_demo.ps1:85>).

### Câu 87. Thầy: “Tại sao điện thoại truy cập HTTP IP LAN lại lỗi camera/GPS?”

**Trả lời mẫu:** Các tính năng browser có yêu cầu quyền và secure context; localhost là trường hợp local đặc biệt, còn điện thoại nên dùng HTTPS tunnel đúng môi trường. HTTPS không tự chứng minh mọi camera/GPS/native translation đều được hỗ trợ. Launcher có QR URL điện thoại nhưng vẫn phải thử quyền trên thiết bị thật.

**Mở để chứng minh:** [scripts/start_demo.ps1:87](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/start_demo.ps1:87>); [frontend/src/features/qr/QrScanner.jsx:5](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/qr/QrScanner.jsx:5>); [frontend/src/features/map/useGeolocation.js:19](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/map/useGeolocation.js:19>).

### Câu 88. Thầy: “Ảnh upload có được kiểm tra ở server hay chỉ tin tên file?”

**Trả lời mẫu:** Server đọc stream chặn trên 5 MiB, Pillow kiểm tra JPEG/PNG/WebP và tối đa 16 triệu pixel; hash nội dung thành tên key. Không chấp nhận SVG chỉ vì đổi đuôi thành jpg. File lưu S3, POI giữ URL API; read_image kiểm tra filename pattern và trả nosniff cùng cache header.

**Mở để chứng minh:** [backend/api/admin_workflow.py:64](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:64>); [backend/api/admin_workflow.py:49](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:49>); [backend/api/admin_workflow.py:95](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:95>).

```python
  64 | async def upload_image(poi_id: str, request: Request, _=Depends(require_permission('poi:write')), db=Depends(get_database), storage=Depends(get_audio_storage_provider)):
  65 |     poi = oid(poi_id)
  66 |     if not await db['poi'].find_one({'_id': poi}):
  67 |         raise HTTPException(404, 'POI not found')
```

### Câu 89. Thầy: “Lỗi trả ra có lộ stack trace hoặc password không?”

**Trả lời mẫu:** Exception handler chuẩn hóa error.code/message/details. Request validation trả 422, lỗi HTTP được ánh xạ, lỗi bất ngờ ghi server log và trả thông báo chung 500. Điều này không chứng minh mọi log/endpoint đều đã được audit secret; khi trình diễn không in env/token, không chia sẻ file cấu hình có credential.

**Mở để chứng minh:** [backend/core/exception_handlers.py:52](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/core/exception_handlers.py:52>); [backend/core/exception_handlers.py:101](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/core/exception_handlers.py:101>); [backend/schemas/common.py:16](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/schemas/common.py:16>).

### Câu 90. Thầy: “Đã có test thì chứng minh đã đạt PRD chưa?”

**Trả lời mẫu:** Chưa. Unit/API test chứng minh điều kiện trong ca đã chạy với dữ liệu/mock tương ứng, không thay camera/GPS thật hoặc nghiệp vụ còn thiếu. Có test audio state, exact-language, concurrency và snapshot; cần báo lệnh, commit, môi trường, kết quả thực chạy. Trong lần soạn tài liệu này em chỉ đọc nguồn test, không tuyên bố suite mới chạy pass.

**Mở để chứng minh:** [tests/test_audio_api.py:451](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/tests/test_audio_api.py:451>); [tests/test_admin_workflow.py:150](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/tests/test_admin_workflow.py:150>); [tests/test_audit_regressions.py:18](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/tests/test_audit_regressions.py:18>); [docs/REQUIREMENTS_TRACEABILITY.md:32](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/docs/REQUIREMENTS_TRACEABILITY.md:32>).

### Câu 91. Thầy: “Backup mỗi MongoDB là đủ mang hệ thống sang máy khác chưa?”

**Trả lời mẫu:** Chưa. MongoDB giữ metadata nhưng MP3/ảnh upload nằm trên SeaweedFS; cần snapshot DB và media nhất quán cùng source/config được bảo vệ. Script backup yêu cầu dừng backend, dump MongoDB và tạm dừng storage để snapshot volume. Model Chrome và bộ offline trong browser không nằm trong backup này.

**Mở để chứng minh:** [scripts/prepare_handoff_backup.py:26](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/prepare_handoff_backup.py:26>); [scripts/prepare_handoff_backup.py:38](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/prepare_handoff_backup.py:38>); [scripts/prepare_handoff_backup.py:61](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/prepare_handoff_backup.py:61>).

### Câu 92. Thầy: “Có file backup rồi có nghĩa chắc chắn khôi phục được?”

**Trả lời mẫu:** Chưa. verify_handoff_backup dựng tài nguyên Docker tạm, restore DB/media rồi so collection counts và size/SHA-256 các asset được kiểm tra. Đó là bằng chứng phục hồi trong phạm vi script khi thực chạy thành công; vẫn cần thử mở ứng dụng, cấu hình môi trường và các dữ liệu khác. Không chạy script backup/restore trực tiếp trong giờ hỏi nếu chưa chuẩn bị vì nó có tác động vận hành.

**Mở để chứng minh:** [scripts/verify_handoff_backup.py:24](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/verify_handoff_backup.py:24>); [scripts/verify_handoff_backup.py:72](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/verify_handoff_backup.py:72>); [scripts/verify_handoff_backup.py:75](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/scripts/verify_handoff_backup.py:75>).

<a id="phan-k"></a>

## K. Hỏi sâu để xem em thật sự đọc code hay chỉ thuộc slide

### Câu 93. Thầy: “Kể một chỗ code gọi nhiều query không cần thiết. Em sửa gì trước?”

**Trả lời mẫu:** list_available_packages lấy packages rồi count_documents riêng từng package; publish_package truy vấn localization/asset theo từng POI. Đây là N+1 có thể giảm bằng query nhóm/aggregation. list_audio_assets và manifest còn inspect storage tuần tự. Phải đo trước/sau, giữ kiểm tra toàn vẹn, không chỉ thêm gather không giới hạn.

**Mở để chứng minh:** [backend/api/audio.py:32](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/audio.py:32>); [backend/api/admin_workflow.py:140](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:140>); [backend/api/admin.py:242](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:242>).

### Câu 94. Thầy: “Hàm tên stream_audio_asset có thật sự stream file từng chunk không?”

**Trả lời mẫu:** Chưa. Provider read gọi Body.read để lấy toàn bộ bytes, service trả tuple và endpoint dùng Response. Tên hàm stream không chứng minh streaming. Khi nhiều người tải file lớn, RAM có thể tăng; cần sửa cả đường đọc storage và response nếu muốn stream thật, không chỉ đổi class response.

**Mở để chứng minh:** [backend/services/audio_storage.py:175](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio_storage.py:175>); [backend/api/audio.py:233](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/audio.py:233>); [backend/services/audio.py:465](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:465>).

```python
 175 |                 return body.read(), response.get("ContentType", "audio/mpeg")
 176 |             finally:
 177 |                 body.close()
 178 | 
```

### Câu 95. Thầy: “Idempotency trong đăng ký audio asset nằm ở đâu?”

**Trả lời mẫu:** AudioService tìm duplicate theo POI/ngôn ngữ/checksum, metadata khớp thì dùng lại, khác thì 409; còn kiểm tra localization có bị trỏ sang audio mới hơn không. Async lock hiện là trong process, không bảo đảm mọi worker/máy đều dùng chung khóa. Transaction/unique constraint phù hợp cần xem riêng, không suy ra distributed idempotency chỉ từ asyncio.Lock.

**Mở để chứng minh:** [backend/services/audio.py:47](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:47>); [backend/services/audio.py:414](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:414>); [backend/services/audio.py:289](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:289>).

### Câu 96. Thầy: “Transaction không hỗ trợ thì code làm gì? Có xóa asset để rollback mọi lỗi không?”

**Trả lời mẫu:** Luồng đăng ký asset generic có fallback compensation khi client không hỗ trợ hoặc lỗi đúng dạng transaction unsupported. Nếu update localization có kết quả không rõ, nó giữ asset để tránh xóa nhầm thứ đã được tham chiếu. Điều này không giống transaction nguyên tử và không áp dụng mặc nhiên cho commit dịch, vốn yêu cầu rs0.

**Mở để chứng minh:** [backend/services/audio.py:264](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:264>); [backend/services/audio.py:339](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:339>); [backend/services/audio.py:435](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:435>); [tests/test_audio_api.py:830](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/tests/test_audio_api.py:830>).

### Câu 97. Thầy: “Em chứng minh không bao giờ có orphan hoặc trạng thái lỗi được không?”

**Trả lời mẫu:** Không nên cam kết tuyệt đối. Create POI/snapshot dùng bù, TTS có nhiều bước MongoDB–S3, các đường ghi trực tiếp vẫn có thể tạo dữ liệu lệch. Em chỉ ra các guard đã có và đề xuất đối soát POI/localization/asset/file cùng cơ chế cleanup có chính sách. Những đề xuất đó chưa phải tính năng đã có.

**Mở để chứng minh:** [backend/api/admin.py:98](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:98>); [backend/api/admin_workflow.py:134](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:134>); [backend/services/admin_narration.py:92](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:92>).

### Câu 98. Thầy: “Nếu em được refactor để code dễ hiểu thì có cần viết lại kiến trúc không?”

**Trả lời mẫu:** Không cần. Em ưu tiên tách nghiệp vụ khỏi hai router admin lớn, gom validation/serialization lặp thật sự, batch query, giữ nguyên hợp đồng HTTP. Với mỗi luồng sửa, kiểm thử quyền, lỗi, trạng thái và dữ liệu. Việc chia nhỏ file không tự là tối ưu nếu tạo nhiều lớp chuyển tiếp không có trách nhiệm.

**Mở để chứng minh:** [backend/api/admin.py:172](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:172>); [backend/api/admin_workflow.py:134](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:134>); [backend/repositories/poi_repository.py:8](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/repositories/poi_repository.py:8>); [Rules.md:10](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/Rules.md:10>).

<a id="phan-l"></a>

## L. Bốn màn bảo vệ tổng hợp

### Câu 99. Thầy: “Cho em 60 giây: mô tả một luồng backend hoàn chỉnh có dữ liệu, quyền và lỗi.”

**Trả lời mẫu:** Em chọn tạo TTS: admin có audio:write gửi poi_id/language/voice; enqueue đọc POI/localization đã lưu, lấy Redis lease và tạo task; trả 202 rồi chạy nền. Edge TTS trả MP3, backend ghi S3 và asset MongoDB, chỉ gắn vào localization nếu task/nội dung còn khớp. Thiếu quyền 403, nội dung chưa có 404, voice sai 422, task trùng 409; lỗi nhà cung cấp dẫn Failed và có thể yêu cầu lại.

**Mở để chứng minh:** [backend/api/admin_workflow.py:119](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin_workflow.py:119>); [backend/services/admin_narration.py:56](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:56>); [backend/services/admin_narration.py:92](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/admin_narration.py:92>).

### Câu 100. Thầy: “Hãy chứng minh một tính năng đạt và một phần PRD chưa đạt ngay bằng code.”

**Trả lời mẫu:** Ví dụ đạt có điều kiện: tải gói kiểm tra SHA-256/size và lưu audio offline, có code manifest và client kiểm bytes. Chưa đạt: nhánh khách thiếu audio tự dùng TTS ở UC-03/04 không tồn tại trong đường resolve, còn UC-10 thiếu heatmap. Em nói rõ phạm vi chứng minh và mở đúng nhánh, không chọn slide thay code.

**Mở để chứng minh:** [frontend/src/features/offline/audioPackages.js:44](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/frontend/src/features/offline/audioPackages.js:44>); [README.md:204](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/README.md:204>); [backend/services/audio.py:452](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:452>); [backend/api/admin.py:172](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/api/admin.py:172>).

### Câu 101. Thầy: “Nếu thầy thay đổi một dữ liệu và ứng dụng sai, em điều tra từ đâu?”

**Trả lời mẫu:** Em xác định endpoint, payload, status/body trong Network trước; kiểm log backend và query theo ID/ngôn ngữ đúng kiểu BSON. Audio kiểm lần lượt localization.audio_url → audio_assets.file_url → object tồn tại → checksum/size; không vội xóa dữ liệu hoặc rerun seed. Ghi lại bước tái hiện và test dùng dữ liệu thử.

**Mở để chứng minh:** [backend/repositories/audio.py:54](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/repositories/audio.py:54>); [backend/services/audio.py:465](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio.py:465>); [backend/services/audio_storage.py:20](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/services/audio_storage.py:20>); [backend/core/exception_handlers.py:105](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/core/exception_handlers.py:105>).

### Câu 102. Thầy: “Phần nào em tự làm và em chứng minh hiểu nó bằng gì?”

**Trả lời mẫu:** Câu này mỗi thành viên phải tự điền trung thực: chức năng mình phụ trách, commit/diff, quyết định thiết kế, lỗi đã xử lý, test đã chạy và giới hạn còn lại. Không có câu trả lời chung thay cho đóng góp thật. Mức hiểu phải đủ để dự đoán kết quả khi đổi một điều kiện trong hàm và chỉ collection bị thay đổi.

**Mở để chứng minh:** [backend/main.py:37](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/backend/main.py:37>); [docs/REQUIREMENTS_TRACEABILITY.md:32](<D:/Program Files (x86)/DULIEUCODE/CNPM/multilingual-guide-services-saigon-zoo/docs/REQUIREMENTS_TRACEABILITY.md:32>).

**Thầy có thể hỏi tiếp / yêu cầu thử:** Tự chọn hai hàm mình sở hữu và giải thích từng điều kiện; không nhận toàn bộ hệ thống là đã tự viết nếu không đúng.

<a id="phan-m"></a>

## M. Kịch bản tập dượt và bảng mở code nhanh

### Một buổi tập 25–30 phút

| Thời gian | Việc cần làm | Bằng chứng |
|---|---|---|
| 0–3 phút | Mở PRD, nói 10 mục tiêu và 3 khoảng cách quan trọng | README + bảng traceability |
| 3–8 phút | POI theo ngôn ngữ, tạo/ẩn, ObjectId, ERD lệch | admin.py + poi_repository.py + seed |
| 8–14 phút | Resolve MP3, manifest, snapshot, file mất | repositories/audio.py + services/audio.py + audio_storage.py |
| 14–19 phút | Login/session/quyền, preview/commit, TTS | admin_auth.py + admin_translation.py + admin_narration.py |
| 19–23 phút | Active, visits, UTC, giới hạn số liệu | visitor.py + analytics_summary |
| 23–30 phút | Mỗi người mở một test, giải thích thất bại và đóng góp cá nhân | tests + git diff/commit thực tế |

### Những phép thử nên chuẩn bị sẵn trên môi trường riêng

| Thử | Kỳ vọng cần giải thích | Ghi chú |
|---|---|---|
| POI active chỉ có tiếng Việt, yêu cầu tiếng Anh | Không được tự dịch/fallback âm thầm trong public POI list | Dùng POI thử |
| Gọi API quản trị chưa login / thiếu quyền | 401 / 403 theo trường hợp | Không chỉ ẩn nút UI |
| Bấm TTS hai lần cùng POI/ngôn ngữ | Lease từ chối trùng | Cần Redis và task đang thực sự chạy |
| Sửa lời trong lúc TTS đang chạy | Không gắn bản thu cũ vào lời mới | Có thể còn file/asset dư; không hứa clean tuyệt đối |
| Phát hành gói rồi tạo lại TTS | Snapshot cũ không tự đổi | So file_url/checksum trước và sau |
| Hai admin preview, một bên sửa trước commit | Commit còn lại từ chối conflict | Dữ liệu dùng một lần, tài khoản thử |
| Tải audio xong ngắt mạng | Phát từ Blob local | Cùng origin/browser, shell đã cache |
| Public rồi admin, chỉ ở admin quá 5 phút | Active hết hạn khi không còn event khác và dashboard refresh | Không dùng tổng active để đoán danh tính một thiết bị |

Không tự chạy các test phá dữ liệu: xóa collection, xóa volume hoặc xóa MP3 đang được nhiều snapshot dùng chung. Muốn chứng minh lỗi file mất, dùng asset/file dùng một lần hoặc test mock có sẵn.

### Từ điển trả lời ngắn

| Thuật ngữ | Nói trong một câu |
|---|---|
| Router | Cửa nhận request HTTP, gắn schema/quyền và gọi xử lý |
| Service | Nơi thực thi quy tắc nghiệp vụ của luồng |
| Repository | Nơi đóng gói truy vấn dữ liệu; code hiện chưa dùng đồng nhất mọi module |
| Schema Pydantic | Hợp đồng/validation request-response, không phải khóa ngoại MongoDB |
| Session | Token opaque ở cookie, ánh xạ user và hạn dùng ở Redis |
| Authentication | Xác định request có phiên/tài khoản hợp lệ |
| Authorization | Kiểm tra quyền thực hiện thao tác |
| Asset | Metadata một bản thu, không phải task và không phải bytes MP3 |
| Manifest | JSON mô tả gói và các asset cần tải |
| Snapshot | Bộ metadata bản thu cố định lúc phát hành; không đóng băng mọi metadata POI |
| Checksum | Giá trị kiểm tra bytes file, không chứng minh bản dịch/giọng là chính xác |
| Lease | Khóa có TTL chống chạy trùng tạm thời, không phải hàng đợi bền vững |
| Transaction | Gom các thay đổi DB trong phạm vi hỗ trợ; không bao gồm S3 và không tự tạo khóa ngoại |
| Soft delete | Đổi trạng thái ẩn, giữ document; khác kiểm tra RESTRICT khi xóa cứng |
| Active | Ước tính browser ID có event trong 5 phút; không phải số người đang ở vườn thú |

### Những câu tuyệt đối tránh khi chưa có bằng chứng

- “Có MongoDB ObjectId nên có khóa ngoại.”
- “DELETE POI đã kiểm tra mọi collection phụ thuộc.”
- “Dịch xong là audio mới tự có.”
- “Redis đang chạy worker TTS.”
- “Gói audio là một ZIP và QR chứa file MP3.”
- “Ẩn POI thu hồi được file đã tải trên điện thoại.”
- “Đổi tunnel vẫn dùng nguyên cache cũ trên URL mới.”
- “Có session_start nghĩa mỗi lần đổi trang thêm một khách.”
- “Có test pass nghĩa tất cả PRD đã hoàn thành.”
- “Dữ liệu ERD không khớp không sao vì MongoDB linh hoạt.”

### Trước khi vào phòng

Chuẩn bị đúng commit, môi trường đã thử, dữ liệu thử, quyền tài khoản và kết quả test thật. Mở sẵn PRD, main.py, admin.py, repositories/audio.py, services/audio.py, services/admin_auth.py, services/admin_narration.py và bảng sai lệch. Ghi rõ phần nào cần Internet, phần nào dùng local; che mọi secret. Khi chưa biết, mở code để xác nhận thay vì đoán.
