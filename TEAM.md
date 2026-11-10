# Team

## Thông tin nhóm

- Tên nhóm: Nhóm 145
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-Nhom145-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 |Trần Tuấn Anh | 2A202603909 | tuananhtr0406@gmail.com | Tanh0406 | Role A |
|   2 |Trần Hải Long | 2A202603891 | longhtr028@gmail.com | longhtr028 | Role B |
|   3 |Vương Toàn Minh Hiếu | 2A202603853 | hieutrung142005@gmail.com | HieuVuong145 | Role C |
|   4 | Nguyễn Đình Trường | 2A202603837 | truesenpai2k3@gmail.com | ngdinhtruong28 | Role D |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## TranTuanAnh-2A202603909

### Phần việc phụ trách

- Role A — Prompt & eval (CP1 baseline, CP2 vòng lặp v0→v3): chạy base eval từng version, ghi `version_log.csv`, điền bảng B1 + B2.

### Đóng góp cụ thể

- Cấu hình chạy eval với OpenRouter `liquid/lfm-3-1.7b:free` (`OPENROUTER_MODEL`, `LLM_MAX_RETRIES` trong provider), chạy preflight.
- Thiết kế 4 version tái lập được trong `artifacts/versions/v0..v3/`, mỗi version đổi đúng một file theo một giả thuyết: v1 prompt (bỏ 3 chỉ dẫn xấu, thêm clarify / xác nhận yes_no / no-tool), v2 `tools.yaml` (USE WHEN / DO NOT USE + convention args + bảng tên→handle), v3 prompt (rule multi-turn + routing table).
- Chạy run hợp lệ v0 (case 0.70) và v1 (case 0.65); phân tích trung thực vì sao v1 giảm điểm và dẫn ra giả thuyết v2.
- Viết bảng B2 (6 case FAIL của v0, loại lỗi, nguyên nhân, cách sửa), phần v0/v1 của B1 và mục 5 (sự cố quota 429, lỗi SSL do Avast).
- Viết `scripts/fill_version_log.py` sinh `version_log.csv` từ run JSON hợp lệ; thêm `.gitattributes` để hash prompt/tools tái lập được.
- Run v2/v3 chính thức do Trần Hải Long chạy (commit `21d2d79`) bằng nguyên artifact v2/v3 ở trên vì key của mình hết hạn mức model free.

### Bằng chứng

- Commit `12c0d62` (merge qua PR #1); báo cáo cá nhân `report/team/2A202603909_TranTuanAnh.md`.
- `starter_v0/artifacts/versions/`, `starter_v0/artifacts/version_log.csv`, `starter_v0/scripts/fill_version_log.py`.
- `starter_v0/runs/v0_B_base_openrouter_20261110T181833875580.json`, `starter_v0/runs/v1_B_base_openrouter_20261110T182026119671.json`, `starter_v0/runs/v2_B_base_openrouter_20261110T182405082078.json` (run lỗi quota, bằng chứng mục 5).
- `report/team/group_report.md`: B1 (v0, v1), B2, mục 5.

## HoVaTen-MSSV

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-

## VuongToanMinhHieu-2A202603853

### Phần việc phụ trách

- CP4: Team eval tests

### Đóng góp cụ thể

- 10 case (5 single-turn + 5 multi-turn) bao phủ 6 loại lỗi: wrong_tool, wrong_arg_value, unneccesary_tool, out_of_scope, missing_info, wrong_boundary.
- Kiểm tra tool mới và cơ chế no-tool
- Chạy eval thực tế với openrouter
- Viết và phân tích bảng B3

### Bằng chứng

- Commit history, các file eval_group.json, bảng 3 trong group_report.md, v3_B_...7587.json

## HoVaTen-MSSV

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
