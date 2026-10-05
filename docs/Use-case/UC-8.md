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
| 2 | Quản trị viên chọn một thao tác quản lý POI. | Hệ thống xác định thao tác được chọn.<br>**Nếu chọn Thêm POI → (A1)**<br>**Nếu chọn Cập nhật POI → (A2)**<br>**Nếu chọn Xóa POI → (A3)** |
| 3 | — | Hệ thống thực hiện luồng tương ứng với thao tác được chọn. |
| 4 | — | Use Case kết thúc. |

## Alternative Path

### A1 — Thêm POI mới
1. Quản trị viên chọn chức năng thêm POI.
2. Hệ thống hiển thị biểu mẫu thêm POI.
3. Quản trị viên nhập thông tin POI mới.
4. Quản trị viên gửi yêu cầu lưu.
5. Hệ thống kiểm tra dữ liệu.
6. **Nếu dữ liệu không hợp lệ → (E1).**
7. Hệ thống tạo POI mới.
8. **Nếu không thể lưu thay đổi → (E2).**
9. Hệ thống cập nhật danh sách POI.
10. Use Case kết thúc.

### A2 — Cập nhật POI
1. Quản trị viên chọn một POI trong danh sách.
2. Quản trị viên chỉnh sửa thông tin POI.
3. Quản trị viên gửi yêu cầu lưu.
4. Hệ thống kiểm tra dữ liệu.
5. **Nếu dữ liệu không hợp lệ → (E1).**
6. Hệ thống cập nhật POI.
7. **Nếu không thể lưu thay đổi → (E2).**
8. Hệ thống cập nhật danh sách POI.
9. Use Case kết thúc.

### A3 — Xóa POI
1. Quản trị viên chọn một POI trong danh sách.
2. Quản trị viên thực hiện thao tác xóa.
3. Hệ thống thực hiện xóa POI.
4. **Nếu không thể xóa POI → (E3).**
5. Hệ thống cập nhật danh sách POI.
6. Use Case kết thúc.

## Exception Paths

### E1 — Dữ liệu POI không hợp lệ
1. Hệ thống phát hiện dữ liệu POI không hợp lệ.
2. Hệ thống thông báo lỗi.
3. Hệ thống không lưu thay đổi.
4. Use Case kết thúc.

### E2 — Không thể lưu thay đổi
1. Hệ thống không thể lưu thay đổi.
2. Hệ thống thông báo lỗi.
3. Thay đổi không được ghi nhận.
4. Use Case kết thúc.

### E3 — Không thể xóa POI
1. Hệ thống không thể hoàn tất thao tác xóa.
2. Hệ thống thông báo lỗi.
3. POI vẫn được giữ trong hệ thống.
4. Use Case kết thúc.

## Diagram

```mermaid
flowchart TD
    S([Start]) --> A[Quản trị viên mở chức năng quản lý POI]
    A --> B[Hệ thống hiển thị danh sách POI]
    B --> C{Quản trị viên chọn thao tác}

    %% Alternative Path A1
    C -- Thêm --> A1[A1: Thêm POI mới]
    A1 --> A1A[Hiển thị biểu mẫu thêm POI]
    A1A --> A1B[Quản trị viên nhập thông tin POI]
    A1B --> A1C[Quản trị viên gửi yêu cầu lưu]
    A1C --> D1[Hệ thống kiểm tra dữ liệu]

    D1 --> F1{Dữ liệu hợp lệ?}

    %% Exception Path E1 - Add
    F1 -- Không --> E1[E1: Dữ liệu POI không hợp lệ]
    E1 --> E1A[Thông báo lỗi]
    E1A --> X([Use Case kết thúc])

    F1 -- Có --> G1[Hệ thống tạo POI mới]
    G1 --> H1{Lưu thay đổi thành công?}

    %% Exception Path E2 - Add
    H1 -- Không --> E2[E2: Không thể lưu thay đổi]
    E2 --> E2A[Thông báo lỗi]
    E2A --> X

    H1 -- Có --> I1[Cập nhật danh sách POI]
    I1 --> Y([End])

    %% Alternative Path A2
    C -- Cập nhật --> A2[A2: Cập nhật POI]
    A2 --> A2A[Quản trị viên chọn POI]
    A2A --> A2B[Quản trị viên chỉnh sửa thông tin POI]
    A2B --> A2C[Quản trị viên gửi yêu cầu lưu]
    A2C --> D2[Hệ thống kiểm tra dữ liệu]

    D2 --> F2{Dữ liệu hợp lệ?}

    %% Exception Path E1 - Update
    F2 -- Không --> E1B[E1: Dữ liệu POI không hợp lệ]
    E1B --> E1C[Thông báo lỗi]
    E1C --> X

    F2 -- Có --> G2[Hệ thống cập nhật POI]
    G2 --> H2{Lưu thay đổi thành công?}

    %% Exception Path E2 - Update
    H2 -- Không --> E2B[E2: Không thể lưu thay đổi]
    E2B --> E2C[Thông báo lỗi]
    E2C --> X

    H2 -- Có --> I2[Cập nhật danh sách POI]
    I2 --> Y

    %% Alternative Path A3
    C -- Xóa --> A3[A3: Xóa POI]
    A3 --> A3A[Quản trị viên chọn POI]
    A3A --> A3B[Quản trị viên thực hiện thao tác xóa]
    A3B --> F3{Xóa thành công?}

    %% Exception Path E3
    F3 -- Không --> E3[E3: Không thể xóa POI]
    E3 --> E3A[Thông báo lỗi]
    E3A --> X

    F3 -- Có --> A3C[Cập nhật danh sách POI]
    A3C --> Y
