# Sơ đồ kiến trúc đối chiếu runtime 09/11/2026

| Sơ đồ | Mã PlantUML thuần | SVG | PNG |
|---|---|---|---|
| Component | [Nguồn](Component_Diagram.md) | [SVG](Component_Diagram.svg) | [PNG](Component_Diagram.png) |
| Deployment | [Nguồn](Deployment_Diagram.md) | [SVG](Deployment_Diagram.svg) | [PNG](Deployment_Diagram.png) |

Ảnh được xuất lại từ nguồn trong lần rà soát UC/DFD; xem [báo cáo](../Use-case/RA_SOAT_UC_DFD_2026-11-09.md). Hai file `.md` chỉ chứa mã `@startuml` để copy vào công cụ PlantUML.

Các module backend cùng một FastAPI. TTS runtime là BackgroundTasks do admin yêu cầu, không có worker bền vững. Dịch văn bản dùng native Chrome desktop; backend giữ preview nguồn/revision và xác nhận lưu transaction, không gọi Cloud Translation. Localhost và HTTPS tunnel đều hỗ trợ theo khả năng browser/cặp ngôn ngữ. Mô hình native thuộc Chrome profile, tách khỏi gói audio và backup database/media.
