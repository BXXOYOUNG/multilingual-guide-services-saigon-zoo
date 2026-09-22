# UC-09 — Quản lý nội dung thuyết minh và bản dịch

## Use Case
**UC-09 — Quản lý nội dung thuyết minh và bản dịch**

## User
**Quản trị viên**

## Summary
Quản trị viên quản lý nội dung thuyết minh của các điểm thuyết minh (POI) và nội dung theo từng ngôn ngữ. Hệ thống cho phép cập nhật nội dung văn bản và quản lý audio tương ứng với từng POI và ngôn ngữ. Dữ liệu bản dịch và audio được liên kết với POI và ngôn ngữ tương ứng.

## Basic Course of Events

| Step | User | System |
|------|------|--------|
| 1 | Quản trị viên mở chức năng quản lý nội dung thuyết minh. | Hệ thống hiển thị các POI và nội dung thuyết minh tương ứng. |
| 2 | Quản trị viên chọn một POI. | Hệ thống hiển thị nội dung thuyết minh của POI. |
| 3 | Quản trị viên chọn ngôn ngữ cần quản lý. | Hệ thống hiển thị nội dung theo ngôn ngữ được chọn. |
| 4 | Quản trị viên nhập hoặc cập nhật nội dung thuyết minh. | Hệ thống tiếp nhận nội dung được cập nhật. |
| 5 | Quản trị viên gửi yêu cầu lưu. | Hệ thống lưu nội dung thuyết minh theo POI và ngôn ngữ. |
| 6 | — | Hệ thống xử lý audio tương ứng với nội dung nếu cần. |
| 7 | — | Hệ thống cập nhật nội dung và trạng thái audio. |
| 8 | — | Use Case kết thúc. |

## Alternative Path

### A1 — Thêm hoặc cập nhật nội dung cho một ngôn ngữ
1. Quản trị viên chọn POI.
2. Quản trị viên chọn ngôn ngữ.
3. Quản trị viên nhập hoặc chỉnh sửa nội dung thuyết minh.
4. Hệ thống lưu nội dung theo POI và ngôn ngữ.
5. Hệ thống xử lý audio tương ứng với nội dung.
6. Hệ thống cập nhật trạng thái nội dung và audio.
7. Use Case kết thúc.

### A2 — Quản lý audio có sẵn
1. Quản trị viên chọn POI.
2. Quản trị viên chọn ngôn ngữ.
3. Hệ thống hiển thị audio tương ứng nếu đã có.
4. Quản trị viên thực hiện thao tác quản lý audio.
5. Hệ thống cập nhật thông tin audio tương ứng.
6. Use Case kết thúc.

## Exception Paths

### E1 — Không thể lưu nội dung
1. Quản trị viên gửi yêu cầu lưu nội dung.
2. Hệ thống không thể lưu dữ liệu.
3. Hệ thống thông báo lỗi.
4. Nội dung mới chưa được ghi nhận.
5. Use Case kết thúc.

### E2 — Không thể xử lý audio
1. Hệ thống nhận nội dung thuyết minh cần xử lý audio.
2. Hệ thống thực hiện xử lý audio.
3. Quá trình xử lý audio không hoàn thành.
4. Hệ thống cập nhật trạng thái audio tương ứng.
5. Hệ thống thông báo audio chưa sẵn sàng.
6. Use Case kết thúc.

### E3 — Không tìm thấy nội dung theo POI và ngôn ngữ
1. Quản trị viên chọn POI và ngôn ngữ.
2. Hệ thống không tìm thấy nội dung tương ứng.
3. Hệ thống thông báo chưa có nội dung cho POI và ngôn ngữ được chọn.
4. Quản trị viên có thể thực hiện thêm nội dung mới.

## Diagram

```mermaid
flowchart TD
    S([Start]) --> A[Quản trị viên mở quản lý nội dung thuyết minh]
    A --> B[Hiển thị danh sách POI]
    B --> C[Quản trị viên chọn POI]
    C --> D[Quản trị viên chọn ngôn ngữ]

    D --> E{Có nội dung theo POI và ngôn ngữ?}

    %% Exception Path E3
    E -- Không --> E3[E3: Không tìm thấy nội dung]
    E3 --> E3A[Thông báo chưa có nội dung]
    E3A --> E3B[Quản trị viên có thể thêm nội dung]
    E3B --> F

    %% Main Flow
    E -- Có --> F[Hiển thị nội dung thuyết minh]

    F --> G{Chọn thao tác}

    %% Alternative Path A1
    G -- Thêm/Cập nhật nội dung --> A1[A1: Thêm hoặc cập nhật nội dung]
    A1 --> A1A[Nhập hoặc chỉnh sửa nội dung]
    A1A --> H[Lưu nội dung]

    %% Alternative Path A2
    G -- Quản lý audio --> A2[A2: Quản lý audio có sẵn]
    A2 --> A2A[Hiển thị audio tương ứng]
    A2A --> A2B[Quản trị viên thực hiện thao tác quản lý audio]
    A2B --> I{Cập nhật audio thành công?}

    I -- Không --> E2[E2: Không thể xử lý audio]
    E2 --> E2A[Cập nhật trạng thái audio chưa sẵn sàng]
    E2A --> E2B[Thông báo audio chưa sẵn sàng]
    E2B --> X([Use Case kết thúc])

    I -- Có --> J[Cập nhật thông tin audio]
    J --> Y([End])

    %% Main Flow continued - Save content
    H --> K{Lưu nội dung thành công?}

    %% Exception Path E1
    K -- Không --> E1[E1: Không thể lưu nội dung]
    E1 --> E1A[Thông báo lỗi]
    E1A --> X

    K -- Có --> L[Cập nhật nội dung theo POI và ngôn ngữ]
    L --> M[Thực hiện xử lý audio nếu cần]

    M --> N{Xử lý audio thành công?}

    %% Exception Path E2
    N -- Không --> E2
    N -- Có --> O[Cập nhật trạng thái nội dung và audio]
    O --> Y