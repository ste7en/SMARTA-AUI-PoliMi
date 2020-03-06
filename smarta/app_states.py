from smarta.state.state import State
from smarta.events.events import Event
from smarta.events.timer import TimerCheckState
from smarta.events.launch import LaunchCheckState
from smarta.data.data_manager import DataManager
from smarta.utility.led import *
import logging
import time


class IdleState(State):
    """
    The state which indicates the machine is ready and waiting
    for an input to start and pass to the next (working) state
    """
    def on_event(self, event):
        if event == Event.START_EV:
            logging.debug('Idle State - Green blinking')
            green_light_duration_s = 6   # start of a turn
            green_light_blinking_time_s = 1   # blinking time of green light at the start of a turn
            green = LedThread(LedColor.GREEN, green_light_duration_s, green_light_blinking_time_s)
            green.start()
            green.join()

            return RunState(self.machine)
        return self

    def execute(self):
        logging.debug('Idle State - Turning off LEDs')
        LedManager.get_instance().color_wipe(LedColor.OFF)  # Turn off LEDs, if they are on


class ResetState(State):
    """
    Reset state, which restart the machine for a new run
    """
    __GREEN_LIGHT_TIME = 3  # Duration of time that time green light will be shown, at the start of a new turn

    def on_event(self, event=None):
        return RunState(self.machine)

    def execute(self):
        logging.debug('-------------------')
        logging.debug('Reset State - Green')
        # LED green light
        green = LedThread(LedColor.GREEN, self.__GREEN_LIGHT_TIME)
        green.start()
        green.join()
        logging.debug('Reset State - Green off')
        logging.info('Starting...')
        self.machine.on_event(Event.START_EV)


class RunState(State):
    """
    The main state, which represents the main features
    of the application and its operations
    """

    __TURN_DURATION_TIME = 15  # Duration of a turn
    __YELLOW_LIGHT_TIME = 5  # Duration of time that yellow blinking light will last, before the end of the turn

    __launch_check_state = None
    __timer_check_state = None

    def __init__(self, machine):
        super().__init__(machine)
        self.__start_time = 0

    @classmethod
    def set_turn_duration_time(cls, duration_in_sec):
        logging.debug('Duration time set to ' + str(duration_in_sec) + ' seconds')
        cls.__TURN_DURATION_TIME = duration_in_sec

    @classmethod
    def get_turn_duration_time(cls):
        return cls.__TURN_DURATION_TIME

    def exit(self):
        logging.debug('RunState - exiting')
        self.__timer_check_state.exit()
        self.__launch_check_state.exit()
        # The end of a RunState corresponds to the end of a turn,
        # updating the average turn duration and number of turns
        elapsed = self.__start_time - time.time()
        DataManager.get_instance().add_turn(elapsed)

    def on_event(self, event) -> State:
        return ResetState(self.machine) if event is Event.TIMER_EXP_EV or Event.LAUNCH_DET_EV else None

    def execute(self):
        # Threads to check gyro/mic/timer
        logging.debug('Run State - creating timer and launch detector instance')
        self.__timer_check_state = TimerCheckState(self.machine, self.__TURN_DURATION_TIME, self.__YELLOW_LIGHT_TIME)
        self.__launch_check_state = LaunchCheckState(self.machine)
        self.__start_time = time.time()


class MicCheckState(State):
    pass
