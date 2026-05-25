# Challenge 4 - Sắp xếp record theo điểm và nhãn

## Mục tiêu

Chương trình đọc `n` record, mỗi record gồm một số `v` và một nhãn `label`. Kết quả trả về danh sách `(v, label)` đã sắp xếp theo tuple nội bộ:

1. `v` giảm dần.
2. `label` tăng dần theo thứ tự bytes.
3. Nếu vẫn bằng nhau, giữ thứ tự ổn định theo chỉ số ban đầu `i`.

Với dữ liệu lớn, code chia danh sách thành các đoạn và sort song song.

## Ý tưởng thuật toán

Mỗi record được đổi thành tuple:

```python
(-v, label, i, v, label)
```

Python sort tuple theo thứ tự từ trái sang phải:

- `-v` tăng dần tương đương `v` giảm dần.
- `label` tăng dần.
- `i` giúp ổn định thứ tự khi `v` và `label` giống nhau.
- Hai trường cuối dùng để trả kết quả gốc.

## Phân tích theo dòng

| Dòng | Phân tích |
|---:|---|
| 1 | Import `multiprocessing` để sort song song khi dữ liệu lớn. |
| 2 | Import `os`, nhưng hiện không dùng trong code. |
| 4 | Khai báo `DATA` global, dùng để worker truy cập danh sách record. |
| 7 | Định nghĩa `init_worker`, hàm khởi tạo process. |
| 8-9 | Gán danh sách record vào biến global `DATA`. |
| 12 | Định nghĩa `sort_part`, sort một đoạn record. |
| 13 | Nhận task gồm `start`, `end`. |
| 14 | Trả về bản sort của `DATA[start:end]`. |
| 17 | Hàm `MAIN` là entry point. |
| 18-19 | Đọc toàn bộ input dạng bytes và tách token. |
| 21-22 | Nếu input rỗng thì trả danh sách rỗng. |
| 24 | Token đầu tiên là số record `n`. |
| 25-26 | Nếu `n == 0`, không có record nên trả `[]`. |
| 28 | Khởi tạo danh sách record. |
| 29 | `pos` trỏ đến token đầu tiên sau `n`. |
| 31 | Lặp qua `n` record. |
| 32 | Đọc giá trị số `v`. |
| 33 | Đọc nhãn `label` ở dạng bytes. |
| 34 | Thêm tuple sort-key vào `records`. |
| 35 | Dịch `pos` qua record kế tiếp. |
| 37 | Nếu `n < 20000`, sort tuần tự để tránh overhead multiprocessing. |
| 38 | Sort trực tiếp danh sách record. |
| 39 | Trả kết quả dạng `(v, label.decode())`. |
| 41 | Chọn số process tối đa `8`, không vượt quá số CPU và `n`. |
| 42 | Tính kích thước mỗi chunk. |
| 44-47 | Tạo danh sách task `(start, end)` cho từng chunk. |
| 49 | Lấy context `fork`. |
| 51-55 | Tạo pool và truyền `records` cho worker qua initializer. |
| 56 | Sort từng chunk song song. |
| 58 | Xóa danh sách `records` cũ để chuẩn bị ghép chunk. |
| 59-60 | Ghép các chunk đã sort lại thành một danh sách. |
| 62 | Sort lại toàn bộ danh sách để bảo đảm thứ tự toàn cục. |
| 64 | Trả kết quả cuối cùng dạng `(v, label string)`. |

## Độ phức tạp

- Parse input: `O(n)`.
- Sort tuần tự: `O(n log n)`.
- Nhánh song song hiện tại vẫn sort lại toàn bộ ở dòng 62, nên độ phức tạp tổng vẫn là `O(n log n)`, thêm chi phí sort từng chunk.
- Bộ nhớ: `O(n)`.

## Nhận xét báo cáo

Code thể hiện ý tưởng song song hóa bằng cách sort từng phần trong các process. Tuy nhiên, vì sau đó vẫn gọi `records.sort()` trên toàn bộ danh sách, phần ghép chưa phải là merge tối ưu `O(n)`. Nếu muốn tối ưu hơn, có thể dùng `heapq.merge` để merge các chunk đã sort.
