# UC-04 — Kích hoạt thuyết minh bằng QR Code

## Use Case
**UC-04 — Kích hoạt thuyết minh bằng QR Code**

## User
**Người tham quan**

## Summary
Người tham quan quét QR Code được gắn tại một điểm thuyết minh trong Thảo Cầm Viên. Hệ thống đọc thông tin từ QR Code, xác định điểm thuyết minh tương ứng và cung cấp nội dung thuyết minh theo ngôn ngữ đã được thiết lập. Chức năng này không yêu cầu sử dụng GPS.

## Basic Course of Events

| Step | User | System |
|------|------|--------|
| 1 | Người tham quan mở chức năng quét QR. | Hệ thống mở chức năng quét QR Code. |
| 2 | Người tham quan đưa camera đến QR Code. | Hệ thống quét và đọc QR Code. |
| 3 | — | Hệ thống xác định điểm thuyết minh tương ứng với QR Code. |
| 4 | — | Hệ thống lấy nội dung thuyết minh theo ngôn ngữ đã được thiết lập. |
| 5 | — | Hệ thống kiểm tra nội dung thuyết minh. |
| 6 | — | Hệ thống phát nội dung thuyết minh cho người tham quan. |
| 7 | — | Use Case kết thúc. |

## Alternative Path

### A1 — Điểm thuyết minh có audio sẵn
1. Hệ thống xác định điểm thuyết minh tương ứng với QR Code.
2. Hệ thống kiểm tra nội dung thuyết minh.
3. Hệ thống tìm thấy audio có sẵn.
4. Hệ thống phát audio cho người tham quan.

### A2 — Điểm thuyết minh chưa có audio sẵn
1. Hệ thống xác định điểm thuyết minh tương ứng với QR Code.
2. Hệ thống kiểm tra nội dung thuyết minh.
3. Hệ thống không tìm thấy audio có sẵn.
4. Hệ thống sử dụng nội dung văn bản để tạo/phát thuyết minh bằng TTS.
5. Hệ thống phát thuyết minh cho người tham quan.

## Exception Paths

### E1 — QR Code không hợp lệ
1. Người tham quan thực hiện quét QR Code.
2. Hệ thống không thể xác định thông tin hợp lệ từ QR Code.
3. Hệ thống thông báo QR Code không hợp lệ.
4. Hệ thống yêu cầu người tham quan thực hiện lại thao tác quét hoặc kết thúc Use Case.

### E2 — Không thể lấy nội dung thuyết minh
1. Hệ thống xác định được điểm thuyết minh từ QR Code.
2. Hệ thống không thể lấy nội dung thuyết minh tương ứng.
3. Hệ thống thông báo không thể tải nội dung thuyết minh.
4. Use Case kết thúc.

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
    D -- Có --> E[Xác định điểm thuyết minh]
    E --> F[Lấy nội dung theo ngôn ngữ đã thiết lập]
    F --> G{Lấy nội dung thành công?}

    %% Exception Path E2
    G -- Không --> E2[E2: Không thể lấy nội dung thuyết minh]
    E2 --> E2A[Thông báo không thể tải nội dung]
    E2A --> X

    %% Main Flow continued
    G -- Có --> H{Có audio thuyết minh sẵn?}

    %% Alternative Path A1
    H -- Có --> A1[A1: Sử dụng audio có sẵn]
    A1 --> I[Phát audio]

    %% Alternative Path A2
    H -- Không --> A2[A2: Sử dụng TTS]
    A2 --> A2A[Tạo/phát thuyết minh bằng TTS]
    A2A --> I

    I --> J([End])