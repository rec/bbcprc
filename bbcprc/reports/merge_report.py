import itertools, yaml
from .. import constants
from .. data import wave_to_numpy


def read():
    with open(constants.CENSUS_RESULTS_FILE) as fp:
        items = [i['nframes'] for i in yaml.safe_load_all(fp)]
        return list(itertools.accumulate(sorted(items)))


def write_numpy(data):
    mmap = wave_to_numpy.memmap(constants.INDEX, mode='w+', dtype='uint64',
                                shape=(len(data),))
    mmap[:] = data


if __name__ == '__main__':
    write_numpy(read())
