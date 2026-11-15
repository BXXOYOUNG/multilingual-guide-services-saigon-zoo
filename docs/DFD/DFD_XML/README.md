# Mã và ảnh DFD theo từng mức

**Cập nhật 10/11/2026.** [Báo cáo](../BAO_CAO_DFD_HE_THONG.md) · [Đối chiếu kho kỹ thuật](KHO_DU_LIEU_DOI_CHIEU.md).

## Danh sách sơ đồ

12 sơ đồ: một ngữ cảnh, một mức 0, sáu mức 1, bốn mức 2. Sơ đồ ngữ cảnh giữ nguyên các luồng; bỏ ghi chú đầu/cuối hình.

| Sơ đồ | Số luồng sau gộp | XML | SVG | PNG có mã draw.io |
|---|---:|---|---|---|
| Ngữ cảnh | 12 | [XML](01_NGU_CANH.xml) | [SVG](01_NGU_CANH.svg) | [PNG](../DFD_IMG/01_NGU_CANH.drawio.png) |
| MỨC 0 — TOÀN HỆ THỐNG | 44 | [XML](02_MUC_0_HE_THONG.xml) | [SVG](02_MUC_0_HE_THONG.svg) | [PNG](../DFD_IMG/02_MUC_0_HE_THONG.drawio.png) |
| MỨC 1 — PHÂN RÃ 1.0 | 12 | [XML](03_MUC_1_1_0_NGON_NGU.xml) | [SVG](03_MUC_1_1_0_NGON_NGU.svg) | [PNG](../DFD_IMG/03_MUC_1_1_0_NGON_NGU.drawio.png) |
| MỨC 1 — PHÂN RÃ 2.0 | 24 | [XML](04_MUC_1_2_0_POI_BAN_DO_LO_TRINH.xml) | [SVG](04_MUC_1_2_0_POI_BAN_DO_LO_TRINH.svg) | [PNG](../DFD_IMG/04_MUC_1_2_0_POI_BAN_DO_LO_TRINH.drawio.png) |
| MỨC 1 — PHÂN RÃ 3.0 | 21 | [XML](05_MUC_1_3_0_NGHE_VA_TU_PHAT.xml) | [SVG](05_MUC_1_3_0_NGHE_VA_TU_PHAT.svg) | [PNG](../DFD_IMG/05_MUC_1_3_0_NGHE_VA_TU_PHAT.drawio.png) |
| MỨC 1 — PHÂN RÃ 4.0 | 21 | [XML](06_MUC_1_4_0_AUDIO_NGOAI_TUYEN.xml) | [SVG](06_MUC_1_4_0_AUDIO_NGOAI_TUYEN.svg) | [PNG](../DFD_IMG/06_MUC_1_4_0_AUDIO_NGOAI_TUYEN.drawio.png) |
| MỨC 1 — PHÂN RÃ 5.0 | 40 | [XML](07_MUC_1_5_0_QUAN_TRI_NOI_DUNG.xml) | [SVG](07_MUC_1_5_0_QUAN_TRI_NOI_DUNG.svg) | [PNG](../DFD_IMG/07_MUC_1_5_0_QUAN_TRI_NOI_DUNG.drawio.png) |
| MỨC 1 — PHÂN RÃ 6.0 | 15 | [XML](08_MUC_1_6_0_ANALYTICS.xml) | [SVG](08_MUC_1_6_0_ANALYTICS.svg) | [PNG](../DFD_IMG/08_MUC_1_6_0_ANALYTICS.drawio.png) |
| MỨC 2 — PHÂN RÃ 5.5 | 21 | [XML](09_MUC_2_5_5_TAO_AUDIO_TTS.xml) | [SVG](09_MUC_2_5_5_TAO_AUDIO_TTS.svg) | [PNG](../DFD_IMG/09_MUC_2_5_5_TAO_AUDIO_TTS.drawio.png) |
| MỨC 2 — PHÂN RÃ 5.7: DỊCH BẰNG CHROME | 20 | [XML](10_MUC_2_5_7_DICH_CHROME.xml) | [SVG](10_MUC_2_5_7_DICH_CHROME.svg) | [PNG](../DFD_IMG/10_MUC_2_5_7_DICH_CHROME.drawio.png) |
| MỨC 2 — PHÂN RÃ 3.3: XÁC ĐỊNH VÙNG KÍCH HOẠT | 8 | [XML](11_MUC_2_3_3_VUNG_KICH_HOAT.xml) | [SVG](11_MUC_2_3_3_VUNG_KICH_HOAT.svg) | [PNG](../DFD_IMG/11_MUC_2_3_3_VUNG_KICH_HOAT.drawio.png) |
| MỨC 2 — PHÂN RÃ 4.3: TẢI, KIỂM TRA VÀ LƯU GÓI | 17 | [XML](12_MUC_2_4_3_TAI_KIEM_TRA_LUU.xml) | [SVG](12_MUC_2_4_3_TAI_KIEM_TRA_LUU.svg) | [PNG](../DFD_IMG/12_MUC_2_4_3_TAI_KIEM_TRA_LUU.drawio.png) |

## Quy ước kho và luồng

- Mức 0: chỉ một kho logic **D1 — Dữ liệu hệ thống**.
- Mức 1/2: chỉ dùng **D1.1 — Dữ liệu dùng chung** và **D1.2 — Dữ liệu trên thiết bị** khi liên quan. Đây là các phần của D1; không phải đổi schema hay tạo database.
- Mỗi kho, tác nhân và tiến trình chỉ vẽ **một lần trong từng sơ đồ**. Bố cục dùng các vùng tác nhân/tham chiếu, xử lý và kho chung, với đường nối vuông góc; không nhân bản kho để trang trí. Sơ đồ không liệt kê collection hay trường dữ liệu.
- Luồng cùng chiều giữa một tiến trình và cùng kho được gộp. Nhãn hình được rút gọn; dữ liệu đầy đủ ở [bảng mức 0](MUC_0_DOI_CHIEU_LUONG.md) và [bảng mức 1/2](MUC_1_VA_2_DOI_CHIEU_LUONG.md). Mũi tên ghi tên dữ liệu ngắn gọn; ID flow dùng tra cứu XML, không cần bảng mã ở cuối hình.
- Dữ liệu tạm trong form dịch và trạng thái xét vùng trong component là bộ nhớ làm việc của xử lý; không tự coi là gói audio offline D1.2.
- E6 là native Chrome Translator tại máy admin. TTS chỉ tạo theo yêu cầu admin; không có Cloud Translation API hoặc dịch vụ dịch trong Docker.

Ảnh chỉ giữ tiêu đề, các ký hiệu và nhãn luồng dữ liệu. Không có dòng cập nhật, chú giải dài hoặc phần đối chiếu ở cuối ảnh; các giải thích nằm trong tài liệu này và bảng riêng.

## Phân rã mức 2

- 3.3: nhận ngữ cảnh → chọn vùng → đối chiếu trạng thái và đề nghị phát.
- 4.3: kiểm tra lưu trữ → tải/kiểm tra → lưu → khôi phục khi lỗi/hủy.
- 5.5: tạo và theo dõi TTS.
- 5.7: dịch Chrome, đối chiếu và xác nhận lưu.

Chỉ phân rã khi cần làm rõ đầu vào, xử lý và đầu ra. Không bắt buộc mọi nhánh xuống cùng mức.

## Dùng với draw.io

Mở từng XML hoặc dán nguyên `<mxGraphModel ...>...</mxGraphModel>` vào **Extras → Edit Diagram**, rồi Replace existing drawing. PNG `.drawio.png` đã nhúng cùng mã XML, có thể mở để sửa. SVG dùng khi cần phóng to hoặc đưa vào báo cáo. Khi sửa nguồn phải xuất lại ảnh tương ứng.
