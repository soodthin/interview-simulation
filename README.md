# Mô Phỏng Phòng Phỏng Vấn Esco AV - Thái Đỗ Thịnh

Dự án mô phỏng buổi phỏng vấn vị trí **IT Support & AV Systems Fresher** tại **Esco AV Vietnam** với ứng viên **Thái Đỗ Thịnh** (thời lượng 8 phút 38 giây).

---

## 🌟 Tính Năng Nổi Bật

1. **Web Animation Đồ Họa 60 FPS (HTML5 Canvas Engine)**:
   - **Bố cục 3 Card Đối Xứng**:
     - **Interviewer (Trái)**: Hoạt họa cử động mắt, miệng đồng bộ giọng nói, hiệu ứng đèn chiếu Cyan.
     - **Esco Smart Collab Display (Giữa)**: Hiển thị hồ sơ năng lực ứng viên, đổi slide thời gian thực theo 14 câu hỏi, tích hợp Audio Visualizer phân tích phổ âm thanh thực tế từ Web Audio API.
     - **Thái Đỗ Thịnh (Phải)**: Tạo hình kính vuông công nghệ, áo polo viền mint, chuyển động khuôn miệng theo giọng nói, viền sáng Emerald.
   - **Góc Quay Camera Điện Ảnh**: Chế độ tự động zoom mượt mà theo người đang nói (`Tự động zoom`), góc toàn cảnh (`Toàn cảnh`), hoặc góc cận từng người.

2. **Phụ Đề Video Podcast Cỡ Lớn (Broadcast Lower-Third)**:
   - Hiển thị cố định trên màn hình (Screen-Space HUD), không bao giờ bị lệch hay cắt khi camera zoom.
   - Định danh người nói tinh gọn chuẩn podcast: `[ ● NGƯỜI PHỎNG VẤN ]` (Cyan) và `[ ● THÁI ĐỖ THỊNH ]` (Emerald) với chấm tín hiệu nảy theo âm lượng.
   - Phụ đề song ngữ: Tiếng Anh cỡ lớn (`23px Bold`), Tiếng Việt neon (`18px Semi-Bold`).
   - Hỗ trợ chuyển đổi nhanh: **Song ngữ**, **Chỉ EN (27px Bold)**, **Chỉ VI (27px Bold)**.

3. **Điều Khiển & Tìm Kiếm 14 Phân Cảnh (Chapters)**:
   - Thanh tìm kiếm câu hỏi / từ khóa kỹ năng theo thời gian thực.
   - Nhảy nhanh đến từng câu hỏi với timestamp chính xác.
   - Phím tắt tiện lợi: `Space` (Phát / Dừng), `← / →` (Tua ±10 giây).

4. **Ghi & Xuất Video MP4 Trực Tiếp**:
   - Tích hợp MediaRecorder API 60 FPS thu trực tiếp Canvas và luồng âm thanh master tải về máy tức thì.

---

## 🚀 Hướng Dẫn Sử Dụng Cục Bộ (Local)

Chạy máy chủ cục bộ bằng Python:
```bash
python serve.py
```
Sau đó mở trình duyệt tại: **`http://localhost:8080`**.

---

## 🌐 Triển Khai Lên GitHub Pages (GitHub Actions)

Dự án đã được tích hợp sẵn quy trình CI/CD tự động trong `.github/workflows/deploy.yml`:
1. Push mã nguồn lên branch `main`.
2. Vào **Settings** > **Pages** trên repository GitHub:
   - **Source**: Chọn `GitHub Actions`.
3. GitHub Actions sẽ tự động kích hoạt workflow và xuất bản trang web trực tiếp lên domain:
   ```
   https://<username>.github.io/<repository-name>/
   ```
