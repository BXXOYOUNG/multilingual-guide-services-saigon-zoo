# UC-08 — Quản lý POI

## Use Case
**UC-08 — Quản lý POI**

## User
**Quản trị viên**

## Summary
Quản trị viên sử dụng chức năng quản lý POI để xem và cập nhật dữ liệu các điểm thuyết minh trong hệ thống. Hệ thống hỗ trợ các thao tác thêm, cập nhật và xóa POI.

## Basic Course of Events

| Step | User | System |
|------|------|--------|
| 1 | Quản trị viên mở chức năng quản lý POI. | Hệ thống hiển thị danh sách các POI. |
| 2 | Quản trị viên chọn một thao tác quản lý POI. | Hệ thống hiển thị giao diện tương ứng với thao tác được chọn. |
| 3 | Quản trị viên nhập hoặc cập nhật thông tin POI. | Hệ thống tiếp nhận dữ liệu POI. |
| 4 | Quản trị viên gửi yêu cầu lưu thay đổi. | Hệ thống kiểm tra dữ liệu POI. |
| 5 | — | Hệ thống lưu thay đổi vào hệ thống. |
| 6 | — | Hệ thống cập nhật danh sách POI. |
| 7 | — | Use Case kết thúc. |

## Alternative Path

### A1 — Thêm POI mới
1. Quản trị viên chọn chức năng thêm POI.
2. Hệ thống hiển thị biểu mẫu thêm POI.
3. Quản trị viên nhập thông tin POI mới.
4. Quản trị viên gửi yêu cầu lưu.
5. Hệ thống kiểm tra dữ liệu.
6. Hệ thống tạo POI mới.
7. Hệ thống cập nhật danh sách POI.
8. Use Case kết thúc.

### A2 — Cập nhật POI
1. Quản trị viên chọn một POI trong danh sách.
2. Quản trị viên chỉnh sửa thông tin POI.
3. Quản trị viên gửi yêu cầu lưu.
4. Hệ thống kiểm tra dữ liệu.
5. Hệ thống cập nhật POI.
6. Hệ thống cập nhật danh sách POI.
7. Use Case kết thúc.

### A3 — Xóa POI
1. Quản trị viên chọn một POI trong danh sách.
2. Quản trị viên thực hiện thao tác xóa.
3. Hệ thống xóa POI.
4. Hệ thống cập nhật danh sách POI.
5. Use Case kết thúc.

## Exception Paths

### E1 — Dữ liệu POI không hợp lệ
1. Quản trị viên nhập hoặc cập nhật thông tin POI.
2. Hệ thống kiểm tra dữ liệu.
3. Hệ thống phát hiện dữ liệu không hợp lệ.
4. Hệ thống thông báo lỗi.
5. Hệ thống không lưu thay đổi.
6. Use Case kết thúc.

### E2 — Không thể lưu thay đổi
1. Quản trị viên gửi yêu cầu thêm hoặc cập nhật POI.
2. Hệ thống kiểm tra dữ liệu hợp lệ.
3. Hệ thống không thể lưu thay đổi.
4. Hệ thống thông báo lỗi.
5. Thay đổi không được ghi nhận.
6. Use Case kết thúc.

### E3 — Không thể xóa POI
1. Quản trị viên thực hiện thao tác xóa POI.
2. Hệ thống không thể hoàn tất thao tác xóa.
3. Hệ thống thông báo lỗi.
4. POI vẫn được giữ trong hệ thống.
5. Use Case kết thúc.

## Diagram

```mermaid
flowchart TD
    S([Start]) --> A[Quản trị viên mở chức năng quản lý POI]
    A --> B[Hiển thị danh sách POI]
    B --> C{Chọn thao tác}

    %% Alternative Path A1
    C -- Thêm --> A1[A1: Thêm POI mới]
    A1 --> A1A[Hiển thị biểu mẫu thêm POI]
    A1A --> A1B[Quản trị viên nhập thông tin POI]
    A1B --> D[Kiểm tra dữ liệu]

    %% Alternative Path A2
    C -- Cập nhật --> A2[A2: Cập nhật POI]
    A2 --> A2A[Quản trị viên chọn POI]
    A2A --> A2B[Quản trị viên chỉnh sửa thông tin]
    A2B --> D

    %% Alternative Path A3
    C -- Xóa --> A3[A3: Xóa POI]
    A3 --> A3A[Quản trị viên chọn POI]
    A3A --> A3B[Thực hiện xóa POI]
    A3B --> E{Xóa thành công?}

    %% Exception Path E3
    E -- Không --> E3[E3: Không thể xóa POI]
    E3 --> E3A[Thông báo lỗi]
    E3A --> X([Use Case kết thúc])

    E -- Có --> A3C[Cập nhật danh sách POI]
    A3C --> Y([End])

    %% Main flow for Add / Update
    D --> F{Dữ liệu hợp lệ?}

    %% Exception Path E1
    F -- Không --> E1[E1: Dữ liệu POI không hợp lệ]
    E1 --> E1A[Thông báo lỗi]
    E1A --> X

    F -- Có --> G{Lưu thay đổi thành công?}

    %% Exception Path E2
    G -- Không --> E2[E2: Không thể lưu thay đổi]
    E2 --> E2A[Thông báo lỗi]
    E2A --> X

    G -- Có --> H[Thêm hoặc cập nhật POI]
    H --> I[Cập nhật danh sách POI]
    I --> Y