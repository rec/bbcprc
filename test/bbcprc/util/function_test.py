from bbcprc.util.function import Function, Output
import unittest


def ok(*args, **kwds):
    return ('Success', *args), kwds


def no(*args, **kwds):
    raise ValueError('I', 'failed!')


class FunctionTest(unittest.TestCase):
    def test_success(self):
        args, kwds = ('1', 'two'), {'foo': 'bar'}
        function = Function(f'{__name__}.ok', args, kwds)
        output = Output()

        args = ('Success', *args)
        self.assertEqual(output.run(function), (args, kwds))
        self.assertFalse(output.error)

    def test_failure(self):
        args, kwds = ('1', 'two'), {'foo': 'bar'}
        function = Function(f'{__name__}.no', args, kwds)
        output = Output()

        self.assertIsNone(output.run(function))
        self.assertTrue(output.error)
        self.assertEqual(output.error.type, 'ValueError')
        self.assertEqual(output.error.args, ('I', 'failed!'))
        self.assertTrue(output.error.tb)
