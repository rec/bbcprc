from bbcprc.data import ADDRESS

if False:
    from bbcprc import constants
    from pyfakefs.fake_filesystem_unittest import TestCase as FakeTestCase

    class AddressTest(FakeTestCase):
        def setUp(self):
            self.setUpPyfakefs()
            self.fs.create_dir(constants.ROOT)

        def test_first(self):
            self.assertTrue(ADDRESS)
