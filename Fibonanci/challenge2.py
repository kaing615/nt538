import multiprocessing

Q_GLOBAL = 1

def init_worker(q):
    global Q_GLOBAL
    Q_GLOBAL = q


def fib_mod(n, q):
    if q == 1:
        return 0

    a = 0
    b = 1

    for k in range(n.bit_length() - 1, -1, -1):
        c = (a * ((b + b - a) % q)) % q
        d = (a * a + b * b) % q

        if (n >> k) & 1:
            a = d
            b = (c + d) % q
        else:
            a = c
            b = d

    return a


def fib_mod_worker(n):
    q = Q_GLOBAL

    a = 0
    b = 1

    for k in range(n.bit_length() - 1, -1, -1):
        c = (a * ((b + b - a) % q)) % q
        d = (a * a + b * b) % q

        if (n >> k) & 1:
            a = d
            b = (c + d) % q
        else:
            a = c
            b = d

    return a


def MAIN(input_file_path):
    with open(input_file_path, "rb") as f:
        data = list(map(int, f.read().split()))

    if not data:
        return []

    n = data[0]
    q = data[1]

    if n == 0:
        return []

    if q == 1:
        return [0] * n

    arr = data[2:2 + n]

    unique = list(set(arr))
    m = len(unique)

    if m == 1:
        return [fib_mod(unique[0], q)] * n

    if m < 2000:
        lookup = {}
        for x in unique:
            lookup[x] = fib_mod(x, q)

        return [lookup[x] for x in arr]

    num_proc = min(multiprocessing.cpu_count(), m)

    chunksize = max(1, m // (num_proc * 4))

    ctx = multiprocessing.get_context("fork")

    with ctx.Pool(
        processes=num_proc,
        initializer=init_worker,
        initargs=(q,)
    ) as pool:
        values = pool.map(fib_mod_worker, unique, chunksize=chunksize)

    lookup = dict(zip(unique, values))

    return [lookup[x] for x in arr]
    