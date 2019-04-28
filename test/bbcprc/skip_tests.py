"""
Rules to skip tests based on environment variables
"""

import os
from unittest import skipIf
from pathlib import Path
from bbcprc import constants


def _check(env):
    return os.getenv(env, '').lower().startswith('t')


no_source = skipIf(not Path(constants.SOURCE).exists(), 'Missing source')
no_corpus = skipIf(not Path(constants.CORPUS).exists(), 'Missing corpus')
travis = skipIf(_check('TRAVIS'), 'Tests that fail in Travis')
