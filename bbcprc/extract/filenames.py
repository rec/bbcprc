from .. data.corpus import Corpus
from .. data import WRITE
import pathlib


def extract():
    shape = (len(Corpus.filenames),)
    data = WRITE.filenames(dtype='int32', shape=shape)
    data[:] = [int(pathlib.Path(f).stem) for f in Corpus.filenames]

    print('Extracted', len(Corpus.filenames), 'filenames')


if __name__ == '__main__':
    extract()
