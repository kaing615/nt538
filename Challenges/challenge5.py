import multiprocessing


_BODY = b""
_KEY = b""
_MAX_WORKERS = 8
_CHUNK_MIN_BYTES = 250000
_MAX_FALSE_HITS = 64


def _context():
    try:
        return multiprocessing.get_context("fork")
    except ValueError:
        return None


def _split_index(body, key, start, end):
    try:
        return body[start:end].split().index(key)
    except ValueError:
        return -1


def _is_boundary(body, start, end):
    return (
        (start == 0 or body[start - 1] <= 32) and
        (end == len(body) or body[end] <= 32)
    )


def _find_index_in_range(body, key, start, end):
    if len(key) == 1:
        return _split_index(body, key, start, end)

    pos = start
    key_len = len(key)
    false_hits = 0

    while True:
        pos = body.find(key, pos, end)

        if pos == -1:
            return -1

        token_end = pos + key_len

        if token_end <= end and _is_boundary(body, pos, token_end):
            return len(body[start:pos].split())

        false_hits += 1

        if false_hits > _MAX_FALSE_HITS:
            return _split_index(body, key, start, end)

        pos += 1


def _make_ranges(n, workers):
    ranges = []
    body = _BODY
    chunk_size = (n + workers - 1) // workers
    start = 0

    while start < n:
        while start < n and body[start] <= 32:
            start += 1

        if start >= n:
            break

        end = start + chunk_size

        if end >= n:
            end = n
        else:
            while end < n and body[end] > 32:
                end += 1

        ranges.append((start, end))
        start = end

    return ranges


def _search_worker(index, start, end, queue):
    try:
        queue.put((index, _find_index_in_range(_BODY, _KEY, start, end)))
    except BaseException as exc:
        queue.put((-1, exc))


def _count_before(ranges, found_range, found_local):
    total = found_local

    for start, end in ranges[:found_range]:
        total += len(_BODY[start:end].split())

    return total


def _search_parallel(body, key):
    global _BODY, _KEY
    _BODY = body
    _KEY = key

    n = len(body)
    if n == 0:
        return -1

    ctx = _context()

    if ctx is None:
        return _find_index_in_range(body, key, 0, n)

    workers = min(
        multiprocessing.cpu_count() or 1,
        _MAX_WORKERS,
        max(1, (n + _CHUNK_MIN_BYTES - 1) // _CHUNK_MIN_BYTES)
    )
    ranges = _make_ranges(n, workers)

    if not ranges:
        return -1

    queue = ctx.SimpleQueue()
    processes = []

    for index, (start, end) in enumerate(ranges):
        process = ctx.Process(
            target=_search_worker,
            args=(index, start, end, queue)
        )
        process.start()
        processes.append(process)

    found = [None] * len(processes)
    error = None

    for _ in processes:
        index, value = queue.get()

        if index == -1:
            error = value
        else:
            found[index] = value

    for process in processes:
        process.join()

    if error is not None:
        raise error

    for index, local_index in enumerate(found):
        if local_index != -1:
            return _count_before(ranges, index, local_index)

    return -1


def MAIN(input_file_path):
    with open(input_file_path, "rb") as f:
        raw = f.read()

    if not raw:
        return -1

    parts = raw.split(None, 1)

    if len(parts) == 1:
        return -1

    key = str(int(parts[0])).encode()
    return _search_parallel(parts[1], key)