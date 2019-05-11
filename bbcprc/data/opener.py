"""
Access to persistent npy data and metadata.

Reading:

    from bbcprc.data import READ

    d = READ.foo.bar.baz()
       # If the file doesn't exist, you'd get an exception here.

       sample = d[0x8000]
       # If you change d.metadata, you get an exception after the block

Writing:

    from bbcprc.data import READ
    d =  WRITE.foo.bar.baz('w', shape=(0x100000, 2))
"""

from .metadata import Metadata
from .. import constants
from ..util.saver import Saver
from numpy.lib.format import open_memmap
from pathlib import Path

PROPERTIES_REQUIRED_FOR_WRITE = {'shape', 'dtype'}

# The memmap data will be backwards compatible with this version
NPY_FILE_VERSION = 2, 0


def _make_path(root, addr, suffix):
    path = Path(addr) if isinstance(addr, str) else Path(*addr)
    return root / path.with_suffix(suffix)


def metadata(mode, address, root=constants.ROOT):
    mode = mode_equivalents.get(mode, mode)
    path = _make_path(root, address, '.yml')
    if 'w' not in 'mode' and not path.exists():
        raise FileNotFoundError(path)

    return Saver(
        path, Metadata(), read_only=(mode == 'r'), must_write=('+' in mode)
    )


def data(mode, address, root=constants.ROOT, **kwds):
    mode = mode_equivalents.get(mode, mode)
    if mode not in valid_filemodes:
        raise ValueError('Unknown file mode', mode)

    data_path = _make_path(root, address, '.npy')
    if 'w' not in mode:
        if kwds:
            raise ValueError(f'Read takes no arguments {kwds}')
        if not data_path.exists():
            raise FileNotFoundError(data_path)

    else:
        missing = PROPERTIES_REQUIRED_FOR_WRITE - set(kwds)
        if missing:
            raise ValueError('Missing required properties', *sorted(missing))

        data_path.parent.mkdir(exist_ok=True, parents=True)
        kwds = dict(kwds, version=NPY_FILE_VERSION)

    return open_memmap(str(data_path), mode, **kwds)


# From numpy/core/memmap.py, which isn't visible from the top...
valid_filemodes = ['r', 'c', 'r+', 'w+']
writeable_filemodes = ['r+', 'w+']

mode_equivalents = {
    'read': 'r',
    'readonly': 'r',
    'copyonwrite': 'c',
    'readwrite': 'r+',
    'write': 'w+',
}
