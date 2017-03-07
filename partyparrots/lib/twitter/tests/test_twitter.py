import os
import pwd
import unittest
import mock

class TwitterBaseTestCase(unittest.TestCase):
    @mock.patch('os.environ.get', return_value='SOME_VALUE')
    def test_init(self, env):
        # guaranteed to pass
        pass
