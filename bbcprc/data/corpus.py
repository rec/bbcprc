import yaml
from .. import constants
from .. util.lazy_property import lazy_property
from numpy.lib.format import open_memmap


class _Corpus:
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
        corpus = self

        class Samples:
            def __getitem__(self, i):
                begin = corpus.index[i - 1] if i else 0
                end = corpus.index[i]
                return corpus.corpus[begin:end]

            def __len__(self):
                return

            def __iter__(self):
                return (self[i] for i in range(len(corpus.index)))

        return Samples()


Corpus = _Corpus()
