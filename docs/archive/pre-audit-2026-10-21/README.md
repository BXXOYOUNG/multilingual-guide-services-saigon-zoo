# Tư liệu lịch sử trước audit 21/10/2026

Các file này được đưa ra khỏi vị trí sử dụng thường ngày vì không còn khớp bản demo hiện tại. Không chạy hoặc dùng chúng làm source of truth. Giữ lại để đối chiếu lịch sử, không phải thành phần runtime.

| File | Vì sao lưu trữ |
|---|---|
| `Component_Diagram.png`, `Deployment_Diagram.png` | Có PMTiles, dịch tự động, worker/cache và triển khai Docker chưa tồn tại đầy đủ trong bản hiện tại |
| `Logical_ERD.png` | Nhãn asset ghi trùng package, một số kiểu/quan hệ không khớp implementation |
| `docker-compose.legacy.yml.txt` | Mongo standalone 27017 và tên container khác; thiếu SeaweedFS, dễ tạo stack/database thứ hai |
| `prepare_mvp_dataset.py.txt` | Thuộc giai đoạn chỉ cho 2 điểm lên map; chạy lại sẽ tắt POI/geofence của bản demo 11 điểm |
| `bootstrap_demo_admin.py.txt` | Script bootstrap một lần cũ; luồng đang dùng là `scripts/create_admin.py` với tài khoản đặt riêng |
| `great-argus-wrong-for-TCV-AN-006.jpg` | Ảnh Great Argus không đúng loài Rheinardia ocellata; đã thay bằng `crested-argus.jpg` |

Kiến trúc hiện hành: [CURRENT_ARCHITECTURE.md](../../CURRENT_ARCHITECTURE.md). Phần `.txt` tránh chạy nhầm các cấu hình/script cũ.

Ảnh Great Argus lưu trữ: SandyCole, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Great_Argus_Pheasant_SMTC.jpg), [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). Ảnh này chỉ là tư liệu lịch sử, không được dùng để minh họa loài Trĩ sao Việt Nam hiện tại.
