# Rà soát UC, DFD và sơ đồ kiến trúc

**Ngày:** 09/11/2026. **Code đối chiếu:** `fb1b0b8`, nhánh `feature/admin-auto-translation`. Người dùng đã xác nhận nghiệm thu luồng dịch Chrome. Lần rà soát này chỉnh tài liệu và hình, không thay code nghiệp vụ hoặc dữ liệu database, không commit/push.

## 1. Kết quả và các chỗ đã sửa

| Vấn đề trước rà soát | Cách phản ánh hiện hành |
|---|---|
| DFD chưa có bước dịch; UC-09 vẫn ghi không bổ sung dịch máy | Thêm 5.7, bốn tiến trình con 5.7.1–5.7.4 và nhánh A3 của UC-09: chuẩn bị → Chrome dịch → đối chiếu → xác nhận lưu. |
| Không phân biệt native Chrome và dịch vụ Cloud | E6 là native API nằm ngoài mã app, chạy trên máy admin; bổ sung cùng dòng dữ liệu ở ngữ cảnh, mức 0, mức 1 và mức 2. Không có Cloud API key/container dịch. |
| Preview có thể bị hiểu là lưu nháp công khai hoặc tự tạo audio | Redis chỉ giữ nguồn/revision/token, TTL 30 phút. Văn bản dịch mới ở bộ nhớ React đến commit. TTS do admin yêu cầu riêng từ lời đã lưu. |
| Không nêu bảo vệ bản dịch đã chỉnh tay | Cần xác nhận thay thế đích đã có; kiểm tra nguồn/revision/token; lưu toàn bộ bản chọn trong một request bằng transaction MongoDB rs0. Xung đột/hết hạn yêu cầu chuẩn bị lại. |
| Chưa phản ánh trạng thái audio và review khi sửa lời | Đổi title/lời đích vô hiệu audio/task hiện tại; sửa nguồn đánh dấu bản dịch phụ thuộc `needs_review`; không tự thay lời/audio đích. |
| UC-03/04 vẽ TTS fallback như đã có | Bộ UC hiện hành chỉ phát audio có sẵn đúng ngôn ngữ; thiếu thì báo lỗi. Nhánh GPS thật còn resolve online; không đọc lịch sử backend để đặt cooldown đầy đủ. |
| UC-05 coi gói đã có là chắc chắn không tải lại | Mã hiện tại cho phép tải lại, giữ dữ liệu trước tải để rollback; kiểm tra dung lượng/checksum theo API/metadata khả dụng. |
| UC-06 có thể hứa đủ thông tin/ảnh offline | Phát Blob đã tải; thông tin/ảnh phụ thuộc cache cùng origin/browser, nền OSM chưa được bảo đảm offline. |
| UC-08 gọi xóa POI và thiếu ảnh/geofence | Đổi thành ẩn POI; bổ sung ảnh upload/HTTPS và geofence tròn. Form gồm nhiều request, không hứa rollback chung. |
| UC-10 dùng ghi chú heatmap/tuyến như chức năng runtime | Chỉ số thực: thiết bị có sự kiện 5 phút, phiên bắt đầu, audio/sự kiện, ngôn ngữ theo sự kiện, POI nổi bật; mốc UTC. Chưa có heatmap/tuyến. |
| Component/deployment ghi TTS chỉ chạy qua script | Bổ sung FastAPI BackgroundTasks → Edge TTS, lease Redis, browser translation UI/native API và backend chuẩn bị/commit. |
| Ảnh và link không đồng bộ thư mục mã | Xuất lại PNG/SVG; PNG UC/DFD nhúng cùng XML chỉnh sửa. Sửa index trỏ đúng thư mục `_IMG`. |

## 2. Bộ tài liệu dùng cho báo cáo hiện tại

- [10 Use Case Diagram](USE_CASE_DIAGRAMS/README.md) và [đặc tả/đối chiếu từng UC](USE_CASE_DIAGRAMS/DOI_CHIEU_10_USE_CASE.md).
- [Báo cáo DFD](BAO_CAO_DFD_HE_THONG.md), [10 file mã và ảnh DFD](DFD_XML/README.md).
- [Mức 0: nguồn/đích/tên đầy đủ các luồng](DFD_XML/MUC_0_DOI_CHIEU_LUONG.md), [mức 1 và 2](DFD_XML/MUC_1_VA_2_DOI_CHIEU_LUONG.md).
- [Component PlantUML](../PRD/Component_Diagram.md), [Deployment PlantUML](../PRD/Deployment_Diagram.md), [ảnh và nguồn kiến trúc](../PRD/README.md).
- [Luồng Chrome](../ADMIN_AUTO_TRANSLATION.md), [kiến trúc runtime](../CURRENT_ARCHITECTURE.md), [đối chiếu PRD](../REQUIREMENTS_TRACEABILITY.md).

Có **10 UC**, mỗi UC một sơ đồ; **10 DFD** gồm một ngữ cảnh, một mức 0, sáu mức 1 và hai mức 2 (TTS 5.5, Chrome 5.7). Giữ sáu tiến trình chính 1.0–6.0, kho D1–D9; thêm E6 là native platform dependency và 5.7 trong phần quản trị. Bố cục DFD dọc đã được giữ; số luồng cập nhật ở từng index và bảng đối chiếu, không giữ số đếm lịch sử 69/181 sau khi thêm chức năng.

## 3. PRD gốc và đặc tả hiện hành

README gốc giữ các yêu cầu mục tiêu chưa được triển khai đầy đủ. Bộ UC trong thư mục này là **đặc tả hiện hành**, không âm thầm coi TTS fallback/heatmap/tuyến là đã đạt PRD. Mã UC-01–10 được giữ để truy vết; mã nhánh A/E trong bản hiện hành không mặc định trùng nhánh của PRD lịch sử. Bảng `REQUIREMENTS_TRACEABILITY.md` ghi khoảng cách yêu cầu–implementation.

Khi viết báo cáo, ghi rõ “sơ đồ luồng hiện hành, đối chiếu code fb1b0b8” và đọc cùng các giới hạn bên dưới từng UC/DFD. Nếu cần trình bày thiết kế mục tiêu tương lai, tạo phiên bản ghi rõ mục tiêu thay vì trộn vào các hình runtime này.

## 4. Quy tắc nhất quán đã đối chiếu

- Chọn ngôn ngữ của khách không kích hoạt dịch máy; POI cần bản ngôn ngữ đúng đã lưu, không fallback ngầm.
- Dịch Chrome dùng desktop qua localhost **hoặc HTTPS tunnel**; mô hình tải theo Chrome profile, không nằm trong gói audio hay MongoDB/SeaweedFS backup. Trình duyệt/cặp không hỗ trợ vẫn nhập thủ công.
- Các dòng vào/ra E6 giữ cùng ý nghĩa xuyên ngữ cảnh → 5.0 → 5.7 → 5.7.2; không vẽ Chrome như tác nhân riêng chỉ xuất hiện ở mức con.
- Bản dịch chưa lưu không đi vào D2. Sau commit, POI active có thể được khách đọc ngay; không có kho nháp đã lưu riêng để chờ xuất bản.
- Chỉ tác vụ TTS khớp task ID và title/lời hiện tại mới được gắn audio. Gói snapshot giữ bản thu cũ; admin phát hành gói mới để cập nhật tải offline.
- ObjectId, các collection và hạ tầng giữ nguyên; metadata translation và unique index đã thuộc luồng code hiện có, không sinh collection/worker từ sơ đồ.

## 5. Phạm vi kiểm tra tài liệu

Đối chiếu các module quản trị, browser translation, audio/offline, geofence và analytics hiện có; kiểm tra XML parse được, ID/đầu nối/kiểu dòng dữ liệu, các bảng luồng, liên kết nội bộ, nguồn XML nhúng trong PNG và ảnh xem trước. Đây là kiểm tra tài liệu/sơ đồ, không chạy lại bộ kiểm thử ứng dụng hoặc chứng nhận mọi thiết bị/cặp ngôn ngữ. Bản sao trước sửa được giữ trong `.demo-run/diagrams-before-chrome-review` trên máy này.

**Kết quả:** kiểm tra tài liệu đạt cho 20 XML (10 UC, 10 DFD), 20 SVG/PNG tương ứng, hai cặp ảnh PlantUML và các link trong bộ UC/DFD/PRD. Không còn đầu nối thiếu, tiến trình DFD thiếu vào/ra hoặc đường nối trực tiếp kho–tác nhân; tập tác nhân ngữ cảnh/mức 0 và chiều trao đổi qua ranh giới của sáu phân rã mức 1 cùng hai phân rã mức 2 khớp mức cha. XML nhúng trong từng PNG UC/DFD khớp nguồn hiện hành. Kiểm tra cấu trúc không tự chứng minh mọi yêu cầu nghiệp vụ của PRD đã được triển khai.
