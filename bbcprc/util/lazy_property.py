import functools


def lazy_property(fn):
    """Decorator that makes a property lazy-evaluated."""
    # https://gist.github.com/sloria/5895501#file-lazy_init_with_decorator-py
    attr_name = '_lazy_' + fn.__name__

    @property
    @functools.wraps(fn)
    def wrapped(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return wrapped
