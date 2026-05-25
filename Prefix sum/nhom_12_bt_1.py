import multiprocessing as mp

def local_prefix_sum(chunk):
res = []
sum = 0
for x in chunk:
sum += x
res.append(sum)
return res

def prefix_sum(a, cores):
if not a:
return []

chunk_size = (len(a) // cores) + 1 
chunks = [a[i:i + chunk_size] for i in range(0, len(a), chunk_size)]

with mp.Pool(cores) as pool:
local_sums = pool.map(local_prefix_sum, chunks)

offsets = [0]

for i in range(1, len(local_sums)):
offsets.append(offsets[-1] + local_sums[i-1][-1])

result = []

for i, chunk in enumerate(local_sums):
for x in chunk:
result.append(x + offsets[i])

return result

if __name__ == "__main__":
a = [i + 1 for i in range(1000)]
b = prefix_sum(a, mp.cpu_count())
print(b)
