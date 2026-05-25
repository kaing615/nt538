import multiprocessing

SHIFT = 17
BASE = 1 << SHIFT
MASK = BASE - 1

MAX_A = 200000000
MAX_HIGH = MAX_A >> SHIFT

Q_GLOBAL = 1
VALUES_GLOBAL = None
OUT_GLOBAL = None

LOW_F_GLOBAL = None
LOW_G_GLOBAL = None
HIGH_F_GLOBAL = None
HIGH_PREV_GLOBAL = None


def fib_pair_mod(n, q):
    a = 0
    b = 1

    if n == 0:
        return 0, 1

    mask = 1 << (n.bit_length() - 1)

    while mask:
        t = b + b - a
        if t < 0:
            t += q
        elif t >= q:
            t -= q

        c = (a * t) % q
        d = (a * a + b * b) % q

        if n & mask:
            s = c + d
            if s >= q:
                s -= q
            a = d
            b = s
        else:
            a = c
            b = d

        mask >>= 1

    return a, b


def precompute_low(q):
    f = [0] * BASE
    g = [0] * BASE

    a = 0
    b = 1

    for i in range(BASE):
        f[i] = a
        g[i] = b

        s = a + b
        if s >= q:
            s -= q

        a = b
        b = s

    return f, g


def precompute_high(max_high, q):
    size = max_high + 1

    f = [0] * size
    prevs = [0] * size

    step_f, step_g = fib_pair_mod(BASE, q)

    a = 0
    b = 1

    for i in range(size):
        f[i] = a

        prev = b - a
        if prev < 0:
            prev += q

        prevs[i] = prev

        na = (a * step_g + prev * step_f) % q
        nb = (a * step_f + b * step_g) % q

        a = na
        b = nb

    return f, prevs


def worker_block(lo, hi):
    q = Q_GLOBAL
    values = VALUES_GLOBAL
    out = OUT_GLOBAL

    low_f = LOW_F_GLOBAL
    low_g = LOW_G_GLOBAL
    high_f = HIGH_F_GLOBAL
    high_prev = HIGH_PREV_GLOBAL

    mask = MASK
    shift = SHIFT

    for i in range(lo, hi):
        x = values[i]

        l = x & mask
        h = x >> shift

        out[i] = (high_f[h] * low_g[l] + high_prev[h] * low_f[l]) % q


def parallel_block(values, q):
    global Q_GLOBAL
    global VALUES_GLOBAL
    global OUT_GLOBAL
    global LOW_F_GLOBAL
    global LOW_G_GLOBAL
    global HIGH_F_GLOBAL
    global HIGH_PREV_GLOBAL

    n = len(values)

    Q_GLOBAL = q
    VALUES_GLOBAL = values
    OUT_GLOBAL = multiprocessing.RawArray("I", n)

    LOW_F_GLOBAL, LOW_G_GLOBAL = precompute_low(q)
    HIGH_F_GLOBAL, HIGH_PREV_GLOBAL = precompute_high(MAX_HIGH, q)

    ctx = multiprocessing.get_context("fork")

    if n >= 4:
        q1 = n >> 2
        q2 = n >> 1
        q3 = q1 + q2

        p1 = ctx.Process(target=worker_block, args=(0, q1))
        p2 = ctx.Process(target=worker_block, args=(q1, q2))
        p3 = ctx.Process(target=worker_block, args=(q2, q3))

        p1.start()
        p2.start()
        p3.start()

        worker_block(q3, n)

        p1.join()
        p2.join()
        p3.join()
    else:
        worker_block(0, n)

    return OUT_GLOBAL[:]


def MAIN(input_file_path):
    with open(input_file_path, "rb") as f:
        tokens = f.read().split()

    if not tokens:
        return []

    it = iter(tokens)
    n = int(next(it))
    q = int(next(it))

    if n == 0:
        return []

    if q == 1:
        return [0] * n

    arr = list(map(int, it))
    del tokens

    if q == 2:
        return [0 if x % 3 == 0 else 1 for x in arr]

    return parallel_block(arr, q)