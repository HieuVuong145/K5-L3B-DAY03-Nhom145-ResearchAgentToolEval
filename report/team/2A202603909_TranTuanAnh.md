# Báo cáo cá nhân — Trần Tuấn Anh (2A202603909)

## 1. Thông tin thành viên

- Họ tên: Trần Tuấn Anh
- MSSV: 2A202603909
- Email: tuananhtr0406@gmail.com
- GitHub: Tanh0406 (commit trong repo được đẩy từ tài khoản git `HiImTanh` — tran37856@gmail.com)
- Nhóm: Nhóm 145 — L3B
- Vai trò: **Role A — Prompt & eval** (CP1 baseline, CP2 vòng lặp tối ưu v0→v3)

## 2. Phần việc phụ trách

- Chạy baseline v0 và các version tối ưu v1, v2, v3 trên bộ `data/eval_base.json`, mỗi version sửa **một** chỗ trong `system_prompt.md` hoặc `tools.yaml` theo một giả thuyết.
- Ghi `starter_v0/artifacts/version_log.csv`.
- Điền bảng B1 (Version Evidence) và B2 (Failure Analysis) trong `report/team/group_report.md`.

## 3. Đóng góp cụ thể

### 3.1. Cấu hình chạy eval bằng provider thật
- Chốt cùng nhóm provider OpenRouter, model `liquid/lfm-3-1.7b:free`; sửa `providers/openrouter_provider.py` để đọc model từ biến `OPENROUTER_MODEL` (eval, `chat.py`, UI, preflight dùng chung một model) và `providers/openai_provider.py` để đọc số lần retry từ `LLM_MAX_RETRIES` (endpoint free hay trả 429/5xx).
- Chạy `scripts/preflight_provider.py --provider openrouter` → `OK provider=openrouter model=liquid/lfm-3-1.7b:free`, model trả structured `tool_calls`.

### 3.2. Thiết kế vòng lặp version có kiểm soát
- Tách mỗi version thành một thư mục `starter_v0/artifacts/versions/vN/{system_prompt.md, tools.yaml}` và chạy bằng `--system-prompt/--tools`, để version nào cũng tái lập được; `artifacts/` gốc = v3.
- Mỗi version chỉ đổi **một** file → hash khác đúng một phía, nên thay đổi metric quy được về đúng giả thuyết đó:

| Version | File đổi | prompt_hash | tools_hash | Giả thuyết |
|---|---|---|---|---|
| v0 | (starter) | eb1c8179815b | e69bc53ed884 | Đo mốc |
| v1 | `system_prompt.md` | d2415095085c | e69bc53ed884 | Prompt starter cố tình ra lệnh "đoán thay vì hỏi" (mặc định Sam Altman, đoán URL), "gửi ngay không cần chờ", "luôn một bước" → gây lỗi missing_info / wrong_boundary. Bỏ đi, thay bằng: thiếu handle/URL → `clarify(text)`, gửi/đăng → `clarify(yes_no)` trước, ngoài phạm vi → không gọi tool, cần nhiều nguồn → gọi nhiều tool |
| v2 | `tools.yaml` | d2415095085c | e4eb19c6d4b7 | Description mơ hồ ("Lấy các bài đăng gần đây", "Tìm trên mạng xã hội") → model nhầm `timeline`/`social_search`, sai handle, sai args. Viết lại mỗi tool: làm gì / USE WHEN / DO NOT USE + convention args ngay trong parameter (handle không `@`, bảng tên→handle, `query` chỉ chủ đề, `topic=news`, `hôm nay→day`, `phổ biến→Top`, `send` chỉ khi `confirmed=true`) |
| v3 | `system_prompt.md` | 8f61986f30fb | e4eb19c6d4b7 | Case multi-turn fail vì không gộp args qua các lượt → thêm rule multi-turn (chỉ xử lý lượt cuối, carry args, lệnh sửa thắng), routing table, bảng tên→handle |

### 3.3. Chạy eval và phân tích lỗi
- Chạy v0 và v1 hợp lệ (`provider_error_cases = 0`, `measured_cases = total_cases = 20`):
  - v0: case 0.70 · routing 0.80 · args 0.70 · multi 0.67.
  - v1: case 0.65 · routing 0.70 · args 0.65 · multi 0.50.
- **B2:** đọc `failures` / `actual_tool_calls` của 6 case FAIL ở v0, gán loại lỗi và nối mỗi lỗi với chỉ dẫn xấu cụ thể của starter (vd R10 tự gọi `timeline("sam_altman")` đúng theo câu "pick a well-known account like Sam Altman"; R12 không xin xác nhận vì "just go ahead and do it").
- **Phân tích v1 giảm điểm (ghi trung thực trong B1):** v1 sửa được R12 (giờ hỏi xác nhận) và R10 không còn đoán người, nhưng làm hỏng R05, M01: câu "pick Sam Altman" tuy xấu nhưng là gợi ý duy nhất cho model biết "tweet CỦA một người → tool theo tài khoản"; bỏ đi trong khi `tools.yaml` vẫn mơ hồ thì model 1.7B chuyển sang `social_search("Elon Musk")`. Kết luận dẫn tới giả thuyết v2: routing phải nằm trong description của tool, không chỉ trong prompt.
- Lần chạy v2 đầu tiên bị `429 free-models-per-day` ở 6/20 case → run không hợp lệ; giữ lại `runs/v2_B_base_openrouter_20261110T182405082078.json` làm bằng chứng sự cố cho mục 5, không dùng làm metric.

### 3.4. Công cụ ghi version log và tái lập hash
- Viết `starter_v0/scripts/fill_version_log.py`: sinh `version_log.csv` trực tiếp từ run JSON (chọn run **hợp lệ** mới nhất của mỗi version, metric_before = metric của version trước) → không gõ tay số liệu.
- Thêm `.gitattributes` đánh dấu file artifact `-text`: hash được tính theo byte, file v0 là CRLF còn các file khác là LF, nên phải giữ nguyên byte khi commit/checkout để `prompt_hash`/`tools_hash` trong run JSON tái lập được trên mọi máy (đã kiểm tra hash của bản commit khớp run).

### 3.5. Xử lý sự cố (mục 5 group report)
- Hết hạn mức model free → dừng pipeline, không để run lỗi lẫn vào số liệu; viết handoff để thành viên khác chạy tiếp bằng key còn hạn mức.
- Avast HTTPS scanning làm `requests` lỗi `SSLCertVerificationError`; `pip-system-certs` lại làm SDK OpenAI lỗi `RecursionError` → dùng CA bundle gộp certifi + chứng chỉ Avast qua `REQUESTS_CA_BUNDLE`.

### 3.6. Phần hoàn thiện do thành viên khác chạy
- Run v2 và v3 chính thức do **Trần Hải Long** chạy bằng key OpenRouter của bạn ấy (commit `21d2d79`), dùng **nguyên** artifact v2/v3 mình đã chuẩn bị (artifact_version trong run: `v2+pd2415095085c+te4eb19c6d4b7` và `v3+p8f61986f30fb+te4eb19c6d4b7`, khớp hash file mình commit). Long cũng viết phân tích v2/v3 trong B1 và mục 7 Reflection.
- Kết quả: v2 case 0.85 · routing 1.00 (giả thuyết v2 đúng — mọi case tweet của một người đã route sang `timeline` với handle đúng); v3 case 0.90 nhưng giả thuyết chính (M03, sửa tên ở lượt sau) **chưa được xác nhận** — mức tăng đến từ R11.

## 4. Bằng chứng

- Commit / PR:
  - `12c0d62` — "A: versioned prompt/tools v0-v3, v0/v1 eval runs, version log, B1/B2" (merge vào `main` qua PR #1, `c47ecd7`).
- File:
  - `starter_v0/artifacts/versions/v0..v3/`, `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`
  - `starter_v0/runs/v0_B_base_openrouter_20261110T181833875580.json` (v0, hợp lệ)
  - `starter_v0/runs/v1_B_base_openrouter_20261110T182026119671.json` (v1, hợp lệ)
  - `starter_v0/runs/v2_B_base_openrouter_20261110T182405082078.json` (v2 lần 1, lỗi 429 — bằng chứng mục 5)
  - `starter_v0/artifacts/version_log.csv`, `starter_v0/scripts/fill_version_log.py`, `.gitattributes`
  - `starter_v0/providers/openrouter_provider.py`, `starter_v0/providers/openai_provider.py`
  - `report/team/group_report.md`: dòng provider/model mục 1, B1 (v0, v1 + phân tích v1), B2, mục 5
- AI / công cụ đã dùng và cách tự kiểm tra:
  - **Claude Code (Claude Opus 5.5)**: hỗ trợ đọc hiểu repo, viết nội dung `system_prompt.md`/`tools.yaml` theo từng giả thuyết, viết `fill_version_log.py`, chạy eval, đọc run JSON và nháp phân tích lỗi.
  - Cách tự kiểm tra:
    - Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases` (script `fill_version_log.py` tự loại run không hợp lệ).
    - Đối chiếu từng case FAIL trong B2 với `actual_tool_calls` và `failures` trong run JSON, không dựa vào cảm giác.
    - Kiểm tra mỗi version chỉ đổi đúng một hash so với version trước; kiểm tra hash của file đã commit khớp hash ghi trong run.
    - `pytest tests/test_tool_contract.py` xanh với `tools.yaml` của từng version.
    - Quét `runs/*.json` để chắc không có API key trước khi commit; không commit `.env`.

## 5. Tự đánh giá

- **Đã làm được:** thiết kế đủ 4 version, mỗi version một giả thuyết và một file thay đổi; v0, v1 hợp lệ; B2 phân tích đủ 6 lỗi của v0 có nguyên nhân cụ thể; ghi nhận trung thực v1 làm giảm điểm và rút ra giả thuyết cho v2; version log sinh tự động từ run thật.
- **Chưa tự làm trọn:** không tự chạy được run chính thức v2, v3 vì hết hạn mức model free; phần này do bạn Long hoàn thiện bằng artifact mình đã chuẩn bị.
- **Điều học được:**
  - Sửa "đúng ý" chưa chắc tăng điểm: một chỉ dẫn xấu có thể đang gánh một hành vi tốt (v1).
  - Với model nhỏ, việc **chọn tool nào** nên mô tả ngay trong `tools.yaml` cạnh tham số — v2 là thay đổi hiệu quả nhất (0.65 → 0.85, routing 1.00); còn prompt hợp với **hành vi/boundary** (hỏi lại, xin xác nhận).
  - Rule chung kiểu "corrections win" không đủ cho model 1.7B (M03 vẫn fail ở v3); vòng sau nên thử ví dụ few-shot và đặt `response_type` của `clarify` thành required.
  - Phải đo trước–sau và chỉ dùng run hợp lệ; quota/provider là rủi ro thật cần lên kế hoạch khi cả nhóm dùng chung model free.
