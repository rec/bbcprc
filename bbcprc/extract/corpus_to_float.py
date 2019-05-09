from .. data import READ, WRITE


def corpus_to_float():
    corpus = READ.corpus()
    outfile = WRITE.corpus.float32(shape=len(corpus), dtype='float32')
    outfile[:] = corpus[:, 0]
    outfile[:] += corpus[:, 1]
    outfile /= 0x10000


if __name__ == '__main__':
    corpus_to_float()
