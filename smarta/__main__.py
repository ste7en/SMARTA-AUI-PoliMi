from smarta.app_states import *
from smarta.events.events import Event
import logging
import time
import threading


class Smarta(object):
    """
    The FSM that will handle the different states of the game.
    """
    def __init__(self):
        self.state = IdleState(self)
        self.state.execute()
        time.sleep(3)
        self.on_event(Event.START_EV)

    def on_event(self, event=None) -> None:
        """
        This function calls the State.on_event() func to realize
        a transition function for every captured event
        :param event: an acceptable event, as described into events.py
        """
        if event is not None:
            # TODO: Log
            print("Event: ", event)
            logging.info(event)
        # Every state is responsible for its transition table
        self.state = self.state.on_event(event)
        threading.Thread(target=self.state.execute).start()


def main():
    Smarta()


if __name__ == '__main__':
    main()
