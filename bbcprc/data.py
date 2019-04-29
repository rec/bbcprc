import yaml
from pathlib import Path
from . import constants
from . lazy_property import lazy_property
from numpy.lib.format import open_memmap

FILENAMES_FILE = Path(__file__).parents[1] / 'results/filenames.yml'


class _Data:
    @lazy_property
    def corpus(self):
        return open_memmap(constants.CORPUS, mode='r')

    @lazy_property
    def index(self):
        return open_memmap(constants.INDEX, mode='r')

    @lazy_property
    def names(self):
        with FILENAMES_FILE.open() as fp:
            return yaml.safe_load(fp)

    def samples_at(self, i):
        begin = self.index[i - 1] if i else 0
        end = self.index[i]
        return self.corpus[begin:end]


Data = _Data()
