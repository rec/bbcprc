import os


def with_suffix(root, suffix=None):
    for f in os.listdir(root):
        if not suffix or f.endswith(suffix):
            yield os.path.join(root, f)
