from .. data import DATA
from .. import constants
from .. util.lazy_property import lazy_property
from numpy.lib.format import open_memmap
import yaml


class Samples:
    def __getitem__(self, i):
        begin = DATA.index.data[i - 1] if i else 0
        end = DATA.index.data[i]
        return DATA.corpus.data[begin:end]

    def __len__(self):
        return len(DATA.index)


SAMPLES = Samples()


class _Corpus:
    @lazy_property
    def corpus(self):
        # DEPRECATED: use DATA.corpus instead
        return open_memmap(constants.CORPUS, mode='r')

    @lazy_property
    def index(self):
        # DEPRECATED: use DATA.index instead
        return open_memmap(constants.INDEX, mode='r')

    @lazy_property
    def filenames(self):
        # Perhaps this becomes index.yml?
        with open(constants.FILENAMES) as fp:
            return yaml.safe_load(fp)


# DEPRECATED: use DATA.corpus instead
Corpus = _Corpus()
