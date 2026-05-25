# Challenge 5 - Tìm vị trí xuất hiện đầu tiên của một khóa trong dãy số

## Mục tiêu

Chương trình đọc một khóa `K` ở đầu file, sau đó tìm vị trí đầu tiên của `K` trong phần dữ liệu còn lại. Vị trí trả về là chỉ số token tính từ `0`. Nếu không tìm thấy, trả `-1`.

Code dùng `multiprocessing.Process` và `SimpleQueue` để chia vùng dữ liệu thành nhiều range byte, mỗi worker tìm trong một range.

## Ý tưởng thuật toán

1. Đọc toàn bộ file dạng bytes.
2. Tách token đầu tiên làm `key`.
3. Phần còn lại là `body`, chứa dãy số cần tìm.
4. Chia `body` thành nhiều range theo byte, nhưng điều chỉnh để không cắt giữa token.
5. Mỗi process tìm `key` trong range của mình.
6. Worker trả về index cục bộ trong range.
7. Process chính lấy range có kết quả sớm nhất theo thứ tự range và cộng số token ở các range trước đó.

## Phân tích theo dòng

| Dòng | Phân tích |
|---:|---|
| 1 | Import `multiprocessing` để tạo process song song. |
| 4-5 | Biến global lưu `body` và `key`, giúp process con dùng dữ liệu sau khi `fork`. |
| 6 | Giới hạn số worker tối đa là `8`. |
| 7 | Mỗi worker xử lý ít nhất khoảng `250000` byte để tránh tạo quá nhiều process nhỏ. |
| 8 | Giới hạn số lần gặp substring sai trước khi fallback sang `split`. |
| 11 | Định nghĩa `_context`, lấy multiprocessing context. |
| 12-15 | Ưu tiên dùng `fork`; nếu hệ điều hành không hỗ trợ thì trả `None`. |
| 18 | `_split_index` tìm vị trí token bằng cách split một đoạn. |
| 19-20 | Nếu tìm được `key`, trả index trong danh sách token của đoạn. |
| 21-22 | Nếu không có `key`, trả `-1`. |
| 25 | `_is_boundary` kiểm tra vị trí tìm thấy có nằm đúng biên token không. |
| 26-29 | Điều kiện đúng: trước key là đầu chuỗi/khoảng trắng và sau key là cuối chuỗi/khoảng trắng. |
| 32 | `_find_index_in_range` tìm key trong một range byte. |
| 33-34 | Nếu key chỉ dài 1 byte, dùng `split().index()` để tránh quá nhiều false hit. |
| 36 | `pos` là vị trí bắt đầu tìm kiếm. |
| 37 | Lưu độ dài key. |
| 38 | Đếm số lần `body.find` tìm thấy substring nhưng không phải token đúng. |
| 40 | Vòng lặp tìm kiếm. |
| 41 | Tìm vị trí xuất hiện tiếp theo của key trong `[pos, end)`. |
| 43-44 | Nếu không tìm thấy thì trả `-1`. |
| 46 | Tính vị trí kết thúc token ứng viên. |
| 48-49 | Nếu đúng biên token, trả số token đứng trước key trong range. |
| 51 | Tăng số false hit. |
| 53-54 | Nếu false hit quá nhiều, fallback sang split để ổn định tốc độ. |
| 56 | Dịch vị trí tìm kiếm lên 1 byte. |
| 59 | `_make_ranges` tạo các range byte cho worker. |
| 60-63 | Khởi tạo danh sách range, lấy body và tính kích thước chunk. |
| 65 | Lặp đến khi chia hết body. |
| 66-67 | Bỏ qua khoảng trắng ở đầu range. |
| 69-70 | Nếu hết dữ liệu thì dừng. |
| 72 | Tính điểm kết thúc dự kiến. |
| 74-75 | Nếu vượt cuối body thì dùng cuối body. |
| 76-78 | Nếu chưa tới cuối, kéo `end` đến biên token tiếp theo. |
| 80 | Thêm range vào danh sách. |
| 81 | Range sau bắt đầu từ `end`. |
| 83 | Trả danh sách range. |
| 86 | `_search_worker` là hàm chạy trong process con. |
| 87-88 | Worker tìm key trong range và gửi kết quả về queue. |
| 89-90 | Nếu có lỗi, gửi exception về process chính. |
| 93 | `_count_before` tính index toàn cục khi biết index cục bộ. |
| 94 | Bắt đầu từ `found_local`. |
| 96-97 | Cộng số token của các range đứng trước. |
| 99 | Trả index toàn cục. |
| 102 | `_search_parallel` điều phối toàn bộ quá trình tìm kiếm. |
| 103-105 | Gán `body`, `key` vào biến global. |
| 107-109 | Nếu body rỗng thì trả `-1`. |
| 111 | Lấy context multiprocessing. |
| 113-114 | Nếu không có `fork`, tìm tuần tự trong toàn body. |
| 116-120 | Chọn số worker dựa trên CPU, giới hạn tối đa và kích thước body. |
| 121 | Tạo danh sách range. |
| 123-124 | Nếu không có range thì trả `-1`. |
| 126 | Tạo `SimpleQueue` để nhận kết quả. |
| 127 | Danh sách process. |
| 129-135 | Tạo và start từng process worker. |
| 137 | Mảng `found` lưu kết quả theo đúng thứ tự range. |
| 138 | Biến giữ lỗi nếu worker lỗi. |
| 140-146 | Nhận kết quả từ queue và lưu theo index range. |
| 148-149 | Join toàn bộ process. |
| 151-152 | Nếu có lỗi thì raise lại. |
| 154-156 | Duyệt range theo thứ tự; range đầu tiên có kết quả là vị trí xuất hiện đầu tiên. |
| 158 | Nếu không range nào tìm thấy thì trả `-1`. |
| 161 | Hàm `MAIN`. |
| 162-163 | Đọc toàn bộ input dạng bytes. |
| 165-166 | File rỗng thì trả `-1`. |
| 168 | Tách token đầu tiên và phần dữ liệu còn lại. |
| 170-171 | Nếu chỉ có key mà không có body thì trả `-1`. |
| 173 | Chuẩn hóa key bằng `int`, rồi encode lại để tránh khác biệt như `001`. |
| 174 | Gọi tìm kiếm song song và trả kết quả. |

## Độ phức tạp

- Trường hợp tốt: `body.find` chạy rất nhanh trong C, gần `O(S)` với `S` là kích thước body.
- Trường hợp nhiều false hit: fallback sang `split`, vẫn tuyến tính theo kích thước range.
- Bộ nhớ: `O(S)` do đọc toàn bộ file, cộng thêm chi phí split khi fallback.

## Nhận xét báo cáo

Điểm cần nhấn mạnh là kiểm tra biên token. Nếu chỉ dùng `body.find(key)`, chương trình có thể nhận nhầm `10` trong `110`. Hàm `_is_boundary` giải quyết vấn đề này.
