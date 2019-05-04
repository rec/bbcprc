"""Serialize attrs - from hardback project"""
import copy
import yaml
from . import save


class Saver:
    def __init__(self, filename, data, mutable=True):
        self.filename = filename
        self.data = data
        self.mutable = mutable
        self.loaded = False
        self.original_data = copy.deepcopy(data)

    def load(self):
        self.loaded = False
        try:
            with open(self.filename) as fp:
                save.load(yaml.safe_load(fp), self.data)
                self.loaded = True
        except Exception:
            pass

        return self.loaded

    def save(self):
        if self.data != self.original_data:
            if not self.mutable:
                raise ValueError('Cannot change mutable value')

            with open(self.filename, 'w') as fp:
                yaml.safe_dump(save.save(self.data), fp)

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, *args):
        self.save()
