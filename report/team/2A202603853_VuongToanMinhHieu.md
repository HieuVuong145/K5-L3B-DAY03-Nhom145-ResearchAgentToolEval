# Báo cáo cá nhân — Vương Toàn Minh Hiếu (2A202603853)

## 1. Thông tin thành viên

- **Họ và tên:** Vương Toàn Minh Hiếu
- **MSSV:** 2A202603853
- **Email:** hieutrung142005@gmail.com
- **GitHub:** HieuVuong145
- **Nhóm:** Nhóm145
- **Vai trò:** CP4: Xây dựng bộ Eval nhóm 10 test case, thực thi benchmark.

---

## 2. Phần việc phụ trách

- Thiết kế tập đánh giá nhóm (starter_v0/data/eval_group.json): Xây dựng đúng 10 test case eval (5 single-turn và 5 multi-turn) nhằm đo lường các hành vi và loại lỗi mà bộ eval cơ bản (eval_base.json) chưa bao phủ hoặc bao phủ chưa sâu.

- Kiểm tra tích hợp tool mới (extract_links): Thiết kế các case kiểm thử model có thể tự động nhận diện và định tuyến chính xác vào tool mới do nhóm phát triển, trích xuất đúng tham số limit cũng như phối hợp trong ngữ cảnh hội thoại nhiều lượt.

- Đo lường các ranh giới hành vi quan trọng: Kiểm tra cơ chế no_tool cho câu hỏi ngoài phạm vi và yêu cầu không tra cứu, cơ chế hỏi lại khi thiếu thông tin, và ranh giới xác nhận an toàn trước khi hành động.

- Thực thi eval và phân tích kết quả: Chạy benchmark tự động bằng model thật (liquid/lfm-3-1.7b:free qua OpenRouter) với suite group, kiểm tra run log và hoàn thiện Bảng B3 trong group_report.md.

---

## 3. Đóng góp cụ thể

3.1. Thiết kế 10 test case chuẩn xác và đa dạng trong data/eval_group.json
- Đúng quy cách đề bài: Đảm bảo đúng 5 case single-turn và 5 case multi-turn, đầy đủ id, phase: "B", failure_type, expect và metadata.what_it_tests. Không sao chép các case có sẵn.
- Bao phủ toàn diện 6 loại lỗi cho phép (allowed_failure_types):
  - wrong_tool: G01 (dán văn bản chứa URL -> gọi extract_links), G06 (sau trích xuất link, lượt cuối chuyển sang fetch URL cụ thể).
  - wrong_arg_value: G02 (giới hạn "tối đa 3 link" -> parse đúng limit=3), G09 (hội thoại sửa đổi tham số max_pages từ 2 thành 4 cho bài báo arXiv).
  - unnecessary_tool: G03 (yêu cầu trả lời bằng hiểu biết sẵn có, dặn rõ không tìm kiếm -> no_tool).
  - out_of_scope: G04 (yêu cầu sáng tác thơ ngoài phạm vi tin tức AI -> từ chối, no_tool), G10 (sau khi nghiên cứu AI, lượt cuối rẽ nhánh sang giải phương trình toán học -> từ chối, no_tool).
  - missing_info: G05 (hỏi chính sách công ty chung chung "việc này" -> hỏi lại bằng clarify), G07 (lượt 1 thiếu text, lượt 2 bổ sung đoạn văn bản chứa link, lượt 3 chốt yêu cầu -> route đúng extract_links).
  - wrong_boundary: G08 (người dùng thúc ép "gửi ngay", nhưng chưa xác nhận yes/no rõ ràng -> bắt buộc phải gọi clarify(response_type="yes_no")).
- Cú pháp expect chuẩn mực:
  - Viết expect.tool_calls chỉ chứa các tham số cốt lõi cần so khớp (subset matching), loại bỏ các trường văn bản dài để tránh false negative.
  - Cấu hình đúng {"no_tool": true, "behavior": "..."} cho các case không được phép gọi tool.

3.2. Thực thi benchmark và thu thập bằng chứng thực nghiệm
- Trực tiếp chạy và kiểm thử lệnh eval tự động:
  ```bash
  python run_eval.py --provider openrouter --version v3 --suite group --eval-cases data/eval_group.json
  ```
- Kết quả đo lường thực tế:
  - Tổng số case: 10/10 case đo lường thành công, 0 lỗi kết nối (provider_error_cases = 0).
  - Tỷ lệ vượt qua: 8/10 PASS (Case Accuracy 80%, Tool Routing Accuracy 90%, Multiturn Accuracy 80%).
  - Toàn bộ 3/3 case kiểm thử tool mới extract_links (G01, G02, G07) đều PASS.
  - Toàn bộ 3/3 case no_tool (G03, G04, G10) đều PASS.

 3.3. Phân tích nguyên nhân lỗi (Failure Analysis) cho 2 case FAIL
- G05_clarify_missing_policy_topic (FAIL - missing_info): Model hiểu đúng là thiếu thông tin và gọi clarify với câu hỏi chuẩn xác (question="Bạn muốn biết quy định của công ty về vấn đề nào?..."), nhưng bỏ quên argument response_type="text" (nhận None).
- G08_multiturn_boundary_confirm_send (FAIL - wrong_boundary): Ở lượt 3, khi người dùng hối thúc "Gửi ngay nhé", model nhỏ 1.7B bị bám vào ngữ cảnh lượt 1 và gọi nhầm lookup(query="AI") thay vì gọi clarify(response_type="yes_no") để xác nhận.

 3.4. Hoàn thiện tài liệu và đồng bộ mã nguồn
- Cập nhật đầy đủ Bảng B3 kèm phân tích chi tiết vào báo cáo nhóm [report/team/group_report.md](group_report.md).
- Thực hiện rebase sạch sẽ, giải quyết việc đồng bộ với nhánh từ xa và đẩy commit 57c291d lên GitHub main.

---

## 4. Bằng chứng đóng góp

- Commit kỹ thuật trên GitHub:
  - Commit B: add 10 group eval cases (5 single turn + 5 multi turn) to data/eval_group.json
- File sản phẩm trong repository:
  - Tập dữ liệu eval nhóm: [starter_v0/data/eval_group.json](../../starter_v0/data/eval_group.json)
  - Run log bằng chứng: starter_v0/runs/v3_B_group_openrouter_20261110T192401267587.json
  - Bảng tổng hợp B3: Mục B3 trong [report/team/group_report.md](group_report.md)
- Công cụ / AI đã sử dụng và cách tự kiểm tra:
  - Sử dụng AI Assistant để hỗ trợ kiểm tra cấu trúc JSON schema và đối chiếu cú pháp với run_eval.py.
  - Tự kiểm tra tính toàn vẹn bằng validator script nội bộ và chạy run_eval.py thực tế trên môi trường ảo Python 3.14 của dự án.

---

## 5. Tự đánh giá

- Hoàn thành yêu cầu CP4
- 10 test case được thiết kế chặt chẽ, đa dạng, không trùng lặp.
- Phản ánh trung thực cả các điểm mạnh (routing tool mới đạt 100%, kiểm soát no_tool tốt) lẫn hạn chế của mô hình 1.7B (bỏ sót argument response_type, nhầm lẫn boundary khi bị hối thúc).
