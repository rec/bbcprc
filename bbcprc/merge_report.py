import yaml
from . import constants, wave_to_numpy


def read():
    with open(constants.CORPUS_INDEX) as fp:
        return [i[1] for i in yaml.safe_load_all(fp)]


def write(data):
    with open(constants.SIMPLE_INDEX, 'w') as fp:
        yaml.dump(data, fp)


def write_numpy(data):
    mmap = wave_to_numpy.memmap(constants.INDEX, mode='w+', dtype='uint64',
                                shape=(len(data),))
    mmap[:] = data


if __name__ == '__main__':
    write_numpy(read())
