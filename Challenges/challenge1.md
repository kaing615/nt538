# Challenge 1 - Tính tổng các số nguyên dương chia hết cho 3

## Mục tiêu

Chương trình đọc một file đầu vào, bỏ qua dòng đầu tiên là `n`, sau đó xử lý phần dữ liệu còn lại để tính tổng các giá trị thỏa mãn đồng thời:

- Có thể chuyển sang số thực bằng `float`.
- Lớn hơn `0`.
- Là số nguyên, tức `val.is_integer() == True`.
- Chia hết cho `3`.

Code dùng `multiprocessing.Pool` để chia file thành nhiều đoạn byte và xử lý song song.

## Ý tưởng thuật toán

1. Đọc dòng đầu để lấy `n`.
2. Xác định vị trí bắt đầu dữ liệu sau dòng đầu tiên.
3. Chia phần còn lại của file thành `16` đoạn theo byte.
4. Điều chỉnh điểm cuối mỗi đoạn để không cắt giữa một token số.
5. Mỗi process đọc đoạn được giao, tách token bằng `split()`, kiểm tra điều kiện và tính tổng cục bộ.
6. Process chính cộng tất cả tổng cục bộ để ra kết quả cuối.

## Phân tích theo dòng

| Dòng | Phân tích |
|---:|---|
| 1 | Import module `multiprocessing` để tạo pool process xử lý song song. |
| 2 | Import `os`, nhưng trong file hiện tại không dùng; có thể bỏ nếu muốn gọn code. |
| 4 | Khai báo hàm `worker_task`, đây là hàm chạy trong từng process con. |
| 5 | Giải nén `args` thành đường dẫn file, byte bắt đầu và byte kết thúc của đoạn cần xử lý. |
| 6 | Khởi tạo tổng cục bộ `total = 0`. |
| 8 | Mở file ở chế độ text để process con đọc phần dữ liệu của mình. |
| 9 | Di chuyển con trỏ file đến `start_byte`. |
| 10 | Đọc đúng số ký tự từ `start_byte` đến `end_byte`. |
| 12 | Tách đoạn đọc được thành các token theo khoảng trắng. |
| 13 | Bắt đầu khối `try` để tránh lỗi nếu token không chuyển được sang số. |
| 14 | Chuyển token sang `float`, cho phép xử lý cả dạng `3`, `3.0`. |
| 15 | Kiểm tra số dương và là số nguyên. |
| 16 | Ép về `int` để kiểm tra chia hết và cộng tổng. |
| 17 | Kiểm tra số nguyên có chia hết cho `3` không. |
| 18 | Nếu đạt điều kiện thì cộng vào tổng cục bộ. |
| 19-20 | Nếu token không hợp lệ thì bỏ qua và tiếp tục. |
| 22 | Trả tổng cục bộ về process chính. |
| 25 | Hàm `MAIN` là entry point được hệ thống chấm gọi. |
| 26 | Mở file input ở chế độ text. |
| 27 | Đọc dòng đầu tiên, giả định đây là số lượng phần tử `n`. |
| 28-29 | Nếu file rỗng thì trả `0`. |
| 30 | Chuyển dòng đầu sang số nguyên `n`. |
| 31-32 | Nếu `n == 0`, không có dữ liệu cần tính nên trả `0`. |
| 34 | Lưu vị trí bắt đầu phần dữ liệu thật sau dòng đầu. |
| 35 | Di chuyển con trỏ đến cuối file. |
| 36 | Lấy kích thước toàn bộ file theo byte/ký tự. |
| 38 | Tính kích thước vùng dữ liệu cần xử lý. |
| 39 | Cố định số process là `16`. |
| 40 | Tính kích thước mỗi đoạn chia theo byte. |
| 42 | Tạo danh sách task rỗng. |
| 43 | Đặt điểm bắt đầu của đoạn đầu tiên. |
| 45 | Mở lại file để dò điểm cắt đoạn an toàn. |
| 46 | Lặp từ process thứ 1 đến process thứ 15 để tạo 15 đoạn đầu. |
| 47 | Tính vị trí kết thúc lý tưởng theo kích thước chunk. |
| 48 | Di chuyển con trỏ file đến vị trí kết thúc lý tưởng. |
| 50-53 | Đọc tiếp từng ký tự đến khi gặp khoảng trắng hoặc EOF, tránh cắt giữa số. |
| 55 | Lấy vị trí kết thúc thật sau khi đã căn theo biên token. |
| 56 | Thêm task `(file_path, start, end)` vào danh sách. |
| 57 | Đặt điểm bắt đầu đoạn kế tiếp. |
| 59 | Thêm đoạn cuối từ `current_start` đến cuối file. |
| 61 | Tạo `Pool` gồm `16` process. |
| 62 | Gửi các task cho pool, mỗi task trả về một tổng cục bộ. |
| 64 | Cộng các tổng cục bộ và trả kết quả cuối cùng. |

## Độ phức tạp

- Thời gian: `O(S)`, với `S` là kích thước phần dữ liệu trong file. Dữ liệu được chia cho nhiều process nên thời gian thực tế phụ thuộc số CPU.
- Bộ nhớ: `O(S / P)` cho mỗi process, với `P = 16`, vì mỗi process đọc một đoạn file.

## Nhận xét báo cáo

Ưu điểm của cách làm là chia dữ liệu theo byte nên không cần load toàn bộ danh sách số vào RAM trong từng process. Điểm quan trọng là chương trình phải điều chỉnh biên chunk đến khoảng trắng để bảo đảm mỗi số chỉ thuộc về đúng một process.
