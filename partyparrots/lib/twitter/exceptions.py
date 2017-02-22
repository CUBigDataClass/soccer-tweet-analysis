class TwitterException(Exception):
    """
    Exception class for Twitter API
    """
    def __init__(self, key):
        message = '%s not in environment' % (key)
        super(Exception, self).__init__(message)

class TwitterDataException(Exception):
    """
    Exception class for Twitter Data
    """
    def __init__(self, message):
        super(Exception, self).__init__(message)
