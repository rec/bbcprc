"""
Merges many .WAV files into one great big one and keeps track of the sample
offset for each one.
"""

import numpy as np, yaml
from . elapsed_bar import elapsed_iterator
from . import constants, wave_to_numpy
from numpy.lib.format import open_memmap

STOP_AFTER = None or 5
TOTAL_FRAMES = 76522480090
RESULTS_FILE = 'results/census.yml'
END = '(END)'


def merge(mmap, nframes, files, index_file):
    writer = open_memmap(mmap, mode='w+', dtype='int16', shape=(nframes, 2))

    def offsets():
        frames = 0

        for f in elapsed_iterator(files):
            f = str(f)
            reader = wave_to_numpy.reader(f)
            nsamples, nchannels = reader.shape
            if nchannels == 1:
                reader = np.repeat(reader, 2, axis=1)
            elif nchannels != 2:
                raise ValueError
            writer[frames:frames + nsamples] = reader
            yield f, frames
            frames += nsamples

        yield END, frames

    with open(index_file, 'w') as out:
        yaml.safe_dump_all(offsets(), out)
    return writer


def sorted_files(filename=RESULTS_FILE):
    def g():
        for i, f in enumerate(yaml.safe_load_all(open(filename))):
            yield f['nframes'], f['filename']

    return [f for (_, f) in sorted(g())][:STOP_AFTER]


if __name__ == '__main__':
    files = sorted_files()
    merge(constants.CORPUS, TOTAL_FRAMES, files, constants.CORPUS_INDEX)
