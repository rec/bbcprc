from . lazy_property import lazy_property

import attr, importlib


@attr.dataclass
class Function:
    address: str = ''
    args: list = attr.Factory(list)
    kwds: dict = attr.Factory(dict)

    @lazy_property
    def function(self):
        module_path, symbol = self.address.rsplit(1)
        module = importlib.import_module(module_path)
        return getattr(module, symbol)

    def __call__(self, *args, **kwds):
        args = self.args + args
        kwds = dict(self.kwds, **kwds)
        return self.function(*args, **kwds)
