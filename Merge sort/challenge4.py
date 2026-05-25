import multiprocessing
import os

DATA = None


def init_worker(data):
    global DATA
    DATA = data


def sort_part(task):
    start, end = task
    return sorted(DATA[start:end])


def MAIN(input_file_path):
    with open(input_file_path, "rb") as f:
        tokens = f.read().split()

    if not tokens:
        return []

    n = int(tokens[0])
    if n == 0:
        return []

    records = []
    pos = 1

    for i in range(n):
        v = int(tokens[pos])
        label = tokens[pos + 1]
        records.append((-v, label, i, v, label))
        pos += 2

    if n < 20000:
        records.sort()
        return [(x[3], x[4].decode()) for x in records]

    num_proc = min(8, multiprocessing.cpu_count(), n)
    chunk_size = (n + num_proc - 1) // num_proc

    tasks = [
        (start, min(start + chunk_size, n))
        for start in range(0, n, chunk_size)
    ]

    ctx = multiprocessing.get_context("fork")

    with ctx.Pool(
        processes=len(tasks),
        initializer=init_worker,
        initargs=(records,)
    ) as pool:
        chunks = pool.map(sort_part, tasks)

    records = []
    for chunk in chunks:
        records.extend(chunk)

    records.sort()

    return [(x[3], x[4].decode()) for x in records]


if __name__ == "__main__":
    result = MAIN("input.txt")
    print(result)
