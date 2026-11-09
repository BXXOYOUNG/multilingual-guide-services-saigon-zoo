# 10 Use Case Diagram — luồng hiện hành

Đối chiếu ngày **09/11/2026**, code `fb1b0b8`. Giữ nguyên 10 mã UC, mỗi UC có một sơ đồ riêng. Các hình trong bộ này mô tả phần đã triển khai; README gốc còn chứa yêu cầu mục tiêu chưa đạt. [Báo cáo rà soát](../RA_SOAT_UC_DFD_2026-11-09.md).

## 1. Mã và ảnh hiện hành

| UC | Tên | PNG có mã draw.io | SVG | XML chỉnh sửa |
|---|---|---|---|---|
| UC-01 | Thiết lập ngôn ngữ thuyết minh | [PNG](../USE_CASE_DIAGRAMS_IMG/UC_01_USE_CASE_CHI_TIET.drawio.png) | [SVG](UC_01_USE_CASE_CHI_TIET.svg) | [XML](UC_01_USE_CASE_CHI_TIET.xml) |
| UC-02 | Xem bản đồ và các điểm thuyết minh | [PNG](../USE_CASE_DIAGRAMS_IMG/UC_02_USE_CASE_CHI_TIET.drawio.png) | [SVG](UC_02_USE_CASE_CHI_TIET.svg) | [XML](UC_02_USE_CASE_CHI_TIET.xml) |
| UC-03 | Nhận thuyết minh tự động theo vị trí | [PNG](../USE_CASE_DIAGRAMS_IMG/UC_03_USE_CASE_CHI_TIET.drawio.png) | [SVG](UC_03_USE_CASE_CHI_TIET.svg) | [XML](UC_03_USE_CASE_CHI_TIET.xml) |
| UC-04 | Kích hoạt thuyết minh bằng QR Code | [PNG](../USE_CASE_DIAGRAMS_IMG/UC_04_USE_CASE_CHI_TIET.drawio.png) | [SVG](UC_04_USE_CASE_CHI_TIET.svg) | [XML](UC_04_USE_CASE_CHI_TIET.xml) |
| UC-05 | Tải gói audio thuyết minh offline | [PNG](../USE_CASE_DIAGRAMS_IMG/UC_05_USE_CASE_CHI_TIET.drawio.png) | [SVG](UC_05_USE_CASE_CHI_TIET.svg) | [XML](UC_05_USE_CASE_CHI_TIET.xml) |
| UC-06 | Khám phá và nghe thuyết minh offline | [PNG](../USE_CASE_DIAGRAMS_IMG/UC_06_USE_CASE_CHI_TIET.drawio.png) | [SVG](UC_06_USE_CASE_CHI_TIET.svg) | [XML](UC_06_USE_CASE_CHI_TIET.xml) |
| UC-07 | Đăng nhập quản trị | [PNG](../USE_CASE_DIAGRAMS_IMG/UC_07_USE_CASE_CHI_TIET.drawio.png) | [SVG](UC_07_USE_CASE_CHI_TIET.svg) | [XML](UC_07_USE_CASE_CHI_TIET.xml) |
| UC-08 | Quản lý POI | [PNG](../USE_CASE_DIAGRAMS_IMG/UC_08_USE_CASE_CHI_TIET.drawio.png) | [SVG](UC_08_USE_CASE_CHI_TIET.svg) | [XML](UC_08_USE_CASE_CHI_TIET.xml) |
| UC-09 | Quản lý nội dung thuyết minh và bản dịch | [PNG](../USE_CASE_DIAGRAMS_IMG/UC_09_USE_CASE_CHI_TIET.drawio.png) | [SVG](UC_09_USE_CASE_CHI_TIET.svg) | [XML](UC_09_USE_CASE_CHI_TIET.xml) |
| UC-10 | Xem dữ liệu phân tích | [PNG](../USE_CASE_DIAGRAMS_IMG/UC_10_USE_CASE_CHI_TIET.drawio.png) | [SVG](UC_10_USE_CASE_CHI_TIET.svg) | [XML](UC_10_USE_CASE_CHI_TIET.xml) |

## 2. Cách đọc

- Actor chính là khách ở UC-01–06, admin ở UC-07–10. Khung hệ thống chứa use case và các hành vi được phân rã trong phạm vi UC đó.
- Association dùng đường liền không mũi tên. `«include»` từ use case sử dụng đến hành vi chung; `«extend»` từ hành vi bổ sung đến use case được mở rộng kèm điều kiện; generalization từ biến thể đến khái quát, tam giác rỗng.
- Mũi tên UML không mô tả thứ tự bước. Trình tự, điều kiện, lỗi và giới hạn đọc trong [đặc tả từng UC](DOI_CHIEU_10_USE_CASE.md). Mã A/E ở đặc tả hiện hành không mặc định trùng mã nhánh README lịch sử.

## 3. Các điểm đã đồng bộ

- UC-03/04 không vẽ TTS fallback như đã triển khai; thiếu audio thì báo lỗi. Geofence GPS thật còn phụ thuộc API online; thủ công/mô phỏng có thể dùng audio đã tải.
- UC-05 nhận gói qua QR/mã/link, kiểm tra manifest/size/checksum khi có, tải IndexedDB; hủy/lỗi khôi phục trước tải. Không cam kết bỏ qua tải lại chỉ vì đã có gói.
- UC-08 là thêm/sửa/**ẩn** POI, ảnh và vùng tròn; không xóa cứng hoặc tự tạo đủ audio/bản dịch.
- UC-09 bổ sung Chrome desktop: lưu nguồn → chuẩn bị revision → bấm dịch/tải mô hình → đối chiếu/sửa/chọn → xác nhận lưu → admin tự yêu cầu TTS → phát hành gói mới. Dịch không tự tạo audio.
- UC-10 chỉ mô tả dashboard đang có: thiết bị 5 phút, phiên truy cập UTC, sự kiện/audio, ngôn ngữ theo sự kiện, POI nổi bật. Không vẽ heatmap/tuyến đường như đã có.

## 4. Dùng trong báo cáo

Mở XML bằng draw.io hoặc dán toàn bộ `<mxGraphModel>` vào **Extras → Edit Diagram**. PNG trong thư mục `_IMG` đã được xuất lại và nhúng cùng XML hiện hành; có thể mở bằng draw.io để chỉnh. SVG nằm cạnh XML để chèn báo cáo không mất nét. Sau mọi chỉnh sửa nguồn, xuất lại cả ảnh để tránh lệch phiên bản.

Đọc cùng [kiến trúc](../../CURRENT_ARCHITECTURE.md), [đối chiếu yêu cầu](../../REQUIREMENTS_TRACEABILITY.md) và [luồng Chrome](../../ADMIN_AUTO_TRANSLATION.md).
