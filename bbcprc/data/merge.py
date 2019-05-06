"""
Merges many .WAV files into one great big one and keeps track of the sample
offset for each one.
"""

from . corpus import Corpus
from . import wave_to_numpy
from .. data import READ
from .. import constants
from .. util.elapsed_bar import elapsed_iterator
import numpy as np

TOTAL_FRAMES = 76522480090
END = '(END)'


def merge(mmap, nframes, files, index):
    # TODO: this should use data. resources now
    writer = wave_to_numpy.memmap(mmap, nframes, 'w+')
    frames = 0

    for i, f in enumerate(elapsed_iterator(files)):
        try:
            reader = wave_to_numpy.reader(f)
            nsamples, nchannels = reader.shape
            if nchannels == 1:
                reader = np.repeat(reader, 2, axis=1)
            elif nchannels != 2:
                raise ValueError
            writer[frames:frames + nsamples] = reader
            frames += nsamples
            if frames != index[i]:
                raise ValueError(f'bad frame count {frames}, {f}, {index[i]}')
        except Exception:
            print('In file', f)
            raise
    return writer


def find_bad(files):
    for f in elapsed_iterator(files):
        try:
            wave_to_numpy.reader(f)
        except Exception:
            print(f)


if __name__ == '__main__':
    if False:
        find_bad(Corpus.filenames)
    else:
        merge(constants.CORPUS, TOTAL_FRAMES, Corpus.filenames, READ.index())
