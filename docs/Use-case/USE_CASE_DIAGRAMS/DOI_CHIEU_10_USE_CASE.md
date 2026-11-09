# Đối chiếu 10 sơ đồ use case hiện hành

Ngày 09/11/2026 — code fb1b0b8. Giữ 10 mã UC gốc; mô tả phần đang triển khai. README gốc còn yêu cầu mục tiêu chưa triển khai như visitor TTS fallback, heatmap và tuyến đường; không lấy các mục tiêu đó làm bằng chứng đã có. Xem REQUIREMENTS_TRACEABILITY.md và báo cáo rà soát trong thư mục cha. Các nhánh A/E ở đây đánh số theo đặc tả hiện hành, không mặc định trùng số nhánh PRD lịch sử.

## UC-01 — Thiết lập ngôn ngữ thuyết minh

[PNG](../USE_CASE_DIAGRAMS_IMG/UC_01_USE_CASE_CHI_TIET.drawio.png) · [SVG](UC_01_USE_CASE_CHI_TIET.svg) · [XML](UC_01_USE_CASE_CHI_TIET.xml)

**Luồng chính:** Mở ứng dụng → kiểm tra lựa chọn đã lưu → chọn và lưu nếu chưa có → áp dụng ngôn ngữ.

### Hành vi hiện hành

| Hành vi | Vai trò trong mô hình |
|---|---|
| Thiết lập ngôn ngữ thuyết minh | Use case chính, giữ mã UC-01 |
| Kiểm tra ngôn ngữ đã lưu | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-01 |
| Xác định ngôn ngữ sử dụng | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-01 |
| Áp dụng ngôn ngữ giao diện và nội dung | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-01 |
| Chọn ngôn ngữ mới | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-01 |
| Lưu lựa chọn ngôn ngữ | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-01 |
| Sử dụng ngôn ngữ đã lưu | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-01 |

### Quan hệ UML

| Nguồn | Quan hệ | Đích | Điều kiện / diễn giải |
|---|---|---|---|
| Thiết lập ngôn ngữ thuyết minh | include | Kiểm tra ngôn ngữ đã lưu | Hành vi được dùng chung. |
| Thiết lập ngôn ngữ thuyết minh | include | Xác định ngôn ngữ sử dụng | Hành vi được dùng chung. |
| Thiết lập ngôn ngữ thuyết minh | include | Áp dụng ngôn ngữ giao diện và nội dung | Hành vi được dùng chung. |
| Chọn ngôn ngữ mới | generalization | Xác định ngôn ngữ sử dụng | Biến thể chuyên biệt kế thừa hành vi chung của use case khái quát. |
| Sử dụng ngôn ngữ đã lưu | generalization | Xác định ngôn ngữ sử dụng | Biến thể chuyên biệt kế thừa hành vi chung của use case khái quát. |
| Chọn ngôn ngữ mới | include | Lưu lựa chọn ngôn ngữ | Hành vi được dùng chung. |

### Nhánh và ngoại lệ hiện hành

- **A1 — Biến thể “Sử dụng ngôn ngữ đã lưu”; không yêu cầu chọn**: Biến thể “Sử dụng ngôn ngữ đã lưu”; không yêu cầu chọn và lưu lại.
- **E1 — Không đọc/lưu được lựa chọn: báo lỗi hoặc mở chọn lại; không**: Không đọc/lưu được lựa chọn: báo lỗi hoặc mở chọn lại; không đánh dấu hoàn tất nếu lưu thất bại.

**Ghi chú mô hình:** 6 ngôn ngữ vi/en/fr/zh-Hans/ja/ko. Đây là chọn ngôn ngữ hiển thị, không phải dịch máy nội dung POI.

### Đặc tả hiện hành để đối chiếu

## Use Case

**UC-01 — Thiết lập ngôn ngữ thuyết minh**

## User

Người tham quan

## Điều kiện trước

Ứng dụng đã tải được trong trình duyệt; các điều kiện bổ sung ghi dưới đây.

## Basic Course of Events

1. Mở ứng dụng.
2. kiểm tra lựa chọn đã lưu.
3. chọn và lưu nếu chưa có.
4. áp dụng ngôn ngữ.

## Alternative / Exception Paths

### A1 — Biến thể “Sử dụng ngôn ngữ đã lưu”; không yêu cầu chọn

Biến thể “Sử dụng ngôn ngữ đã lưu”; không yêu cầu chọn và lưu lại.

### E1 — Không đọc/lưu được lựa chọn: báo lỗi hoặc mở chọn lại; không

Không đọc/lưu được lựa chọn: báo lỗi hoặc mở chọn lại; không đánh dấu hoàn tất nếu lưu thất bại.

## Quy tắc và giới hạn

6 ngôn ngữ vi/en/fr/zh-Hans/ja/ko. Đây là chọn ngôn ngữ hiển thị, không phải dịch máy nội dung POI.

---

## UC-02 — Xem bản đồ và các điểm thuyết minh

[PNG](../USE_CASE_DIAGRAMS_IMG/UC_02_USE_CASE_CHI_TIET.drawio.png) · [SVG](UC_02_USE_CASE_CHI_TIET.svg) · [XML](UC_02_USE_CASE_CHI_TIET.xml)

**Luồng chính:** Mở bản đồ → lấy dữ liệu POI → hiển thị POI → lấy vị trí và làm nổi bật điểm gần nhất khi có GPS.

### Hành vi hiện hành

| Hành vi | Vai trò trong mô hình |
|---|---|
| Xem bản đồ và các điểm thuyết minh | Use case chính, giữ mã UC-02 |
| Lấy dữ liệu POI khả dụng | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-02 |
| Hiển thị bản đồ và các POI | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-02 |
| Sử dụng dữ liệu POI offline | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-02 |
| Hiển thị vị trí và POI gần nhất | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-02 |

### Quan hệ UML

| Nguồn | Quan hệ | Đích | Điều kiện / diễn giải |
|---|---|---|---|
| Xem bản đồ và các điểm thuyết minh | include | Lấy dữ liệu POI khả dụng | Hành vi được dùng chung. |
| Xem bản đồ và các điểm thuyết minh | include | Hiển thị bản đồ và các POI | Hành vi được dùng chung. |
| Sử dụng dữ liệu POI offline | extend | Lấy dữ liệu POI khả dụng | [không lấy được POI từ máy chủ] |
| Hiển thị vị trí và POI gần nhất | extend | Xem bản đồ và các điểm thuyết minh | [GPS khả dụng] |

### Nhánh và ngoại lệ hiện hành

- **A1 — Không có GPS: vẫn hiển thị POI, không thực hiện phần mở**: Không có GPS: vẫn hiển thị POI, không thực hiện phần mở rộng định vị.
- **A2 — Mở rộng việc lấy dữ liệu bằng dữ liệu POI đã lưu**: Mở rộng việc lấy dữ liệu bằng dữ liệu POI đã lưu trên thiết bị.
- **E1 — API lỗi và không có cache đúng ngôn ngữ: hiển thị lỗi**: API lỗi và không có cache đúng ngôn ngữ: hiển thị lỗi, cho thử lại; không dùng nội dung sai ngôn ngữ.

**Ghi chú mô hình:** POI chỉ hiển thị khi active và có bản đúng ngôn ngữ. Cache tách ngôn ngữ; nền OSM online không được bảo đảm ngoại tuyến. GPS không bắt buộc để xem POI.

### Đặc tả hiện hành để đối chiếu

## Use Case

**UC-02 — Xem bản đồ và các điểm thuyết minh**

## User

Người tham quan

## Điều kiện trước

Ứng dụng đã tải được trong trình duyệt; các điều kiện bổ sung ghi dưới đây.

## Basic Course of Events

1. Mở bản đồ.
2. lấy dữ liệu POI.
3. hiển thị POI.
4. lấy vị trí và làm nổi bật điểm gần nhất khi có GPS.

## Alternative / Exception Paths

### A1 — Không có GPS: vẫn hiển thị POI, không thực hiện phần mở

Không có GPS: vẫn hiển thị POI, không thực hiện phần mở rộng định vị.

### A2 — Mở rộng việc lấy dữ liệu bằng dữ liệu POI đã lưu

Mở rộng việc lấy dữ liệu bằng dữ liệu POI đã lưu trên thiết bị.

### E1 — API lỗi và không có cache đúng ngôn ngữ: hiển thị lỗi

API lỗi và không có cache đúng ngôn ngữ: hiển thị lỗi, cho thử lại; không dùng nội dung sai ngôn ngữ.

## Quy tắc và giới hạn

POI chỉ hiển thị khi active và có bản đúng ngôn ngữ. Cache tách ngôn ngữ; nền OSM online không được bảo đảm ngoại tuyến. GPS không bắt buộc để xem POI.

---

## UC-03 — Nhận thuyết minh tự động theo vị trí

[PNG](../USE_CASE_DIAGRAMS_IMG/UC_03_USE_CASE_CHI_TIET.drawio.png) · [SVG](UC_03_USE_CASE_CHI_TIET.svg) · [XML](UC_03_USE_CASE_CHI_TIET.xml)

**Luồng chính:** Bật tự phát → nhận vị trí → xét vùng tròn → chọn bản thu đúng ngôn ngữ → phát nếu trình duyệt cho phép.

### Hành vi hiện hành

| Hành vi | Vai trò trong mô hình |
|---|---|
| Nhận thuyết minh tự động theo vị trí | Use case chính, giữ mã UC-03 |
| Nhận GPS hoặc vị trí mô phỏng | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-03 |
| Xét vùng tròn và chọn POI gần nhất trong vùng | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-03 |
| Kiểm tra trạng thái đã kích hoạt trong lần mở map | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-03 |
| Chọn bản thu đúng ngôn ngữ | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-03 |
| Phát audio có sẵn | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-03 |
| Dừng tự phát và cập nhật khi rời vùng | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-03 |
| Mô phỏng đến POI | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-03 |
| Gửi sự kiện nghe và vùng theo kết nối | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-03 |

### Quan hệ UML

| Nguồn | Quan hệ | Đích | Điều kiện / diễn giải |
|---|---|---|---|
| Nhận thuyết minh tự động theo vị trí | include | Nhận GPS hoặc vị trí mô phỏng | Hành vi được dùng chung. |
| Nhận thuyết minh tự động theo vị trí | include | Xét vùng tròn và chọn POI gần nhất trong vùng | Hành vi được dùng chung. |
| Nhận thuyết minh tự động theo vị trí | include | Kiểm tra trạng thái đã kích hoạt trong lần mở map | Hành vi được dùng chung. |
| Nhận thuyết minh tự động theo vị trí | include | Chọn bản thu đúng ngôn ngữ | Hành vi được dùng chung. |
| Nhận thuyết minh tự động theo vị trí | include | Phát audio có sẵn | Hành vi được dùng chung. |
| Dừng tự phát và cập nhật khi rời vùng | extend | Nhận thuyết minh tự động theo vị trí | [rời vùng hoặc đổi POI] |
| Mô phỏng đến POI | extend | Nhận thuyết minh tự động theo vị trí | [admin/khách bật mô phỏng] |
| Gửi sự kiện nghe và vùng theo kết nối | extend | Nhận thuyết minh tự động theo vị trí | [API tiếp nhận được sự kiện] |

### Nhánh và ngoại lệ hiện hành

- **A1 — Mô phỏng tại POI dùng audio đã chuẩn bị, không đòi hỏi**: Mô phỏng tại POI dùng audio đã chuẩn bị, không đòi hỏi đang có mặt ở vườn thú.
- **A2 — Rời vùng/đổi POI dừng audio tự phát**: Rời vùng/đổi POI dừng audio tự phát.
- **E1 — Thiếu audio, GPS/quyền/API lỗi hoặc autoplay bị chặn: thông báo và cho**: Thiếu audio, GPS/quyền/API lỗi hoặc autoplay bị chặn: thông báo và cho nghe thủ công.

**Ghi chú mô hình:** Không có TTS fallback cho khách, không đọc playback_history để đặt cooldown. Nhánh GPS thật resolve audio qua API online; nghe thủ công/mô phỏng có thể dùng bản đã tải. Autoplay và tab nền phụ thuộc browser.

### Đặc tả hiện hành để đối chiếu

## Use Case

**UC-03 — Nhận thuyết minh tự động theo vị trí**

## User

Người tham quan

## Điều kiện trước

Ứng dụng đã tải được trong trình duyệt; các điều kiện bổ sung ghi dưới đây.

## Basic Course of Events

1. Bật tự phát.
2. nhận vị trí.
3. xét vùng tròn.
4. chọn bản thu đúng ngôn ngữ.
5. phát nếu trình duyệt cho phép.

## Alternative / Exception Paths

### A1 — Mô phỏng tại POI dùng audio đã chuẩn bị, không đòi hỏi

Mô phỏng tại POI dùng audio đã chuẩn bị, không đòi hỏi đang có mặt ở vườn thú.

### A2 — Rời vùng/đổi POI dừng audio tự phát

Rời vùng/đổi POI dừng audio tự phát.

### E1 — Thiếu audio, GPS/quyền/API lỗi hoặc autoplay bị chặn: thông báo và cho

Thiếu audio, GPS/quyền/API lỗi hoặc autoplay bị chặn: thông báo và cho nghe thủ công.

## Quy tắc và giới hạn

Không có TTS fallback cho khách, không đọc playback_history để đặt cooldown. Nhánh GPS thật resolve audio qua API online; nghe thủ công/mô phỏng có thể dùng bản đã tải. Autoplay và tab nền phụ thuộc browser.

---

## UC-04 — Kích hoạt thuyết minh bằng QR Code

[PNG](../USE_CASE_DIAGRAMS_IMG/UC_04_USE_CASE_CHI_TIET.drawio.png) · [SVG](UC_04_USE_CASE_CHI_TIET.svg) · [XML](UC_04_USE_CASE_CHI_TIET.xml)

**Luồng chính:** Quét hoặc nhập TCV-POI:ObjectId → kiểm tra định dạng → tìm bản thu đúng ngôn ngữ → phát.

### Hành vi hiện hành

| Hành vi | Vai trò trong mô hình |
|---|---|
| Kích hoạt thuyết minh bằng QR Code | Use case chính, giữ mã UC-04 |
| Nhận và xác thực mã QR POI | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-04 |
| Xác định ngôn ngữ đang chọn | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-04 |
| Tra bản thu đã tải hoặc resolve online | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-04 |
| Phát audio đúng POI và ngôn ngữ | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-04 |
| Quét mã bằng camera | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-04 |

### Quan hệ UML

| Nguồn | Quan hệ | Đích | Điều kiện / diễn giải |
|---|---|---|---|
| Kích hoạt thuyết minh bằng QR Code | include | Nhận và xác thực mã QR POI | Hành vi được dùng chung. |
| Kích hoạt thuyết minh bằng QR Code | include | Xác định ngôn ngữ đang chọn | Hành vi được dùng chung. |
| Kích hoạt thuyết minh bằng QR Code | include | Tra bản thu đã tải hoặc resolve online | Hành vi được dùng chung. |
| Kích hoạt thuyết minh bằng QR Code | include | Phát audio đúng POI và ngôn ngữ | Hành vi được dùng chung. |
| Quét mã bằng camera | extend | Nhận và xác thực mã QR POI | [người dùng chọn quét camera] |

### Nhánh và ngoại lệ hiện hành

- **A1 — Ưu tiên bản đã tải để nghe ngoại tuyến; nếu không có**: Ưu tiên bản đã tải để nghe ngoại tuyến; nếu không có mới resolve online.
- **A2 — TCV-PACKAGE:ObjectId chuyển sang tải gói UC-05, không bị hiểu thành POI**: TCV-PACKAGE:ObjectId chuyển sang tải gói UC-05, không bị hiểu thành POI.
- **E1 — Mã sai/camera không có quyền/audio thiếu: thông báo; không tự gọi TTS**: Mã sai/camera không có quyền/audio thiếu: thông báo; không tự gọi TTS.

**Ghi chú mô hình:** Không cần GPS. Camera cần secure context và quyền; nhập mã thủ công vẫn dùng được. Không tự chọn audio khác ngôn ngữ hoặc dịch máy cho khách.

### Đặc tả hiện hành để đối chiếu

## Use Case

**UC-04 — Kích hoạt thuyết minh bằng QR Code**

## User

Người tham quan

## Điều kiện trước

Ứng dụng đã tải được trong trình duyệt; các điều kiện bổ sung ghi dưới đây.

## Basic Course of Events

1. Quét hoặc nhập TCV-POI:ObjectId.
2. kiểm tra định dạng.
3. tìm bản thu đúng ngôn ngữ.
4. phát.

## Alternative / Exception Paths

### A1 — Ưu tiên bản đã tải để nghe ngoại tuyến; nếu không có

Ưu tiên bản đã tải để nghe ngoại tuyến; nếu không có mới resolve online.

### A2 — TCV-PACKAGE:ObjectId chuyển sang tải gói UC-05, không bị hiểu thành POI

TCV-PACKAGE:ObjectId chuyển sang tải gói UC-05, không bị hiểu thành POI.

### E1 — Mã sai/camera không có quyền/audio thiếu: thông báo; không tự gọi TTS

Mã sai/camera không có quyền/audio thiếu: thông báo; không tự gọi TTS.

## Quy tắc và giới hạn

Không cần GPS. Camera cần secure context và quyền; nhập mã thủ công vẫn dùng được. Không tự chọn audio khác ngôn ngữ hoặc dịch máy cho khách.

---

## UC-05 — Tải gói audio thuyết minh offline

[PNG](../USE_CASE_DIAGRAMS_IMG/UC_05_USE_CASE_CHI_TIET.drawio.png) · [SVG](UC_05_USE_CASE_CHI_TIET.svg) · [XML](UC_05_USE_CASE_CHI_TIET.xml)

**Luồng chính:** Chọn gói → lấy manifest → tải/kiểm tra từng bản thu → lưu IndexedDB → báo hoàn tất.

### Hành vi hiện hành

| Hành vi | Vai trò trong mô hình |
|---|---|
| Tải gói audio thuyết minh offline | Use case chính, giữ mã UC-05 |
| Chọn gói bằng QR, mã hoặc liên kết | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-05 |
| Lấy manifest và kiểm tra gói | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-05 |
| Tải các asset trong gói | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-05 |
| Ước tính dung lượng khi browser hỗ trợ | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-05 |
| Kiểm tra size và checksum khi có | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-05 |
| Lưu Blob audio và metadata gói | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-05 |
| Hủy tải và khôi phục dữ liệu trước tải | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-05 |

### Quan hệ UML

| Nguồn | Quan hệ | Đích | Điều kiện / diễn giải |
|---|---|---|---|
| Tải gói audio thuyết minh offline | include | Chọn gói bằng QR, mã hoặc liên kết | Hành vi được dùng chung. |
| Tải gói audio thuyết minh offline | include | Lấy manifest và kiểm tra gói | Hành vi được dùng chung. |
| Tải gói audio thuyết minh offline | include | Tải các asset trong gói | Hành vi được dùng chung. |
| Tải gói audio thuyết minh offline | include | Kiểm tra size và checksum khi có | Hành vi được dùng chung. |
| Tải gói audio thuyết minh offline | include | Lưu Blob audio và metadata gói | Hành vi được dùng chung. |
| Ước tính dung lượng khi browser hỗ trợ | extend | Tải các asset trong gói | [Storage Estimate API khả dụng] |
| Hủy tải và khôi phục dữ liệu trước tải | extend | Tải các asset trong gói | [người dùng hủy hoặc tải lỗi] |

### Nhánh và ngoại lệ hiện hành

- **A1 — Gói đã tải vẫn có thể được tải lại; client giữ dữ**: Gói đã tải vẫn có thể được tải lại; client giữ dữ liệu cũ để rollback khi lỗi.
- **A2 — Manifest chưa xác minh toàn bộ checksum cần người dùng xác nhận**: Manifest chưa xác minh toàn bộ checksum cần người dùng xác nhận tiếp tục bản demo.
- **E1 — Thiếu dung lượng, checksum/size sai, lỗi mạng hoặc hủy: không ghi nhận**: Thiếu dung lượng, checksum/size sai, lỗi mạng hoặc hủy: không ghi nhận tải thành công.

**Ghi chú mô hình:** Một gói/một ngôn ngữ, không phải ZIP. Chỉ kiểm tra checksum khi có SHA-256 hợp lệ; không cam kết đủ dung lượng nếu browser không cung cấp estimate. Mô hình Chrome dịch không thuộc gói audio.

### Đặc tả hiện hành để đối chiếu

## Use Case

**UC-05 — Tải gói audio thuyết minh offline**

## User

Người tham quan

## Điều kiện trước

Ứng dụng đã tải được trong trình duyệt; các điều kiện bổ sung ghi dưới đây.

## Basic Course of Events

1. Chọn gói.
2. lấy manifest.
3. tải/kiểm tra từng bản thu.
4. lưu IndexedDB.
5. báo hoàn tất.

## Alternative / Exception Paths

### A1 — Gói đã tải vẫn có thể được tải lại; client giữ dữ

Gói đã tải vẫn có thể được tải lại; client giữ dữ liệu cũ để rollback khi lỗi.

### A2 — Manifest chưa xác minh toàn bộ checksum cần người dùng xác nhận

Manifest chưa xác minh toàn bộ checksum cần người dùng xác nhận tiếp tục bản demo.

### E1 — Thiếu dung lượng, checksum/size sai, lỗi mạng hoặc hủy: không ghi nhận

Thiếu dung lượng, checksum/size sai, lỗi mạng hoặc hủy: không ghi nhận tải thành công.

## Quy tắc và giới hạn

Một gói/một ngôn ngữ, không phải ZIP. Chỉ kiểm tra checksum khi có SHA-256 hợp lệ; không cam kết đủ dung lượng nếu browser không cung cấp estimate. Mô hình Chrome dịch không thuộc gói audio.

---

## UC-06 — Khám phá và nghe thuyết minh offline

[PNG](../USE_CASE_DIAGRAMS_IMG/UC_06_USE_CASE_CHI_TIET.drawio.png) · [SVG](UC_06_USE_CASE_CHI_TIET.svg) · [XML](UC_06_USE_CASE_CHI_TIET.xml)

**Luồng chính:** Xem danh sách → chọn đối tượng → tìm audio cục bộ → hiển thị thông tin → nghe không cần Internet.

### Hành vi hiện hành

| Hành vi | Vai trò trong mô hình |
|---|---|
| Khám phá và nghe thuyết minh offline | Use case chính, giữ mã UC-06 |
| Xem danh sách bản thu đã tải | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-06 |
| Tìm audio đã lưu theo đối tượng | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-06 |
| Xem metadata POI đã cache khi có | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-06 |
| Phát audio ngoại tuyến | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-06 |
| Chọn đối tượng khác | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-06 |

### Quan hệ UML

| Nguồn | Quan hệ | Đích | Điều kiện / diễn giải |
|---|---|---|---|
| Khám phá và nghe thuyết minh offline | include | Xem danh sách bản thu đã tải | Hành vi được dùng chung. |
| Khám phá và nghe thuyết minh offline | include | Tìm audio đã lưu theo đối tượng | Hành vi được dùng chung. |
| Khám phá và nghe thuyết minh offline | include | Phát audio ngoại tuyến | Hành vi được dùng chung. |
| Chọn đối tượng khác | extend | Khám phá và nghe thuyết minh offline | [chọn đối tượng khác] |
| Xem metadata POI đã cache khi có | extend | Khám phá và nghe thuyết minh offline | [có metadata POI đã cache] |

### Nhánh và ngoại lệ hiện hành

- **A1 — Mở rộng tại điểm đang xem/nghe: đổi đối tượng, dừng audio cũ**: Mở rộng tại điểm đang xem/nghe: đổi đối tượng, dừng audio cũ nếu cần và xử lý đối tượng mới.
- **E1 — Chưa có bản thu phù hợp hoặc dữ liệu cục bộ lỗi:**: Chưa có bản thu phù hợp hoặc dữ liệu cục bộ lỗi: báo chưa có/không phát được; không tự tải khi đang offline.

**Ghi chú mô hình:** Điều kiện: mở app và tải audio trước trên cùng origin/browser. Không cần gọi server để phát Blob đã tải. Ảnh, metadata và nền map chỉ có theo dữ liệu đã cache; không bắt UC-05 chạy lại ở mỗi lần nghe.

### Đặc tả hiện hành để đối chiếu

## Use Case

**UC-06 — Khám phá và nghe thuyết minh offline**

## User

Người tham quan

## Điều kiện trước

Đã có audio phù hợp trong IndexedDB và app shell đã cache.

## Basic Course of Events

1. Xem danh sách.
2. chọn đối tượng.
3. tìm audio cục bộ.
4. hiển thị thông tin.
5. nghe không cần Internet.

## Alternative / Exception Paths

### A1 — Mở rộng tại điểm đang xem/nghe: đổi đối tượng, dừng audio cũ

Mở rộng tại điểm đang xem/nghe: đổi đối tượng, dừng audio cũ nếu cần và xử lý đối tượng mới.

### E1 — Chưa có bản thu phù hợp hoặc dữ liệu cục bộ lỗi:

Chưa có bản thu phù hợp hoặc dữ liệu cục bộ lỗi: báo chưa có/không phát được; không tự tải khi đang offline.

## Quy tắc và giới hạn

Điều kiện: mở app và tải audio trước trên cùng origin/browser. Không cần gọi server để phát Blob đã tải. Ảnh, metadata và nền map chỉ có theo dữ liệu đã cache; không bắt UC-05 chạy lại ở mỗi lần nghe.

---

## UC-07 — Đăng nhập quản trị

[PNG](../USE_CASE_DIAGRAMS_IMG/UC_07_USE_CASE_CHI_TIET.drawio.png) · [SVG](UC_07_USE_CASE_CHI_TIET.svg) · [XML](UC_07_USE_CASE_CHI_TIET.xml)

**Luồng chính:** Kiểm tra phiên → nếu cần, nhập thông tin và xác thực → tạo phiên → vào khu vực quản trị.

### Hành vi hiện hành

| Hành vi | Vai trò trong mô hình |
|---|---|
| Đăng nhập quản trị | Use case chính, giữ mã UC-07 |
| Kiểm tra phiên đăng nhập | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-07 |
| Truy cập khu vực quản trị | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-07 |
| Đăng nhập bằng tài khoản | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-07 |
| Sử dụng phiên hợp lệ | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-07 |
| Xác thực tài khoản | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-07 |
| Tạo phiên đăng nhập | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-07 |

### Quan hệ UML

| Nguồn | Quan hệ | Đích | Điều kiện / diễn giải |
|---|---|---|---|
| Đăng nhập quản trị | include | Kiểm tra phiên đăng nhập | Hành vi được dùng chung. |
| Đăng nhập quản trị | include | Truy cập khu vực quản trị | Hành vi được dùng chung. |
| Đăng nhập bằng tài khoản | generalization | Truy cập khu vực quản trị | Biến thể chuyên biệt kế thừa hành vi chung của use case khái quát. |
| Sử dụng phiên hợp lệ | generalization | Truy cập khu vực quản trị | Biến thể chuyên biệt kế thừa hành vi chung của use case khái quát. |
| Đăng nhập bằng tài khoản | include | Xác thực tài khoản | Hành vi được dùng chung. |
| Đăng nhập bằng tài khoản | include | Tạo phiên đăng nhập | Hành vi được dùng chung. |

### Nhánh và ngoại lệ hiện hành

- **A1 — Biến thể “Sử dụng phiên hợp lệ” truy cập khu vực quản**: Biến thể “Sử dụng phiên hợp lệ” truy cập khu vực quản trị mà không nhập lại thông tin.
- **E1 — Sai tài khoản/mật khẩu, phiên hết hạn hoặc tài khoản không hoạt**: Sai tài khoản/mật khẩu, phiên hết hạn hoặc tài khoản không hoạt động: từ chối; nhập lại khi phù hợp.
- **E2 — Backend/Redis lỗi hoặc rate limit: báo lỗi và cho thử lại sau**: Backend/Redis lỗi hoặc rate limit: báo lỗi và cho thử lại sau; không tạo phiên giả.

**Ghi chú mô hình:** Cookie HTTP-only; session Redis 8 giờ; backend kiểm tra role/permission cho từng request. Hết phiên hoặc không đủ quyền thì không mở chức năng quản trị; chưa có UI quản lý tài khoản/role.

### Đặc tả hiện hành để đối chiếu

## Use Case

**UC-07 — Đăng nhập quản trị**

## User

Quản trị viên

## Điều kiện trước

Ứng dụng đã tải được trong trình duyệt; các điều kiện bổ sung ghi dưới đây.

## Basic Course of Events

1. Kiểm tra phiên.
2. nếu cần, nhập thông tin và xác thực.
3. tạo phiên.
4. vào khu vực quản trị.

## Alternative / Exception Paths

### A1 — Biến thể “Sử dụng phiên hợp lệ” truy cập khu vực quản

Biến thể “Sử dụng phiên hợp lệ” truy cập khu vực quản trị mà không nhập lại thông tin.

### E1 — Sai tài khoản/mật khẩu, phiên hết hạn hoặc tài khoản không hoạt

Sai tài khoản/mật khẩu, phiên hết hạn hoặc tài khoản không hoạt động: từ chối; nhập lại khi phù hợp.

### E2 — Backend/Redis lỗi hoặc rate limit: báo lỗi và cho thử lại sau

Backend/Redis lỗi hoặc rate limit: báo lỗi và cho thử lại sau; không tạo phiên giả.

## Quy tắc và giới hạn

Cookie HTTP-only; session Redis 8 giờ; backend kiểm tra role/permission cho từng request. Hết phiên hoặc không đủ quyền thì không mở chức năng quản trị; chưa có UI quản lý tài khoản/role.

---

## UC-08 — Quản lý POI

[PNG](../USE_CASE_DIAGRAMS_IMG/UC_08_USE_CASE_CHI_TIET.drawio.png) · [SVG](UC_08_USE_CASE_CHI_TIET.svg) · [XML](UC_08_USE_CASE_CHI_TIET.xml)

**Luồng chính:** Xem danh sách → thêm/sửa/ẩn → lưu POI → lưu ảnh và vùng bằng request riêng khi cần.

### Hành vi hiện hành

| Hành vi | Vai trò trong mô hình |
|---|---|
| Quản lý POI | Use case chính, giữ mã UC-08 |
| Xem và tìm/lọc danh sách POI | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-08 |
| Thêm POI mới | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-08 |
| Sửa thông tin chung POI | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-08 |
| Ẩn POI khỏi catalog | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-08 |
| Kiểm tra dữ liệu POI | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-08 |
| Lưu POI và cập nhật danh sách | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-08 |
| Upload hoặc đổi URL ảnh | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-08 |
| Cấu hình geofence tròn | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-08 |

### Quan hệ UML

| Nguồn | Quan hệ | Đích | Điều kiện / diễn giải |
|---|---|---|---|
| Quản lý POI | include | Xem và tìm/lọc danh sách POI | Hành vi được dùng chung. |
| Thêm POI mới | extend | Quản lý POI | [chọn thêm] |
| Sửa thông tin chung POI | extend | Quản lý POI | [chọn sửa] |
| Ẩn POI khỏi catalog | extend | Quản lý POI | [chọn ẩn] |
| Upload hoặc đổi URL ảnh | extend | Quản lý POI | [POI đã lưu; chọn ảnh] |
| Cấu hình geofence tròn | extend | Quản lý POI | [POI đã lưu; cấu hình vùng] |
| Thêm POI mới | include | Kiểm tra dữ liệu POI | Hành vi được dùng chung. |
| Sửa thông tin chung POI | include | Kiểm tra dữ liệu POI | Hành vi được dùng chung. |
| Thêm POI mới | include | Lưu POI và cập nhật danh sách | Hành vi được dùng chung. |
| Sửa thông tin chung POI | include | Lưu POI và cập nhật danh sách | Hành vi được dùng chung. |
| Ẩn POI khỏi catalog | include | Lưu POI và cập nhật danh sách | Hành vi được dùng chung. |

### Nhánh và ngoại lệ hiện hành

- **A1 — Tạo POI kèm bản ngôn ngữ đầu tiên, mặc định ẩn**: Tạo POI kèm bản ngôn ngữ đầu tiên, mặc định ẩn.
- **A2 — Đổi ảnh/tọa độ/bán kính/trạng thái; tọa độ POI cập nhật tâm vùng**: Đổi ảnh/tọa độ/bán kính/trạng thái; tọa độ POI cập nhật tâm vùng tròn.
- **A3 — Ẩn POI, giữ dữ liệu/audio/gói cũ; không xóa cứng**: Ẩn POI, giữ dữ liệu/audio/gói cũ; không xóa cứng.

**Ghi chú mô hình:** Ảnh upload JPEG/PNG/WebP ≤5 MB, ≤16 MP. Bán kính 5–500 m. Không vẽ polygon. Các bước form không chung một transaction. Thêm POI không tự tạo đủ bản dịch/audio; tiếp tục UC-09.

### Đặc tả hiện hành để đối chiếu

## Use Case

**UC-08 — Quản lý POI**

## User

Quản trị viên

## Điều kiện trước

Đã đăng nhập và có quyền tương ứng.

## Basic Course of Events

1. Xem danh sách.
2. thêm/sửa/ẩn.
3. lưu POI.
4. lưu ảnh và vùng bằng request riêng khi cần.

## Alternative / Exception Paths

### A1 — Tạo POI kèm bản ngôn ngữ đầu tiên, mặc định ẩn

Tạo POI kèm bản ngôn ngữ đầu tiên, mặc định ẩn.

### A2 — Đổi ảnh/tọa độ/bán kính/trạng thái; tọa độ POI cập nhật tâm vùng

Đổi ảnh/tọa độ/bán kính/trạng thái; tọa độ POI cập nhật tâm vùng tròn.

### A3 — Ẩn POI, giữ dữ liệu/audio/gói cũ; không xóa cứng

Ẩn POI, giữ dữ liệu/audio/gói cũ; không xóa cứng.

## Quy tắc và giới hạn

Ảnh upload JPEG/PNG/WebP ≤5 MB, ≤16 MP. Bán kính 5–500 m. Không vẽ polygon. Các bước form không chung một transaction. Thêm POI không tự tạo đủ bản dịch/audio; tiếp tục UC-09.

---

## UC-09 — Quản lý nội dung thuyết minh và bản dịch

[PNG](../USE_CASE_DIAGRAMS_IMG/UC_09_USE_CASE_CHI_TIET.drawio.png) · [SVG](UC_09_USE_CASE_CHI_TIET.svg) · [XML](UC_09_USE_CASE_CHI_TIET.xml)

**Luồng chính:** Chọn POI/ngôn ngữ → lưu thủ công hoặc Chrome preview/đối chiếu/xác nhận → admin yêu cầu TTS từng ngôn ngữ → nghe thử → phát hành gói mới khi cần.

### Hành vi hiện hành

| Hành vi | Vai trò trong mô hình |
|---|---|
| Quản lý nội dung thuyết minh và bản dịch | Use case chính, giữ mã UC-09 |
| Chọn POI và ngôn ngữ nội dung | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-09 |
| Xem nội dung và audio hiện có | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-09 |
| Nhập và lưu nội dung thủ công | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-09 |
| Dịch và lưu bản dịch qua Chrome | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-09 |
| Chuẩn bị nguồn và revision đích | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-09 |
| Tải mô hình khi cần và dịch tại máy | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-09 |
| Đối chiếu, sửa và chọn bản lưu | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-09 |
| Xác nhận thay thế và lưu transaction | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-09 |
| Yêu cầu TTS từ lời đã lưu | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-09 |
| Theo dõi tác vụ và nghe thử | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-09 |
| Phát hành snapshot audio mới | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-09 |

### Quan hệ UML

| Nguồn | Quan hệ | Đích | Điều kiện / diễn giải |
|---|---|---|---|
| Quản lý nội dung thuyết minh và bản dịch | include | Chọn POI và ngôn ngữ nội dung | Hành vi được dùng chung. |
| Quản lý nội dung thuyết minh và bản dịch | include | Xem nội dung và audio hiện có | Hành vi được dùng chung. |
| Nhập và lưu nội dung thủ công | extend | Quản lý nội dung thuyết minh và bản dịch | [admin nhập/sửa một ngôn ngữ] |
| Dịch và lưu bản dịch qua Chrome | extend | Quản lý nội dung thuyết minh và bản dịch | [admin chọn dịch; Chrome desktop hỗ trợ] |
| Dịch và lưu bản dịch qua Chrome | include | Chuẩn bị nguồn và revision đích | Hành vi được dùng chung. |
| Dịch và lưu bản dịch qua Chrome | include | Tải mô hình khi cần và dịch tại máy | Hành vi được dùng chung. |
| Dịch và lưu bản dịch qua Chrome | include | Đối chiếu, sửa và chọn bản lưu | Hành vi được dùng chung. |
| Dịch và lưu bản dịch qua Chrome | include | Xác nhận thay thế và lưu transaction | Hành vi được dùng chung. |
| Yêu cầu TTS từ lời đã lưu | extend | Quản lý nội dung thuyết minh và bản dịch | [admin chọn tạo audio; đã có lời lưu] |
| Yêu cầu TTS từ lời đã lưu | include | Theo dõi tác vụ và nghe thử | Hành vi được dùng chung. |
| Phát hành snapshot audio mới | extend | Quản lý nội dung thuyết minh và bản dịch | [admin chọn phát hành; có audio sẵn sàng] |

### Nhánh và ngoại lệ hiện hành

- **A1 — Nhập/sửa thủ công, có thể chỉ lưu văn bản**: Nhập/sửa thủ công, có thể chỉ lưu văn bản.
- **A2 — Theo dõi hoặc tạo lại audio, nghe thử khi Completed**: Theo dõi hoặc tạo lại audio, nghe thử khi Completed.
- **A3 — Chrome desktop: lưu nguồn → chuẩn bị preview → bấm dịch →**: Chrome desktop: lưu nguồn → chuẩn bị preview → bấm dịch → sửa/chọn → xác nhận lưu.
- **E1 — Browser/cặp ngôn ngữ không hỗ trợ hoặc tải mô hình lỗi: nhập**: Browser/cặp ngôn ngữ không hỗ trợ hoặc tải mô hình lỗi: nhập thủ công.
- **E2 — Preview hết hạn hoặc nguồn/đích đổi: từ chối 409, chuẩn bị mới**: Preview hết hạn hoặc nguồn/đích đổi: từ chối 409, chuẩn bị mới.
- **E3 — TTS lỗi: báo Failed và admin chủ động yêu cầu lại**: TTS lỗi: báo Failed và admin chủ động yêu cầu lại.

**Ghi chú mô hình:** 6 ngôn ngữ tổng cộng, tối đa 5 đích. Không Cloud API key. Redis giữ nguồn/revision 30 phút; bản dịch mới ở bộ nhớ React trước commit. Lưu lời đổi vô hiệu audio; POI active cho đọc ngay sau lưu. TTS không tự chạy do bấm dịch. Gói cũ không tự cập nhật.

### Đặc tả hiện hành để đối chiếu

## Use Case

**UC-09 — Quản lý nội dung thuyết minh và bản dịch**

## User

Quản trị viên

## Điều kiện trước

Đã đăng nhập và có quyền tương ứng.

## Basic Course of Events

1. Chọn POI/ngôn ngữ.
2. lưu thủ công hoặc Chrome preview/đối chiếu/xác nhận.
3. admin yêu cầu TTS từng ngôn ngữ.
4. nghe thử.
5. phát hành gói mới khi cần.

## Alternative / Exception Paths

### A1 — Nhập/sửa thủ công, có thể chỉ lưu văn bản

Nhập/sửa thủ công, có thể chỉ lưu văn bản.

### A2 — Theo dõi hoặc tạo lại audio, nghe thử khi Completed

Theo dõi hoặc tạo lại audio, nghe thử khi Completed.

### A3 — Chrome desktop: lưu nguồn → chuẩn bị preview → bấm dịch →

Chrome desktop: lưu nguồn → chuẩn bị preview → bấm dịch → sửa/chọn → xác nhận lưu.

### E1 — Browser/cặp ngôn ngữ không hỗ trợ hoặc tải mô hình lỗi: nhập

Browser/cặp ngôn ngữ không hỗ trợ hoặc tải mô hình lỗi: nhập thủ công.

### E2 — Preview hết hạn hoặc nguồn/đích đổi: từ chối 409, chuẩn bị mới

Preview hết hạn hoặc nguồn/đích đổi: từ chối 409, chuẩn bị mới.

### E3 — TTS lỗi: báo Failed và admin chủ động yêu cầu lại

TTS lỗi: báo Failed và admin chủ động yêu cầu lại.

## Quy tắc và giới hạn

6 ngôn ngữ tổng cộng, tối đa 5 đích. Không Cloud API key. Redis giữ nguồn/revision 30 phút; bản dịch mới ở bộ nhớ React trước commit. Lưu lời đổi vô hiệu audio; POI active cho đọc ngay sau lưu. TTS không tự chạy do bấm dịch. Gói cũ không tự cập nhật.

---

## UC-10 — Xem dữ liệu phân tích

[PNG](../USE_CASE_DIAGRAMS_IMG/UC_10_USE_CASE_CHI_TIET.drawio.png) · [SVG](UC_10_USE_CASE_CHI_TIET.svg) · [XML](UC_10_USE_CASE_CHI_TIET.xml)

**Luồng chính:** Mở dashboard → kiểm tra quyền → tổng hợp từ sự kiện đã nhận → xem thiết bị, phiên, audio, ngôn ngữ và điểm nổi bật.

### Hành vi hiện hành

| Hành vi | Vai trò trong mô hình |
|---|---|
| Xem dữ liệu phân tích | Use case chính, giữ mã UC-10 |
| Kiểm tra quyền analytics:read | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-10 |
| Lấy dữ liệu sự kiện đã ghi nhận | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-10 |
| Tổng hợp KPI theo UTC | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-10 |
| Hiển thị KPI, thời gian, ngôn ngữ và POI | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-10 |
| Làm mới số liệu dashboard | Hành vi hỗ trợ hoặc biến thể trong phạm vi UC-10 |

### Quan hệ UML

| Nguồn | Quan hệ | Đích | Điều kiện / diễn giải |
|---|---|---|---|
| Xem dữ liệu phân tích | include | Kiểm tra quyền analytics:read | Hành vi được dùng chung. |
| Xem dữ liệu phân tích | include | Lấy dữ liệu sự kiện đã ghi nhận | Hành vi được dùng chung. |
| Xem dữ liệu phân tích | include | Tổng hợp KPI theo UTC | Hành vi được dùng chung. |
| Xem dữ liệu phân tích | include | Hiển thị KPI, thời gian, ngôn ngữ và POI | Hành vi được dùng chung. |
| Làm mới số liệu dashboard | extend | Xem dữ liệu phân tích | [admin làm mới hoặc chu kỳ 60 giây] |

### Nhánh và ngoại lệ hiện hành

- **A1 — Làm mới theo nút hoặc tự động mỗi 60 giây**: Làm mới theo nút hoặc tự động mỗi 60 giây.
- **E1 — Hết phiên/thiếu quyền/API lỗi: báo lỗi, không giả số liệu**: Hết phiên/thiếu quyền/API lỗi: báo lỗi, không giả số liệu.
- **E2 — Chưa có sự kiện: hiển thị trạng thái trống/0**: Chưa có sự kiện: hiển thị trạng thái trống/0.

**Ghi chú mô hình:** Thiết bị hoạt động: có sự kiện 5 phút gần nhất; visits là phiên bắt đầu, không phải người thật. Mốc ngày/giờ UTC; ngôn ngữ theo sự kiện. Chưa có heatmap, lịch sử tuyến hoặc queue đồng bộ analytics offline.

### Đặc tả hiện hành để đối chiếu

## Use Case

**UC-10 — Xem dữ liệu phân tích**

## User

Quản trị viên

## Điều kiện trước

Đã đăng nhập và có quyền tương ứng.

## Basic Course of Events

1. Mở dashboard.
2. kiểm tra quyền.
3. tổng hợp từ sự kiện đã nhận.
4. xem thiết bị, phiên, audio, ngôn ngữ và điểm nổi bật.

## Alternative / Exception Paths

### A1 — Làm mới theo nút hoặc tự động mỗi 60 giây

Làm mới theo nút hoặc tự động mỗi 60 giây.

### E1 — Hết phiên/thiếu quyền/API lỗi: báo lỗi, không giả số liệu

Hết phiên/thiếu quyền/API lỗi: báo lỗi, không giả số liệu.

### E2 — Chưa có sự kiện: hiển thị trạng thái trống/0

Chưa có sự kiện: hiển thị trạng thái trống/0.

## Quy tắc và giới hạn

Thiết bị hoạt động: có sự kiện 5 phút gần nhất; visits là phiên bắt đầu, không phải người thật. Mốc ngày/giờ UTC; ngôn ngữ theo sự kiện. Chưa có heatmap, lịch sử tuyến hoặc queue đồng bộ analytics offline.

---
