
import itertools
def eratosthenes():
    print("inside")
    '''Yields the sequence of prime numbers via the Sieve of Eratosthenes.'''
    D = {  }
    print("UUUUUUUUUUUU")
    # map each composite integer to its first-found prime factor
    for q in itertools.count(2):     # q gets 2, 3, 4, 5, ... ad infinitum
        p = D.pop(q, None)
        if p is None:
            # q not a key in D, so q is prime, therefore, yield it
            yield q
            print("00000000000",q)
            # mark q squared as not-prime (with q as first-found prime factor)
            D[ q *q] = q
        else:
            # let x <- smallest (N*p)+q which wasn't yet known to be composite
            # we just learned x is composite, with p first-found prime factor,
            # since p is the first-found prime factor of q -- find and mark it
            x = p + q
            while x in D:
                x += p
            D[x] = p
            print("11111111111",D)
        print("2222222222222",D)
    print("333333333333",D)
eratosthenes()