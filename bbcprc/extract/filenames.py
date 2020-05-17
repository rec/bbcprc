from ..data import WRITE
from ..data.corpus import Corpus
import pathlib


def extract():
    shape = (len(Corpus.filenames),)
    data = WRITE.filenames(dtype='int32', shape=shape)
    data[:] = [int(pathlib.Path(f).stem) for f in Corpus.filenames]

    print('Extracted', len(Corpus.filenames), 'filenames')


if __name__ == '__main__':
    extract()
