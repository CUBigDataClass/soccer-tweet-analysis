import unittest
import os
import sys
from partyparrots import settings

partyparrots_suite = unittest.TestSuite()

for app in settings.INSTALLED_APPS:
    mod = __import__(app, fromlist=[''])

    app_dir = os.path.dirname(os.path.abspath(mod.__file__))
    test_dir = os.path.join(app_dir, 'tests')
    try:
        app_suite = unittest.TestLoader().discover(test_dir)
        partyparrots_suite.addTests(app_suite)
    except ImportError:
        print 'No tests found for {}'.format(app)


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    ret = not runner.run(partyparrots_suite).wasSuccessful()
    sys.exit(ret)
