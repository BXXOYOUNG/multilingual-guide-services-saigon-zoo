# Mã và ảnh DFD theo từng mức — hiện hành

Đối chiếu **09/11/2026**, code `fb1b0b8`. [Đặc tả dữ liệu đầy đủ](../BAO_CAO_DFD_HE_THONG.md) · [Báo cáo rà soát](../RA_SOAT_UC_DFD_2026-11-09.md).

## 1. Danh sách sơ đồ

| File | Cấp / tiến trình cha | Số luồng | XML | SVG | PNG có mã draw.io |
|---|---|---:|---|---|---|
| 01 | Ngữ cảnh | 12 | [XML](01_NGU_CANH.xml) | [SVG](01_NGU_CANH.svg) | [PNG](../DFD_IMG/01_NGU_CANH.drawio.png) |
| 02 | Mức 0: toàn hệ thống | 71 | [XML](02_MUC_0_HE_THONG.xml) | [SVG](02_MUC_0_HE_THONG.svg) | [PNG](../DFD_IMG/02_MUC_0_HE_THONG.drawio.png) |
| 03 | Mức 1: 1.0 | 12 | [XML](03_MUC_1_1_0_NGON_NGU.xml) | [SVG](03_MUC_1_1_0_NGON_NGU.svg) | [PNG](../DFD_IMG/03_MUC_1_1_0_NGON_NGU.drawio.png) |
| 04 | Mức 1: 2.0 | 25 | [XML](04_MUC_1_2_0_POI_BAN_DO_LO_TRINH.xml) | [SVG](04_MUC_1_2_0_POI_BAN_DO_LO_TRINH.svg) | [PNG](../DFD_IMG/04_MUC_1_2_0_POI_BAN_DO_LO_TRINH.drawio.png) |
| 05 | Mức 1: 3.0 | 23 | [XML](05_MUC_1_3_0_NGHE_VA_TU_PHAT.xml) | [SVG](05_MUC_1_3_0_NGHE_VA_TU_PHAT.svg) | [PNG](../DFD_IMG/05_MUC_1_3_0_NGHE_VA_TU_PHAT.drawio.png) |
| 06 | Mức 1: 4.0 | 21 | [XML](06_MUC_1_4_0_AUDIO_NGOAI_TUYEN.xml) | [SVG](06_MUC_1_4_0_AUDIO_NGOAI_TUYEN.svg) | [PNG](../DFD_IMG/06_MUC_1_4_0_AUDIO_NGOAI_TUYEN.drawio.png) |
| 07 | Mức 1: 5.0 | 60 | [XML](07_MUC_1_5_0_QUAN_TRI_NOI_DUNG.xml) | [SVG](07_MUC_1_5_0_QUAN_TRI_NOI_DUNG.svg) | [PNG](../DFD_IMG/07_MUC_1_5_0_QUAN_TRI_NOI_DUNG.drawio.png) |
| 08 | Mức 1: 6.0 | 18 | [XML](08_MUC_1_6_0_ANALYTICS.xml) | [SVG](08_MUC_1_6_0_ANALYTICS.svg) | [PNG](../DFD_IMG/08_MUC_1_6_0_ANALYTICS.drawio.png) |
| 09 | Mức 2: 5.5 TTS | 32 | [XML](09_MUC_2_5_5_TAO_AUDIO_TTS.xml) | [SVG](09_MUC_2_5_5_TAO_AUDIO_TTS.svg) | [PNG](../DFD_IMG/09_MUC_2_5_5_TAO_AUDIO_TTS.drawio.png) |
| 10 | Mức 2: 5.7 Dịch Chrome | 24 | [XML](10_MUC_2_5_7_DICH_CHROME.xml) | [SVG](10_MUC_2_5_7_DICH_CHROME.svg) | [PNG](../DFD_IMG/10_MUC_2_5_7_DICH_CHROME.drawio.png) |

## 2. Quy ước và bố cục

Thứ tự: **ngữ cảnh → mức 0 → mức 1 → mức 2**. Mức 0 có sáu tiến trình 1.0–6.0. Mức 1 của 5.0 có thêm 5.7; mức 2 có hai sơ đồ riêng cho TTS 5.5 và Chrome 5.7.

Các file 02–10 dùng cùng bố cục dọc rộng 1690 đơn vị, một vùng ngang/tiến trình. E/D và tiến trình tham chiếu có thể lặp để giữ đường ngắn, nhưng cùng mã vẫn cùng đối tượng. Khung nền chỉ hỗ trợ đọc. Hình tròn là tiến trình; chữ nhật vàng là tác nhân ngoài; hai đường song song là kho; khung nét đứt là tiến trình tham chiếu ngoài phạm vi phân rã.

Mũi tên xám là dòng gần tiến trình, mũi tên xanh ký hiệu F là trao đổi giữa tiến trình trong cùng sơ đồ. **Mã F bắt đầu lại ở mỗi file**, không dùng làm khóa xuyên các sơ đồ. Xem [mức 0](MUC_0_DOI_CHIEU_LUONG.md) và [mức 1/2](MUC_1_VA_2_DOI_CHIEU_LUONG.md) để tra dữ liệu đầy đủ.

E6 là **Chrome Translator API tại máy admin**, ngoài mã app như GPS/camera E5; không phải Cloud Translation hoặc container dịch. D7 giữ token/nguồn/revision có TTL; bản dịch chưa lưu ở bộ nhớ React, không phải dữ liệu persistent của D9. TTS chỉ chạy theo yêu cầu admin; bản dịch mới không tự tạo MP3.

## 3. Copy vào draw.io hoặc dùng ảnh

Mở từng XML hoặc dán nguyên `<mxGraphModel ...>...</mxGraphModel>` vào **Extras → Edit Diagram**, rồi Replace existing drawing. Không dán dấu Markdown bao code. Có thể mở PNG `.drawio.png` trong thư mục `_IMG` vì ảnh đã nhúng cùng XML hiện hành. SVG nằm cạnh XML; dùng SVG khi báo cáo cần phóng to. Khi sửa nguồn, xuất lại ảnh.

Mỗi PNG/SVG hiện hành đã được tạo lại trong lần rà soát này. Không dùng ảnh từ phiên bản trước để chứng nhận bước Chrome hoặc TTS runtime. Các ảnh/sơ đồ là tài liệu, không thay thế kiểm thử ứng dụng.
