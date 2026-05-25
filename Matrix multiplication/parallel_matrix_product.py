import multiprocessing
import time

A_GLOBAL = None
BT_GLOBAL = None
N_GLOBAL = 0


def init_worker(A, BT, N):
global A_GLOBAL, BT_GLOBAL, N_GLOBAL
A_GLOBAL = A
BT_GLOBAL = BT
N_GLOBAL = N


def compute_block(task):
start, end = task

A = A_GLOBAL
BT = BT_GLOBAL
N = N_GLOBAL

block = []
diag_main_part = []
diag_secondary_part = []
block_sum = 0

for i in range(start, end):
row_a = A[i]
row_c = [0] * N

for j in range(N):
col_b = BT[j]

s = 0
for k in range(N):
s += row_a[k] * col_b[k]

row_c[j] = s

block.append(row_c)

diag_main_part.append(row_c[i])
diag_secondary_part.append(row_c[N - 1 - i])
block_sum += sum(row_c)

return start, block, diag_main_part, diag_secondary_part, block_sum


def read_matrix_input(input_file_path):
with open(input_file_path, "rb") as f:
first_line = f.readline()

if not first_line:
return 0, [], []

N = int(first_line.strip())

A = []
for _ in range(N):
A.append(list(map(int, f.readline().split())))

B = []
for _ in range(N):
B.append(list(map(int, f.readline().split())))

return N, A, B


def MAIN(input_file_path):
N, A, B = read_matrix_input(input_file_path)

if N == 0:
return {
"matrix": [],
"diag_main": [],
"diag_secondary": [],
"total_sum": 0
}

BT = [list(col) for col in zip(*B)]

num_processes = min(multiprocessing.cpu_count(), N)

num_tasks = num_processes * 4
rows_per_task = max(1, (N + num_tasks - 1) // num_tasks)

tasks = []
for start in range(0, N, rows_per_task):
end = min(start + rows_per_task, N)
tasks.append((start, end))

C = [None] * N
diag_main = [0] * N
diag_secondary = [0] * N
total_sum = 0

if num_processes == 1:
init_worker(A, BT, N)

for task in tasks:
start, block, dm, ds, subtotal = compute_block(task)

block_len = len(block)
C[start:start + block_len] = block
diag_main[start:start + block_len] = dm
diag_secondary[start:start + block_len] = ds
total_sum += subtotal
else:
with multiprocessing.Pool(
processes=num_processes,
initializer=init_worker,
initargs=(A, BT, N)
) as pool:

for start, block, dm, ds, subtotal in pool.imap_unordered(
compute_block,
tasks,
chunksize=1
):
block_len = len(block)
C[start:start + block_len] = block
diag_main[start:start + block_len] = dm
diag_secondary[start:start + block_len] = ds
total_sum += subtotal

return {
"matrix": C,
"diag_main": diag_main,
"diag_secondary": diag_secondary,
"total_sum": total_sum
}

def MAIN_TIMED(input_file_path):
start_time = time.perf_counter()

result = MAIN(input_file_path)

end_time = time.perf_counter()
elapsed_time = end_time - start_time

print("Thoi gian thuc hien:", elapsed_time, "giay")

return result

if __name__ == '__main__':
multiprocessing.set_start_method('fork', force=True)

input_file_path = "input.txt"

result = MAIN_TIMED(input_file_path)

print("Matrix C:")
for row in result["matrix"]:
print(" ".join(map(str, row)))

print("\nMain diagonal:", " ".join(map(str, result["diag_main"])))
print("Secondary diagonal:", " ".join(map(str, result["diag_secondary"])))
print("Total sum of elements in C:", result["total_sum"])