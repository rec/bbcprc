"""
Access to persistent npy data and metadata.

Reading:

    from bbcprc.data import DATA

    with READ.foo.bar.baz() as d:
       # If the file doesn't exist, you'd get an exception here.

       sample = d.data[0x8000]
       # If you change d.meta, you get an exception after the block

Writing:

    from bbcprc.data import WRITE
    with WRITE.foo.bar.baz(shape=(0x100000, 2)) as d:
       d.meta.column_names = 'left', 'right'
       d.meta.index_name = 'index'
       d.data[:] = compute()
       # Metadata is written at the end of the with block
"""

from . import context


class Data:
    def __init__(self, *address):
        self.address = address

    def __getattr__(self, name):
        return __class__(*self.address, name)

    def __call__(self, mode='r', **kwds):
        return context.Context(self.address, mode, *kwds)


DATA = Data()
