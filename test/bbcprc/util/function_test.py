import unittest
# from attr import dataclass, Factory
from bbcprc.util.function import Job


def success(*args, **kwds):
    return ('Success', *args), kwds


def failure(*args, **kwds):
    raise ValueError('I', 'failed!')


class FunctionTest(unittest.TestCase):
    def test_success(self):
        job = Job()
        job.function.address = f'{__name__}.success'
        job.function.args = '1', 'two'
        job.function.kwds = {'foo': 'bar'}
        expected = (('Success', '1', 'two', 'bing', 'bang'),
                    {'bong': 'bung', 'foo': 'bar'})
        self.assertEqual(job.state, job.State.READY)
        actual = job('bing', 'bang', bong='bung')
        self.assertEqual(actual, expected)
        self.assertEqual(job.state, job.State.FINISHED)
        self.assertFalse(job.error)

    def test_failure(self):
        job = Job()
        job.function.address = f'{__name__}.failure'
        job.function.args = '1', 'two'
        job.function.kwds = {'foo': 'bar'}
        expected = None
        actual = job('bing', 'bang', bong='bung')
        self.assertEqual(actual, expected)
        self.assertTrue(job.error)
        self.assertEqual(job.error.type, 'ValueError')
        self.assertEqual(job.error.args, ('I', 'failed!'))
        self.assertTrue(job.error.tb)
