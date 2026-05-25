# Challenge 3 - Nhân ma trận song song

## Mục tiêu

Chương trình đọc hai ma trận vuông `A` và `B` kích thước `N x N`, tính ma trận tích `C = A x B`, đồng thời trả thêm:

- Đường chéo chính của `C`.
- Đường chéo phụ của `C`.
- Tổng tất cả phần tử của `C`.

Việc tính toán được chia theo các block dòng và xử lý bằng multiprocessing.

## Ý tưởng thuật toán

1. Đọc `N`, ma trận `A` và ma trận `B`.
2. Chuyển vị `B` thành `BT` để truy cập cột của `B` như một hàng, giúp phép nhân cache-friendly hơn.
3. Chia các dòng của `A` thành nhiều task, mỗi task xử lý một đoạn dòng liên tiếp.
4. Mỗi worker tính các dòng tương ứng trong `C`.
5. Worker trả về block dòng, phần đường chéo chính, phần đường chéo phụ và tổng block.
6. Process chính ghép các block về đúng vị trí.

## Phân tích theo dòng

| Dòng | Phân tích |
|---:|---|
| 1 | Import `multiprocessing` để chạy các block dòng song song. |
| 3-5 | Khai báo biến global để worker truy cập ma trận `A`, ma trận `BT` và kích thước `N`. |
| 8 | Định nghĩa `init_worker`, chạy khi mỗi process được tạo. |
| 9-12 | Gán dữ liệu dùng chung vào biến global trong worker. |
| 15 | Định nghĩa `compute_block`, hàm tính một đoạn dòng của ma trận kết quả. |
| 16 | Nhận task gồm `start` và `end`, là khoảng dòng cần xử lý. |
| 18-20 | Lấy dữ liệu global vào biến local để truy cập nhanh hơn. |
| 22 | Tạo danh sách chứa các dòng kết quả của block. |
| 23 | Tạo danh sách chứa phần đường chéo chính thuộc block. |
| 24 | Tạo danh sách chứa phần đường chéo phụ thuộc block. |
| 25 | Khởi tạo tổng các phần tử trong block. |
| 27 | Lặp qua từng dòng `i` từ `start` đến `end - 1`. |
| 28 | Lấy dòng `i` của ma trận `A`. |
| 29 | Khởi tạo dòng `i` của ma trận kết quả `C`. |
| 31 | Lặp qua từng cột `j` của ma trận `B`. |
| 32 | Lấy cột `j` của `B` từ ma trận chuyển vị `BT`. |
| 34 | Khởi tạo tích vô hướng `s`. |
| 35-36 | Tính tích vô hướng giữa dòng `A[i]` và cột `B[j]`. |
| 38 | Gán giá trị `C[i][j] = s`. |
| 40 | Thêm dòng kết quả vào block. |
| 42 | Lấy phần tử đường chéo chính `C[i][i]`. |
| 43 | Lấy phần tử đường chéo phụ `C[i][N - 1 - i]`. |
| 44 | Cộng tổng dòng vào tổng block. |
| 46 | Trả về vị trí bắt đầu, block kết quả, hai đoạn đường chéo và tổng block. |
| 49 | Định nghĩa hàm đọc input. |
| 50-51 | Mở file và đọc dòng đầu tiên. |
| 53-54 | Nếu file rỗng thì trả ma trận rỗng. |
| 56 | Chuyển dòng đầu thành kích thước `N`. |
| 58-60 | Đọc `N` dòng tiếp theo làm ma trận `A`. |
| 62-64 | Đọc `N` dòng tiếp theo làm ma trận `B`. |
| 66 | Trả `N`, `A`, `B`. |
| 69 | Hàm `MAIN` là entry point. |
| 70 | Đọc input. |
| 72-78 | Nếu `N == 0`, trả cấu trúc kết quả rỗng. |
| 80 | Chuyển vị `B` thành `BT` bằng `zip(*B)`. |
| 82 | Chọn số process bằng min giữa số CPU và `N`. |
| 84 | Số task được đặt bằng `num_processes * 4` để cân bằng tải tốt hơn. |
| 85 | Tính số dòng mỗi task. |
| 87-90 | Tạo danh sách task `(start, end)`. |
| 92 | Khởi tạo ma trận kết quả `C` với `N` dòng. |
| 93-94 | Khởi tạo hai danh sách đường chéo. |
| 95 | Khởi tạo tổng toàn ma trận. |
| 97-107 | Nếu chỉ có một process, chạy tuần tự nhưng vẫn dùng cùng hàm `compute_block`. |
| 109-113 | Nếu có nhiều process, tạo pool và truyền `A`, `BT`, `N` qua initializer. |
| 115-119 | Dùng `imap_unordered` để nhận block nào xong trước thì xử lý trước. |
| 120-124 | Ghép block, đường chéo và tổng block vào kết quả chung. |
| 126-131 | Trả dictionary gồm ma trận kết quả, hai đường chéo và tổng. |

## Độ phức tạp

- Thời gian tính toán: `O(N^3)`.
- Bộ nhớ: `O(N^2)` cho `A`, `B`, `BT`, `C`.
- Khi chạy song song, thời gian thực tế xấp xỉ `O(N^3 / P)` với `P` là số process, nhưng còn phụ thuộc overhead truyền dữ liệu và ghép kết quả.

## Nhận xét báo cáo

Điểm quan trọng là chuyển vị ma trận `B`. Nếu không chuyển vị, mỗi lần truy cập cột của `B` sẽ không liên tục trong bộ nhớ. Với `BT`, phép nhân dùng hai danh sách hàng, giúp vòng lặp trong worker đơn giản và nhanh hơn.
