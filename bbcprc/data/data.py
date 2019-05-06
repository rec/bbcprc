"""
Access to persistent npy data and metadata.

Reading:

    from bbcprc.data import DATA

    with DATA.foo.bar.baz() as d:
       # If the file doesn't exist, you'd get an exception here.

       sample = d.data[0x8000]
       # If you change d.metadata, you get an exception after the block

Writing:

    from bbcprc.data import DATA
    with DATA.foo.bar.baz('w', shape=(0x100000, 2)) as d:
       d.metadata.column_names = 'left', 'right'
       d.metadata.index_name = 'index'
       d.data[:] = compute()
       # Metadata is written at the end of the with block
"""

from . metadata import Metadata
from .. import constants
from .. util.lazy_property import lazy_property
from .. util.saver import Saver
from numpy.lib.format import open_memmap
import pathlib


PROPERTIES_REQUIRED_FOR_WRITE = {'shape', 'dtype'}
READ_MODES = {'r', 'c', 'r+'}

# The memmap data will be backwards compatible with this version
NPY_FILE_VERSION = 2, 0


class Data:
    def __init__(self, address, mode='r', root=constants.ROOT, **kwds):
        if isinstance(address, str):
            self.address = pathlib.Path(address)
        else:
            self.address = pathlib.Path(*address)
        self.mode = mode
        self.root = root
        self.kwds = kwds

    @property
    def path(self):
        return self.root / self.address

    @lazy_property
    def data(self):
        mode = mode_equivalents.get(self.mode, self.mode)
        if mode not in valid_filemodes:
            raise ValueError('Unknown file mode', self.mode)

        data_path = self.path.with_suffix('.npy')
        kwds = self.kwds
        if mode in READ_MODES:
            if kwds:
                raise ValueError('Read takes no arguments')
            if not data_path.exists():
                raise FileNotFoundError(data_path)

        else:
            missing = PROPERTIES_REQUIRED_FOR_WRITE - set(kwds)
            if missing:
                raise ValueError(
                    'Missing required properties', *sorted(missing))

            data_path.parent.mkdir(exist_ok=True, parents=True)
            kwds = dict(kwds, version=NPY_FILE_VERSION)

        return open_memmap(str(data_path), mode, **kwds)

    @lazy_property
    def metadata(self):
        return Saver(
            self.path.with_suffix('.yml'),
            Metadata(),
            read_only=(self.mode == 'r'),
            must_write=(self.mode in writeable_filemodes))


class Address:
    def __init__(self, *address):
        self.address = address

    def __getattr__(self, name):
        return __class__(*self.address, name)

    def __call__(self, mode='r', **kwds):
        return Data(self.address, mode, **kwds)


DATA = Address()

# From numpy/core/memmap.py, which isn't visible from the top...
valid_filemodes = ["r", "c", "r+", "w+"]
writeable_filemodes = ["r+", "w+"]

mode_equivalents = {
    "readonly": "r",
    "copyonwrite": "c",
    "readwrite": "r+",
    "write": "w+"
    }
