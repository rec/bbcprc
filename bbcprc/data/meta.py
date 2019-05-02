from .. util.function import Function
from .. util.git import Git
import attr, datetime


def get_timestamp():
    return datetime.datetime.now().isoformat()


@attr.dataclass
class Meta:
    function: Function = attr.Factory(Function)
    git: Git = attr.Factory(Git)
    column_names: list = attr.Factory(list)
    index_name: str = ''
    comments: str = ''
    timestamp: str = attr.Factory(get_timestamp)
