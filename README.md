# multilingual-guide-services-saigon-zoo

Use case: US1

User: Visitor

Summary: Hệ thống cung cấp dịch vụ thuyết minh tự động đa ngôn ngữ cho khách tham quan thảo cầm viên, sử dụng GPS để tự động phát nội dung thuyết minh tương ứng khi khách tham quan đi vào các khu vực được chỉ định.

Basic Course of Events:
1. Visitor mở phần mềm.
2. Hệ thống hiển thị màn hình đăng nhập và yêu cầu Visitor nhập số điện thoại.
3. Visitor nhập số điện thoại.
4. Hệ thống kiểm tra tài khoản tương ứng với số điện thoại.
5. Hệ thống yêu cầu Visitor nhập mã OTP.
6. Visitor nhập mã OTP.
7. Hệ thống xác thực mã OTP và đăng nhập Visitor. E1
8. Hệ thống hiển thị trang chủ của phần mềm.
9. Visitor lựa chọn ngôn ngữ sử dụng.
10. Hệ thống cập nhật ngôn ngữ audio được lựa chọn.
11. Hệ thống yêu cầu Visitor cấp quyền truy cập GPS.
12. Visitor cấp quyền truy cập GPS. E2
13. Hệ thống bắt đầu theo dõi vị trí của Visitor.
14. Hệ thống xác định Visitor đang ở trong phạm vi Thảo Cầm Viên. E3
15. Visitor di chuyển trong khu vực tham quan.
16. Hệ thống phát hiện Visitor đi vào Domain của một POI.
17. Hệ thống xác định POI tương ứng với Domain.
18. Hệ thống phát audio thuyết minh của POI và hiển thị thông tin, hình ảnh tương ứng. A1, A2, A3, A4, A5, E4
19. Visitor tiếp tục tham quan.
20. Hệ thống tiếp tục theo dõi vị trí và xử lý các POI tiếp theo.

Alternative Course of Events

A1. Visitor di chuyển vào Domain của POI khác trong khi audio hiện tại đang phát, hệ thống thay thế audio đang chờ bằng audio của POI mới nhất.

A2. Visitor di chuyển vào Domain của POI đã có trong hàng chờ, hệ thống không thay đổi audio đang chờ.

A3. Visitor chủ động bỏ qua audio hiện tại, hệ thống phát audio đang có trong hàng chờ.

A4. Visitor quay lại Domain của một POI đã từng được phát, hệ thống phát lại audio của POI đó.

A5. Audio hiện tại kết thúc, hệ thống phát audio đang có trong hàng chờ.

Exception Course of Events

E1. Mã OTP không hợp lệ, hệ thống thông báo thông tin đăng nhập không hợp lệ và yêu cầu Visitor nhập lại mã OTP.

E2. Visitor từ chối quyền truy cập GPS, hệ thống thông báo chức năng thuyết minh tự động không thể hoạt động và cung cấp lựa chọn tải audio để Visitor chủ động nghe.

E3. Visitor ở ngoài phạm vi Thảo Cầm Viên, hệ thống thông báo Visitor cần di chuyển vào khu vực Thảo Cầm Viên và không kích hoạt audio tự động.

E4. Hệ thống không lấy được audio của POI, hệ thống thông báo cho Visitor và tự động thử tải lại audio.
