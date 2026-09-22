# UC-02 — Xem bản đồ và các điểm thuyết minh

## Use Case
**UC-02 — Xem bản đồ và các điểm thuyết minh**

## User
**Người tham quan**

## Summary
Người tham quan sử dụng chức năng bản đồ để xem vị trí của mình và các điểm thuyết minh (POI) trong hệ thống. Hệ thống hiển thị các POI trên bản đồ và có thể làm nổi bật POI gần vị trí hiện tại của người tham quan.

## Basic Course of Events

| Step | User | System |
|------|------|--------|
| 1 | Người tham quan mở chức năng bản đồ. | Hệ thống hiển thị bản đồ và kiểm tra khả năng lấy dữ liệu POI từ máy chủ. |
| 2 | — | Hệ thống kiểm tra dữ liệu POI từ máy chủ.<br>**Nếu dữ liệu POI từ máy chủ khả dụng → tiếp tục bước 3.**<br>**Nếu không khả dụng → (A2)** |
| 3 | — | Hệ thống nhận dữ liệu POI từ máy chủ. |
| 4 | — | Hệ thống hiển thị các POI trên bản đồ. |
| 5 | — | Hệ thống kiểm tra khả năng lấy vị trí GPS của người tham quan.<br>**Nếu GPS không khả dụng → (A1)** |
| 6 | — | Hệ thống lấy vị trí hiện tại của người tham quan. |
| 7 | — | Hệ thống hiển thị vị trí hiện tại của người tham quan trên bản đồ. |
| 8 | — | Hệ thống xác định và highlight POI gần nhất. |
| 9 | — | Use Case kết thúc. |

## Alternative Path

### A1 — Không có vị trí GPS
1. Người tham quan mở chức năng bản đồ.
2. Hệ thống tải và hiển thị bản đồ.
3. Hệ thống hiển thị các POI.
4. Hệ thống không hiển thị vị trí hiện tại của người tham quan.
5. Hệ thống không thực hiện xác định POI gần nhất dựa trên vị trí hiện tại.

### A2 — Sử dụng dữ liệu POI đã lưu offline
1. Hệ thống không lấy được dữ liệu POI mới từ máy chủ.
2. Hệ thống kiểm tra dữ liệu POI đã được lưu trên thiết bị.
3. Hệ thống sử dụng dữ liệu POI cục bộ.
4. Hệ thống hiển thị các POI trên bản đồ.

## Exception Paths

### E1 — Không có dữ liệu POI khả dụng
1. Hệ thống không lấy được dữ liệu POI từ máy chủ.
2. Hệ thống không tìm thấy dữ liệu POI đã lưu trên thiết bị.
3. Hệ thống thông báo không thể tải dữ liệu POI.
4. Chức năng hiển thị POI kết thúc.

## Diagram

```mermaid
flowchart TD
    S([Start]) --> A[Người tham quan mở chức năng bản đồ]
    A --> B[Hiển thị bản đồ]

    B --> C{Dữ liệu POI từ máy chủ khả dụng?}

    %% Main Flow
    C -- Có --> D[Nhận dữ liệu POI]
    D --> E[Hiển thị các POI trên bản đồ]
    E --> F{GPS khả dụng?}

    F -- Có --> G[Lấy vị trí người tham quan]
    G --> H[Hiển thị vị trí người tham quan]
    H --> I[Highlight POI gần nhất]
    I --> J([End])

    %% Alternative Path A1
    F -- Không --> A1[A1: Không hiển thị vị trí hiện tại]
    A1 --> A2[Không xác định POI gần nhất]
    A2 --> J

    %% Alternative Path A2
    C -- Không --> K{Có dữ liệu POI offline?}

    K -- Có --> A3[A2: Lấy dữ liệu POI đã lưu offline]
    A3 --> E

    %% Exception Path E1
    K -- Không --> E1[E1: Thông báo không thể tải dữ liệu POI]
    E1 --> X([Use Case kết thúc])
