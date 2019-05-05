from . lazy_property import lazy_property
import attr
import importlib
import traceback


@attr.dataclass
class Error:
    type: str = ''
    args: tuple = attr.Factory(tuple)
    tb: str = ''

    def __bool__(self):
        return bool(self.type)

    def __enter__(self):
        self.type = ''
        self.tb = ''
        self.args = ()

        return self

    def __exit__(self, type, value, tb):
        self.type = getattr(type, '__name__', '')
        self.args = getattr(value, 'args', ())
        self.tb = tb and traceback.format_tb(tb) or ''

        return True


@attr.dataclass
class Output:
    error: Error = attr.Factory(Error)
    result: object = None

    def run(self, function):
        self.result = None
        with self.error:
            self.result = function()
        return self.result


@attr.dataclass
class Function:
    address: str = ''
    args: list = attr.Factory(list)
    kwds: dict = attr.Factory(dict)

    @lazy_property
    def function(self):
        *module_path, symbol = self.address.rsplit('.', maxsplit=1)
        if module_path:
            module = importlib.import_module(module_path[0])
        else:
            module = __builtins__
        return getattr(module, symbol)

    def __call__(self):
        return self.function(*self.args, **self.kwds)
