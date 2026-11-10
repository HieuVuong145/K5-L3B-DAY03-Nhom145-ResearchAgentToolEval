# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: OpenRouter (`--provider openrouter`), model `liquid/lfm-3-1.7b:free` (đặt qua `OPENROUTER_MODEL` trong `.env`), temperature 0

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline (starter) | Đo mốc ban đầu | – | case 0.70 · routing 0.80 · args 0.70 · multi 0.67 | `starter_v0/runs/v0_B_base_openrouter_20261110T181833875580.json` |
| v1 | `system_prompt.md` | Prompt starter ra lệnh đoán bừa / gửi ngay / một bước → bỏ, thay bằng clarify + xác nhận yes_no + no-tool | case 0.70 | case 0.65 · routing 0.70 · args 0.65 · multi 0.50 | `starter_v0/runs/v1_B_base_openrouter_20261110T182026119671.json` |
| v2 | `tools.yaml` | Description mơ hồ → model nhầm timeline/social_search, sai handle; thêm USE WHEN/DO NOT USE + bảng tên→handle + convention args | case 0.65 | _chờ run hợp lệ (run 18:24 bị 429 hết hạn mức ngày)_ | _TBD_ |
| v3 | `system_prompt.md` | Case multi-turn fail do không gộp args qua lượt; thêm rule multi-turn + routing table | _TBD_ | _TBD_ | _TBD_ |

**Phân tích v1 (giảm 0.70 → 0.65, ghi trung thực):** v1 sửa được đúng mục tiêu — R12 giờ hỏi xác nhận (`clarify`) thay vì `lookup`, R10 không còn đoán `sam_altman`. Nhưng khi bỏ câu "pick a well-known account like Sam Altman", model 1.7B mất luôn gợi ý duy nhất về tên→handle nên chuyển sang `social_search(query="Elon Musk")` thay vì `timeline` (R01, R05, M01, M03, M05). R11 gọi đúng `clarify` nhưng bỏ trống `response_type` (eval không tự điền default) → fail. Kết luận: chỉ sửa prompt không đủ; routing timeline vs social_search phải nằm trong description của tool (giả thuyết v2).

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

Run v0: `starter_v0/runs/v0_B_base_openrouter_20261110T181833875580.json` — 6/20 case FAIL.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R01_user_tweets_routing | wrong_tool | `social_search(query="Sam Altman", limit=1)` | Tin CỦA một người nhưng gọi search theo chủ đề; không map tên → `sama` | v2: description `timeline` = "posts FROM one account" + bảng tên→handle; `social_search` DO NOT USE cho tweet của 1 người |
| R10_missing_handle | missing_info | `timeline(screenname="sam_altman", limit=5)` | Không nói của ai nhưng tự đoán Sam Altman — đúng chỉ dẫn xấu "pick Sam Altman" của starter | v1: bỏ chỉ dẫn đoán, thiếu handle → `clarify(response_type="text")` |
| R11_missing_url | missing_info | `lookup(query="article", topic="general")` | "Bài này" không có link nhưng đi search web thay vì hỏi URL — theo chỉ dẫn "assume a likely URL" | v1: thiếu URL → `clarify`; v2: `fetch` DO NOT USE khi không có URL |
| R12_confirm_before_send | wrong_boundary | `lookup(query="bản tin", topic="news", timeframe="week")` | Yêu cầu đăng Telegram nhưng không xin xác nhận — starter bảo "just go ahead and do it" | v1: gửi/đăng → `clarify(response_type="yes_no")` trước; v2: `send` mô tả boundary `confirmed=true` |
| M03_correction_handle | wrong_arg_value | `timeline(screenname="@samaltman", limit=3)` | Không áp dụng lệnh sửa "à nhầm, của Andrej Karpathy"; handle có `@` và sai | v3: rule multi-turn "correction wins"; v2: handle không `@` + `karpathy` trong bảng |
| M05_correction_limit | wrong_arg_value | `timeline(screenname="Elon Musk", limit=3)` | limit đúng 3 nhưng truyền tên thật thay vì handle `elonmusk` | v2: convention handle + bảng tên→handle |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

- **Hết hạn mức model free (OpenRouter `liquid/lfm-3-1.7b:free`):** run v2 lúc 18:24 chạy đúng 14/20 case rồi 6 case multi-turn bị `RateLimitError 429 – free-models-per-day` → `provider_error_cases = 6`, run không hợp lệ, không dùng làm bằng chứng metric. Bằng chứng: `starter_v0/runs/v2_B_base_openrouter_20261110T182405082078.json`. Xử lý: chạy lại v2, v3 sau khi hạn mức reset (0h UTC) hoặc sau khi nạp 10 credit (mở 1000 request/ngày cho model free). 14 case đã chạy của v2 cho tín hiệu sớm: 13/14 PASS (chỉ R12 trả `response_type="text"` thay vì `yes_no`). Lưu ý: run lỗi này dùng bản nháp v2 `tools.yaml` (tools_hash `562f34dda65f`, có khai báo thêm tool mới của B); bản v2 chính thức chỉ còn phần của A (tools_hash `e4eb19c6d4b7`), nên run này chỉ là bằng chứng sự cố quota, không so sánh metric.
- **Avast HTTPS scanning chặn SSL:** `requests` báo `SSLCertVerificationError` khi gọi Tavily/Firecrawl/RapidAPI. Thử `pip-system-certs` thì làm SDK OpenAI lỗi `RecursionError`, nên gỡ ra; giải pháp cuối: bundle CA gộp certifi + chứng chỉ Avast, trỏ bằng `REQUESTS_CA_BUNDLE` trong `.env` (chỉ máy có Avast cần).

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
