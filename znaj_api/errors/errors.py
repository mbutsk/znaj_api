class DefaultException(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidCredentials(DefaultException): pass
class UnknownException  (DefaultException): pass
class SessionClosed     (DefaultException): pass
class AccessDenied      (DefaultException): pass