from . lazy_property import lazy_property
import attr
import enum
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

    def __call__(self, *args, **kwds):
        args = self.args + args
        kwds = dict(self.kwds, **kwds)
        return self.function(*args, **kwds)


@attr.dataclass
class Job:
    @enum.unique
    class State(enum.IntEnum):
        READY = 0
        RUNNING = 1
        FINISHED = 2

    function: Function = attr.Factory(Function)
    state: State = State.READY
    error: Error = attr.Factory(Error)

    def __call__(self, *args, **kwds):
        result = None
        self.state = Job.State.RUNNING

        with self.error:
            result = self.function(*args, **kwds)

        self.state = Job.State.FINISHED
        return result
