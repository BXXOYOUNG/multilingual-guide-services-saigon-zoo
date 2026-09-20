# multilingual-guide-services-saigon-zoo

Use case: US1

User: Visitor

Summary: Hệ thống cung cấp dịch vụ thuyết minh tự động đa ngôn ngữ cho khách tham quan thảo cầm viên, sử dụng GPS để tự động phát nội dung thuyết minh tương ứng khi khách tham quan đi vào các khu vực được chỉ định.

| Basic Course of Events | Actor Action                                       | System Response                                                                                                   |
| ---------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
|                        | **1. Visitor mở phần mềm.**                        |                                                                                                                   |
|                        |                                                    | **2. Hệ thống yêu cầu Visitor nhập số điện thoại.**                                                               |
|                        | **3. Visitor nhập số điện thoại.**                 |                                                                                                                   |
|                        |                                                    | **4. Hệ thống kiểm tra tài khoản theo số điện thoại và yêu cầu nhập mã OTP.**                                     |
|                        | **5. Visitor nhập mã OTP.**                        |                                                                                                                   |
|                        |                                                    | **6. Hệ thống xác thực mã OTP và đăng nhập Visitor. E1**                                                          |
|                        |                                                    | **7. Hệ thống hiển thị trang chủ của phần mềm.**                                                                  |
|                        | **8. Visitor lựa chọn ngôn ngữ sử dụng.**          |                                                                                                                   |
|                        |                                                    | **9. Hệ thống cập nhật ngôn ngữ audio được lựa chọn.**                                                            |
|                        |                                                    | **10. Hệ thống yêu cầu Visitor cấp quyền truy cập GPS.**                                                          |
|                        | **11. Visitor cấp quyền truy cập GPS. E2**         |                                                                                                                   |
|                        |                                                    | **12. Hệ thống bắt đầu theo dõi vị trí của Visitor.**                                                             |
|                        |                                                    | **13. Hệ thống xác định Visitor đang ở trong phạm vi Thảo Cầm Viên. E3**                                          |
|                        | **14. Visitor di chuyển trong khu vực tham quan.** |                                                                                                                   |
|                        |                                                    | **15. Hệ thống phát hiện Visitor đi vào Domain của một POI.**                                                     |
|                        |                                                    | **16. Hệ thống xác định POI tương ứng với Domain.**                                                               |
|                        |                                                    | **17. Hệ thống phát audio thuyết minh của POI và hiển thị thông tin, hình ảnh tương ứng. A1, A2, A3, A4, A5, E4** |
|                        | **18. Visitor tiếp tục tham quan.**                |                                                                                                                   |
|                        |                                                    | **19. Hệ thống tiếp tục theo dõi vị trí và xử lý các POI tiếp theo.**                                             |
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Alternative Paths:

A1. Visitor di chuyển vào Domain của POI khác trong khi audio hiện tại đang phát, hệ thống thay thế audio đang chờ bằng audio của POI mới nhất.

A2. Visitor di chuyển vào Domain của POI đã có trong hàng chờ, hệ thống không thay đổi audio đang chờ.

A3. Visitor chủ động bỏ qua audio hiện tại, hệ thống phát audio đang có trong hàng chờ.

A4. Visitor quay lại Domain của một POI đã từng được phát, hệ thống phát lại audio của POI đó.

A5. Audio hiện tại kết thúc, hệ thống phát audio đang có trong hàng chờ.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Exception Paths:

E1. Nếu số điện thoại hoặc mã OTP không hợp lệ, hệ thống thông báo thông tin đăng nhập không hợp lệ và yêu cầu Visitor nhập lại mã OTP.

E2. Nếu Visitor từ chối quyền truy cập GPS, hệ thống thông báo chức năng thuyết minh tự động không thể hoạt động và cung cấp lựa chọn tải audio để Visitor chủ động nghe.

E3. Nếu Visitor ở ngoài phạm vi Thảo Cầm Viên, hệ thống thông báo Visitor cần di chuyển vào khu vực Thảo Cầm Viên và không kích hoạt audio tự động.

E4. Nếu hệ thống không lấy được audio của POI, hệ thống thông báo cho Visitor và tự động thử tải lại audio.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Diagram: 

<img width="1399" height="1920" alt="USC1 drawio" src="https://github.com/user-attachments/assets/81efa552-380d-406a-b91f-1a18202a25cf" />


