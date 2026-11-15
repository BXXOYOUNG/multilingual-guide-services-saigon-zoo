# Sơ đồ kiến trúc hệ thống

## Bản tinh gọn — 13/11/2026

Vẽ lại từ hai ảnh có sẵn, đối chiếu tài liệu và mã nguồn hiện tại. Component thể hiện cấu trúc mã nguồn; deployment thể hiện node, runtime, artifact, lưu trữ và kết nối. Đường nối vuông góc dùng làn riêng; các quan hệ dùng chung được gom theo biên package.

| Sơ đồ | SVG | PNG | Nguồn chỉnh sửa |
|---|---|---|---|
| Component | [SVG](Component_Diagram_Refined.svg) | [PNG](Component_Diagram_Refined.png) | [drawio](Component_Diagram_Refined.drawio) |
| Deployment | [SVG](Deployment_Diagram_Refined.svg) | [PNG](Deployment_Diagram_Refined.png) | [drawio](Deployment_Diagram_Refined.drawio) |

Xem [thuyết minh, đối chiếu component với code, kết nối triển khai và cách xuất lại](DIAGRAMS_REFINED.md). Nguồn sinh ảnh: [render_refined_diagrams.py](render_refined_diagrams.py). Hai ảnh mới không thay đổi kiến trúc hệ thống.

## Bản tham chiếu giữ nguyên — 09/11/2026

| Sơ đồ | Mã PlantUML thuần | SVG | PNG |
|---|---|---|---|
| Component | [Nguồn](Component_Diagram.md) | [SVG](Component_Diagram.svg) | [PNG](Component_Diagram.png) |
| Deployment | [Nguồn](Deployment_Diagram.md) | [SVG](Deployment_Diagram.svg) | [PNG](Deployment_Diagram.png) |

Ảnh được xuất lại từ nguồn trong lần rà soát UC/DFD; xem [báo cáo](../Use-case/RA_SOAT_UC_DFD_2026-11-09.md). Hai file `.md` chỉ chứa mã `@startuml` để copy vào công cụ PlantUML.

Các module backend cùng một FastAPI. TTS runtime là BackgroundTasks do admin yêu cầu, không có worker bền vững. Dịch văn bản dùng native Chrome desktop; backend giữ preview nguồn/revision và xác nhận lưu transaction, không gọi Cloud Translation. Localhost và HTTPS tunnel đều hỗ trợ theo khả năng browser/cặp ngôn ngữ. Mô hình native thuộc Chrome profile, tách khỏi gói audio và backup database/media.
