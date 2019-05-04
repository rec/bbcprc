"""Serialize attrs"""
import attr


def load(source, data):
    """Unserialize from JSON-like data (dicts, strings, etc) to a dataclass"""
    try:
        fields = attr.fields_dict(data.__class__)
    except Exception:
        try:
            return type(data)(source)
        except Exception:
            return source

    unknown = set(source) - set(fields)
    if unknown:
        raise ValueError('Do not understand fields:', *unknown)

    for k, v in source.items():
        subitem = getattr(data, k)
        setattr(data, k, load(v, subitem))

    return data


def save(data):
    """Serialize from a data class to JSON-like data"""
    return attr.asdict(data)
