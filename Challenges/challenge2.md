# Challenge 2 - Tính Fibonacci Modulo cho Nhiều Giá Trị

## Mục tiêu

Tính F(A_i) mod Q cho N truy vấn, với F là dãy Fibonacci tiêu chuẩn (F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)).

## Ý tưởng thuật toán

1. **Split-based lookup**: Decompose mỗi index A_i thành hai phần:
   - `low = A_i & MASK` (17 bits thấp, tức 0..131071)
   - `high = A_i >> SHIFT` (17 bits cao)

2. **Precompute hai bảng**:
   - `low_f[i] = F(i)`, `low_g[i] = F(i+1)` cho i = 0..BASE-1
   - `high_f[h] = F(h*BASE)`, `high_prev[h] = F(h*BASE+1) - F(h*BASE)` cho h = 0..MAX_HIGH

3. **Công thức tính F(A_i)**:
   ```
   F(A_i) = high_f[h] * low_g[l] + high_prev[h] * low_f[l] (mod q)
   ```
   trong đó `l = A_i & MASK`, `h = A_i >> SHIFT`

4. **Multiprocessing**: 3 worker process + 1 main process xử lý song song 4 phần của mảng

## Phân tích theo dòng

| Dòng | Phân tích |
|---:|---|
| 3-5 | Constants: `SHIFT=17`, `BASE=1<<17=131072`, `MASK=BASE-1` |
| 7-8 | `MAX_A=200000000`, `MAX_HIGH=MAX_A>>17` |
| 10-17 | Khởi tạo biến global cho multiprocessing |
| 20-51 | `fib_pair_mod(n, q)`: tính cặp (F(n), F(n+1)) mod q bằng fast doubling |
| 23-25 | Base case: n=0 trả (0, 1) |
| 27 | Lấy mask = bit cao nhất của n |
| 29-49 | Vòng lặp fast doubling: cập nhật (F(k), F(k+1)) thành (F(2k), F(2k+1)) hoặc (F(2k+1), F(2k+2)) |
| 54-72 | `precompute_low(q)`: tạo bảng `low_f[i]=F(i)`, `low_g[i]=F(i+1)` cho i=0..131071 |
| 75-101 | `precompute_high(max_high, q)`: tạo bảng `high_f[h]=F(h*BASE)`, `high_prev[h]=F(h*BASE+1)-F(h*BASE)` cho h=0..MAX_HIGH |
| 81 | Tính cặp (F(BASE), F(BASE+1)) bằng fast doubling làm step |
| 95-96 | Công thức nhảy: F((h+1)*BASE) và F((h+1)*BASE+1) từ F(h*BASE) và F(h*BASE+1) |
| 104-123 | `worker_block(lo, hi)`: worker process tính Fibonacci cho đoạn [lo, hi) |
| 120-121 | Tách mỗi giá trị: `l = x & mask`, `h = x >> shift` |
| 123 | Tính kết quả bằng công thức split |
| 126-167 | `parallel_block(values, q)`: xử lý song song với 4 process |
| 139 | Dùng `RawArray("I")` để share memory không copy giữa các process |
| 141-142 | Precompute bảng low và high trước khi fork |
| 146-163 | Tạo 3 worker process, mỗi xử lý 1/4 mảng; main xử lý 1/4 còn lại |
| 170-193 | `MAIN(input_file_path)`: entry point chính |
| 172 | Đọc input bằng bytes và split thành tokens |
| 178-179 | Parse n và q |
| 184-185 | Edge case: q=1 trả toàn 0 |
| 190-191 | Edge case: q=2 dùng period=3 |
| 193 | Gọi `parallel_block(arr, q)` |

## Các hàm chính

### fib_pair_mod(n, q)
Tính cặp (F(n), F(n+1)) mod q bằng fast doubling:
- F(2k) = F(k) * (2*F(k+1) - F(k))
- F(2k+1) = F(k)^2 + F(k+1)^2

### precompute_low(q)
Tạo bảng `low_f[i]=F(i)`, `low_g[i]=F(i+1)` cho i = 0..131071

### precompute_high(max_high, q)
Tạo bảng `high_f[h]=F(h*BASE)`, `high_prev[h]=F(h*BASE+1)-F(h*BASE)` cho h = 0..MAX_HIGH

### worker_block(lo, hi)
Worker process: với mỗi giá trị trong [lo, hi), tách thành `l` và `h`, tính:
```
out[i] = (high_f[h] * low_g[l] + high_prev[h] * low_f[l]) % q
```

### parallel_block(values, q)
Xử lý song song với 3 worker process + 1 main process

## Fast Doubling (trong fib_pair_mod)

```
while mask:
    t = b + b - a
    c = (a * t) % q  # F(2k)
    d = (a * a + b * b) % q  # F(2k+1)
    
    if n & mask:
        a, b = d, (c + d) % q  # F(2k+1), F(2k+2)
    else:
        a, b = c, d  # F(2k), F(2k+1)
    mask >>= 1
```

## Split-Based Computation

Với A_i = h * BASE + l (0 ≤ l < BASE):

```
F(A_i) = F(h*BASE + l)
       = F(h*BASE) * F(l+1) + (F(h*BASE+1) - F(h*BASE)) * F(l)
       = high_f[h] * low_g[l] + high_prev[h] * low_f[l] (mod q)
```

## Độ phức tạp

- Precompute low table: O(BASE * log q)
- Precompute high table: O(MAX_HIGH * log q)
- Mỗi query: O(1) với 2 array lookups và vài phép nhân
- Parallel: O(n / 4) cho mỗi process
- Memory: O(BASE + MAX_HIGH) ≈ 131072 + 1526 ≈ 133K entries

## Tối ưu

1. **BASE=131072** (2^17): chia đều index thành 2 phần 17-bit
2. **Multiprocessing**: 4 process xử lý song song
3. **RawArray**: share memory không copy giữa parent và child
4. **Edge cases**: q=1 → 0, q=2 → dùng period 3
5. **High table step**: dùng fast doubling để nhảy BASE mỗi lần
