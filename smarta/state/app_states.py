from smarta.state import State
from smarta.events import *
from smarta.utility import VibratorManager
from smarta.utility.led import *
from smarta.data import DataManager
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
    Reset state, which restart the machine for a new run but waits
    if the turn has expired and the ball hasn't been launched yet.
    """
    __GREEN_LIGHT_TIME = 2  # Duration of time that time green light will be shown, at the start of a new turn
    __WAIT_BEFORE_SIGNALLING = 2  # Time to wait before signalling the player with red LED and vibration
    __VIBRATION_DURATION = 1

    def __init__(self, machine, wait_for_launch=True):
        super().__init__(machine)
        self.__timer: Timer
        if wait_for_launch:
            self.__launch_check_state = LaunchCheckState(self.machine)
            self.__timer = self.__create_timer()
            self.__timer.start()
            self.__start_time = time.time()
            self.__exit_from_loop = False
        else:
            self.__start_new_turn()

    def __create_timer(self) -> Timer:
        return Timer(ResetState.__WAIT_BEFORE_SIGNALLING, self.__signal)

    def __signal(self):
        # TODO: - RED LED
        VibratorManager.get_instance().vibrate(ResetState.__VIBRATION_DURATION)
        if not self.__exit_from_loop:
            self.__timer = self.__create_timer()
            self.__timer.start()

    def on_event(self, event):
        if event is Event.LAUNCH_DET_EV:
            elapsed = time.time() - self.__start_time
            DataManager.get_instance().add_turn(elapsed, new_turn=False)
            self.__start_new_turn()
            return RunState(self.machine)
        return None

    def __start_new_turn(self):
        logging.debug('-------------------')
        logging.debug('Reset State - Green')
        # LED green light
        green = LedThread(LedColor.GREEN, self.__GREEN_LIGHT_TIME)
        green.start()
        green.join()
        logging.debug('Reset State - Green off')
        logging.info('Starting...')
        self.machine.on_event(Event.START_EV)

    def exit(self) -> None:
        self.__launch_check_state.exit()
        if self.__timer is Timer: self.__timer.cancel()
        self.__exit_from_loop = True


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
        elapsed = time.time() - self.__start_time
        DataManager.get_instance().add_turn(elapsed)

    def on_event(self, event) -> State:
        return ResetState(self.machine) if event is Event.TIMER_EXP_EV \
            else ResetState(self.machine, wait_for_launch=False) if event is Event.LAUNCH_DET_EV \
            else None  # TODO: - Insert here the voice overlap event

    def execute(self):
        # Threads to check gyro/mic/timer
        logging.debug('Run State - creating timer and launch detector instance')
        self.__timer_check_state = TimerCheckState(self.machine, self.__TURN_DURATION_TIME, self.__YELLOW_LIGHT_TIME)
        self.__launch_check_state = LaunchCheckState(self.machine)
        self.__start_time = time.time()
        VibratorManager.get_instance().vibrate(0.5)
