import tempfile, unittest
from bbcprc.data import data


class DataTest(unittest.TestCase):
    def test_first(self):
        with tempfile.TemporaryDirectory() as td:
            data.Attr(root=td)
