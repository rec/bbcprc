from . meta import Meta
from .. util.saver import Saver
from numpy.lib.format import open_memmap
import pathlib

# The memmap data will be backwards compatible with this version
NPY_FILE_VERSION = '1.16.3'

READ_MODES = 'r', 'r+', 'c'
WRITE_MODES = 'w', 'w+'


class Context:
    def __init__(self, path, mode, *args, **kwds):
        self.mode = mode
        path = pathlib.Path(*path)
        self.data_path = path.with_suffix('.npy')
        self.meta_path = path.with_suffix('.yml')

        self.meta = Meta()
        mutable = (mode != 'r')
        self._save_meta = Saver(self.meta, self.meta_path, mutable)
        loaded = self._save_meta.load()
        if mode in READ_MODES:
            if not loaded:
                raise ValueError('Did not load metadata in read mode')
            if args or kwds:
                raise ValueError('Read takes no arguments')
            if not self.data_path.exists():
                raise FileNotFoundError(self.data_path)
            if not self.meta_path.exists():
                raise FileNotFoundError(self.meta_path)

        elif mode in WRITE_MODES:
            self.data_path.parent.mkdir(exist_ok=True, parents=True)
            kwds.update(version=NPY_FILE_VERSION)

        else:
            raise ValueError('Unknown file mode', mode)

        self.data = open_memmap(self.data_path, mode, *args, **kwds)

    def save(self):
        self._saver.save()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.save()
