import contextlib, os


def with_suffix(root, suffix=None):
    for f in os.listdir(root):
        if not suffix or f.endswith(suffix):
            yield os.path.join(root, f)


@contextlib.contextmanager
def delete_on_fail(fname, mode='wb', open=open, delete=True):
    with open(fname, mode) as fp:
        try:
            yield fp
        except:
            if delete:
                try:
                    os.remove(fname)
                except:
                    pass
            raise
