from smarta.state import State
from smarta.events import Event
from smarta.utility.led import *
from smarta.utility import VibratorManager
from threading import Timer
import logging

# LED blinking times configuration:
BLINKING_TIME_RED = 0.5
BLINKING_TIME_YELLOW = 1   # blinking interval of yellow light (signalling end of turn soon)


class TimerCheckState(State):

    def __init__(self, machine, turn_duration, timeout_signalling_duration):
        super().__init__(machine)

        self.timeout_signalling_t = timeout_signalling_duration   # needed inside yellow_blinking_light function
        self.timer_start_of_light = turn_duration - timeout_signalling_duration

        self.timer_one = Timer(self.timer_start_of_light, self.__timeout_is_expiring)
        self.timer_one.start()

        logging.debug('TimerCheckState - OK.')

    def __timeout_is_expiring(self):
        yellow = LedThread(LedColor.YELLOW, self.timeout_signalling_t, BLINKING_TIME_YELLOW)
        yellow.start()
        VibratorManager.get_instance().vibrate(self.timeout_signalling_t, intermittent=True)
        yellow.join()
        self.__timeout_has_expired()

    def __timeout_has_expired(self):
        logging.info('TimerCheckState - Timer expired, sending timer expired event...')
        self.machine.on_event(Event.TIMER_EXP_EV)

    def exit(self) -> None:
        self.timer_one.cancel()
        logging.debug('TimerCheckState - exiting')
