import math
import multiprocessing


_INF = 10**40
_OFFSET = 1000000000
_MASK = (1 << 32) - 1
_NEIGHBORS = 8
_PARALLEL_SINGLE_MIN = 120000
_PARALLEL_TOTAL_MIN = 50000
_PARALLEL_CHUNK_MIN = 50000
_MAX_WORKERS = 16

_CPU_COUNT = multiprocessing.cpu_count() or 1
_GLOBAL_XS = []
_GLOBAL_YS = []
_GLOBAL_DATASETS = []


def _get_fork_context():
    try:
        ctx = multiprocessing.get_context("fork")
    except ValueError:
        return None

    if ctx.get_start_method() != "fork":
        return None

    return ctx


def _scan_range(xs, ys, left, right):
    n = len(xs)
    if n < 2:
        return _INF

    if right > n - 1:
        right = n - 1

    best = _INF
    neighbors = _NEIGHBORS
    i = left

    while i < right:
        x = xs[i]
        y = ys[i]
        end = i + neighbors + 1

        if end > n:
            end = n

        j = i + 1
        while j < end:
            dx = xs[j] - x
            dx2 = dx * dx

            if dx2 >= best:
                break

            dy = ys[j] - y
            dist = dx2 + dy * dy

            if dist < best:
                if dist == 0:
                    return 0
                best = dist

            j += 1

        i += 1

    return best


def _scan_worker(left, right, result_queue):
    try:
        result_queue.put(_scan_range(_GLOBAL_XS, _GLOBAL_YS, left, right))
    except BaseException as exc:
        result_queue.put(exc)


def _scan_parallel(xs, ys):
    n = len(xs)

    if _CPU_COUNT < 2 or n < _PARALLEL_SINGLE_MIN:
        return _scan_range(xs, ys, 0, n - 1)

    ctx = _get_fork_context()
    if ctx is None:
        return _scan_range(xs, ys, 0, n - 1)

    chunks = min(
        _CPU_COUNT,
        _MAX_WORKERS,
        (n - 1) // _PARALLEL_CHUNK_MIN
    )

    if chunks < 2:
        return _scan_range(xs, ys, 0, n - 1)

    global _GLOBAL_XS
    global _GLOBAL_YS
    _GLOBAL_XS = xs
    _GLOBAL_YS = ys

    result_queue = ctx.SimpleQueue()
    processes = []
    total = n - 1

    for chunk in range(chunks):
        left = total * chunk // chunks
        right = total * (chunk + 1) // chunks
        process = ctx.Process(
            target=_scan_worker,
            args=(left, right, result_queue)
        )
        process.start()
        processes.append(process)

    best = _INF
    error = None

    for _ in processes:
        value = result_queue.get()

        if isinstance(value, BaseException):
            error = value
        elif value < best:
            best = value

    for process in processes:
        process.join()

    _GLOBAL_XS = []
    _GLOBAL_YS = []

    if error is not None:
        raise error

    return best


def _scan_transposed(xs, ys):
    n = len(xs)
    if n < 2:
        return _INF

    swapped = [0] * n

    for i in range(n):
        swapped[i] = (ys[i] << 32) | xs[i]

    swapped.sort()

    tx = [0] * n
    ty = [0] * n
    mask = _MASK

    for i in range(n):
        value = swapped[i]
        tx[i] = value >> 32
        ty[i] = value & mask

    return _scan_parallel(tx, ty)


def _solve_encoded(values, use_parallel):
    n = len(values)
    if n < 2:
        values.clear()
        return _INF

    values.sort()

    xs = [0] * n
    ys = [0] * n
    mask = _MASK
    previous = values[0]
    previous_x = previous >> 32
    xs[0] = previous_x
    ys[0] = previous & mask
    x_run = 1
    max_x_run = 1

    for i in range(1, n):
        value = values[i]

        if value == previous:
            values.clear()
            return 0

        previous = value
        x = value >> 32
        xs[i] = x
        ys[i] = value & mask

        if x == previous_x:
            x_run += 1

            if x_run > max_x_run:
                max_x_run = x_run
        else:
            previous_x = x
            x_run = 1

    values.clear()

    if use_parallel:
        best = _scan_parallel(xs, ys)
    else:
        best = _scan_range(xs, ys, 0, n - 1)

    if max_x_run > _NEIGHBORS:
        transposed_best = _scan_transposed(xs, ys)

        if transposed_best < best:
            best = transposed_best

    return best


def _dataset_worker(indices, result_queue):
    try:
        datasets = _GLOBAL_DATASETS
        result_queue.put([
            (index, _solve_encoded(datasets[index], False))
            for index in indices
        ])
    except BaseException as exc:
        result_queue.put([(-1, exc)])


def _solve_all(datasets, total_points):
    q = len(datasets)

    if q == 1:
        return [_solve_encoded(datasets[0], True)]

    workers = min(_CPU_COUNT, q, _MAX_WORKERS)
    ctx = _get_fork_context()

    if workers < 2 or total_points < _PARALLEL_TOTAL_MIN or ctx is None:
        return [_solve_encoded(values, False) for values in datasets]

    groups = [[] for _ in range(workers)]
    loads = [0] * workers

    for index in sorted(range(q), key=lambda item: len(datasets[item]), reverse=True):
        target = 0
        smallest = loads[0]

        for worker_index in range(1, workers):
            load = loads[worker_index]

            if load < smallest:
                smallest = load
                target = worker_index

        groups[target].append(index)
        loads[target] += len(datasets[index])

    global _GLOBAL_DATASETS
    _GLOBAL_DATASETS = datasets

    result_queue = ctx.SimpleQueue()
    processes = []

    for indices in groups:
        process = ctx.Process(
            target=_dataset_worker,
            args=(indices, result_queue)
        )
        process.start()
        processes.append(process)

    result = [None] * q
    error = None

    for _ in processes:
        batch = result_queue.get()

        for index, value in batch:
            if index == -1:
                error = value
            else:
                result[index] = value

    for process in processes:
        process.join()

    _GLOBAL_DATASETS = []

    if error is not None:
        raise error

    return result


def _encode_dataset(data, left, right):
    offset = _OFFSET
    return [
        ((data[i] + offset) << 32) | (data[i + 1] + offset)
        for i in range(left, right, 2)
    ]


def MAIN(input_file_path):
    with open(input_file_path, "rb") as f:
        data = list(map(int, f.read().split()))

    if not data:
        return []

    q = data[0]
    pos = 1
    datasets = []
    total_points = 0

    for _ in range(q):
        n = data[pos]
        pos += 1
        end = pos + n + n
        total_points += n
        datasets.append(_encode_dataset(data, pos, end))
        pos = end

    del data

    answer = []
    append = answer.append

    for dist2 in _solve_all(datasets, total_points):
        if dist2 == _INF:
            append(0.0)
        else:
            append(round(math.sqrt(dist2), 4))

    return answer


if __name__ == "__main__":
    for value in MAIN("large_input.txt"):
        print(f"{value:.4f}")
