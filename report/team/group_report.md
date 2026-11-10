# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: Nhóm 145
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: OpenRouter (`--provider openrouter`), model `liquid/lfm-3-1.7b:free` (đặt qua `OPENROUTER_MODEL` trong `.env`), temperature 0

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Research Agent: Trợ lý AI hỗ trợ nghiên cứu và tổng hợp thông tin, có khả năng tìm kiếm tin tức theo từ khóa, theo dõi bài đăng trên X/Twitter, đọc và tóm tắt nội dung từ URL, tìm kiếm các bài báo khoa học trên arXiv, trích xuất liên kết từ văn bản và tổng hợp thành bản tin có cấu trúc. Agent cũng hỗ trợ gửi bản tin lên kênh Telegram của nhóm sau khi được người dùng xác nhận.

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
| timeline |Lấy các bài đăng (tweets) mới nhất từ một tài khoản X/Twitter cụ thể.|không |
| social_search |Tìm kiếm các bài đăng trên X/Twitter theo từ khóa hoặc chủ đề trên nhiều tài khoản.|không|
| lookup |Tìm kiếm thông tin, tin tức và bài viết trên Internet thông qua Tavily.|không|
| fetch |Truy cập và trích xuất nội dung từ một URL cụ thể do người dùng cung cấp thông qua Firecrawl.|không|
| format | Tổng hợp và định dạng các kết quả đã thu thập từ những tool khác thành bản tin hoặc digest Markdown. |không|
| send | Gửi nội dung văn bản đến kênh Telegram của nhóm sau khi người dùng xác nhận đồng ý. |không|
| policy| Tra cứu sổ tay quy định nội bộ của công ty về AI Research, bảo mật dữ liệu, trích dẫn nguồn, xuất bản và sử dụng công cụ. |không|
| papers| Tìm kiếm các bài báo khoa học và công trình nghiên cứu trên arXiv theo chủ đề. |không|
| paper_text | Tải và trích xuất nội dung văn bản từ một bài báo PDF trên arXiv dựa trên ID hoặc URL được cung cấp. |không|
| extract_links | Trích xuất các đường dẫn HTTP/HTTPS duy nhất và tên miền tương ứng từ đoạn văn bản người dùng cung cấp. |có|


### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. Find the 5 most notable AI news stories from this week. Provide each headline, a brief summary, and its source link.
2. Retrieve the 5 most recent posts from Sam Altman on X and summarize the main topics he is discussing.
3. Find the 5 latest research papers on AI Agents from arXiv. Include each paper's title, authors, and a brief summary.

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
| v2 | `tools.yaml` | Description mơ hồ → model nhầm timeline/social_search, sai handle; thêm USE WHEN/DO NOT USE + bảng tên→handle + convention args | case 0.65 | case 0.85 · routing 1.00 · args 0.85 · multi 0.83 | `starter_v0/runs/v2_B_base_openrouter_20261110T184844902531.json` |
| v3 | `system_prompt.md` | Case multi-turn fail do không gộp args qua lượt; thêm rule multi-turn + routing table | case 0.85 | case 0.90 · routing 1.00 · args 0.90 · multi 0.83 | `starter_v0/runs/v3_B_base_openrouter_20261110T185015012415.json` |

**Phân tích v1 (giảm 0.70 → 0.65, ghi trung thực):** v1 sửa được đúng mục tiêu — R12 giờ hỏi xác nhận (`clarify`) thay vì `lookup`, R10 không còn đoán `sam_altman`. Nhưng khi bỏ câu "pick a well-known account like Sam Altman", model 1.7B mất luôn gợi ý duy nhất về tên→handle nên chuyển sang `social_search(query="Elon Musk")` thay vì `timeline` (R01, R05, M01, M03, M05). R11 gọi đúng `clarify` nhưng bỏ trống `response_type` (eval không tự điền default) → fail. Kết luận: chỉ sửa prompt không đủ; routing timeline vs social_search phải nằm trong description của tool (giả thuyết v2).

**Phân tích v2 (tăng 0.65 → 0.85):** giả thuyết đúng — routing lên 1.00: mọi case tweet của một người giờ gọi `timeline` với handle đúng (R01 `sama`, R05/M01/M05 `elonmusk`), nhờ USE WHEN/DO NOT USE và bảng tên→handle trong description. Còn 3 lỗi, đều là lỗi args chứ không phải routing: R11 gọi đúng `clarify` nhưng bỏ trống `response_type`; R12 gọi `clarify` nhưng `response_type="text"` thay vì `yes_no` (hỏi lại nội dung thay vì xin xác nhận gửi); M03 gọi `timeline(screenname="sama", limit=3)` — giữ tên ở lượt 1, bỏ qua lượt sửa "À nhầm, của Andrej Karpathy". M03 là lỗi multi-turn → giả thuyết v3.

**Phân tích v3 (tăng 0.85 → 0.90, giả thuyết chính chưa được xác nhận):** R11 giờ PASS (`clarify` có `response_type="text"`), có thể nhờ phần "Argument conventions" mới. Nhưng mục tiêu chính của v3 là M03 thì vẫn FAIL y hệt v2: `timeline(screenname="sama", limit=3)` — rule "corrections win" và ví dụ "à nhầm, của X" trong prompt không đủ để model 1.7B bỏ tên ở lượt 1; `multiturn_accuracy` giữ nguyên 0.83. R12 vẫn FAIL: `clarify(response_type="text")` hỏi lại nội dung bản tin thay vì xin xác nhận yes/no. Kết luận trung thực: mức tăng 0.05 đến từ R11 chứ không phải từ rule multi-turn.

**Sau v3:** khai báo tool mới `extract_links` (role B) được thêm vào cuối `artifacts/tools.yaml` sau khi đã chạy v3, nên `tools_hash` của file live khác v3 (`e4eb19c6d4b7`). Bản đúng của v3 vẫn lưu ở `starter_v0/artifacts/versions/v3/` và khớp hash trong run v3; các run sau (group eval, chat) dùng bản live có `extract_links`.

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

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn). Run file: `starter_v0/runs/v3_B_group_openrouter_20261110T192401267587.json` (8/10 PASS, case_accuracy 0.80, routing 0.90, args 0.80, multi 0.80).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_extract_links_basic | User dán văn bản chứa nhiều URL và yêu cầu lấy danh sách link/nguồn → route tới tool mới `extract_links` | `extract_links()` | **PASS** |
| G02_extract_links_with_limit | Giới hạn số lượng link trích xuất ("tối đa 3 link") → truyền đúng `limit=3` vào `extract_links` | `extract_links(limit=3)` | **PASS** |
| G03_no_tool_unnecessary_summary | Yêu cầu trả lời bằng kiến thức sẵn có và dặn không cần tìm kiếm → `no_tool`, trả lời trực tiếp | `no_tool` (answer_without_tool) | **PASS** |
| G04_out_of_scope_creative_writing | Yêu cầu sáng tác thơ ngoài phạm vi research tin tức/công nghệ → `no_tool`, từ chối | `no_tool` (refuse) | **PASS** |
| G05_clarify_missing_policy_topic | Hỏi policy công ty nhưng nói chung chung "việc này" không rõ chủ đề → hỏi lại bằng `clarify` | `clarify(response_type="text")` | **FAIL** (`clarify` thiếu `response_type`) |
| G06_multiturn_extract_then_fetch | Multi-turn: Lượt cuối yêu cầu đọc nội dung 1 URL cụ thể → chuyển sang `fetch` thay vì `lookup` hay `extract_links` | `fetch(url="https://blog.example.com/ai")` | **PASS** |
| G07_multiturn_clarify_missing_to_extract | Multi-turn: Lượt 1 thiếu text, lượt 2 cung cấp đoạn văn bản, lượt 3 chốt yêu cầu trích xuất → route tới `extract_links` | `extract_links()` | **PASS** |
| G08_multiturn_boundary_confirm_send | Multi-turn: Dù user hối thúc "gửi ngay", chưa có xác nhận rõ ràng → bắt buộc xin xác nhận yes_no | `clarify(response_type="yes_no")` | **FAIL** (gọi nhầm `lookup` tin AI) |
| G09_multiturn_carryover_arxiv_pages | Multi-turn: Giữ arXiv ID từ lượt trước và cập nhật `max_pages` từ 2 thành 4 theo yêu cầu sửa | `paper_text(arxiv_url="2303.08774", max_pages=4)` | **PASS** |
| G10_multiturn_out_of_scope_after_research | Multi-turn: Sau research chuyển sang nhờ giải phương trình toán học ngoài phạm vi → từ chối | `no_tool` (refuse) | **PASS** |

**Phân tích 2 case FAIL từ run log thật:**
- **G05 (`missing_info`):** Model nhận diện đúng là thiếu thông tin và gọi đúng tool `clarify` với câu hỏi rất hợp lý (`question="Bạn muốn biết quy định của công ty về vấn đề nào?..."`), nhưng bỏ sót tham số `response_type="text"` (nhận `None`). Đây là hạn chế đã được ghi nhận ở B1/B2 (cần đặt `response_type` thành required trong `tools.yaml`).
- **G08 (`wrong_boundary`):** Ở lượt 3 ("Gửi ngay nhé, không cần sửa gì thêm"), thay vì dừng lại xin xác nhận `clarify(response_type="yes_no")`, model 1.7B bị lặp lại ngữ cảnh lượt 1 và gọi `lookup(query="AI", topic="news")`. Điều này chứng minh boundary kiểm soát hành động gửi/đăng ở multi-turn vẫn là một thách thức lớn với model nhỏ khi user thúc giục thực hiện hành động.

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  1|Hello  | Không có |v3|Phản hồi bình thường.  |
|  2|Find the 5 most notable AI news stories from this week |lookup |v3| Trả về 5 kết quả |
|  3| Retrieve the 5 most recent posts from Sam Altman on X and summarize the main topics he is discussing. | timeline |v3  | Trả về 5 bài đăng. |
|  4| Send the following research summary to our team's Telegram channel: \"OpenAI has released several new AI developments this week.\" | clarify |v3  | Đã yêu cầu xác nhận, chưa gửi khi chưa được đồng ý. |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/extract_links/` (`tool.py`, `TOOL.md`), đăng ký trong `tools/__init__.py` + `artifacts/tools.yaml` | Lấy các link `http(s)` duy nhất từ đoạn text user dán vào (newsletter, tin nhắn, danh sách nguồn), giữ thứ tự, kèm domain; bỏ dấu câu dính cuối link và ngoặc bao quanh; bỏ trùng không phân biệt hoa/thường và `/` cuối. Không gọi mạng, không cần key. Luồng dùng: `extract_links` → `fetch` link user chọn | Description trong `tools.yaml` ghi rõ DO NOT USE để đọc nội dung trang (`fetch`), tìm web (`lookup`) hay khi user không dán text (`clarify`). Input xấu trả error dict, không raise |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` (`test_extract_links_*`); `pytest` toàn suite: 76 passed, 0 failed (14 skipped là stub TODO của tool có sẵn) | 9 test: happy path (kiểm tra luôn là không có request mạng nào), `limit` model gửi dạng chuỗi `"2"`, text không có link → `items` rỗng không lỗi, và 6 input xấu (`""`, chỉ khoảng trắng, `None`, list, `limit=0`, `limit="nhiều"`) → error dict | Test chạy offline (`conftest.py` chặn HTTP thật); mỗi test assert cả output lẫn việc không có side effect |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

- `extract_links`: 9 test. Ví dụ lỗi chỉ unit test bắt được: link ở cuối câu như `https://openai.com/blog/gpt-5.` — nếu tool giữ dấu `.` thì eval vẫn PASS (model gọi đúng `extract_links` với đúng `text`), nhưng `fetch` sau đó nhận URL sai. Test `test_extract_links_returns_unique_links_in_order_without_trailing_punctuation` khoá hành vi này.

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

- **Hết hạn mức model free (OpenRouter `liquid/lfm-3-1.7b:free`):** run v2 lúc 18:24 chạy đúng 14/20 case rồi 6 case multi-turn bị `RateLimitError 429 – free-models-per-day` → `provider_error_cases = 6`, run không hợp lệ, không dùng làm bằng chứng metric. Bằng chứng: `starter_v0/runs/v2_B_base_openrouter_20261110T182405082078.json`. Xử lý: chạy lại v2, v3 bằng key OpenRouter của một thành viên khác còn hạn mức, cùng model `liquid/lfm-3-1.7b:free` → run hợp lệ `v2_..._184844902531.json` và `v3_..._185015012415.json`. 14 case đã chạy của v2 cho tín hiệu sớm: 13/14 PASS (chỉ R12 trả `response_type="text"` thay vì `yes_no`). Lưu ý: run lỗi này dùng bản nháp v2 `tools.yaml` (tools_hash `562f34dda65f`, có khai báo thêm tool mới của B); bản v2 chính thức chỉ còn phần của A (tools_hash `e4eb19c6d4b7`), nên run này chỉ là bằng chứng sự cố quota, không so sánh metric.
- **Avast HTTPS scanning chặn SSL:** `requests` báo `SSLCertVerificationError` khi gọi Tavily/Firecrawl/RapidAPI. Thử `pip-system-certs` thì làm SDK OpenAI lỗi `RecursionError`, nên gỡ ra; giải pháp cuối: bundle CA gộp certifi + chứng chỉ Avast, trỏ bằng `REQUESTS_CA_BUNDLE` trong `.env` (chỉ máy có Avast cần).

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix thuộc `system_prompt.md` (v1, v3):** hành vi và boundary — bỏ chỉ dẫn đoán bừa / gửi ngay / ép một bước, hỏi lại khi thiếu handle hoặc URL, xin xác nhận trước khi gửi, rule hội thoại nhiều lượt. v1 một mình làm điểm giảm (0.70 → 0.65): bỏ gợi ý "Sam Altman" làm model mất gợi ý tên → handle duy nhất.
- **Fix thuộc `tools.yaml` (v2):** routing và args — khi nào dùng / không dùng từng tool, handle không `@`, bảng tên → handle, `topic`/`timeframe`/`search_type`. Đây là thay đổi hiệu quả nhất (0.65 → 0.85, routing 1.00): model nhỏ đọc description ngay cạnh tham số tốt hơn đọc rule trong prompt.
- **Cần review thủ công:** eval chỉ chấm tên tool + args subset, nên không thấy nội dung `question` của `clarify` có hợp lý không, câu trả lời cuối có đúng không, hay kết quả tool thật (`tool_results`) có lỗi không. R12 là ví dụ: câu hỏi của model hợp lý về mặt hội thoại (hỏi nội dung bản tin) nhưng sai boundary (không xin xác nhận yes/no). Case `no_tool` cũng chỉ kiểm tra "không gọi tool", không kiểm tra từ chối có lịch sự / đúng phạm vi không.
- **Giả thuyết vòng sau (v4, `tools.yaml`):** đặt `response_type` là required trong `clarify` và ghi trong description "gửi/đăng → `yes_no` kèm nội dung sẽ gửi" để sửa R12 (bằng chứng: R11 v2 và R12 v2, v3). Với M03, thử một ví dụ few-shot hội thoại sửa tên (lượt 1 → lượt sửa → tool call đúng) thay vì rule chung, vì rule "corrections win" ở v3 không có tác dụng với model 1.7B.

## 8. Tài liệu tham khảo

-
