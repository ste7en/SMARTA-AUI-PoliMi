from .events.events import Event

try:
    from .smarta_fsm import Smarta
except ImportError:
    from .mock.testing import Smarta
