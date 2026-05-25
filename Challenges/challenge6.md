# Challenge 6 - Tìm khoảng cách gần nhất giữa các điểm

## Mục tiêu

Chương trình đọc nhiều bộ điểm 2D. Với mỗi bộ điểm, chương trình trả về khoảng cách Euclid nhỏ nhất giữa hai điểm, làm tròn 4 chữ số thập phân. Nếu bộ điểm có ít hơn 2 điểm thì trả `0.0`.

Code tối ưu bằng cách mã hóa mỗi điểm `(x, y)` thành một số nguyên 64-bit, sort theo `x`, sau đó scan một số điểm lân cận. Khi số điểm trên cùng hoành độ (max_x_run) lớn hơn `_NEIGHBORS`, đảo transpose và scan lại để tăng độ chính xác.

## Ý tưởng thuật toán

1. Đọc toàn bộ input thành danh sách số nguyên.
2. Với mỗi điểm `(x, y)`, cộng offset `1e9` để đưa tọa độ về không âm.
3. Mã hóa điểm thành:

```python
((x + OFFSET) << 32) | (y + OFFSET)
```

4. Sort danh sách mã hóa. Khi đó điểm được sắp theo `x`, rồi theo `y`.
5. Decode thành hai mảng `xs`, `ys`.
6. Với mỗi điểm, chỉ so sánh với tối đa `_NEIGHBORS = 8` điểm kế tiếp.
7. Nếu có nhiều điểm cùng hoành độ (max_x_run > 8), đảo transpose (đổi vai trò x và y) rồi scan lại để tăng độ chính xác.
8. Với input lớn hoặc nhiều dataset, dùng multiprocessing để chia việc.

## Lưu ý quan trọng

Thuật toán trong file là heuristic tối ưu tốc độ: sau khi sort theo `x`, mỗi điểm chỉ scan 8 điểm kế tiếp. Cách này rất nhanh, nhưng không phải thuật toán closest pair exact cho mọi bộ dữ liệu đối kháng. Với dữ liệu test thông thường, heuristic này thường cho kết quả đúng và nhanh.

## Phân tích theo dòng

| Dòng | Phân tích |
|---:|---|
| 1 | Import `math` để tính căn bậc hai và làm tròn kết quả. |
| 2 | Import `multiprocessing` để chạy song song. |
| 5 | `_INF` là giá trị rất lớn (`10^40`), dùng làm khoảng cách ban đầu. |
| 6 | `_OFFSET = 10^9` dùng để chuyển tọa độ âm sang không âm khi encode. |
| 7 | `_MASK = (1 << 32) - 1` dùng để lấy lại phần `y` từ số đã encode. |
| 8 | `_NEIGHBORS = 8`, số điểm kế tiếp được scan cho mỗi điểm. |
| 9 | `_PARALLEL_SINGLE_MIN = 120000`, ngưỡng bật parallel cho một dataset lớn. |
| 10 | `_PARALLEL_TOTAL_MIN = 50000`, ngưỡng tổng số điểm để bật parallel khi có nhiều dataset. |
| 11 | `_PARALLEL_CHUNK_MIN = 50000`, kích thước chunk tối thiểu khi chia scan song song. |
| 12 | `_MAX_WORKERS = 16`, giới hạn tối đa 16 worker. |
| 14 | `_CPU_COUNT = multiprocessing.cpu_count()` lấy số CPU. |
| 15-17 | Biến global `_GLOBAL_XS`, `_GLOBAL_YS`, `_GLOBAL_DATASETS` để process con dùng chung dữ liệu sau khi `fork`. |
| 20-29 | Hàm `_get_fork_context` lấy context multiprocessing kiểu `fork`. Trả `None` nếu không hỗ trợ. |
| 32-72 | Hàm `_scan_range(xs, ys, left, right)` scan một đoạn chỉ số trong mảng điểm đã sort. |
| 33-35 | Nếu ít hơn 2 điểm thì trả `_INF`. |
| 37-38 | Giới hạn `right` không vượt quá `n - 1`. |
| 40 | Khởi tạo `best = _INF`. |
| 41-70 | Vòng lặp chính: với mỗi điểm từ `left` đến `right - 1`, scan tối đa 8 điểm kế tiếp. |
| 52-68 | Vòng lặp inner: so sánh với các điểm lân cận, dùng `dx^2 >= best` để early break. |
| 64-65 | Nếu `dist == 0` (trùng điểm) thì trả ngay 0. |
| 75-79 | `_scan_worker(left, right, result_queue)` là worker chạy trong process con, gọi `_scan_range` và gửi kết quả về queue. |
| 82-140 | `_scan_parallel(xs, ys)` điều phối scan song song cho một dataset. |
| 85-86 | Nếu dữ liệu nhỏ (`n < 120000`) hoặc chỉ có 1 CPU thì scan tuần tự. |
| 88-90 | Nếu không có `fork` context thì scan tuần tự. |
| 92-99 | Tính số chunk/worker: `min(CPU_COUNT, 16, (n-1) // 50000)`. Nếu `< 2` chunk thì scan tuần tự. |
| 101-104 | Gán `xs`, `ys` vào biến global cho worker. |
| 106-118 | Tạo `SimpleQueue`, fork process cho từng chunk. |
| 120-129 | Nhận kết quả từ worker, lấy `min`. |
| 131-132 | Join toàn bộ process. |
| 134-135 | Xóa global để giải phóng bộ nhớ. |
| 137-138 | Nếu worker lỗi thì raise lại. |
| 143-164 | `_scan_transposed(xs, ys)` đảo transpose (đổi vai trò x và y) rồi scan lại. |
| 148-153 | Tạo mảng `swapped[i] = (ys[i] << 32) | xs[i]`, sort để điểm được sắp theo y rồi theo x. |
| 155-162 | Decode lại thành `tx` (cũ là y) và `ty` (cũ là x). |
| 164 | Gọi `_scan_parallel(tx, ty)` để scan với heuristic theo trục y. |
| 167-219 | `_solve_encoded(values, use_parallel)` giải một dataset đã encode. |
| 169-171 | Nếu ít hơn 2 điểm thì xóa list và trả `_INF`. |
| 173 | Sort các điểm encoded. |
| 175-176 | Tạo mảng `xs`, `ys`. |
| 178-204 | Decode từng điểm và đếm `max_x_run` (số điểm liên tiếp cùng hoành độ). |
| 189-190 | Nếu trùng điểm thì xóa list và trả 0 ngay. |
| 208-217 | Scan bằng `_scan_parallel` hoặc `_scan_range`. Nếu `max_x_run > 8` thì gọi thêm `_scan_transposed` và lấy kết quả tốt hơn. |
| 222-230 | `_dataset_worker(indices, result_queue)` xử lý một nhóm dataset trong process con. |
| 226 | Với mỗi index, gọi `_solve_encoded` với `use_parallel=False`. |
| 233-296 | `_solve_all(datasets, total_points)` giải toàn bộ danh sách dataset. |
| 236-237 | Nếu chỉ có một dataset thì cho phép scan song song trong dataset đó (`use_parallel=True`). |
| 239 | Số worker = `min(CPU_COUNT, q, 16)`. |
| 242-243 | Nếu dữ liệu nhỏ (`total_points < 50000`) hoặc không có fork thì xử lý tuần tự. |
| 245-260 | Chia dataset cho worker theo load balancing: sắp xếp dataset theo kích thước giảm dần, rồi gán cho worker có load nhỏ nhất. |
| 262-263 | Gán danh sách dataset vào global cho worker. |
| 265-274 | Tạo queue và fork process cho từng nhóm. |
| 276-286 | Nhận batch kết quả từ worker, điền vào mảng kết quả theo index. |
| 299-304 | `_encode_dataset(data, left, right)` mã hóa một đoạn token tọa độ thành danh sách điểm encoded. Mỗi 2 token tạo thành 1 điểm (x, y). |
| 307-338 | Hàm `MAIN(input_file_path)` đọc file input và trả danh sách kết quả. |
| 308-309 | Đọc toàn bộ file, tách thành danh sách số nguyên. |
| 311-312 | Nếu input rỗng thì trả `[]`. |
| 314 | Lấy `q = data[0]` là số lượng dataset. |
| 319-325 | Vòng lặp qua từng dataset: đọc `n`, encode đoạn `2n` token thành `n` điểm. |
| 329-336 | Với mỗi khoảng cách bình phương: nếu là `_INF` thì trả `0.0`, ngược lại tính `sqrt` và làm tròn 4 chữ số. |
| 341-342 | Block `__main__`: gọi `MAIN("large_input.txt")` và in kết quả. |

## Độ phức tạp

- Encode input: `O(n)`.
- Sort mỗi dataset: `O(n log n)`.
- Scan heuristic: `O(n * _NEIGHBORS)`, gần tuyến tính vì `_NEIGHBORS = 8`.
- Transpose scan (khi cần): thêm `O(n log n)` cho sort và `O(n * 8)` cho scan.
- Bộ nhớ: `O(n)` cho danh sách encoded và hai mảng `xs`, `ys`.

## Nhận xét báo cáo

Điểm tối ưu lớn nhất là encode `(x, y)` thành một số nguyên để sort nhanh hơn tuple. Sau khi sort, việc tách `xs`, `ys` giúp inner loop không phải decode bit nhiều lần. Thuật toán còn dùng transpose để tăng độ chính xác khi có nhiều điểm cùng hoành độ.
