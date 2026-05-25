import multiprocessing as mp
import random

ROWS = 1000
COLS = 1000

def local_prefix_sum(chunk):
res = []
total = 0

for x in chunk:
total += x
res.append(total)

return res

def scan_exclusive(a, cores=mp.cpu_count()):
if not a:
return [], 0

chunk_size = (len(a) + cores - 1) // cores
chunks = [a[i:i + chunk_size] for i in range(0, len(a), chunk_size)]

with mp.Pool(cores) as pool:
local_sums = pool.map(local_prefix_sum, chunks)

inclusive = []
total = 0
for sums in local_sums:
inclusive.extend([s + total for s in sums])
total += sums[-1]

exclusive = [0] + inclusive[:-1]

return exclusive, inclusive[-1] if inclusive else 0

def flatten(A, num_processes=mp.cpu_count()):
with mp.Pool(processes=num_processes) as pool:
sizes = pool.map(len, A)

offsets, total_size = scan_exclusive(sizes, num_processes)
result = [0] * total_size

for i in range(len(A)):
offset = offsets[i]
result[offset:offset + len(A[i])] = A[i]

return result


if __name__ == "__main__":
A = [
[random.randint(0, 100000) for _ in range(COLS)]
for _ in range(ROWS)
]

result = flatten(A)

print(len(result))