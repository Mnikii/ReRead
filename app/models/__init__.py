try:
    from .user import User
except ModuleNotFoundError:
    User = None

from .books import Book

__all__ = []
if User is not None:
    __all__.append('User')
__all__.append('Book')
