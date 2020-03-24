from smarta.events import Event
from smarta.utility.led import *
from smarta.observer import ObservableState, ObserverState
from threading import Timer
import logging

# LED blinking times configuration:
BLINKING_TIME_RED = 0.5
BLINKING_TIME_YELLOW = 1   # blinking interval of yellow light (signalling end of turn soon)


class TimerCheckState(ObservableState):

    def __init__(self, turn_duration, timeout_signalling_duration):
        super().__init__()
        self.timeout_signalling_t = timeout_signalling_duration   # needed inside yellow_blinking_light function
        self.timer_start_of_light = turn_duration - timeout_signalling_duration

        self.timer_one = Timer(self.timer_start_of_light, self.__timeout_is_expiring)
        self.timer_one.start()
        logging.debug('TimerCheckState - OK.')

    def __timeout_is_expiring(self):
        yellow = LedThread(LedColor.YELLOW, self.timeout_signalling_t, BLINKING_TIME_YELLOW)
        yellow.start()
        yellow.join()
        self.__timeout_has_expired()

    def __timeout_has_expired(self):
        logging.info('TimerCheckState - Timer expired, sending timer expired event...')
        self._notify_observer(Event.TIMER_EXP_EV)

    def detach(self, obs: ObserverState):
        super().detach(obs)
        self.timer_one.cancel()
        logging.debug('TimerCheckState - exiting')
