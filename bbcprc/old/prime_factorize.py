import math

def prime_factorize(n):
    factors = []
    number = abs(n)
    factor = 2

    while number > 1:
        factor = get_next_prime_factor(number, factor)
        factors.append(factor)
        number //= factor

    if n < -1:  # If we'd check for < 0, -1 would give us trouble
        factors[0] = -factors[0]

    return factors


def get_next_prime_factor(n, f):
    if n % 2 == 0:
        return 2

    # Not 'good' [also] checking non-prime numbers I guess?
    # But the alternative, creating a list of prime numbers,
    # wouldn't it be more demanding? Process of creating it.
    for x in range(max(f, 3), int(math.sqrt(n) + 1), 2):
        if n % x == 0:
            return x

    return n

def run():
    N = 76358303439
    for i in range(10):
        print(N, prime_factorize(N + i))


run()
