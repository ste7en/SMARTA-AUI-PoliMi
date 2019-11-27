from smarta.app_states import *
import logging


class Smarta(object):
    """
    The FSM that will handle the different states of the game.
    """

    def __init__(self):
        self.state = IdleState(self)
        self.on_event(Event.START_EV)

    def on_event(self, event=None):
        """
        This function calls the State.on_event() func to realize
        a transition function for every captured event
        :param event: an acceptable event, as described into events.py
        :return: a subclass of State
        """
        if event is not None:
            logging.info(event)
        # Every state is responsible for its transition table
        self.state = self.state.on_event(event)


def main():
    Smarta()


if __name__ == '__main__':
    main()
