# UC-05 — Tải gói audio thuyết minh offline

## Use Case
**UC-05 — Tải gói audio thuyết minh offline**

## User
**Người tham quan**

## Summary
Người tham quan quét QR Code được cung cấp bởi hệ thống để tải toàn bộ gói audio thuyết minh của Thảo Cầm Viên về thiết bị. Gói audio được tải về và lưu trữ cục bộ trên thiết bị, cho phép người tham quan nghe nội dung thuyết minh mà không cần kết nối Internet.

## Basic Course of Events

| Step | User | System |
|------|------|--------|
| 1 | Người tham quan mở chức năng quét QR. | Hệ thống mở chức năng quét QR Code. |
| 2 | Người tham quan đưa camera đến QR Code tải gói audio. | Hệ thống quét và đọc QR Code. |
| 3 | — | Hệ thống xác định gói audio thuyết minh của Thảo Cầm Viên. |
| 4 | — | Hệ thống kiểm tra trạng thái gói audio trên thiết bị. |
| 5 | — | Hệ thống tải toàn bộ gói audio thuyết minh về thiết bị. |
| 6 | — | Hệ thống lưu gói audio vào bộ nhớ cục bộ. |
| 7 | — | Hệ thống thông báo tải gói audio thành công. |
| 8 | — | Người tham quan có thể sử dụng gói audio để nghe thuyết minh khi không có Internet. |
| 9 | — | Use Case kết thúc. |

## Alternative Path

### A1 — Gói audio đã được tải trước đó
1. Người tham quan quét QR Code.
2. Hệ thống xác định gói audio thuyết minh của Thảo Cầm Viên.
3. Hệ thống kiểm tra dữ liệu đã lưu trên thiết bị.
4. Hệ thống phát hiện gói audio đã tồn tại trên thiết bị.
5. Hệ thống không tải lại gói audio.
6. Hệ thống thông báo gói audio đã có sẵn.
7. Người tham quan có thể sử dụng gói audio để nghe offline.
8. Use Case kết thúc.

## Exception Paths

### E1 — QR Code không hợp lệ
1. Người tham quan thực hiện quét QR Code.
2. Hệ thống không thể xác định gói audio hợp lệ từ QR Code.
3. Hệ thống thông báo QR Code không hợp lệ.
4. Use Case kết thúc.

### E2 — Không thể tải gói audio
1. Hệ thống xác định được gói audio cần tải.
2. Hệ thống bắt đầu tải toàn bộ gói audio.
3. Quá trình tải không thể hoàn thành.
4. Hệ thống thông báo không thể tải gói audio.
5. Hệ thống không đánh dấu gói audio là đã tải hoàn chỉnh.
6. Use Case kết thúc.

### E3 — Không đủ bộ nhớ thiết bị
1. Hệ thống xác định được gói audio cần tải.
2. Hệ thống kiểm tra dung lượng lưu trữ của thiết bị.
3. Hệ thống phát hiện thiết bị không đủ dung lượng.
4. Hệ thống không thực hiện tải gói audio.
5. Hệ thống thông báo không đủ bộ nhớ.
6. Use Case kết thúc.

## Diagram

```mermaid
flowchart TD
    S([Start]) --> A[Người tham quan mở chức năng quét QR]
    A --> B[Đưa camera đến QR Code]
    B --> C[Hệ thống quét và đọc QR Code]

    C --> D{QR Code hợp lệ?}

    %% Exception Path E1
    D -- Không --> E1[E1: QR Code không hợp lệ]
    E1 --> E1A[Thông báo QR Code không hợp lệ]
    E1A --> X([Use Case kết thúc])

    %% Main Flow
    D -- Có --> F[Xác định toàn bộ gói audio của Thảo Cầm Viên]
    F --> G{Gói audio đã tồn tại trên thiết bị?}

    %% Alternative Path A1
    G -- Có --> A1[A1: Gói audio đã được tải trước đó]
    A1 --> A1A[Không tải lại gói audio]
    A1A --> A1B[Thông báo gói audio đã có sẵn]
    A1B --> A1C[Có thể sử dụng gói audio offline]
    A1C --> X

    %% Main Flow continued
    G -- Không --> H[Kiểm tra dung lượng thiết bị]

    H --> I{Đủ dung lượng?}

    %% Exception Path E3
    I -- Không --> E3[E3: Không đủ bộ nhớ thiết bị]
    E3 --> E3A[Thông báo không đủ bộ nhớ]
    E3A --> X

    %% Main Flow continued
    I -- Có --> J[Tải toàn bộ gói audio]

    J --> K{Tải thành công?}

    %% Exception Path E2
    K -- Không --> E2[E2: Không thể tải gói audio]
    E2 --> E2A[Thông báo không thể tải gói audio]
    E2A --> X

    %% Main Flow continued
    K -- Có --> L[Lưu gói audio vào bộ nhớ cục bộ]
    L --> M[Thông báo tải gói audio thành công]
    M --> N[Có thể sử dụng gói audio khi không có Internet]
    N --> E([End])