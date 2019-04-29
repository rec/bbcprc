import yaml
from . import constants
from . lazy_property import lazy_property
from numpy.lib.format import open_memmap


class _Data:
    @lazy_property
    def corpus(self):
        return open_memmap(constants.CORPUS, mode='r')

    @lazy_property
    def index(self):
        return open_memmap(constants.INDEX, mode='r')

    @lazy_property
    def filenames(self):
        with open(constants.FILENAMES) as fp:
            return yaml.safe_load(fp)

    @lazy_property
    def samples(self):
        data = self

        class Samples:
            def __getitem__(self, i):
                begin = data.index[i - 1] if i else 0
                end = data.index[i]
                return data.corpus[begin:end]

            def __len__(self):
                return

            def __iter__(self):
                return (self[i] for i in range(len(data.index)))

        return Samples()


Data = _Data()
