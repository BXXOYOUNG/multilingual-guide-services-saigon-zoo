# Biểu đồ tuần tự – Sequence Diagram

Bộ 13 sơ đồ XML draw.io đối chiếu hệ thống tại thời điểm tạo và các mục II.3.1–II.3.13 của báo cáo `docs/reports/BAO_CAO_HOC_THUAT_THEO_MAU_NHOM_8_THAO_CAM_VIEN.docx`.

## Mở và chỉnh sửa

Mở diagrams.net / draw.io → File → Open From → Device → chọn file trong `XML/`. Có thể nhập vào draw.io Desktop hoặc extension tương thích. Chọn Fit để xem toàn sơ đồ rồi phóng to vùng cần đọc.

Các file dùng mxGraphModel không nén; participant, lifeline, activation, thông điệp, nhãn và khung điều kiện đều là phần tử chỉnh sửa được. Xuất PNG/SVG vào `IMG/` nếu cần chèn báo cáo.

| Mục báo cáo | Sơ đồ | File XML |
|---|---|---|
| II.3.1 | Chọn và khôi phục ngôn ngữ | [01_CHON_KHOI_PHUC_NGON_NGU.xml](XML/01_CHON_KHOI_PHUC_NGON_NGU.xml) |
| II.3.2 | Xem bản đồ và nội dung POI | [02_XEM_BAN_DO_NOI_DUNG_POI.xml](XML/02_XEM_BAN_DO_NOI_DUNG_POI.xml) |
| II.3.3 | Xét vùng và tự phát thuyết minh | [03_XET_VUNG_TU_PHAT_THUYET_MINH.xml](XML/03_XET_VUNG_TU_PHAT_THUYET_MINH.xml) |
| II.3.4 | Quét QR và phát bản thu | [04_QUET_QR_PHAT_BAN_THU.xml](XML/04_QUET_QR_PHAT_BAN_THU.xml) |
| II.3.5 | Tải gói audio ngoại tuyến | [05_TAI_GOI_AUDIO_NGOAI_TUYEN.xml](XML/05_TAI_GOI_AUDIO_NGOAI_TUYEN.xml) |
| II.3.6 | Nghe audio đã tải khi mất mạng | [06_NGHE_AUDIO_DA_TAI_OFFLINE.xml](XML/06_NGHE_AUDIO_DA_TAI_OFFLINE.xml) |
| II.3.7 | Đăng nhập, kiểm tra phiên và đăng xuất | [07_DANG_NHAP_PHIEN_DANG_XUAT.xml](XML/07_DANG_NHAP_PHIEN_DANG_XUAT.xml) |
| II.3.8 | Quản lý POI, ảnh và geofence | [08_QUAN_LY_POI_ANH_GEOFENCE.xml](XML/08_QUAN_LY_POI_ANH_GEOFENCE.xml) |
| II.3.9 | Dịch hàng loạt và xác nhận tất cả | [09_DICH_HANG_LOAT_XAC_NHAN_TAT_CA.xml](XML/09_DICH_HANG_LOAT_XAC_NHAN_TAT_CA.xml) |
| II.3.10 | Tạo audio, theo dõi tác vụ và nghe thử | [10_TAO_AUDIO_THEO_DOI_NGHE_THU.xml](XML/10_TAO_AUDIO_THEO_DOI_NGHE_THU.xml) |
| II.3.11 | Phát hành gói snapshot và QR | [11_PHAT_HANH_SNAPSHOT_VA_QR.xml](XML/11_PHAT_HANH_SNAPSHOT_VA_QR.xml) |
| II.3.12 | Ghi sự kiện và tổng hợp thiết bị hoạt động | [12_GHI_SU_KIEN_THIET_BI_ACTIVE.xml](XML/12_GHI_SU_KIEN_THIET_BI_ACTIVE.xml) |
| II.3.13 | Lộ trình gợi ý và khoảng cách giữa hai POI | [13_LO_TRINH_KHOANG_CACH_HAI_POI.xml](XML/13_LO_TRINH_KHOANG_CACH_HAI_POI.xml) |

## Quy ước

- Mũi tên liền tam giác tô: thông điệp gọi; mũi tên liền đầu mở: gửi bất đồng bộ/sự kiện; nét đứt đầu mở: phản hồi/kết quả.
- Lifeline nét đứt biểu diễn đối tượng/thành phần; activation được giản lược theo các cặp gọi/trả về và thao tác ghi.
- `alt`: nhánh loại trừ; `opt`: phần tùy chọn; `loop`: lặp; `critical`: phạm vi transaction nhóm bản dịch. Điều kiện trong ngoặc vuông là guard.
- Các thành phần được gom theo trách nhiệm để đọc được ở mức thiết kế; không phải sơ đồ của mọi hàm nội bộ hoặc mỗi request phụ trợ.

## Các điểm cần giữ đúng khi thuyết minh

- Khôi phục ngôn ngữ ưu tiên IndexedDB, có localStorage dự phòng; không gọi dịch máy khi khách chỉ đổi ngôn ngữ.
- Nhánh GPS thật resolve audio qua API. Mô phỏng/nghe thủ công có thể dùng bản đã tải; không khẳng định tự phát GPS hoàn toàn offline.
- Nghe Blob offline không cần gọi server để phát. Analytics khi mất mạng không có queue gửi bù.
- POI, ảnh và vùng là các request riêng; sơ đồ không cam kết transaction chung cho toàn form.
- Các lệnh Translator.create khởi tạo trong click trước khi await preview API. SD-09 thể hiện một cách xen kẽ kết quả hợp lệ; xử lý dịch có thể diễn ra trong lúc preview đang chuẩn bị. Không phải năm lần bấm hay dịch Cloud ở backend.
- Xác nhận tất cả là lựa chọn chủ động, bao gồm đồng ý thay thế bản đích hiện có; backend vẫn kiểm tra quyền/token/revision. Không tự TTS sau dịch.
- BackgroundTasks chạy trong process API, không phải worker/queue bền vững. Cần kiểm tra nội dung/task hiện tại trước gắn audio.
- Snapshot cố định audio; không đóng băng toàn bộ metadata POI.
- Thiết bị active là device_id khác nhau có sự kiện trong năm phút; không đếm IP và không xóa lịch sử để giảm số active.
- Khoảng cách hai POI là Haversine trực tiếp, không tính theo lối đi và không tối ưu thứ tự tham quan.

## Đối chiếu mã nguồn

- SD-01 (UC-01): `frontend/src/features/localization/LanguageContext.jsx`; `frontend/src/features/localization/languageStorage.js`.
- SD-02 (UC-02): `frontend/src/features/map/poiLoader.js`; `frontend/src/features/map/InteractiveMap.jsx`; `backend/api/pois.py`; `backend/repositories/poi_repository.py`.
- SD-03 (UC-03): `frontend/src/features/map/InteractiveMap.jsx`; `frontend/src/features/map/useGeolocation.js`; `frontend/src/features/map/geoUtils.js`; `backend/api/geofences.py`.
- SD-04 (UC-04): `frontend/src/components/views/ExploreView.jsx`; `frontend/src/features/offline/audioPackages.js`; `backend/api/audio.py`.
- SD-05 (UC-05): `frontend/src/features/offline/audioPackages.js`; `backend/services/audio.py`; `frontend/src/db/indexedDB.js`.
- SD-06 (UC-06): `frontend/src/components/views/ExploreView.jsx`; `frontend/src/features/offline/audioPackages.js`; `frontend/src/db/indexedDB.js`.
- SD-07 (UC-07): `backend/api/admin_auth.py`; `backend/services/admin_auth.py`; `frontend/src/components/views/AdminView.jsx`.
- SD-08 (UC-08): `frontend/src/components/views/AdminPoiWorkflow.jsx`; `backend/api/admin.py`; `backend/api/admin_workflow.py`.
- SD-09 (UC-09): `frontend/src/components/views/AdminTranslationPanel.jsx`; `frontend/src/services/browserTranslation.js`; `backend/api/admin_translation.py`.
- SD-10 (UC-09): `backend/api/admin_workflow.py`; `backend/services/admin_narration.py`; `frontend/src/components/views/AdminPoiWorkflow.jsx`.
- SD-11 (UC-09 mở rộng / UC-05): `backend/api/admin_workflow.py`; `frontend/src/components/views/AdminView.jsx`; `frontend/src/components/views/HomeView.jsx`.
- SD-12 (UC-10): `frontend/src/services/analytics.js`; `frontend/src/components/layout/PublicLayout.jsx`; `backend/api/visitor.py`; `backend/api/admin.py`.
- SD-13 (Chức năng tra cứu bổ sung): `frontend/src/components/views/ItineraryView.jsx`; `frontend/src/features/map/geoUtils.js`; `frontend/src/features/map/poiLoader.js`.

Đã kiểm tra XML parse, ID duy nhất, tham chiếu nguồn/đích, cân bằng khung và giới hạn tọa độ trang. Việc này không thay thế kiểm thử runtime hay nghiệm thu tương tác draw.io.
