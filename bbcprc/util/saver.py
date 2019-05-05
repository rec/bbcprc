"""Serialize attrs - from hardback project"""
import copy
import yaml
from . import save


class Saver:
    def __init__(self, filename, data, read_only=False, must_write=True):
        self.filename = filename
        self.data = data
        self.read_only = read_only
        self.must_write = must_write
        self.loaded = False
        self.original_data = copy.deepcopy(data)

    def __enter__(self):
        self.loaded = False
        try:
            with open(self.filename) as fp:
                save.load(yaml.safe_load(fp), self.data)
                self.loaded = True
        except Exception:
            pass

        return self.data

    def __exit__(self, *args):
        if self.data == self.original_data:
            return

        elif self.read_only:
            raise ValueError('Cannot change read_only value')

        elif self.must_write:
            with open(self.filename, 'w') as fp:
                yaml.safe_dump(save.save(self.data), fp)
