from .. import constants
from .. util.lazy_property import lazy_property
import yaml


class _Corpus:
    @lazy_property
    def filenames(self):
        # Perhaps this becomes metadata?
        with open(constants.FILENAMES) as fp:
            return yaml.safe_load(fp)


Corpus = _Corpus()
