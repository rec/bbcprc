from . metadata import Metadata
from .. import constants
from .. util.save import Saver
import copy, pathlib
from numpy.lib.format import open_memmap

# The memmap data will be backwards compatible to this version
NPY_FILE_VERSION = '1.16.3'


class Attr:
    def __init__(self, *address, root=constants.MEMMAP):
        self.address = address
        self.root = root

    def __getattr__(self, name):
        return Attr(*self.address, name, root=self.root)

    def __call__(self, mode, **kwds):
        return _DataContext(self.address, self.root, **kwds)


Data = Attr()


class _DataContext:
    def __init__(self, address, root, mode, **kwds):
        if 'r' in mode and kwds:
            raise ValueError('No keywords in read mode')
        self.address = address
        self.root = root
        self.mode = mode
        self.kwds = kwds

    @property
    def data_file(self):
        return pathlib.Path(*self.address, self.root).with_suffix('.npy')

    @property
    def metadata_file(self):
        return self.data_file.with_suffix('.yml')

    def __enter__(self):
        self.metadata = Metadata()
        self.save_metadata = Saver(self.metadata, self.metadata_file)

        if not self.save_metadata.load() and 'r' in self.mode:
            raise FileNotFoundError('Could not read metadata file')

        self.data = open_memmap(self.data_file, self.mode,
                                version=NPY_FILE_VERSION, **self.kwds)
        self._original_metadata = copy.deepcopy(self.metadata)
        return self

    def __exit__(self, *args):
        if self.metadata != self._original_metadata:
            if self.mode == 'r':
                raise ValueError('Metadata changed in read mode')
            if self.mode != 'c':
                self.save_metadata.save()
