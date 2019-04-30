"""
Merges many .WAV files into one great big one and keeps track of the sample
offset for each one.
"""

import numpy as np
from . elapsed_bar import elapsed_iterator
from . import constants, wave_to_numpy
from . data import Data

TOTAL_FRAMES = 76522480090
END = '(END)'


def merge(mmap, nframes, files, index):
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
        except:
            print('In file', f)
            raise
    return writer


def find_bad(files):
    for f in elapsed_iterator(files):
        try:
            wave_to_numpy.reader(f)
        except:
            print(f)


if __name__ == '__main__':
    if False:
        find_bad(Data.filenames)
    else:
        merge(constants.CORPUS, TOTAL_FRAMES, Data.filenames, Data.index)
