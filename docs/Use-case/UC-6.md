# UC-06 — Khám phá và nghe thuyết minh offline

## Use Case
**UC-06 — Khám phá và nghe thuyết minh offline**

## User
**Người tham quan**

## Summary
Người tham quan sử dụng chức năng Khám phá để xem các đối tượng thuyết minh trong Thảo Cầm Viên và lựa chọn một đối tượng để nghe nội dung thuyết minh. Hệ thống sử dụng gói audio đã được lưu trên thiết bị từ UC-05, do đó người tham quan có thể nghe thuyết minh mà không cần kết nối Internet.

## Basic Course of Events

| Step | User | System |
|------|------|--------|
| 1 | Người tham quan mở chức năng Khám phá. | Hệ thống hiển thị danh sách các đối tượng có nội dung thuyết minh. |
| 2 | Người tham quan chọn một đối tượng. | Hệ thống xác định đối tượng được chọn. |
| 3 | — | Hệ thống kiểm tra audio thuyết minh tương ứng trong bộ nhớ cục bộ. |
| 4 | — | Hệ thống tìm thấy audio tương ứng. |
| 5 | — | Hệ thống hiển thị thông tin thuyết minh của đối tượng. |
| 6 | Người tham quan chọn nghe thuyết minh. | Hệ thống phát audio từ bộ nhớ cục bộ. |
| 7 | — | Hệ thống tiếp tục phát audio mà không cần kết nối Internet. |
| 8 | — | Use Case kết thúc. |

## Alternative Path

### A1 — Người tham quan chọn đối tượng khác trong danh sách
1. Người tham quan đang xem hoặc nghe một đối tượng.
2. Người tham quan chọn một đối tượng khác.
3. Hệ thống dừng nội dung đang được phát nếu cần.
4. Hệ thống xác định đối tượng mới.
5. Hệ thống kiểm tra audio tương ứng trong bộ nhớ cục bộ.
6. Hệ thống phát audio của đối tượng mới.

## Exception Paths

### E1 — Không tìm thấy audio offline
1. Người tham quan chọn một đối tượng.
2. Hệ thống kiểm tra audio tương ứng trong bộ nhớ cục bộ.
3. Hệ thống không tìm thấy audio.
4. Hệ thống thông báo nội dung thuyết minh của đối tượng chưa có trên thiết bị.
5. Hệ thống không phát thuyết minh offline.
6. Use Case kết thúc.

### E2 — Audio offline không thể phát
1. Người tham quan chọn một đối tượng.
2. Hệ thống tìm thấy audio tương ứng trong bộ nhớ cục bộ.
3. Hệ thống cố gắng phát audio.
4. Hệ thống không thể phát audio.
5. Hệ thống thông báo không thể phát nội dung thuyết minh.
6. Use Case kết thúc.

## Diagram

```mermaid
flowchart TD
    S([Start]) --> A[Người tham quan mở chức năng Khám phá]
    A --> B[Hiển thị danh sách các đối tượng có nội dung thuyết minh]
    B --> C[Người tham quan chọn một đối tượng]
    C --> D[Hệ thống xác định đối tượng được chọn]
    D --> E[Kiểm tra audio trong bộ nhớ cục bộ]

    E --> F{Tìm thấy audio offline?}

    %% Exception Path E1
    F -- Không --> E1[E1: Không tìm thấy audio offline]
    E1 --> E1A[Thông báo nội dung chưa có trên thiết bị]
    E1A --> X([Use Case kết thúc])

    %% Main Flow
    F -- Có --> G[Hiển thị thông tin thuyết minh]
    G --> H[Người tham quan chọn nghe thuyết minh]
    H --> I[Phát audio từ bộ nhớ cục bộ]

    I --> J{Phát audio thành công?}

    %% Exception Path E2
    J -- Không --> E2[E2: Audio offline không thể phát]
    E2 --> E2A[Thông báo không thể phát nội dung]
    E2A --> X

    %% Main Flow continued
    J -- Có --> K[Tiếp tục phát audio không cần Internet]

    K --> L{Người tham quan chọn đối tượng khác?}

    %% Alternative Path A1
    L -- Có --> A1[A1: Chọn đối tượng khác]
    A1 --> A1A[Dừng nội dung đang phát nếu cần]
    A1A --> A1B[Xác định đối tượng mới]
    A1B --> E

    L -- Không --> M([End])