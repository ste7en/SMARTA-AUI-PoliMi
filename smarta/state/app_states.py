from smarta.state import State
from smarta.events import Event
from smarta.events.launch import LaunchCheckState
from smarta.events.timer import TimerCheckState
from smarta.events.microphone import MicrophoneCheckState
from smarta.utility import VibratorManager
from smarta.utility.led import *
from smarta.data import DataManager
from smarta.observer import ObserverState
import logging
import time


class IdleState(State):
    """
    The state which indicates the machine is ready and waiting
    for an input to start and pass to the next (working) state
    """
    def on_event(self, event):
        if event == Event.START_EV:
            logging.debug('Idle State - received Start event')

            return RunState(self.machine)
        return self

    def execute(self):
        logging.debug('Idle State - Turning off LEDs')
        LedManager.get_instance().color_wipe(LedColor.OFF)  # Turn off LEDs, if they are on


class ResetState(State, ObserverState):
    """
    Reset state, which restart the machine for a new run and waits
    when the turn has expired and the ball hasn't been launched yet.
    """
    __GREEN_LIGHT_TIME = 2  # Duration of time that time green light will be shown, at the start of a new turn
    __WAIT_BEFORE_SIGNALLING = 2  # Time to wait before signalling the player with red LED and vibration

    __yellow: Thread
    __launch_check_state: LaunchCheckState
    __timer: Timer
    __start_time: float

    def notify(self, event: Event) -> None:
        self.machine.on_event(event)

    def __signal(self):
        self.__yellow.start()  # start yellow steady light
        VibratorManager.get_instance().vibrate()

    def on_event(self, event):
        if event is Event.LAUNCH_DET_EV or Event.START_EV:
            return RunState(self.machine)
        return None

    def exit(self) -> None:
        if self.__timer.is_alive(): self.__timer.cancel()
        self.__launch_check_state.detach(self)
        self.__yellow.running = False   # stop yellow steady light
        VibratorManager.get_instance().stop()
        elapsed = time.time() - self.__start_time
        DataManager.get_instance().add_turn(elapsed, new_turn=False)

    def execute(self) -> None:
        super().execute()
        self.__yellow = LedThread(LedColor.YELLOW, 30)  # defining yellow light (without starting it yet)

        self.__launch_check_state = LaunchCheckState()
        self.__launch_check_state.attach(self)

        self.__timer = Timer(ResetState.__WAIT_BEFORE_SIGNALLING, self.__signal)
        self.__timer.start()

        self.__start_time = time.time()


class RunState(State, ObserverState):
    """
    The main state, which represents the main features
    of the application and its operations
    """

    __TURN_DURATION_TIME = 15  # Duration of a turn
    __YELLOW_LIGHT_TIME = 5  # Duration of time that yellow blinking light will last, before the end of the turn

    __launch_check_state = None
    __timer_check_state = None
    __mic_check_state = None
    __start_time = 0

    @classmethod
    def set_turn_duration_time(cls, duration_in_sec):
        logging.debug('Duration time set to ' + str(duration_in_sec) + ' seconds')
        cls.__TURN_DURATION_TIME = duration_in_sec

    @classmethod
    def get_turn_duration_time(cls):
        return cls.__TURN_DURATION_TIME

    def exit(self):
        logging.debug('RunState - exiting')
        # Detaching observers
        self.__timer_check_state.detach(self)
        self.__launch_check_state.detach(self)
        self.__mic_check_state.detach(self)
        # The end of a RunState corresponds to the end of a turn,
        # updating the average turn duration and number of turns
        elapsed = time.time() - self.__start_time
        DataManager.get_instance().add_turn(elapsed)

    def on_event(self, event) -> State:
        if event is Event.VOICE_OVERLAP_DET_EV: self._on_overlap()
        else:
            return RunState(self.machine) if event is Event.LAUNCH_DET_EV \
                else ResetState(self.machine) if event is Event.TIMER_EXP_EV \
                else None
        return None

    def execute(self):
        logging.info('-------- Turn n. %s --------', DataManager.get_instance().get_number_of_turns())
        green = LedThread(LedColor.GREEN, 2, 0.5)  # green light lasting 2s, blinking every 0.5s, to signal new turn
        green.start()

        # Threads to check gyro/mic/timer
        logging.debug('Run State - creating timer, launch detector and overlap detector instance')
        # Timer observer
        self.__timer_check_state = TimerCheckState(self.__TURN_DURATION_TIME, self.__YELLOW_LIGHT_TIME)
        self.__timer_check_state.attach(self)
        # Launch observer
        self.__launch_check_state = LaunchCheckState()
        self.__launch_check_state.attach(self)
        # Voice overlap observer
        self.__mic_check_state = MicrophoneCheckState()
        self.__mic_check_state.attach(self)

        self.__start_time = time.time()
        VibratorManager.get_instance().vibrate(0.5)

    @staticmethod
    def _on_overlap():
        DataManager.get_instance().add_overlap();
        red = LedThread(LedColor.RED, 1)   # on overlap: red steady light for 1 second
        red.start()
        VibratorManager.get_instance().vibrate(1, intermittent=False)

    def notify(self, event: Event) -> None:
        self.machine.on_event(event)
