# Gửi em, một chút nắng ☀

Trang chúc mừng 20/10 đến muộn một ngày với lời nhắn ngắn gọn, nhẹ nhàng. Có ảnh thật, bó hoa SVG rực rỡ, hiệu ứng cánh hoa, thư mở được và nhạc nền **Một chút nắng**, lưu bằng tệp WAV ngay trong repo.

## Xem trên máy

Mở `index.html` bằng trình duyệt, hoặc chạy trong thư mục này:

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Sau đó mở <http://127.0.0.1:4173>. Không cần Node.js hay cài thư viện. Nhạc được phát từ tệp trong repo, dùng được cả khi mở `index.html` trực tiếp trên máy và không có Internet.

## Đưa lên GitHub Pages khi chưa có repository

1. Đăng nhập GitHub, chọn **New repository**, đặt tên `mot-chut-nang` (hoặc tên anh thích), chọn **Public** nếu dùng GitHub Free, rồi tạo repo. Không thêm README tự động nếu đẩy bằng Git.
2. Đưa `index.html`, `styles.css`, `script.js`, `.nojekyll`, thư mục `assets`, `scripts`, `.github` và README này lên nhánh `main`. Các ảnh gốc ở ngoài thư mục `assets` không cần đưa lên.
3. Vào **Settings → Pages → Build and deployment → Source → GitHub Actions**.
4. Vào **Actions → Publish greeting to GitHub Pages → Run workflow**. Những lần đẩy thay đổi tiếp theo lên `main` sẽ tự đăng lại.
5. Khi workflow hoàn tất, liên kết trang nằm trong phần deployment `github-pages`, thường là `https://TEN-TAI-KHOAN.github.io/mot-chut-nang/`.

Nếu đã có Git trên máy, có thể dùng các lệnh sau, thay đường dẫn repo bằng repo thực tế vừa tạo:

```powershell
git init -b main
git add .
git commit -m "Create a cheerful October 20 greeting"
git remote add origin https://github.com/TEN-TAI-KHOAN/mot-chut-nang.git
git push -u origin main
```

Hướng dẫn workflow dựa trên [tài liệu GitHub Pages chính thức](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Chỉnh lời chúc / ảnh / nhạc

- Sửa lời chúc, tiêu đề và nội dung thư trong `index.html`.
- Ảnh dùng trong trang nằm trong `assets/photos/`; tên gốc và ảnh gốc được giữ nguyên ở thư mục ngoài.
- Nhạc mặc định là bản instrumental tự tạo **Một chút nắng**, nằm tại `assets/audio/mot-chut-nang.wav`. Bấm **Bật nhạc vui** hoặc mở quà/nhận hoa để nghe. Có nút tạm dừng và chỉnh âm lượng; nhạc tiếp tục phát khi xem ảnh hoặc mở thư.
- Trình duyệt cần thao tác của người xem trước khi phát nhạc. Trang chỉ tải bài hát khi bắt đầu phát. Nút tạm dừng vẫn dùng được trong lúc nhạc đang tải.
- Bản MP3 **Good to Go — Josh Woodward** vẫn được giữ như tài nguyên thay thế, không dùng làm nhạc mặc định. Tệp này theo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); nguồn và ghi công nằm tại `assets/audio/CREDITS.txt`. Khi chia sẻ lại tệp MP3, giữ phần ghi công này.
- Chạy `python scripts/create_assets.py` để tạo lại bó hoa và bản nhạc **Một chút nắng**; không cần chạy lệnh này khi đăng trang.
- Chạy `python scripts/build_site.py` để tạo thư mục `dist` chỉ gồm tệp website. GitHub Actions chạy lệnh này tự động.
- Trang hỗ trợ màn hình nhỏ, bàn phím, đọc ảnh lớn, phím trái/phải, Escape và tùy chọn giảm chuyển động của thiết bị.

Toàn bộ ảnh, font hệ thống, nội dung và nhạc hoạt động từ tệp trong repo bằng đường dẫn tương đối. Trang dùng được ở GitHub Pages project URL và khi mở tệp HTML trực tiếp. Không nhúng video, không dùng dịch vụ phát nhạc ngoài và không gửi ảnh tới dịch vụ ngoài.

Nguồn nhạc và giấy phép: [Good to Go trên website của Josh Woodward](https://www.joshwoodward.com/song/GoodtoGo).
