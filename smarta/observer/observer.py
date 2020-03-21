from abc import ABC, abstractmethod
from smarta.events import Event


class ObserverState(ABC):

    @abstractmethod
    def notify(self, event: Event) -> None:
        pass
