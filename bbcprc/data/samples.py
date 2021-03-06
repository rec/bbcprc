from . import READ
from ..util.lazy_property import lazy_property


class Samples:
    @lazy_property
    def index(self):
        return READ.index()

    @lazy_property
    def corpus(self):
        return READ.corpus()

    def __getitem__(self, i):
        begin = self.index[i - 1] if i else 0
        end = self.index[i]
        return self.corpus[begin:end]

    def __len__(self):
        return len(self.index)


SAMPLES = Samples()
