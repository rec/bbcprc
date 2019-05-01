"""Serialize attrs - from hardback project"""
import attr, yaml


def unserialize(data, dataclass):
    """Unserialize from JSON-like data (dicts, strings, etc) to a dataclass"""
    try:
        fields = attr.fields_dict(dataclass.__class__)
    except:
        try:
            return type(dataclass)(data)
        except:
            return data

    unknown = set(data) - set(fields)
    if unknown:
        raise ValueError('Do not understand fields:', *unknown)

    for k, v in data.items():
        subitem = getattr(dataclass, k)
        setattr(dataclass, k, unserialize(v, subitem))

    return dataclass


def serialize(dataclass):
    """Serialize from a dataclass to JSON-like data"""
    return attr.asdict(dataclass)


def save(filename, dataclass):
    ser = serialize(dataclass)

    with open(filename, 'w') as fp:
        yaml.safe_dump(ser, fp)


class Save:
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

    def load(self):
        try:
            with open(self.filename) as fp:
                unserialize(yaml.safe_load(fp), self.data)
                return True
        except:
            return False

    def save(self):
        with open(self.filename, 'w') as fp:
            yaml.safe_dump(serialize(self.data), fp)
