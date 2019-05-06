import functools
from . opener import data
from . opener import metadata


class _Address:
    def __init__(self, call, *address):
        self.call = call
        self.address = address

    def __getattr__(self, name):
        return __class__(self.call, *self.address, name)

    def __call__(self, **kwds):
        return self.call(self.address, **kwds)


read = functools.partial(data, 'read')
readonly = functools.partial(data, 'readonly')
copyonwrite = functools.partial(data, 'copyonwrite')
readwrite = functools.partial(data, 'readwrite')
write = functools.partial(data, 'write')
metadata_read = functools.partial(metadata, 'read')
metadata_write = functools.partial(metadata, 'write')

READ = _Address(read)
READONLY = _Address(readonly)
COPYONWRITE = _Address(copyonwrite)
READWRITE = _Address(readwrite)
WRITE = _Address(write)
METADATA_READ = _Address(metadata_read)
METADATA_WRITE = _Address(metadata_write)
