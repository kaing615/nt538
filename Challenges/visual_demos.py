"""
=============================================================
VISUAL DEMOS - HIỂU CÁC CHALLENGES QUA HÌNH ẢNH
=============================================================
MINH HỌA TỪNG DÒNG CODE VỚI VÍ DỤ CỤ THỂ
"""

import time

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    CLEAR = '\033[2J\033[H'

def print_header(title):
    print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title:^60}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

def print_section(title, code_lines, explanation, example=None, current_line=None):
    """In một phần với code và giải thích chi tiết"""
    print(f"\n{Colors.BLUE}📝 {title}{Colors.ENDC}")
    print(f"{Colors.DIM}{'─'*60}{Colors.ENDC}")
    
    for i, line in enumerate(code_lines, 1):
        if current_line and i == current_line:
            print(f"{Colors.GREEN}  ► {i:2d} │ {line}{Colors.ENDC}")
        else:
            print(f"{Colors.DIM}    {i:2d} │ {line}{Colors.ENDC}")
    
    print(f"{Colors.DIM}{'─'*60}{Colors.ENDC}")
    print(explanation)
    
    if example:
        print(f"\n{Colors.YELLOW}📌 Ví dụ:{Colors.ENDC}")
        print(example)
    
    input(f"\n{Colors.YELLOW}  Nhấn Enter để tiếp tục...{Colors.ENDC}")

def input_continue():
    input(f"{Colors.YELLOW}  Nhấn Enter để tiếp tục...{Colors.ENDC}")

# ============================================================
# CHALLENGE 1: BYTE-RANGE FILE SPLITTING (challenge1.py)
# ============================================================
def demo_challenge1():
    print_header("CHALLENGE 1: Byte-Range File Splitting (challenge1.py)")
    
    # Dòng 1-10: Imports và Constants
    print_section(
        "1. IMPORTS & WORKER_TASK",
        [
            "import multiprocessing",
            "",
            "def worker_task(args):",
            "    file_path, start_byte, end_byte = args",
            "    total = 0",
            "    with open(file_path, 'r') as f:",
            "        f.seek(start_byte)",
            "        chunk = f.read(end_byte - start_byte)",
            "        for s in chunk.split():",
            "            try:",
            "                val = float(s)",
            "                if val > 0 and val.is_integer():",
            "                    ival = int(val)",
            "                    if ival % 3 == 0:",
            "                        total += ival",
            "            except ValueError:",
            "                continue",
            "    return total",
        ],
        f"""
{Colors.GREEN}✅ Giải thích:{Colors.ENDC}
• worker_task nhận (file_path, start_byte, end_byte)
• Mỗi worker đọc một đoạn file riêng
• Xử lý: chuyển string → float → int → kiểm tra chia hết cho 3

{Colors.GREEN}✅ Chi tiết từng bước:{Colors.ENDC}
1. f.seek(start_byte) → di chuyển con trỏ file
2. f.read(end - start) → đọc đúng số bytes
3. chunk.split() → tách thành các tokens
4. float(s) → chuyển string thành số thực
5. val.is_integer() → kiểm tra là số nguyên (không phải 3.14)
6. ival % 3 == 0 → kiểm tra chia hết cho 3
        """,
        """
Input: "9 3 6 1.5 12"
Workers: 2

Worker 1 (bytes 0-10): "9 3 6 1"
• 9 → float(9) = 9.0, is_integer=True, 9%3=0 ✓ +9
• 3 → float(3) = 3.0, is_integer=True, 3%3=0 ✓ +3
• 6 → float(6) = 6.0, is_integer=True, 6%3=0 ✓ +6
• 1 → float(1) = 1.0, is_integer=True, 1%3=1 ✗
• Kết quả Worker 1 = 18

Worker 2 (bytes 10-20): "5 12"
• 1.5 → float(1.5) = 1.5, is_integer=False ✗ (bỏ qua)
• 12 → float(12) = 12.0, is_integer=True, 12%3=0 ✓ +12
• Kết quả Worker 2 = 12

Tổng = 18 + 12 = 30"""
    )
    
    # Dòng tiếp theo: MAIN
    print_section(
        "2. MAIN() - CHIA FILE VÀ TỔNG HỢP",
        [
            "def MAIN(input_file_path):",
            "    with open(input_file_path, 'r') as f:",
            "        line1 = f.readline()",
            "        n = int(line1.strip())",
            "        data_start_pos = f.tell()",
            "        f.seek(0, 2)",
            "        file_size = f.tell()",
            "    data_size = file_size - data_start_pos",
            "    num_proc = 16",
            "    chunk_size = data_size // num_proc",
            "    tasks = []",
            "    # Tìm điểm cắt ở khoảng trắng",
            "    for i in range(1, num_proc):",
            "        target_end = data_start_pos + i * chunk_size",
            "        f.seek(target_end)",
            "        while True:",
            "            char = f.read(1)",
            "            if not char or char.isspace():",
            "                break",
            "        current_end = f.tell()",
            "        tasks.append((file_path, current_start, current_end))",
            "    # Chạy Pool",
            "    with multiprocessing.Pool(processes=num_proc) as pool:",
            "        results = pool.map(worker_task, tasks)",
            "    return sum(results)",
        ],
        f"""
{Colors.GREEN}✅ Giải thích CHI TIẾT từng dòng:{Colors.ENDC}

DÒNG 2-4: Đọc số n
• f.readline() → đọc dòng đầu tiên (số n)
• f.tell() → lưu vị trí bắt đầu dữ liệu

DÒNG 5-6: Lấy kích thước file
• f.seek(0, 2) → nhảy đến cuối file
• f.tell() → lấy kích thước file

DÒNG 7-8: Chia file thành 16 phần
• data_size = file_size - data_start_pos
• chunk_size = data_size // 16

{Colors.RED}⚠️ QUAN TRỌNG: Tìm điểm cắt an toàn{Colors.ENDC}
• Không cắt giữa một số!
• Đọc từng ký tự từ target_end
• Dừng khi gặp whitespace (space, newline)
        """,
        """
File: "100\\n1 2 3 6 9 12 15 18 21 24"
                      ↑
              Điểm cắt phải ở whitespace

File size = 50 bytes, data bắt đầu byte 4
data_size = 46 bytes
chunk_size = 46 // 16 = 2 bytes

Target 1: byte 6 → " 1" → gặp space → cắt ở byte 5
Target 2: byte 8 → " 3" → gặp space → cắt ở byte 7
...

Tasks: [(file, 4, 5), (file, 5, 7), (file, 7, 10), ...]

Pool.map: gửi 16 tasks cho 16 workers
Kết quả: [18, 27, 54, ...] → sum() = 99"""
    )
    
    print(f"\n{Colors.GREEN}🎉 HOÀN THÀNH CHALLENGE 1!{Colors.ENDC}\n")

# ============================================================
# CHALLENGE 2: FAST DOUBLING FIBONACCI (challenge2.py - 354 dòng)
# ============================================================
def demo_challenge2():
    print_header("CHALLENGE 2: Fast Doubling Fibonacci (354 dòng)")
    
    # 1. Constants
    print_section(
        "1. CONSTANTS (dòng 3-14)",
        [
            "GAP_LIMIT = 65536",
            "MAX_PROC = 8",
            "LINEAR_LIMIT = 300000",
            "PERIOD_Q_LIMIT = 80000",
            "PARALLEL_MIN = 2",
            "",
            "Q_GLOBAL = 1",
            "VALUES_GLOBAL = None",
            "OUT_GLOBAL = None",
            "GAP_F_GLOBAL = None",
            "GAP_G_GLOBAL = None",
            "POWERS_GLOBAL = None",
        ],
        f"""
{Colors.GREEN}✅ Giải thích từng constant:{Colors.ENDC}
• GAP_LIMIT = 65536: Giới hạn bảng lookup cho gap
• LINEAR_LIMIT = 300000: Ngưỡng precompute liên tục
• PERIOD_Q_LIMIT = 80000: Ngưững dùng Pisano period
• MAX_PROC = 8: Số process tối đa
• PARALLEL_MIN = 2: Ngưỡng tối thiểu để parallel

{Colors.GREEN}Global variables cho multiprocessing:{Colors.ENDC}
• VALUES_GLOBAL: mảng giá trị cần tính F(n)
• OUT_GLOBAL: RawArray lưu kết quả
• GAP_F_GLOBAL, GAP_G_GLOBAL: bảng gap precomputed
• POWERS_GLOBAL: F(2^i) đã precompute
        """,
        """
Ví dụ GAP_LIMIT:
• Khi tính F(m) từ F(n), gap d = m - n
• Nếu d ≤ 65536: lookup O(1) từ bảng gap_f[d]
• Nếu d > 65536: tính bằng fast doubling"""
    )
    
    # 2. fib_pair_mod
    print_section(
        "2. fib_pair_mod() - FAST DOUBLING (dòng 17-48)",
        [
            "def fib_pair_mod(n, q):",
            "    a = 0  # F(0)",
            "    b = 1  # F(1)",
            "    if n == 0:",
            "        return 0, 1",
            "    mask = 1 << (n.bit_length() - 1)  # Bit cao nhất",
            "    while mask:",
            "        t = b + b - a",
            "        if t < 0: t += q",
            "        elif t >= q: t -= q",
            "        c = (a * t) % q     # F(2k)",
            "        d = (a * a + b * b) % q  # F(2k+1)",
            "        if n & mask:",
            "            s = c + d",
            "            if s >= q: s -= q",
            "            a = d",
            "            b = s",
            "        else:",
            "            a = c",
            "            b = d",
            "        mask >>= 1",
            "    return a, b",
        ],
        f"""
{Colors.GREEN}✅ Giải thích thuật toán Fast Doubling:{Colors.ENDC}

{Colors.YELLOW}Công thức toán học:{Colors.ENDC}
• F(2k) = F(k) × [2F(k+1) - F(k)]
• F(2k+1) = F(k)² + F(k+1)²

{Colors.YELLOW}Trong code:{Colors.ENDC}
• t = 2b - a (tương đương 2F(k+1) - F(k))
• c = a × t mod q = F(2k)
• d = a² + b² mod q = F(2k+1)

{Colors.YELLOW}Xử lý bit:{Colors.ENDC}
• mask = bit cao nhất của n
• Duyệt từ MSB đến LSB
• Bit = 1: (a,b) = (d, c+d) = (F(2k+1), F(2k+2))
• Bit = 0: (a,b) = (c, d) = (F(2k), F(2k+1))
        """,
        """
Tính F(10) mod 1000:

n = 10 = 1010 (binary)
bit_length = 4
mask = 1 << 3 = 8 (1000)

Khởi tạo: a = F(0) = 0, b = F(1) = 1

=== VÒNG LẶP ===

mask = 8 (1000), n & mask = 1 (bit = 1)
  t = 1 + 1 - 0 = 2
  c = 0 × 2 = 0 = F(0)
  d = 0 + 1 = 1 = F(1)
  Vì bit = 1: a = d = 1, b = c + d = 1
  a = F(1), b = F(2)

mask = 4 (0100), n & mask = 0 (bit = 0)
  t = 1 + 1 - 1 = 1
  c = 1 × 1 = 1 = F(2)
  d = 1 + 4 = 5 = F(5) (mod 1000)
  Vì bit = 0: a = c = 1, b = d = 5
  a = F(2), b = F(3)

mask = 2 (0010), n & mask = 1 (bit = 1)
  t = 5 + 5 - 1 = 9
  c = 1 × 9 = 9 = F(4)
  d = 1 + 25 = 26 = F(5)
  Vì bit = 1: a = d = 26, b = c + d = 35
  a = F(5), b = F(6)

mask = 1 (0001), n & mask = 0 (bit = 0)
  t = 35 + 35 - 26 = 44
  c = 26 × 44 = 55 = F(10) ✓
  d = 26² + 35² = 1961 → 961 = F(11)
  Vì bit = 0: a = c = 55, b = d = 961

=== KẾT QUẢ ===
return (55, 961) → F(10) mod 1000 = 55"""
    )
    
    # 3. make_powers
    print_section(
        "3. make_powers() (dòng 51-59)",
        [
            "def make_powers(q):",
            "    powers = []",
            "    x = 1",
            "    while x <= 268435456:  # 2^28",
            "        powers.append(fib_pair_mod(x, q))",
            "        x <<= 1",
            "    return powers",
        ],
        f"""
{Colors.GREEN}✅ Giải thích:{Colors.ENDC}
• Precompute F(2^i) cho i = 0..28
• Mỗi phần tử là (F(2^i), F(2^i+1))
• Dùng cho gap jumping nhanh

{Colors.YELLOW}Tại sao cần powers?:{Colors.ENDC}
• Khi gap d > GAP_LIMIT (65536)
• Tính F(d) bằng cách kết hợp các powers
• Không cần tính lại từ đầu
        """,
        """
Khi x = 1 (2^0):
  powers[0] = fib_pair_mod(1, q) = (F(1), F(2))

Khi x = 2 (2^1):
  powers[1] = fib_pair_mod(2, q) = (F(2), F(3))

Khi x = 4 (2^2):
  powers[2] = fib_pair_mod(4, q) = (F(4), F(5))

... cho đến x = 268435456 (2^28)

Result: 29 cặp (F(2^i), F(2^i+1))"""
    )
    
    # 4. precompute_gap
    print_section(
        "4. precompute_gap() (dòng 87-105)",
        [
            "def precompute_gap(limit, q):",
            "    f = [0] * (limit + 1)  # F(0..limit)",
            "    g = [0] * (limit + 1)  # F(1..limit+1)",
            "    a = 0  # F(0)",
            "    b = 1  # F(1)",
            "    for i in range(limit + 1):",
            "        f[i] = a  # Lưu F(i)",
            "        g[i] = b  # Lưu F(i+1)",
            "        s = a + b",
            "        if s >= q: s -= q",
            "        a = b",
            "        b = s",
            "    return f, g",
        ],
        f"""
{Colors.GREEN}✅ Giải thích:{Colors.ENDC}
• Tạo bảng gap_f[d] = F(d) mod q cho d = 0..65536
• Tạo bảng gap_g[d] = F(d+1) mod q
• Lookup O(1) thay vì tính lại

{Colors.YELLOW}Ứng dụng trong worker:{Colors.ENDC}
• Khi tính F(m) từ F(n) với gap d = m-n
• Nếu d ≤ 65536: fd = gap_f[d], fd1 = gap_g[d]
• Không cần gọi fib_pair_mod(d)
        """,
        """
Với limit = 5, q = 100:

i=0: f[0]=0, g[0]=1 → a=1, b=1
i=1: f[1]=1, g[1]=1 → a=1, b=2
i=2: f[2]=1, g[2]=2 → a=2, b=3
i=3: f[3]=2, g[3]=3 → a=3, b=5
i=4: f[4]=3, g[4]=5 → a=5, b=8
i=5: f[5]=5, g[5]=8 → a=8, b=13→3

gap_f = [0, 1, 1, 2, 3, 5]
gap_g = [1, 1, 2, 3, 5, 8]

Khi cần F(3): gap_f[3] = 2 ✓"""
    )
    
    # 5. worker_build_values
    print_section(
        "5. worker_build_values() (dòng 108-147)",
        [
            "def worker_build_values(lo, hi):",
            "    q = Q_GLOBAL",
            "    values = VALUES_GLOBAL",
            "    out = OUT_GLOBAL",
            "    gap_f = GAP_F_GLOBAL",
            "    gap_g = GAP_G_GLOBAL",
            "    powers = POWERS_GLOBAL",
            "    # Tính F(values[lo]) từ đầu",
            "    x = values[lo]",
            "    f, g = fib_pair_from_powers(x, q, powers)",
            "    out[lo] = f",
            "    cur = x",
            "    # Gap jumping cho các giá trị tiếp theo",
            "    for i in range(lo + 1, hi):",
            "        x = values[i]",
            "        if x == cur:",
            "            out[i] = f  # Trùng giá trị",
            "            continue",
            "        d = x - cur  # Gap",
            "        if d <= GAP_LIMIT:",
            "            fd = gap_f[d]; fd1 = gap_g[d]  # Lookup O(1)",
            "        else:",
            "            fd, fd1 = fib_pair_from_powers(d, q, powers)",
            "        prev = g - f",
            "        if prev < 0: prev += q",
            "        # F(n+d) = F(n)*F(d+1) + (F(n+1)-F(n))*F(d)",
            "        nf = (f * fd1 + prev * fd) % q",
            "        ng = (f * fd + g * fd1) % q",
            "        out[i] = nf",
            "        cur = x; f = nf; g = ng",
        ],
        f"""
{Colors.GREEN}✅ Giải thích chi tiết:{Colors.ENDC}

{Colors.YELLOW}Gap Jumping Formula (công thức cộng):{Colors.ENDC}
• F(n+d) = F(n) × F(d+1) + (F(n+1) - F(n)) × F(d)

{Colors.YELLOW}Trong code:{Colors.ENDC}
• prev = g - f = F(n+1) - F(n)
• nf = f × fd1 + prev × fd = F(n+d)
• ng = f × fd + g × fd1 = F(n+d+1)

{Colors.YELLOW}Tại sao nhanh?:{Colors.ENDC}
• Tính F(values[0]) từ đầu (một lần)
• Các giá trị tiếp theo: nhảy gap từ giá trị trước
• Nếu gap nhỏ (< 65536): lookup O(1)
• Nếu gap lớn: dùng precomputed powers
        """,
        """
values = [0, 5, 10, 15, 20], q = 100

Tính F(0): fib_pair_mod(0) = (0, 1) → f=0, g=1
out[0] = 0

i=1: x=5, d=5-0=5, d≤65536 → fd=gap_f[5]=5, fd1=gap_g[5]=8
  prev = 1-0 = 1
  nf = 0×8 + 1×5 = 5 → F(5) mod 100 = 5 ✓
  ng = 0×5 + 1×8 = 8
  out[1] = 5, f=5, g=8

i=2: x=10, d=10-5=5, fd=5, fd1=8
  prev = 8-5 = 3
  nf = 5×8 + 3×5 = 55 → F(10) mod 100 = 55 ✓
  ng = 5×5 + 8×8 = 89
  out[2] = 55, f=55, g=89

i=3: x=15, d=15-10=5, fd=5, fd1=8
  prev = 89-55 = 34
  nf = 55×8 + 34×5 = 610 → 10
  out[3] = 10

Kết quả: out = [0, 5, 55, 10, ...]"""
    )
    
    # 6. build_lookup_parallel
    print_section(
        "6. build_lookup_parallel() (dòng 150-196)",
        [
            "def build_lookup_parallel(values, q):",
            "    values.sort()  # QUAN TRỌNG: sort để gap jumping",
            "    m = len(values)",
            "    if m == 1:",
            "        return {values[0]: fib_pair_mod(values[0], q)[0]}",
            "    # Setup global variables",
            "    Q_GLOBAL = q",
            "    VALUES_GLOBAL = values",
            "    OUT_GLOBAL = multiprocessing.RawArray('i', m)",
            "    GAP_F_GLOBAL, GAP_G_GLOBAL = precompute_gap(GAP_LIMIT, q)",
            "    POWERS_GLOBAL = make_powers(q)",
            "    # Tính số processes",
            "    proc_count = multiprocessing.cpu_count()",
            "    if proc_count > MAX_PROC: proc_count = MAX_PROC",
            "    if proc_count > m: proc_count = m",
            "    step = (m + proc_count - 1) // proc_count",
            "    ctx = multiprocessing.get_context('fork')",
            "    processes = []",
            "    start = 0",
            "    while start < m:",
            "        end = start + step",
            "        if end > m: end = m",
            "        p = ctx.Process(target=worker_build_values, args=(start, end))",
            "        p.start()",
            "        processes.append(p)",
            "        start = end",
            "    for p in processes: p.join()",
            "    return dict(zip(values, OUT_GLOBAL))",
        ],
        f"""
{Colors.GREEN}✅ Giải thích chi tiết:{Colors.ENDC}

{Colors.YELLOW}Tại sao phải sort trước?:{Colors.ENDC}
• Gap jumping chỉ hoạt động khi sorted
• Tính F(values[i]) từ F(values[i-1])
• Nếu không sorted: gap jumping sai!

{Colors.YELLOW}RawArray vs Array:{Colors.ENDC}
• RawArray('i', m): shared memory, không có lock
• Array: thread-safe nhưng overhead cao hơn
• Ở đây dùng RawArray vì chỉ write một lần

{Colors.YELLOW}Chia công việc:{Colors.ENDC}
• m values chia cho proc_count workers
• Mỗi worker xử lý ~ m/proc_count values
• Fork: copy memory của parent process
        """,
        """
values = [100, 10, 50, 5, 25] (chưa sort)

SAI: 
  Tính F(100) từ F(10) → gap = 90 (lớn)
  Tính F(10) từ F(50) → gap = -40 (âm!)

ĐÚNG sau khi sort:
values = [5, 10, 25, 50, 100]
  Tính F(5) từ đầu
  Tính F(10) từ F(5) → gap = 5 (nhỏ, lookup O(1))
  Tính F(25) từ F(10) → gap = 15 (nhỏ, lookup O(1))
  ...

m=1000000, proc_count=8, step=125000
Worker 0: [0, 125000)
Worker 1: [125000, 250000)
...
Worker 7: [875000, 1000000)"""
    )
    
    # 7. MAIN
    print_section(
        "7. MAIN() - CHIẾN LƯỢC TỐI ƯU (dòng 300-354)",
        [
            "def MAIN(input_file_path):",
            "    tokens = f.read().split()",
            "    n = int(tokens[0]); q = int(tokens[1])",
            "    if n == 0: return []",
            "    if q == 1: return [0] * n",
            "    arr = list(map(int, tokens[2:2 + n]))",
            "    if n == 1: return [fib_pair_mod(arr[0], q)[0]]",
            "    if q == 2: return [0 if x % 3 == 0 else 1 for x in arr]",
            "    # Chiến lược 1: Pisano Period",
            "    if q <= PERIOD_Q_LIMIT:",
            "        period = find_pisano_period(q)",
            "        if period:",
            "            fibs = precompute_period(period, q)",
            "            return [fibs[x % period] for x in arr]",
            "    # Chiến lược 2: Linear Range",
            "    min_a = min(arr); max_a = max(arr)",
            "    if max_a - min_a <= LINEAR_LIMIT:",
            "        fibs = precompute_range(min_a, max_a, q)",
            "        return [fibs[x - min_a] for x in arr]",
            "    # Chiến lược 3: Parallel/Sequential",
            "    sample_len = 4096",
            "    if n < sample_len: sample_len = n",
            "    sample_unique = len(set(arr[:sample_len]))",
            "    if sample_unique * 10 >= sample_len * 8:",
            "        values = arr[:]  # Nhiều unique",
            "    else:",
            "        values = list(set(arr))  # Ít unique",
            "    if len(values) >= PARALLEL_MIN:",
            "        lookup = build_lookup_parallel(values, q)",
            "    else:",
            "        lookup = build_lookup_sequential(values, q)",
            "    return [lookup[x] for x in arr]",
        ],
        f"""
{Colors.GREEN}✅ Giải thích 5 CHIẾN LƯỢC TỐI ƯU:{Colors.ENDC}

{Colors.YELLOW}1. Edge cases (nhanh):{Colors.ENDC}
• q == 1: F(n) mod 1 = 0 luôn
• n == 1: chỉ một giá trị, tính trực tiếp
• q == 2: period = 3, F(n) mod 2 = 0 khi n%3==0

{Colors.YELLOW}2. Pisano Period (q ≤ 80000):{Colors.ENDC}
• F(n) mod q lặp lại sau Pisano period
• F(n) = fibs[n % period]
• O(period) precompute, O(1) lookup

{Colors.YELLOW}3. Linear Range (max-min ≤ 300000):{Colors.ENDC}
• Precompute F(min..max) liên tục
• F(x) = fibs[x - min]
• Tốt khi giá trị phân bố đều

{Colors.YELLOW}4. Sample để quyết định:{Colors.ENDC}
• Lấy 4096 samples đầu
• Tính tỉ lệ unique
• Nếu unique > 80%: dùng arr (giữ thứ tự)
• Ngược lại: dùng set (bỏ duplicates)

{Colors.YELLOW}5. Parallel vs Sequential:{Colors.ENDC}
• values ≥ 2: build_lookup_parallel (fork)
• values < 2: build_lookup_sequential
        """,
        """
Input: "5 100 0 10 20 30 40"
• n=5, q=100
• arr = [0, 10, 20, 30, 40]

Kiểm tra:
• n=5, q=100: không phải edge case
• q=100 ≤ 80000: dùng Pisano period
• period(100) = 300
• fibs[0..299] = precompute_period(300, 100)

Lookup:
• F(0) = fibs[0 % 300] = fibs[0] = 0
• F(10) = fibs[10 % 300] = fibs[10]
• F(20) = fibs[20 % 300] = fibs[20]
...

Output: [0, 55, 65, 5, 15]"""
    )
    
    print(f"\n{Colors.GREEN}🎉 HOÀN THÀNH CHALLENGE 2!{Colors.ENDC}\n")

# ============================================================
# CHALLENGE 3: PARALLEL MATRIX MULTIPLICATION (challenge3.py)
# ============================================================
def demo_challenge3():
    print_header("CHALLENGE 3: Parallel Matrix Multiplication (131 dòng)")
    
    # 1. Global variables
    print_section(
        "1. GLOBAL VARIABLES & INIT_WORKER (dòng 1-12)",
        [
            "import multiprocessing",
            "",
            "A_GLOBAL = None",
            "BT_GLOBAL = None",
            "N_GLOBAL = 0",
            "",
            "def init_worker(A, BT, N):",
            "    global A_GLOBAL, BT_GLOBAL, N_GLOBAL",
            "    A_GLOBAL = A",
            "    BT_GLOBAL = BT",
            "    N_GLOBAL = N",
        ],
        f"""
{Colors.GREEN}✅ Giải thích:{Colors.ENDC}
• Lưu A, BT, N vào biến global cho worker
• Pool initializer gọi init_worker một lần mỗi worker
• Workers đọc từ biến global thay vì nhận parameter

{Colors.YELLOW}Tại sao dùng global?:{Colors.ENDC}
• multiprocessing.Pool gọi worker nhiều lần
• Nếu truyền A, BT, N mỗi lần → overhead
• Global: chỉ truyền task (start, end)
        """,
        """
Worker Pool với 4 workers:

Pool khởi tạo:
  Worker 1: A_GLOBAL=A, BT_GLOBAL=BT, N_GLOBAL=N
  Worker 2: A_GLOBAL=A, BT_GLOBAL=BT, N_GLOBAL=N
  Worker 3: A_GLOBAL=A, BT_GLOBAL=BT, N_GLOBAL=N
  Worker 4: A_GLOBAL=A, BT_GLOBAL=BT, N_GLOBAL=N

Task gửi: (0, 100) → Worker 1 tính dòng 0-100
Task gửi: (100, 200) → Worker 2 tính dòng 100-200
..."""
    )
    
    # 2. compute_block
    print_section(
        "2. compute_block() - XỬ LÝ BLOCK DÒNG (dòng 15-46)",
        [
            "def compute_block(task):",
            "    start, end = task",
            "    A = A_GLOBAL",
            "    BT = BT_GLOBAL",
            "    N = N_GLOBAL",
            "    block = []",
            "    diag_main_part = []",
            "    diag_secondary_part = []",
            "    block_sum = 0",
            "    for i in range(start, end):  # Mỗi dòng i",
            "        row_a = A[i]",
            "        row_c = [0] * N",
            "        for j in range(N):  # Mỗi cột j",
            "            col_b = BT[j]  # Cột j của BT",
            "            s = 0",
            "            for k in range(N):  # Dot product",
            "                s += row_a[k] * col_b[k]",
            "            row_c[j] = s",
            "        block.append(row_c)",
            "        diag_main_part.append(row_c[i])      # C[i][i]",
            "        diag_secondary_part.append(row_c[N-1-i])  # C[i][N-1-i]",
            "        block_sum += sum(row_c)",
            "    return start, block, diag_main_part, diag_secondary_part, block_sum",
        ],
        f"""
{Colors.GREEN}✅ Giải thích chi tiết:{Colors.ENDC}

{Colors.YELLOW}Matrix Transpose để tối ưu:{Colors.ENDC}
• B transpose → BT (hàng thành cột)
• C[i][j] = A[i] · BT[j] (dot product hàng)
• Truy cập liên tục trong memory (cache-friendly)

{Colors.YELLOW}Thuật toán:{Colors.ENDC}
• Vòng ngoài: i = start..end (các dòng được giao)
• Vòng giữa: j = 0..N-1 (các cột)
• Vòng trong: k = 0..N-1 (dot product)

{Colors.YELLOW}Trả về:{Colors.ENDC}
• block: các dòng C[start:end]
• diag_main_part: C[i][i] cho i=start..end
• diag_secondary_part: C[i][N-1-i]
• block_sum: tổng tất cả phần tử trong block
        """,
        """
N=2, A=[[1,2],[3,4]], B=[[5,6],[7,8]]

BT = [[5,7],   (transpose của B)
      [6,8]]

Tính C[0][0] = A[0] · BT[0]:
  = [1,2] · [5,7]
  = 1*5 + 2*7 = 19

Tính C[0][1] = A[0] · BT[1]:
  = [1,2] · [6,8]
  = 1*6 + 2*8 = 22

Tính C[1][0] = A[1] · BT[0]:
  = [3,4] · [5,7]
  = 3*5 + 4*7 = 43

Tính C[1][1] = A[1] · BT[1]:
  = [3,4] · [6,8]
  = 3*6 + 4*8 = 50

C = [[19, 22],
     [43, 50]]

diag_main = [19, 50]    (C[0][0], C[1][1])
diag_secondary = [22, 43]  (C[0][1], C[1][0])
block_sum = 19+22+43+50 = 134"""
    )
    
    # 3. MAIN
    print_section(
        "3. MAIN() - CHIA CÔNG VIỆC VÀ TỔNG HỢP (dòng 69-131)",
        [
            "def MAIN(input_file_path):",
            "    N, A, B = read_matrix_input(input_file_path)",
            "    if N == 0: return {...}",
            "    BT = [list(col) for col in zip(*B)]  # Transpose",
            "    num_processes = min(cpu_count(), N)",
            "    num_tasks = num_processes * 4",
            "    rows_per_task = max(1, (N + num_tasks - 1) // num_tasks)",
            "    tasks = []",
            "    for start in range(0, N, rows_per_task):",
            "        end = min(start + rows_per_task, N)",
            "        tasks.append((start, end))",
            "    if num_processes == 1:",
            "        init_worker(A, BT, N)",
            "        for task in tasks:",
            "            start, block, dm, ds, subtotal = compute_block(task)",
            "            C[start:start+len(block)] = block",
            "            diag_main[start:start+len(block)] = dm",
            "            diag_secondary[start:start+len(block)] = ds",
            "            total_sum += subtotal",
            "    else:",
            "        with Pool(processes=num_processes, initializer=init_worker, initargs=(A, BT, N)) as pool:",
            "            for start, block, dm, ds, subtotal in pool.imap_unordered(compute_block, tasks):",
            "                C[start:start+len(block)] = block",
            "                ...  # Tổng hợp kết quả",
            "    return {...}",
        ],
        f"""
{Colors.GREEN}✅ Giải thích chi tiết:{Colors.ENDC}

{Colors.YELLOW}Chia công việc:{Colors.ENDC}
• num_tasks = processes × 4 (ít nhất 4 tasks mỗi worker)
• rows_per_task = ceil(N / num_tasks)
• Mỗi task xử lý ~N/num_tasks dòng

{Colors.YELLOW}Pool vs Sequential:{Colors.ENDC}
• num_processes == 1: gọi trực tiếp (không cần Pool)
• num_processes > 1: dùng Pool với initializer

{Colors.YELLOW}imap_unordered vs map:{Colors.ENDC}
• map: kết quả theo thứ tự tasks
• imap_unordered: kết quả khi nào ready
• imap_unordered nhanh hơn vì không chờ
        """,
        """
N=8, cpu_count=4

num_tasks = 4 * 4 = 16
rows_per_task = ceil(8/16) = 1

Tasks:
  Task 0: (0, 1)   → Worker tính dòng 0
  Task 1: (1, 2)   → Worker tính dòng 1
  Task 2: (2, 3)   → Worker tính dòng 2
  ...
  Task 7: (7, 8)   → Worker tính dòng 7

imap_unordered trả về khi nào ready:
  Worker 3 done first → returns (3, block_3, dm, ds, sum_3)
  Worker 1 done second → returns (1, block_1, dm, ds, sum_1)
  ...

Main ghép kết quả vào C đúng vị trí."""
    )
    
    print(f"\n{Colors.GREEN}🎉 HOÀN THÀNH CHALLENGE 3!{Colors.ENDC}\n")

# ============================================================
# CHALLENGE 4: PARALLEL SORTING RECORDS (challenge4.py)
# ============================================================
def demo_challenge4():
    print_header("CHALLENGE 4: Parallel Sorting Records (64 dòng)")
    
    # 1. Tuple encoding
    print_section(
        "1. TUPLE ENCODING & SORT (dòng 28-39)",
        [
            "records = []",
            "pos = 1",
            "for i in range(n):",
            "    v = int(tokens[pos])",
            "    label = tokens[pos + 1]",
            "    # Encode: (-v, label, i, v, label)",
            "    # -v: giảm dần = v tăng dần",
            "    # label: tăng dần theo bytes",
            "    # i: index gốc (độ ổn định)",
            "    records.append((-v, label, i, v, label))",
            "    pos += 2",
            "if n < 20000:",
            "    records.sort()  # Python sort tuple từ trái",
            "    return [(x[3], x[4].decode()) for x in records]",
        ],
        f"""
{Colors.GREEN}✅ Giải thích chi tiết:{Colors.ENDC}

{Colors.YELLOW}Cấu trúc tuple 5 phần tử:{Colors.ENDC}
• [0] -v: sort giảm dần theo v (Python tăng dần, -v tăng = v giảm)
• [1] label: sort tăng dần theo bytes (lexicographic)
• [2] i: index gốc → độ ổn định (stable sort)
• [3] v: để phục hồi kết quả
• [4] label: để phục hồi kết quả

{Colors.YELLOW}Tại sao encode như vậy?:{Colors.ENDC}
• Python sort tuple so sánh từ trái sang
• -v → v giảm dần
• label → cùng v thì sort theo label
• i → cùng v và label thì giữ thứ tự gốc
        """,
        """
Input: [(100, b"A"), (50, b"B"), (100, b"A"), (75, b"C")]

Encode:
index=0: (-100, b"A", 0, 100, b"A")
index=1: (-50,  b"B", 1, 50,  b"B")
index=2: (-100, b"A", 2, 100, b"A")
index=3: (-75,  b"C", 3, 75,  b"C")

Sort:
1. (-100, b"A", 0, ...)  ← v=100, label="A", i=0
2. (-100, b"A", 2, ...)  ← v=100, label="A", i=2 (i=0 < i=2)
3. (-75,  b"C", 3, ...)  ← v=75
4. (-50,  b"B", 1, ...)  ← v=50

Decode:
[(100, "A"), (100, "A"), (75, "C"), (50, "B")]"""
    )
    
    # 2. Parallel sorting
    print_section(
        "2. PARALLEL SORTING (dòng 41-62)",
        [
            "num_proc = min(8, cpu_count(), n)",
            "chunk_size = (n + num_proc - 1) // num_proc",
            "tasks = [(start, min(start + chunk_size, n)) for start in range(0, n, chunk_size)]",
            "ctx = multiprocessing.get_context('fork')",
            "with ctx.Pool(processes=len(tasks), initializer=init_worker, initargs=(records,)) as pool:",
            "    chunks = pool.map(sort_part, tasks)",
            "records = []",
            "for chunk in chunks:",
            "    records.extend(chunk)  # Merge chunks",
            "records.sort()  # Sort lần cuối",
            "return [(x[3], x[4].decode()) for x in records]",
        ],
        f"""
{Colors.GREEN}✅ Giải thích chi tiết:{Colors.ENDC}

{Colors.YELLOW}Thuật toán 2-phase sort:{Colors.ENDC}
• Phase 1: Mỗi worker sort chunk của mình
• Phase 2: Merge tất cả chunks → sort lại

{Colors.YELLOW}Tại sao cần sort lại sau merge?:{Colors.ENDC}
• Sort chunk 1: [(3,A), (1,B)] → [(1,B), (3,A)]
• Sort chunk 2: [(4,A), (2,B)] → [(2,B), (4,A)]
• Merge: [(1,B), (3,A), (2,B), (4,A)] → KHÔNG sorted!
• Sort lại: [(1,B), (2,B), (3,A), (4,A)] ✓

{Colors.YELLOW}Tại sao không merge trực tiếp?:{Colors.ENDC}
• Merge k-way phức tạp
• Chỉ sort lại O(n log n) → đủ nhanh cho large n
        """,
        """
n=8, num_proc=4, chunk_size=2

Tasks:
  Task 0: (0, 2) → records[0:2]
  Task 1: (2, 4) → records[2:4]
  Task 2: (4, 6) → records[4:6]
  Task 3: (6, 8) → records[6:8]

Workers:
  Worker 0: sort records[0:2] = [(-5,), (-3,)] → [(-5,), (-3,)]
  Worker 1: sort records[2:4] = [(-8,), (-1,)] → [(-8,), (-1,)]
  Worker 2: sort records[4:6] = [(-2,), (-7,)] → [(-7,), (-2,)]
  Worker 3: sort records[6:8] = [(-6,), (-4,)] → [(-6,), (-4,)]

Merge:
  chunks = [[(-5,), (-3,)], [(-8,), (-1,)], [(-7,), (-2,)], [(-6,), (-4,)]]
  records = [(-5,), (-3,), (-8,), (-1,), (-7,), (-2,), (-6,), (-4,)]
  
Sort cuối:
  records = [(-8,), (-7,), (-6,), (-5,), (-4,), (-3,), (-2,), (-1,)]"""
    )
    
    print(f"\n{Colors.GREEN}🎉 HOÀN THÀNH CHALLENGE 4!{Colors.ENDC}\n")

# ============================================================
# CHALLENGE 5: BYTE-RANGE SEARCH (challenge5.py - 174 dòng)
# ============================================================
def demo_challenge5():
    print_header("CHALLENGE 5: Byte-Range Search (174 dòng)")
    
    # 1. Constants
    print_section(
        "1. CONSTANTS (dòng 4-8)",
        [
            "_BODY = b\"\"",
            "_KEY = b\"\"",
            "_MAX_WORKERS = 8",
            "_CHUNK_MIN_BYTES = 250000",
            "_MAX_FALSE_HITS = 64",
        ],
        f"""
{Colors.GREEN}✅ Giải thích:{Colors.ENDC}
• _BODY, _KEY: global variables cho workers
• _MAX_WORKERS = 8: tối đa 8 processes
• _CHUNK_MIN_BYTES = 250000: chunk tối thiểu 250KB
• _MAX_FALSE_HITS = 64: tối đa 64 false hits trước khi fallback
        """,
        """
Khi n=1 triệu bytes:
  workers = min(cpu_count, 8, max(1, 1000000/250000))
         = min(8, 8, 4) = 4
  
4 workers, mỗi worker xử lý ~250KB"""
    )
    
    # 2. _is_boundary
    print_section(
        "2. _is_boundary() - KIỂM TRA WORD BOUNDARY (dòng 25-29)",
        [
            "def _is_boundary(body, start, end):",
            "    return (",
            "        (start == 0 or body[start - 1] <= 32) and",
            "        (end == len(body) or body[end] <= 32)",
            "    )",
        ],
        f"""
{Colors.GREEN}✅ Giải thích:{Colors.ENDC}
• Kiểm tra xem [start:end] có phải là một token riêng không
• body[start-1] phải là whitespace (ASCII ≤ 32) hoặc start=0
• body[end] phải là whitespace (ASCII ≤ 32) hoặc end=len

{Colors.YELLOW}Tại sao cần kiểm tra?:{Colors.ENDC}
• Tìm "10" trong "110" sẽ nhầm!
• "10" xuất hiện trong "110" nhưng không phải token riêng
        """,
        """
Tìm "10" trong "10 110 1000 100":

Vị trí pos=0 (đầu tiên):
  start=0, end=2
  start==0 ✓
  body[2]=' ' (space, ASCII 32) ✓
  → IS BOUNDARY ✓

Vị trí pos=3 trong "110":
  start=3, end=5
  start>0, body[2]=' ' (space) ✓
  body[5]=' ' ✓
  → IS BOUNDARY ✓ (NHẦM!)

Vị trí pos=3 trong "110" (byte tiếp theo):
  body.find("10", 3) → pos=3
  start=3, body[2]=' ' ✓
  end=5, body[5]='1' (ASCII 49) ✗
  → NOT BOUNDARY ✓ (Đúng!)"""
    )
    
    # 3. _find_index_in_range
    print_section(
        "3. _find_index_in_range() - TÌM VỊ TRÍ (dòng 32-56)",
        [
            "def _find_index_in_range(body, key, start, end):",
            "    if len(key) == 1:",
            "        return body[start:end].split().index(key)",
            "    pos = start",
            "    false_hits = 0",
            "    while True:",
            "        pos = body.find(key, pos, end)",
            "        if pos == -1: return -1",
            "        token_end = pos + len(key)",
            "        if token_end <= end and _is_boundary(body, pos, token_end):",
            "            return len(body[start:pos].split())  # Index",
            "        false_hits += 1",
            "        if false_hits > _MAX_FALSE_HITS:",
            "            return body[start:end].split().index(key)  # Fallback",
            "        pos += 1",
        ],
        f"""
{Colors.GREEN}✅ Giải thích chi tiết:{Colors.ENDC}

{Colors.YELLOW}Thuật toán tìm kiếm:{Colors.ENDC}
1. body.find(key, pos, end) → tìm vị trí xuất hiện
2. Kiểm tra boundary → có phải token riêng không
3. Đếm số tokens trước vị trí → index

{Colors.YELLOW}False hits và fallback:{Colors.ENDC}
• key xuất hiện nhiều lần trong body nhưng không phải word
• Đếm false_hits
• > 64 false hits → fallback dùng split().index()
        """,
        """
body = b"10 110 1000 100", key = b"10"
start = 0, end = len(body)

pos = body.find(b"10", 0, 18) → pos = 0
  token_end = 2
  _is_boundary(0, 2) → True ✓
  return len(b"10 ".split()) = 1
  → Index = 1 ✓ (token thứ 2)

Tìm b"10" trong b"10 110 1000 100":

pos=0: body[0:2] = b"10", boundary ✓ → return 1
pos=6: body[6:8] = b"10" (trong b"110")
  body[5] = b' ' ✓
  body[8] = b'1' (không phải space) ✗
  → NOT BOUNDARY, false_hits++

pos=11: body[11:13] = b"10" (trong b"1000")
  body[10] = b' ' ✓
  body[13] = b'0' (không phải space) ✗
  → NOT BOUNDARY, false_hits++

pos=15: body[15:17] = b"10" (trong b"100")
  body[14] = b' ' ✓
  body[17] = b'' (end of body) ✓
  → BOUNDARY ✓ → return 4

Kết quả: index = 4 (token thứ 4)"""
    )
    
    # 4. _make_ranges
    print_section(
        "4. _make_ranges() - CHIA BODY THÀNH CHUNKS (dòng 59-83)",
        [
            "def _make_ranges(n, workers):",
            "    ranges = []",
            "    body = _BODY",
            "    chunk_size = (n + workers - 1) // workers",
            "    start = 0",
            "    while start < n:",
            "        while start < n and body[start] <= 32:",
            "            start += 1  # Bỏ qua leading whitespace",
            "        if start >= n: break",
            "        end = start + chunk_size",
            "        if end >= n:",
            "            end = n",
            "        else:",
            "            while end < n and body[end] > 32:",
            "                end += 1  # Đến whitespace kế tiếp",
            "        ranges.append((start, end))",
            "        start = end",
            "    return ranges",
        ],
        f"""
{Colors.GREEN}✅ Giải thích chi tiết:{Colors.ENDC}

{Colors.YELLOW}Mục đích:{Colors.ENDC}
• Chia body thành chunks cho workers
• Mỗi chunk bắt đầu và kết thúc ở whitespace

{Colors.YELLOW}Tại sao phải align với whitespace?:{Colors.ENDC}
• Worker xử lý [start, end)
• Tìm key trong chunk
• Đếm tokens từ start → vị trí tìm thấy
• Nếu cắt giữa token → đếm sai!
        """,
        """
body = b"10 110 1000 100 20 30", n=22
workers=3
chunk_size = ceil(22/3) = 8

start=0:
  body[0]=' ' → bỏ qua
  start=1
  end = 1 + 8 = 9
  body[1..8] = b"10 110 1"
  body[9]='0' (không phải space) → end++ đến khi gặp space
  end = 13 (body[13]=' ')
  ranges: [(1, 13)]

start=13:
  body[13]=' ' → bỏ qua
  start=14
  end = 14 + 8 = 22
  end >= n → end = 22
  ranges: [(14, 22)]

Ranges: [(1, 13), (14, 22)]

Worker 1: tìm trong b"10 110 1000"
Worker 2: tìm trong b"100 20 30\""""
    )
    
    # 5. MAIN
    print_section(
        "5. MAIN() - ENTRY POINT (dòng 161-174)",
        [
            "def MAIN(input_file_path):",
            "    with open(input_file_path, 'rb') as f:",
            "        raw = f.read()",
            "    if not raw: return -1",
            "    parts = raw.split(None, 1)  # Tách dòng đầu",
            "    if len(parts) == 1: return -1",
            "    key = str(int(parts[0])).encode()  # Chuyển số → bytes",
            "    return _search_parallel(parts[1], key)",
        ],
        f"""
{Colors.GREEN}✅ Giải thích:{Colors.ENDC}

{Colors.YELLOW}Input format:{Colors.ENDC}
• Dòng đầu: số cần tìm
• Phần còn lại: body để tìm kiếm

{Colors.YELLOW}Chuyển đổi:{Colors.ENDC}
• parts[0] = b"10" → int("10") = 10 → str(10) = "10" → b"10"
• parts[1] = body cần tìm
        """,
        """
Input File:
Line 1: 10
Line 2: 10 110 1000 100 20 30 40

raw = b'10\\n10 110 1000 100 20 30 40\\n'
parts = raw.split(None, 1)

key = str(int(parts[0])).encode()
body = parts[1]

_search_parallel(body, key)
Kết quả: 0"""
    )
    
    print(f"\n{Colors.GREEN}🎉 HOÀN THÀNH CHALLENGE 5!{Colors.ENDC}\n")

# ============================================================
# MENU CHÍNH
# ============================================================
def show_menu():
    print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════╗
║{Colors.ENDC}      {Colors.BOLD}🎯 VISUAL DEMOS - HIỂU CODE QUA VÍ DỤ{Colors.ENDC}         {Colors.CYAN}║
╠══════════════════════════════════════════════════════════╣
║{Colors.ENDC}  Chọn challenge để xem demo chi tiết:               {Colors.CYAN}║
║{Colors.ENDC}                                                          {Colors.CYAN}║
║{Colors.ENDC}  1. 📁 Challenge 1: Byte-Range File Splitting        {Colors.CYAN}║
║{Colors.ENDC}  2. 🔢 Challenge 2: Fast Doubling Fibonacci           {Colors.CYAN}║
║{Colors.ENDC}  3. 📐 Challenge 3: Parallel Matrix Multiplication     {Colors.CYAN}║
║{Colors.ENDC}  4. 📊 Challenge 4: Parallel Sorting Records            {Colors.CYAN}║
║{Colors.ENDC}  5. 🔍 Challenge 5: Byte-Range Search                   {Colors.CYAN}║
║{Colors.ENDC}  6. 📍 Challenge 6: Closest Pair of Points           {Colors.CYAN}║
║{Colors.ENDC}  0. 🚪 Thoát                                          {Colors.CYAN}║
╚══════════════════════════════════════════════════════════╝
{Colors.ENDC}
    """)
    return input(f"  {Colors.YELLOW}Nhập lựa chọn (0-6): {Colors.ENDC}")

def main():
    while True:
        print(f"\n{Colors.CLEAR}")
        choice = show_menu()
        
        if choice == '1':
            demo_challenge1()
        elif choice == '2':
            demo_challenge2()
        elif choice == '3':
            demo_challenge3()
        elif choice == '4':
            demo_challenge4()
        elif choice == '5':
            demo_challenge5()
        elif choice == '6':
            print(f"\n{Colors.YELLOW}Xem demo chi tiết Challenge 6 trong file code_guide.html{Colors.ENDC}")
            print(f"{Colors.YELLOW}Hoặc chạy: python3 visual_demos.py và chọn 6{Colors.ENDC}\n")
            input_continue()
        elif choice == '0':
            print(f"\n{Colors.GREEN}👋 Tạm biệt!{Colors.ENDC}\n")
            break
        else:
            print(f"\n{Colors.RED}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
            time.sleep(1)

if __name__ == "__main__":
    main()