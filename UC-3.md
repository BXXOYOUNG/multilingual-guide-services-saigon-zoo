# UC-03 — Nhận thuyết minh tự động theo vị trí

## Use Case
**UC-03 — Nhận thuyết minh tự động theo vị trí**

## User
**Người tham quan**

## Summary
Khi người tham quan cho phép hệ thống sử dụng vị trí, hệ thống theo dõi vị trí hiện tại và kiểm tra vị trí đó với các vùng kích hoạt của các điểm thuyết minh (POI). Khi người tham quan đi vào vùng của một POI, hệ thống xác định POI tương ứng và tự động xử lý nội dung thuyết minh để phát cho người tham quan.

## Alternative Path

### A1 — POI có sẵn audio thuyết minh
1. Hệ thống phát hiện người tham quan đi vào vùng của một POI.
2. Hệ thống xác định POI tương ứng.
3. Hệ thống kiểm tra nội dung thuyết minh.
4. Hệ thống tìm thấy audio thuyết minh của POI.
5. Hệ thống phát audio cho người tham quan.

### A2 — POI không có audio, sử dụng TTS
1. Hệ thống phát hiện người tham quan đi vào vùng của một POI.
2. Hệ thống xác định POI tương ứng.
3. Hệ thống kiểm tra nội dung thuyết minh.
4. Hệ thống không tìm thấy audio thuyết minh có sẵn.
5. Hệ thống sử dụng nội dung văn bản để tạo/phát thuyết minh bằng TTS.
6. Hệ thống phát thuyết minh cho người tham quan.

### A3 — Người tham quan rời khỏi vùng của POI
1. Hệ thống phát hiện người tham quan đã rời khỏi vùng của POI.
2. Hệ thống xác định POI không còn nằm trong vùng hoạt động.
3. Hệ thống cập nhật trạng thái POI.
4. Hệ thống không tiếp tục kích hoạt thuyết minh của POI đó.

## Exception Paths

### E1 — Không thể lấy được vị trí người tham quan
1. Hệ thống yêu cầu vị trí hiện tại của người tham quan.
2. Hệ thống không nhận được dữ liệu vị trí hợp lệ.
3. Hệ thống không thể kiểm tra vùng kích hoạt của POI.
4. Hệ thống không tự động phát thuyết minh.
5. Hệ thống thông báo rằng không thể sử dụng chức năng thuyết minh tự động theo vị trí.

### E2 — Không thể lấy nội dung thuyết minh
1. Hệ thống phát hiện người tham quan đi vào vùng của POI.
2. Hệ thống xác định POI cần thuyết minh.
3. Hệ thống không lấy được nội dung thuyết minh cần thiết.
4. Hệ thống không thể phát thuyết minh.
5. Hệ thống thông báo lỗi.

### E3 — POI đã được phát gần đây
1. Hệ thống phát hiện người tham quan đi vào vùng của POI.
2. Hệ thống xác định POI tương ứng.
3. Hệ thống kiểm tra trạng thái/lịch sử phát thuyết minh.
4. Hệ thống xác định POI đã được phát gần đây.
5. Hệ thống không phát lại thuyết minh.
6. Hệ thống tiếp tục theo dõi vị trí của người tham quan.

## Diagram

```mermaid
flowchart TD
    S([Start]) --> A[Người tham quan cho phép sử dụng vị trí]
    A --> B[Hệ thống theo dõi vị trí]
    B --> C{Nhận được vị trí hợp lệ?}

    %% Exception Path E1
    C -- Không --> E1[E1: Không thể lấy vị trí]
    E1 --> E1A[Thông báo không thể sử dụng thuyết minh tự động]
    E1A --> X([Use Case kết thúc])

    %% Main Flow
    C -- Có --> D[Kiểm tra vị trí với các vùng POI]
    D --> E{Người tham quan đi vào vùng POI?}

    E -- Không --> B
    E -- Có --> F[Xác định POI]
    F --> G{POI đã được phát gần đây?}

    %% Exception Path E3
    G -- Có --> E3[E3: POI đã được phát gần đây]
    E3 --> E3A[Không phát lại thuyết minh]
    E3A --> B

    %% Main Flow continued
    G -- Không --> H[Lấy nội dung thuyết minh]
    H --> I{Lấy nội dung thành công?}

    %% Exception Path E2
    I -- Không --> E2[E2: Không thể lấy nội dung thuyết minh]
    E2 --> E2A[Thông báo lỗi]
    E2A --> B

    %% Main Flow continued
    I -- Có --> J{Có audio thuyết minh?}

    %% Alternative Path A1
    J -- Có --> A1[A1: Sử dụng audio có sẵn]
    A1 --> K[Phát audio]

    %% Alternative Path A2
    J -- Không --> A2[A2: Sử dụng TTS]
    A2 --> A2A[Tạo/phát thuyết minh bằng TTS]
    A2A --> K

    K --> L[Ghi nhận trạng thái/lịch sử phát]
    L --> M{Người tham quan rời vùng POI?}

    %% Alternative Path A3
    M -- Có --> A3[A3: Người tham quan rời khỏi vùng POI]
    A3 --> A3A[Cập nhật trạng thái POI]
    A3A --> B

    M -- Không --> B