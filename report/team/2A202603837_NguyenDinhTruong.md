# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Nguyễn Đình Trường
- MSSV: 2A202603837
- Email: truong.ngdinh2003@gmail.com
- Github: ngdinhtruong28
- Nhóm: Nhóm 145 - L3B
- Vai trò: Role D - UI & Báo cáo

## 2. Phần việc phụ trách
- Làm UI Streamlit + mở link qua Cloudflare
- Chạy chat.py 3 lượt: yêu cầu thường / thiếu thông tin rồi bổ sung / yêu cầu gửi Telegram
- Viết Phần A báo cáo + bảng B4
## 3. Đóng góp cụ thể
- Xây dựng giao diện người dùng (UI): Phát triển giao diện ứng dụng bằng Streamlit, hỗ trợ người dùng nhập câu hỏi nghiên cứu, tương tác với Research Agent và theo dõi kết quả trả về.
- Tích hợp Research Agent: Kết nối giao diện với các thành phần xử lý Agent, Provider và Tool, hỗ trợ quá trình tiếp nhận yêu cầu, gọi công cụ và tổng hợp kết quả.
- Hiển thị quá trình thực thi: Bổ sung khả năng theo dõi execution trace, bao gồm trạng thái xử lý, các tool được gọi, tham số đầu vào, kết quả trả về và trạng thái hoàn thành.
- Triển khai và chia sẻ ứng dụng: Cấu hình Streamlit để chạy trên local, sử dụng Cloudflare Quick Tunnel tạo public URL giúp các thành viên truy cập và kiểm thử ứng dụng từ xa.
- Tài liệu hóa: Bổ sung hướng dẫn cài đặt dependencies, chạy ứng dụng, tạo public link và các lưu ý khi chia sẻ ứng dụng.

## 4. Bằng chứng

- File/commit/PR:
    + starter_v0/app.py: Giao diện Streamlit của Research Agent.
    + starter_v0/requirements.txt: Khai báo các thư viện cần thiết cho ứng dụng.
    + starter_v0/transcripts: Xuất transcript khi chat với Agent
    + report/team: Phần báo cáo A và bảng B4

- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
    + ChatGPT: Hỗ trợ phân tích cấu trúc project, đề xuất cách tích hợp Streamlit, hướng dẫn xử lý lỗi và tối ưu quy trình triển khai.
    + Streamlit: Xây dựng và chạy giao diện ứng dụng web.
    + Cloudflare Tunnel: Tạo public URL để kiểm thử ứng dụng từ bên ngoài máy local.
    + VS Code / PowerShell: Chỉnh sửa source code, cài đặt dependencies, chạy ứng dụng và kiểm tra log.
- Cách tự kiểm tra:
1. Chạy ứng dụng bằng python -m streamlit run app.py.
2. Truy cập http://localhost:8501 để kiểm tra giao diện.
3. Thử nhập câu hỏi và kiểm tra khả năng tương tác với Research Agent.
4. Theo dõi execution trace để kiểm tra các bước gọi Tool và kết quả trả về.
5. Tạo Cloudflare Tunnel và truy cập public URL trên trình duyệt hoặc thiết bị khác để kiểm tra khả năng chia sẻ ứng dụng.
## 5. Tự đánh giá
Qua quá trình thực hiện, mình hiểu rõ hơn về cấu trúc và cách hoạt động của Research Agent, từ System Prompt, cách Agent tiếp nhận và xử lý yêu cầu đến cơ chế gọi Tool và trả về kết quả. Mình cũng học được cách kết nối các thành phần này với giao diện Streamlit và sử dụng AI để hỗ trợ phát triển. Tuy vẫn còn một số phần cần cải thiện, nhưng mình đã hiểu rõ hơn về cách xây dựng và vận hành một hệ thống AI Agent thực tế.
