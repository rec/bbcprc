from bbcprc import constants
from bbcprc.data import DATA
from pyfakefs.fake_filesystem_unittest import TestCase as FakeTestCase


class DataTest(FakeTestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.create_dir(constants.ROOT)

    def test_first(self):
        self.assertTrue(DATA)
