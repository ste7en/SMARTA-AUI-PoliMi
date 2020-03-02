from smarta.state.state import State
from smarta.events.events import Event
from smarta.utility.led import *
from threading import Timer
import logging

# LED blinking times configuration:
BLINKING_TIME_RED = 0.5
BLINKING_TIME_YELLOW = 1   # blinking interval of yellow light (signalling end of turn soon)


class TimerCheckState(State):

    def __init__(self, machine, turn_duration, light_duration):
        super().__init__(machine)

        self.light_duration = light_duration   # needed inside yellow_blinking_light function
        self.timer_start_of_light = turn_duration - light_duration

        self.timer_one = Timer(self.timer_start_of_light, self.__yellow_blinking_light)
        self.timer_one.start()

        logging.debug('TimerCheckState - OK.')

    def __yellow_blinking_light(self):
        yellow = LedThread(LedColor.YELLOW, self.light_duration, BLINKING_TIME_YELLOW)
        yellow.start()
        yellow.join()
        self.__timeout_expired()

    def __timeout_expired(self):
        logging.info('TimerCheckState - Timer expired, sending timer expired event...')
        self.machine.on_event(Event.TIMER_EXP_EV)

    def exit(self) -> None:
        self.timer_one.cancel()
        logging.debug('TimerCheckState - exiting')
