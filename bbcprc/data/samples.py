from . import DATA
from .. util.lazy_property import lazy_property


class Samples:
    @lazy_property
    def index(self):
        return DATA.index().data

    @lazy_property
    def corpus(self):
        return DATA.corpus().data

    def __getitem__(self, i):
        begin = self.index[i - 1] if i else 0
        end = self.index[i]
        return self.corpus[begin:end]

    def __len__(self):
        return len(self.index)


SAMPLES = Samples()
