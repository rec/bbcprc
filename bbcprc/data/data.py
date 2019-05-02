"""

Access to persistent npy data and metadata.

Reading:

    from bbcprc.data import DATA
    with DATA.foo.bar.baz() as data, meta:
       sample = d.data[0x8000]


Writing:
    with DATA.foo.bar.baz('w', shape=(0x100000, 2)) as data:
       data.meta.column_names = 'left', 'right'
       data.meta.index_name = 'index'
       # Write the data

"""

from . meta import Meta
from .. import constants
from .. util.save import Saver
import copy
import pathlib
from numpy.lib.format import open_memmap

# The memmap data will be backwards compatible to this version
NPY_FILE_VERSION = '1.16.3'


class Attr:
    def __init__(self, *address, root=constants.ROOT):
        self.address = address
        self.root = root

    def __getattr__(self, name):
        return Attr(*self.address, name, root=self.root)

    def __call__(self, mode, **kwds):
        return _DataContext(self.address, self.root, **kwds)


DATA = Attr()


class _DataContext:
    def __init__(self, address, root, mode, **kwds):
        if 'r' in mode and kwds:
            raise ValueError('No keywords in read mode')
        self.address = address
        self.root = root
        self.mode = mode
        self.kwds = kwds
        self.meta = Meta()
        self.save_meta = Saver(self.meta, self.meta_file)

        if not self.save_meta.load() and 'r' in self.mode:
            raise FileNotFoundError('Could not read meta file')

        self.data = open_memmap(self.data_file, self.mode,
                                version=NPY_FILE_VERSION, **self.kwds)
        self._original_meta = copy.deepcopy(self.meta)

    @property
    def data_file(self):
        return pathlib.Path(*self.address, self.root).with_suffix('.npy')

    @property
    def meta_file(self):
        return self.data_file.with_suffix('.yml')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.meta != self._original_meta:
            if self.mode == 'r':
                raise ValueError('Metadata changed in read mode')
            if self.mode != 'c':
                self.save_meta.save()
