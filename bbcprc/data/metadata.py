from .. util.function import Function
from .. util.git import Git
import attr
import datetime


def get_timestamp():
    return datetime.datetime.now().isoformat()


@attr.dataclass
class Metadata:
    function: Function = attr.Factory(Function)
    git: Git = attr.Factory(Git)
    column_names: list = attr.Factory(list)
    row_names: list = attr.Factory(list)
    index_name: str = ''
    comments: str = ''
    timestamp: str = attr.Factory(get_timestamp)
