from smarta.app_states import *

from smarta.utility.led import LedManager
from smarta.utility.vibrator import vibratorManager

from smarta.utility.led import *

import logging

from smarta.utility.vibrator import vibratorManager


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

    #led = LedManager.get_instance()
    #led.red_blinking(5)
    x = vibratorManager.get_instance()

    Smarta()



if __name__ == '__main__':
    main()
