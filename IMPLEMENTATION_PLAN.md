# IMPLEMENTATION PLAN — Hệ thống Thuyết minh Tự động Đa ngôn ngữ Thảo Cầm Viên TP.HCM

> **Status:** Implementation planning
> 
> **Purpose:** Chuyển bộ PRD/thiết kế hiện tại thành kế hoạch triển khai có thể dùng trực tiếp cho coding agent/vibe coding.
> 
> **Scope:** Bám theo 10 Use Case hiện tại, Component Diagram, Deployment Diagram và Logical ERD đã chốt. Không đưa Scrum thành quy trình bắt buộc của đồ án.

---

## 1. Source of Truth

Các tài liệu sau là cơ sở để triển khai:

1. **10 Use Cases** trong `README.md`:
   - UC-01 — Thiết lập ngôn ngữ thuyết minh
   - UC-02 — Xem bản đồ và các điểm thuyết minh
   - UC-03 — Nhận thuyết minh tự động theo vị trí
   - UC-04 — Kích hoạt thuyết minh bằng QR Code
   - UC-05 — Tải gói audio thuyết minh offline
   - UC-06 — Khám phá và nghe thuyết minh offline
   - UC-07 — Đăng nhập quản trị
   - UC-08 — Quản lý POI
   - UC-09 — Quản lý nội dung thuyết minh và bản dịch
   - UC-10 — Xem dữ liệu phân tích
2. **Component Diagram** — kiến trúc PWA + FastAPI + các domain modules + data layer.
3. **Deployment Diagram** — client/PWA, FastAPI backend, MongoDB, Redis, media/object storage, external translation/TTS/map services.
4. **Logical ERD** — các MongoDB collections phục vụ admin, POI/localization, audio, location/playback và analytics.

> **Rule:** Nếu implementation mâu thuẫn với một trong các tài liệu trên, không tự ý sửa architecture. Phải dừng và xác định nguyên nhân trước.

---

## 2. Architecture Decision

### 2.1. Kiểu kiến trúc triển khai

**Modular Monolith**, không triển khai microservices độc lập.

FastAPI là một backend duy nhất; các “Service” trong Component/Deployment Diagram là **domain modules/logical services bên trong cùng backend**.

```text
PWA Client
    |
    | HTTPS / REST API
    v
FastAPI Backend
    |
    +-- API Gateway & Core
    +-- Authentication & RBAC
    +-- Content Service
    +-- Localization Service
    +-- Audio Service
    +-- Map Service
    +-- Location & Geofence Service
    +-- Analytics Service
    +-- Admin Service
    +-- Runtime Location Service
    +-- Data Access Layer
           |
           +-- MongoDB
           +-- Redis
           +-- File / Object Storage
```

**Lý do:** phù hợp quy mô đồ án; giảm độ phức tạp vận hành; vẫn giữ separation of concerns để sau này có thể refactor thành service riêng nếu cần.

---

## 3. Technology Baseline

### Frontend / Client

- React
- Vite
- PWA
- MapLibre GL
- QR Scanner
- HTML5 Audio / audio player của ứng dụng
- Geolocation API
- Service Worker
- IndexedDB
- Cache Storage

### Backend

- Python
- FastAPI
- REST API
- MongoDB driver/ODM theo lựa chọn triển khai
- Redis
- Background task mechanism cho các tác vụ audio nếu cần

### Storage / External Services

- S3-compatible Object Storage hoặc storage adapter tương đương cho audio/static assets
- Translation Service/API bên thứ ba — thông qua adapter, provider cụ thể chưa hard-code trong core domain
- Edge-TTS — dùng cho TTS
- MapLibre + PMTiles cho bản đồ/vector tiles và dữ liệu bản đồ offline

### Deployment / Development

- Docker cho backend và các dependency server-side khi cần
- `.env` / secret management cho credentials
- Git repository

> **Không được tự ý thêm framework/backend/database khác chỉ vì agent “thấy tiện”.**

---

## 4. Functional Scope Mapping

| UC | Chức năng triển khai chính | Module chính |
|---|---|---|
| UC-01 | Chọn/lưu/ngôn ngữ hiện hành | Frontend Localization + Localization Service |
| UC-02 | Bản đồ, POI, GPS, POI gần nhất, fallback offline POI | Map + Location + Offline |
| UC-03 | Geolocation, geofence, auto trigger, audio/TTS, playback history | Location & Geofence + Audio + Runtime Location + Analytics |
| UC-04 | Scan QR → POI → content theo language → audio/TTS | QR Client + Content + Localization + Audio |
| UC-05 | Scan QR → tải toàn bộ audio package → local storage | Audio + Storage + Offline Manager |
| UC-06 | Explore POI → tìm audio local → phát offline | Explorer + Offline Manager + Audio Player |
| UC-07 | Admin login/session/access control | Authentication & RBAC + Admin |
| UC-08 | CRUD POI | Content Service + Admin Service |
| UC-09 | Nội dung đa ngôn ngữ + audio | Localization + Content + Audio |
| UC-10 | Thu thập/tổng hợp/hiển thị analytics | Analytics + Runtime Location |

---

## 5. Data Model Boundary

Logical ERD hiện tại gồm các nhóm collection sau.

### 5.1. Admin / RBAC

- `roles`
- `admin_users`
- `audit_logs`

### 5.2. POI / localization / audio

- `poi`
- `poi_localizations`
- `languages`
- `audio_tasks`
- `audio_packages`
- `audio_assets`

### 5.3. Location / playback

- `location_events`
- `geofence_zones`
- `playback_history`

### 5.4. Analytics / runtime

- `analytics_devices`
- `analytics_sessions`
- `analytics_events`
- `analytics_metrics`
- `runtime_location`

### 5.5. Data-model rules

1. Không thêm collection mới chỉ để giải quyết một vấn đề code nhỏ nếu chưa xác định nó thuộc domain nào.
2. Không đổi tên field/collection đã có trong ERD khi chưa có quyết định rõ ràng.
3. Không tạo public `users` collection chỉ vì cần `user_id` cho analytics/location nếu PRD chưa yêu cầu tài khoản người tham quan.
4. `admin_users` phục vụ khu vực quản trị; visitor-side tracking phải tuân thủ mô hình ẩn danh/thiết bị/session đã được thiết kế.

### 5.6. Audio data mapping (không thay đổi ERD)

Giữ nguyên các collection và field trong Logical ERD. Ánh xạ triển khai thống nhất như sau:

- `audio_tasks` ghi nhận yêu cầu/trạng thái xử lý audio cho POI và ngôn ngữ; task không phải audio có thể phát.
- Khi audio sẵn sàng, `audio_assets` là bản ghi asset có thể phát, gồm tham chiếu POI/ngôn ngữ, vị trí file và metadata theo ERD.
- `poi_localizations.audio_url` là URL/đường dẫn phát của audio sẵn sàng cho đúng POI và ngôn ngữ. Audio Service chịu trách nhiệm duy trì giá trị này theo asset tương ứng; không dùng URL của task hoặc URL của gói thay cho audio của localization.
- `audio_packages` mô tả gói phân phối offline theo ngôn ngữ; `audio_assets` thuộc gói qua `package_id` theo quan hệ ERD. Gói tập hợp các asset để tải offline, không thay thế `poi_localizations.audio_url`.
- API/repository phải phân biệt trạng thái task, asset sẵn sàng và trạng thái gói offline. Không thêm field/collection hoặc đổi quan hệ ERD để thực hiện ánh xạ này.

### 5.7. Required data-contract decisions before implementation

ERD có `user_id` trong dữ liệu visitor tracking/playback nhưng không có Use Case xác thực visitor. Trước khi triển khai các repository/API đụng tới `user_id` trong `location_events`, `playback_history`, `analytics_sessions` (hoặc collection visitor-side tương ứng), cần chốt và ghi nhận quyết định kiến trúc/data-contract về ý nghĩa, nguồn tạo và vòng đời của định danh đó.

- Không được mặc định `user_id` là tài khoản đã đăng nhập.
- Không tạo visitor authentication hoặc `users` collection nếu chưa có yêu cầu được phê duyệt.
- Nếu không thể xác định semantics mà không đổi yêu cầu/ERD, dừng phần repository/API bị ảnh hưởng và xin quyết định; không tự suy diễn.

### 5.8. Pre-coding consistency check

Trước khi code data access layer phải xác nhận cách hiểu của `user_id` xuất hiện trong các collection như `location_events`, `playback_history`, `analytics_sessions`:

- Nếu là định danh ẩn danh của visitor/device/session → ghi rõ trong data contract.
- Nếu là tài khoản người dùng → phải có requirement/ERD tương ứng trước khi triển khai.

**Không tự suy diễn.**

---

## 6. Implementation Order

Không code theo thứ tự “vẽ diagram nào trước thì code module đó trước”. Code theo dependency và theo luồng chạy end-to-end.

```text
0. Project skeleton + environment
        ↓
1. Data access + database initialization
        ↓
2. Backend core + API contracts
        ↓
3. Frontend PWA shell
        ↓
4. Language + POI/content read flow
        ↓
5. Audio domain foundation + shared QR scan/package resolution
        ↓
6. UC-05 package download + UC-06 offline playback
        ↓
7. UC-04 QR narration (reuse shared scanner/payload validation)
        ↓
8. Map + GPS + geofence + auto narration
        ↓
9. Admin authentication + POI/content management
        ↓
10. Analytics
        ↓
11. Integration testing + offline/error hardening
```

UC-05 bắt đầu bằng việc quét QR để nhận diện gói audio. Vì vậy, scanner và payload validation/resolution đủ dùng cho QR gói phải sẵn sàng trước khi tải gói; đây là entry mechanism được UC-05 phê duyệt, không phải entry method mới. UC-04 sau đó bổ sung việc resolve QR sang POI/nội dung thuyết minh và tái sử dụng scanner/validation đã có.

---

# 7. Phase 0 — Project Skeleton

## Goal

Tạo codebase sạch, chạy được frontend và backend độc lập; chưa implement business logic lớn.

## Tasks

- Mở rộng repository hiện có; giữ và dùng lại `backend/api/`, `backend/models/`, `backend/services/`, `docs/`, và `tests/`.
- Chỉ tạo các thư mục/file còn thiếu theo cấu trúc được duyệt; không thay thế, xóa, hoặc di chuyển cấu trúc hiện hữu trong T01.
- Đặt frontend và backend entry/configuration vào cấu trúc thống nhất mà không làm mất các thư mục hiện có.
- Khởi tạo React + Vite frontend.
- Khởi tạo FastAPI backend.
- Thiết lập environment variables.
- Thiết lập lint/format cơ bản.
- Thiết lập Docker cho server-side dependencies nếu sử dụng ngay từ đầu.
- Tạo README dành cho developer.
- Tạo cấu trúc module backend/frontend.

## Exit Criteria

- Frontend chạy được.
- Backend chạy được.
- Health endpoint hoạt động.
- Frontend gọi được health endpoint.
- Không có business feature nào bị nhồi vào file bootstrap/main.

---

# 8. Phase 1 — Data Access Layer + Core Backend

## Goal

Kết nối MongoDB/Redis và tạo backend foundation trước khi xây các use case.

## Tasks

- Database connection lifecycle.
- Collection/index initialization cần thiết.
- Repository/data-access abstraction.
- API error model thống nhất.
- Request validation / response schema.
- Logging cơ bản.
- Authentication/RBAC foundation ở mức shared middleware/module.
- Storage adapter interface cho audio/static files.

## Rule

Domain module không truy cập database một cách tùy tiện từ nhiều chỗ. Truy cập dữ liệu phải đi qua data-access layer đã thống nhất.

## Exit Criteria

- Backend kết nối được MongoDB.
- Redis connection/cache path có thể kiểm tra độc lập.
- Repository mẫu chạy được.
- Có error response nhất quán.
- Có cấu trúc để thêm các domain module mà không sửa `main.py` quá nhiều.

---

# 9. Phase 2 — Frontend PWA Shell

## Goal

Dựng khung client để các feature sau cùng dùng chung navigation/state/offline infrastructure.

## Components

```text
App Shell
├── Router
├── Navigation
├── Language State
├── Network State
├── Audio Player State
├── Offline Manager
├── Notification/Error UI
└── Shared UI components
```

## Tasks

- React Router.
- Public app shell.
- Admin route shell.
- Responsive layout.
- PWA manifest.
- Service Worker skeleton.
- IndexedDB wrapper.
- Cache Storage wrapper.

## Exit Criteria

- App cài được dưới dạng PWA.
- Reload không làm vỡ routing.
- IndexedDB có thể ghi/đọc test data.
- Service Worker được register an toàn.

---

# 10. Phase 3 — Core Visitor Flow: UC-01 + UC-02 + Content Read

## Goal

Tạo luồng visitor cơ bản: mở app → chọn language → tải/đọc danh sách POI → xem bản đồ.

## UC-01

### Implementation

- `LanguageContext` hoặc state module tương đương.
- Lưu language selection ở client.
- Load language đã lưu khi app khởi động.
- Đồng bộ language hiện hành với các request cần localization.

### Acceptance

- First launch yêu cầu chọn language.
- Lần mở tiếp theo dùng language đã lưu.
- Language state được dùng cho content/audio selection.

## UC-02

### Implementation

- POI API.
- POI repository ở client.
- MapLibre initialization.
- POI markers.
- GPS permission/read.
- Highlight POI gần nhất.
- Fallback sang POI data local khi server không khả dụng.

### Acceptance

- Có dữ liệu server → hiển thị POI.
- Không có server nhưng có cache → hiển thị POI local.
- Không có cả hai → hiển thị lỗi phù hợp.
- GPS unavailable → app vẫn có thể xem POI, nhưng không hiển thị current position/nearest POI.

---

# 11. Phase 4 — Audio + Offline Core: UC-05 + UC-06

## Goal

Đây là **core product path** của đồ án: tải gói audio và sử dụng được khi offline.

## 11.1. Audio domain

Implement:

- `audio_tasks`
- `audio_packages`
- `audio_assets`
- Audio metadata API
- Audio URL/storage abstraction
- Audio package manifest
- Package integrity/status handling

Áp dụng ánh xạ tại mục 5.6: `audio_tasks` theo dõi xử lý; `audio_assets` là audio sẵn sàng; `poi_localizations.audio_url` tham chiếu audio theo POI/ngôn ngữ; `audio_packages` gom asset để phân phối offline. Giữ nguyên schema/quan hệ Logical ERD.

## 11.2. UC-05 QR entry prerequisite

Trước khi triển khai download UC-05, hoàn thành scanner, đọc/validate payload và resolve QR tải gói audio đúng theo Use Case. Payload chỉ nhận diện gói audio hiện có. Không đưa package download vào trước scanner/package resolution, và không thay QR entry bằng URL, nút, hay cơ chế khác.

## 11.3. UC-05 — Download Audio Package

### Flow

```text
Scan approved audio-package QR
    ↓
Resolve audio package
    ↓
Check local package
    ↓
Check storage capacity / download availability
    ↓
Download package
    ↓
Verify package/files
    ↓
Persist local metadata + audio
    ↓
Mark package ready
```

### Important

- Package phải có trạng thái rõ ràng: chưa tải / đang tải / hoàn tất / lỗi.
- Không đánh dấu package hoàn tất nếu download thất bại hoặc dữ liệu chưa đầy đủ.
- Có thể retry khi lỗi download.

## 11.4. Offline storage

- IndexedDB: metadata/POI/package state.
- Cache Storage hoặc cơ chế local phù hợp: audio/static resources.
- Service Worker: phục vụ asset đã cache.

## 11.5. UC-06 — Explore + Offline Playback

### Flow

```text
Open Explore
   ↓
List POI / narrated objects
   ↓
Select object
   ↓
Find local audio
   ↓
Show content
   ↓
Play local audio
```

### Acceptance

- Khi audio tồn tại local → phát không cần Internet.
- Khi audio không tồn tại → thông báo rõ, không giả vờ playback thành công.
- Khi audio lỗi → báo lỗi playback.
- Chuyển object → audio hiện tại được xử lý đúng trước khi phát audio mới.

---

# 12. Phase 5 — UC-04 QR Flow

## Goal

Hoàn chỉnh QR-based narration.

## Tasks

- Reuse QR scanner, payload parser, and validation implemented for the UC-05 package QR entry.
- Resolve POI từ QR.
- Resolve localization theo selected language.
- Resolve audio asset.
- Audio playback.
- TTS fallback khi không có audio.

## Rule

QR payload chỉ làm nhiệm vụ định danh/định tuyến đến resource đã có trong hệ thống. Không đưa business data lớn trực tiếp vào QR nếu PRD không yêu cầu.

## Acceptance

- QR hợp lệ → xác định đúng POI.
- QR không hợp lệ → thông báo và không crash.
- Không lấy được content → lỗi rõ ràng.
- Có audio → ưu tiên audio.
- Không có audio → TTS fallback theo UC-04.

> TTS fallback là external/online capability; không được giả định rằng TTS fallback hoạt động offline.

---

# 13. Phase 6 — UC-03 Automatic Narration by Location

## Goal

Triển khai chức năng có tính “đặc trưng” nhất của đề tài: visitor đi vào vùng POI và hệ thống tự động xử lý thuyết minh.

## Components

- Geolocation client
- Location Service
- Geofence data
- Geofence detection engine
- Runtime Location Service
- Audio/ TTS fallback
- Playback history
- Location event logging

## Flow

```text
Permission
   ↓
Start location tracking
   ↓
Validate location
   ↓
Find matching POI/geofence
   ↓
Check recently-played state
   ↓
Resolve content
   ↓
Audio available?
  /       \
 yes       no
  |         |
play      TTS
  \         /
   ↓       ↓
Record playback
   ↓
Continue tracking
```

## Acceptance

- Không có location hợp lệ → không auto-play.
- Không vào geofence → không play.
- POI vừa được phát → không phát lại theo rule trong UC.
- Có audio → dùng audio.
- Không có audio → TTS.
- Rời vùng POI → không tiếp tục trigger POI đó.
- Location/playback events được ghi nhận theo data model.

## Performance rule

Không thực hiện request backend ở mọi GPS sample nếu không cần thiết. Geofence evaluation nên được xử lý client-side ở mức có thể, và chỉ gọi backend khi cần content/event persistence.

---

# 14. Phase 7 — Admin: UC-07 + UC-08 + UC-09

## Goal

Sau khi visitor flow chạy ổn, xây phần quản trị để có dữ liệu thật cho hệ thống.

## UC-07 — Admin Login

Implement:

- Login form.
- Authentication API.
- Session/token handling.
- Protected admin routes.
- Role/permission check.
- Logout.
- Invalid credential handling.

### Decision pending

PRD xác định **admin authentication/session/RBAC**, nhưng chưa khóa cơ chế token/session cụ thể. Đây là quyết định bắt buộc trước khi bắt đầu UC-07: chốt token hay server-managed session, cách lưu/refresh/expire và cách bảo vệ session phù hợp với Deployment Diagram; ghi nhận quyết định trước implementation. Cơ chế phải dùng `admin_users`/`roles` theo ERD, không tạo visitor auth, không làm thay đổi ERD hoặc Deployment Diagram.

Không coi authentication/RBAC foundation ở Phase 1 là lựa chọn cơ chế đã được phê duyệt. Phase 1 chỉ được dựng điểm tích hợp/shared middleware cần thiết; không khóa session mechanism thay cho quyết định này.

## UC-08 — POI Management

CRUD:

- Create POI
- Read/list POI
- Update POI
- Delete POI
- Validate coordinates/basic data
- Active/inactive state
- Geofence-related data

## UC-09 — Content + Localization + Audio

Implement:

- Select POI.
- Select language.
- Create/update localized narration content.
- View localization availability.
- Manage existing audio.
- Trigger/track audio processing where applicable.
- Show audio readiness/status.

### Acceptance

Admin có thể quản lý một POI và nội dung theo từng language mà không phải sửa trực tiếp database.

---

# 15. Phase 8 — UC-10 Analytics

## Goal

Có pipeline tối thiểu từ event → stored data → dashboard.

## Events to support from current design

- Playback-related events.
- Location-related events.
- Session/device information.
- POI interaction events theo mô hình analytics hiện tại.

## Implementation

```text
Client Event
   ↓
Analytics API
   ↓
analytics_events / sessions / devices
   ↓
Aggregation / metrics
   ↓
Analytics UI
```

## Acceptance

- Event có schema rõ ràng.
- Không gửi dữ liệu ngoài scope analytics.
- Admin xem được dữ liệu đã tổng hợp.
- Không để dashboard phụ thuộc vào dữ liệu hard-coded.

---

# 16. Phase 9 — Integration + Hardening

## 16.1. Functional integration

Kiểm tra tối thiểu các chuỗi:

### Flow A — First use

```text
Open App
→ Choose Language
→ View Map / POI
→ Explore
```

### Flow B — Offline

```text
Download Audio Package
→ Disable Internet
→ Explore
→ Play Audio
```

### Flow C — QR

```text
Scan QR
→ Resolve POI
→ Resolve language
→ Play Audio / TTS
```

### Flow D — Automatic narration

```text
Allow GPS
→ Enter geofence
→ Resolve POI
→ Play narration
→ Avoid immediate replay
→ Leave geofence
```

### Flow E — Admin

```text
Admin Login
→ Manage POI
→ Manage localized content
→ Manage audio
→ View analytics
```

## 16.2. Negative cases

Phải test ít nhất:

- Invalid QR.
- No network.
- No cached POI.
- GPS denied/unavailable.
- Invalid login.
- Missing localized content.
- Missing audio.
- TTS unavailable.
- Download interrupted.
- Insufficient local storage.
- Corrupted/unplayable audio.
- Unauthorized admin access.
- Database/service unavailable.

---

# 17. Suggested Repository Structure

```text
project-root/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── localization/
│   │   │   ├── map/
│   │   │   ├── qr/
│   │   │   ├── audio/
│   │   │   ├── explorer/
│   │   │   ├── location/
│   │   │   ├── offline/
│   │   │   ├── admin/
│   │   │   └── analytics/
│   │   ├── services/
│   │   ├── stores/
│   │   ├── db/
│   │   └── sw/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   ├── api/
│   │   ├── modules/
│   │   │   ├── auth/
│   │   │   ├── content/
│   │   │   ├── localization/
│   │   │   ├── audio/
│   │   │   ├── maps/
│   │   │   ├── location/
│   │   │   ├── analytics/
│   │   │   └── admin/
│   │   ├── repositories/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── integrations/
│   │       ├── tts/
│   │       ├── translation/
│   │       └── storage/
│   └── tests/
│
├── docs/
│   ├── PRD/
│   ├── architecture/
│   └── decisions/
│
├── scripts/
├── docker/
├── .env.example
├── README.md
└── IMPLEMENTATION_PLAN.md
```

> Folder names can be adjusted to the final repository convention, but the separation between client, backend modules, data access and external adapters should remain.

---

# 18. Coding Agent Rules

These rules are part of the implementation contract.

## Must

1. Read relevant existing files before modifying them.
2. Follow the approved architecture and ERD.
3. Implement the smallest coherent change for the requested task.
4. Reuse existing abstractions instead of creating duplicates.
5. Validate inputs and handle expected failures.
6. Keep external services behind adapters/interfaces.
7. Keep business logic out of UI components when it belongs to a feature/service layer.
8. After each task, report files changed and remaining issues.
9. Run the relevant tests/build/lint after implementation.
10. Preserve backward compatibility of already working features.

## Must Not

1. Do not invent new business requirements.
2. Do not silently modify the ERD.
3. Do not turn logical modules into separate microservices.
4. Do not replace MongoDB/FastAPI/React without an explicit decision.
5. Do not hard-code external API keys.
6. Do not silently introduce a new auth model that changes the domain model.
7. Do not claim a feature is offline-capable unless it has a local data/resource path.
8. Do not hide errors with fake fallback data in production logic.
9. Do not rewrite large portions of the repository for a small feature.
10. Do not add speculative abstractions “for future scalability”.

---

# 19. Definition of Done for a Coding Task

Một task chỉ được coi là hoàn thành khi:

```text
[ ] Requirement/behavior implemented
[ ] Relevant UI/API/data path works
[ ] Expected errors handled
[ ] Existing behavior not broken
[ ] Relevant test/manual verification completed
[ ] Lint/build passes where applicable
[ ] No unrelated large refactor
[ ] Files changed are reported
[ ] Any assumption/decision is explicitly reported
```

---

# 20. Vibe Coding Workflow

Vibe coding sẽ được thực hiện **task-by-task**, không phải “build toàn bộ hệ thống trong một prompt”.

### Prompt pattern

```text
TASK
Implement <specific feature>.

SOURCE OF TRUTH
- Relevant UC(s)
- Existing architecture
- Existing ERD
- Existing files/components

CONSTRAINTS
- Do not change ERD.
- Do not change architecture.
- Do not invent requirements.
- Reuse existing code.

ACCEPTANCE CRITERIA
- ...

DELIVERABLE
- Code
- Tests/manual verification
- Files changed
- Remaining issues
```

### Recommended task size

Một task nên nhỏ đủ để agent có thể:

1. đọc code liên quan;
2. implement;
3. test;
4. giải thích chính xác những gì đã thay đổi.

Nếu task kéo theo nhiều module và agent bắt đầu tự thiết kế lại kiến trúc, task đó đã quá lớn.

---

# 21. Initial Coding Task Queue

Đây là thứ tự thực tế để bắt đầu vibe coding.

| ID | Task | Depends on | Priority |
|---|---|---|---|
| T01 | Initialize repository structure | — | P0 |
| T02 | Frontend React/Vite shell | T01 | P0 |
| T03 | FastAPI backend shell + health endpoint | T01 | P0 |
| T04 | MongoDB/Redis configuration + connection layer | T03 | P0 |
| T05 | Define API/error/schema conventions | T03 | P0 |
| T06 | PWA/service-worker/indexedDB foundation | T02 | P0 |
| T07 | Language selection + persistence (UC-01) | T02, T06 | P0 |
| T08 | POI API + client repository | T04, T05 | P0 |
| T09 | MapLibre + POI rendering (UC-02) | T08 | P0 |
| T10 | Audio asset/package backend model + APIs | T04, T05 | P0 |
| T13 | Shared QR scanner/payload validation and audio-package QR resolution for UC-05 | T06, T10 | P0; prerequisite to T11 |
| T11 | Audio package local download/storage (UC-05) | T06, T10, T13 | P0 |
| T12 | Explore + offline playback (UC-06) | T09, T11 | P0 |
| T14 | UC-04 POI QR resolution + localized audio/TTS narration | T08, T10, T13 | P1 |
| T15 | Geolocation + geofence detection | T09, T14 | P1 |
| T16 | Automatic narration + playback history (UC-03) | T15 | P1 |
| T17 | Admin auth/RBAC (UC-07) | T04, T05 | P1 |
| T18 | POI CRUD (UC-08) | T17 | P1 |
| T19 | Localization/content management (UC-09) | T17, T18 | P1 |
| T20 | Audio management from admin | T19 | P1 |
| T21 | Analytics event collection | T16, T12 | P2 |
| T22 | Analytics aggregation/dashboard (UC-10) | T21 | P2 |
| T23 | End-to-end integration tests (final integration gate) | T07–T22 | P0 (gate) |
| T24 | Offline/error hardening (final hardening gate) | T23 | P0 (gate) |

> T23/T24 retain P0 as completion/release gates, not as early implementation work. Schedule T23 only after T07–T22 are implemented; schedule T24 only after T23 passes. Their priority does not override these dependencies.

---

# 22. First Coding Milestone

Không cần chờ đến khi toàn bộ hệ thống hoàn thành mới có bản demo.

**Milestone M1 — Visitor Core Demo**

```text
Open App
→ Select Language
→ View POIs / Map
→ Download Audio Package
→ Turn off Internet
→ Explore
→ Play Audio Offline
```

M1 chứng minh được ba ý cốt lõi của đề tài:

- đa ngôn ngữ;
- nội dung thuyết minh theo POI;
- hoạt động offline với audio đã tải.

Sau M1 mới mở rộng QR, auto-location, admin và analytics.

---

# 23. Pre-coding Checklist

Trước khi yêu cầu agent viết code task T01–T06, xác nhận:

```text
[ ] Repository hiện tại đã được xác định
[ ] Frontend stack: React + Vite + PWA
[ ] Backend stack: FastAPI
[ ] Database: MongoDB
[ ] Cache: Redis
[ ] Map: MapLibre + PMTiles
[ ] TTS: Edge-TTS integration adapter
[ ] Translation: external provider adapter, provider cụ thể chưa hard-code
[ ] Storage: storage adapter
[ ] Offline: Service Worker + IndexedDB + Cache Storage
[ ] Không dùng microservices độc lập
[ ] ERD không đổi
[ ] user_id semantics đã được xác nhận
[ ] Auth mechanism đã được quyết định trước khi implement UC-07
```

---

# 24. Immediate Next Step

**Không code toàn hệ thống ngay.**

Bước tiếp theo là thực hiện **T01 — Extend Existing Repository Structure**: bổ sung skeleton còn thiếu và giữ nguyên `backend/api/`, `backend/models/`, `backend/services/`, `docs/`, và `tests/`. Sau đó thực hiện T02–T06.

Trước khi bắt đầu các repository/API visitor-side có `user_id`, phải hoàn tất quyết định tại mục 5.7. Trước khi bắt đầu T17/UC-07, phải chốt cơ chế admin authentication/session tại Phase 7.

Khi skeleton ổn định, bắt đầu vertical slice:

```text
T07 → T08 → T09 → T10 → T13 → T11 → T12
```

Đây là đường đi ngắn nhất để có một phiên bản chạy được của sản phẩm trước khi mở rộng các chức năng phức tạp hơn.
