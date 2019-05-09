from .. data import READ, WRITE
from icecream import ic

DIVISOR = 1


def corpus_to_float():
    ic()
    corpus = READ.corpus()
    ic()
    length = len(corpus) // DIVISOR
    outfile = WRITE.corpus.float32(shape=length, dtype='float32')
    ic()
    outfile[:] = corpus[:length, 0]
    ic()
    outfile[:] += corpus[:length, 1]
    ic()
    outfile /= 0x10000
    ic()


if __name__ == '__main__':
    corpus_to_float()
