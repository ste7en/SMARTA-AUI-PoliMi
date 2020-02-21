from smarta.state.state import State
from smarta.events.events import Event
from smarta.utility.led import *
from threading import Timer
import logging


class TimerCheckState(State):

    def __init__(self, machine, turn_duration, light_duration):
        super().__init__(machine)

        self.light_duration = light_duration   # needed inside yellow_blinking_light function
        timer_start_of_light = turn_duration - light_duration

        self.timer_one = Timer(timer_start_of_light, self.__yellow_blinking_light)
        self.timer_one.start()
        self.timer_two = Timer(turn_duration, self.__timeout_expired)
        self.timer_two.start()
        logging.debug('TimerCheckState - OK.')

    def __yellow_blinking_light(self):
        yellow = YellowLightThread(self.light_duration)
        yellow.start()

    def __timeout_expired(self):
        logging.info('TimerCheckState - Timer expired, sending timer expired event...')
        self.machine.on_event(Event.TIMER_EXP_EV)

    def exit(self) -> None:
        self.timer_one.cancel()
        self.timer_two.cancel()
        logging.debug('TimerCheckState - exiting')
