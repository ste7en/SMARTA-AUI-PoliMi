from smarta.observer import ObserverState
from smarta.events import Event
from typing import List
from abc import ABC


class ObservableState(ABC):

    _observers: List[ObserverState]

    def __init__(self):
        super().__init__()
        self._observers = []

    def attach(self, obs: ObserverState):
        self._observers.append(obs)

    def detach(self, obs: ObserverState):
        if self._observers.__contains__(obs):
            self._observers.remove(obs)

    def _notify_observer(self, event: Event) -> None:
        for observer in self._observers:
            observer.notify(event)
