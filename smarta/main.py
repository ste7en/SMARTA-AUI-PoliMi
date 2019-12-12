from smarta.utility.launch_detector import LaunchDetector
from smarta.utility.led import LedManager
from smarta.utility.vibrator import VibratorManager
from smarta.utility.led import *
from smarta.app_states import *

import logging
import time



class Smarta(object):
    """
    The FSM that will handle the different states of the game.
    """
    def __init__(self):
        self.state = IdleState(self)
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


def main():

    # led = LedManager().get_instance()
    # red = led.RedLightThread(led)
    # red.start()
    # time.sleep(5)
    # red.running = False

    # time.sleep(1)
    # yellow = led.YellowLightThread(led, 10)
    # yellow.start()
    # time.sleep(10)
    # time.sleep(1)

    # green = led.GreenLightThread(led, 5)
    # green.start()

    Smarta()


if __name__ == '__main__':

    main()
