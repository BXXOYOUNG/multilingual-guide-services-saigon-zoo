# UC-07 — Đăng nhập quản trị

## Use Case
**UC-07 — Đăng nhập quản trị**

## User
**Quản trị viên**

## Summary
Quản trị viên đăng nhập vào hệ thống quản trị để sử dụng các chức năng quản lý nội dung của hệ thống thuyết minh tự động đa ngôn ngữ. Hệ thống kiểm tra thông tin đăng nhập và chỉ cho phép truy cập khu vực quản trị khi thông tin hợp lệ.

## Basic Course of Events

| Step | User | System |
|------|------|--------|
| 1 | Quản trị viên mở trang đăng nhập quản trị. | Hệ thống hiển thị biểu mẫu đăng nhập. |
| 2 | Quản trị viên nhập thông tin đăng nhập. | Hệ thống tiếp nhận thông tin đăng nhập. |
| 3 | Quản trị viên gửi thông tin đăng nhập. | Hệ thống kiểm tra thông tin đăng nhập. |
| 4 | — | Hệ thống xác thực tài khoản quản trị. |
| 5 | — | Hệ thống tạo phiên đăng nhập cho quản trị viên. |
| 6 | — | Hệ thống chuyển quản trị viên đến khu vực quản trị. |
| 7 | — | Use Case kết thúc. |

## Alternative Path

### A1 — Quản trị viên đã có phiên đăng nhập hợp lệ
1. Quản trị viên truy cập khu vực quản trị.
2. Hệ thống kiểm tra phiên đăng nhập hiện tại.
3. Hệ thống xác định phiên đăng nhập vẫn hợp lệ.
4. Hệ thống không yêu cầu đăng nhập lại.
5. Hệ thống chuyển quản trị viên đến khu vực quản trị.
6. Use Case kết thúc.

## Exception Paths

### E1 — Thông tin đăng nhập không hợp lệ
1. Quản trị viên nhập thông tin đăng nhập.
2. Hệ thống kiểm tra thông tin đăng nhập.
3. Hệ thống xác định thông tin đăng nhập không hợp lệ.
4. Hệ thống thông báo đăng nhập thất bại.
5. Hệ thống yêu cầu quản trị viên nhập lại thông tin đăng nhập.
6. Use Case kết thúc.

### E2 — Không thể thực hiện xác thực
1. Quản trị viên gửi thông tin đăng nhập.
2. Hệ thống không thể hoàn tất quá trình xác thực.
3. Hệ thống thông báo không thể thực hiện đăng nhập.
4. Quản trị viên chưa được truy cập khu vực quản trị.
5. Use Case kết thúc.

## Diagram

```mermaid
flowchart TD
    S([Start]) --> A[Quản trị viên mở trang đăng nhập]
    A --> B{Đã có phiên đăng nhập hợp lệ?}

    %% Alternative Path A1
    B -- Có --> A1[A1: Đã có phiên đăng nhập hợp lệ]
    A1 --> A1A[Không yêu cầu đăng nhập lại]
    A1A --> A1B[Chuyển đến khu vực quản trị]
    A1B --> E([End])

    %% Main Flow
    B -- Không --> C[Hiển thị biểu mẫu đăng nhập]
    C --> D[Quản trị viên nhập thông tin đăng nhập]
    D --> E1{Có thể thực hiện xác thực?}

    %% Exception Path E2
    E1 -- Không --> E2[E2: Không thể thực hiện xác thực]
    E2 --> E2A[Thông báo không thể thực hiện đăng nhập]
    E2A --> X([Use Case kết thúc])

    E1 -- Có --> F[Kiểm tra thông tin đăng nhập]
    F --> G{Thông tin đăng nhập hợp lệ?}

    %% Exception Path E1
    G -- Không --> E3[E1: Thông tin đăng nhập không hợp lệ]
    E3 --> E3A[Thông báo đăng nhập thất bại]
    E3A --> X

    %% Main Flow continued
    G -- Có --> H[Tạo phiên đăng nhập]
    H --> I[Chuyển đến khu vực quản trị]
    I --> E