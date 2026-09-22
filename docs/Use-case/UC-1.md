# UC-01 — Thiết lập ngôn ngữ thuyết minh

## Use Case
**UC-01 — Thiết lập ngôn ngữ thuyết minh**

## User
**Người tham quan**

## Summary
Khi người tham quan mở ứng dụng lần đầu, hệ thống hiển thị màn hình lựa chọn ngôn ngữ. Người tham quan chọn một ngôn ngữ được hệ thống hỗ trợ, sau đó hệ thống lưu lựa chọn và sử dụng ngôn ngữ này làm ngôn ngữ cho nội dung thuyết minh.

## Basic Course of Events

| Step | User | System |
|------|------|--------|
| 1 | Người tham quan mở ứng dụng. | Hệ thống khởi động ứng dụng và kiểm tra ngôn ngữ đã được lưu trên thiết bị. |
| 2 | — | Hệ thống kiểm tra ngôn ngữ đã được lưu.<br>**Nếu đã có ngôn ngữ → (A1)** |
| 3 | — | Hệ thống hiển thị màn hình lựa chọn ngôn ngữ. |
| 4 | Người tham quan chọn một ngôn ngữ. | Hệ thống tiếp nhận ngôn ngữ được chọn. |
| 5 | — | Hệ thống lưu ngôn ngữ đã chọn.<br>**Nếu không thể lưu → (E1)** |
| 6 | — | Hệ thống thiết lập ngôn ngữ đã chọn làm ngôn ngữ thuyết minh. |
| 7 | — | Use Case kết thúc. |

## Alternative Path

### A1 — Người dùng đã có ngôn ngữ được lưu trước đó
1. Người tham quan mở ứng dụng.
2. Hệ thống kiểm tra ngôn ngữ đã được lưu trên thiết bị.
3. Hệ thống tìm thấy ngôn ngữ đã được thiết lập.
4. Hệ thống sử dụng ngôn ngữ đã lưu làm ngôn ngữ thuyết minh.
5. Người tham quan tiếp tục sử dụng ứng dụng mà không cần chọn lại.

## Exception Paths

### E1 — Không thể lưu ngôn ngữ đã chọn
1. Người tham quan chọn ngôn ngữ.
2. Hệ thống không thể lưu lựa chọn ngôn ngữ.
3. Hệ thống thông báo lỗi.
4. Use Case kết thúc mà ngôn ngữ chưa được thiết lập thành công.

## Diagram

```mermaid
flowchart TD
    S([Start]) --> A[Người tham quan mở ứng dụng]

    A --> B{Đã có ngôn ngữ được lưu?}

    %% Main Flow
    B -- Không --> C[Hiển thị màn hình chọn ngôn ngữ]
    C --> D[Người tham quan chọn ngôn ngữ]
    D --> E[Lưu ngôn ngữ đã chọn]

    E --> F{Lưu thành công?}

    F -- Có --> G[Thiết lập ngôn ngữ thuyết minh]
    G --> H([End])

    %% Exception Path E1
    F -- Không --> E1[E1: Thông báo lỗi không thể lưu ngôn ngữ]
    E1 --> X([Use Case kết thúc])

    %% Alternative Path A1
    B -- Có --> A1[A1: Lấy ngôn ngữ đã lưu]
    A1 --> A2[Sử dụng ngôn ngữ đã lưu làm ngôn ngữ thuyết minh]
    A2 --> H
