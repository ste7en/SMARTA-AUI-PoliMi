from smarta.state.state import State
from smarta.events.events import Event
from smarta.events.timer import TimerCheckState
from smarta.events.launch import LaunchCheckState
from smarta.utility.led import *
import logging


class IdleState(State):
    """
    The state which indicates the machine is ready and waiting
    for an input to start and pass to the next (working) state
    """
    def on_event(self, event):
        if event == Event.START_EV:
            # TODO: - Manage blinking with a specific function of LedManager
            logging.debug('Idle State - Green blinking')
            for i in range(0, 3):
                logging.debug('blink ' + str(i))
                t = GreenLightThread(1)
                t.start()
                t.join()
                time.sleep(0.5)
            return RunState(self.machine)
        return self

    def execute(self):
        logging.debug('Idle State - Turning off LEDs')
        LedManager.get_instance().turn_off()  # Turn off LEDs, if they are on


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
        # LED green light blinks
        green = GreenLightThread(self.__GREEN_LIGHT_TIME)
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
    __YELLOW_LIGHT_TIME = 5  # Duration of time that yellow light will blink, before the end of the turn

    __launch_check_state = None
    __timer_check_state = None

    def exit(self):
        logging.debug('RunState - exiting')
        self.__timer_check_state.exit()
        self.__launch_check_state.exit()

    def on_event(self, event) -> State:
        return ResetState(self.machine) if event is Event.TIMER_EXP_EV or Event.LAUNCH_DET_EV else None

    def execute(self):
        # Threads to check gyro/mic/timer
        logging.debug('Run State - creating timer and launch detector instance')
        self.__timer_check_state = TimerCheckState(self.machine, self.__TURN_DURATION_TIME, self.__YELLOW_LIGHT_TIME)
        self.__launch_check_state = LaunchCheckState(self.machine)


class MicCheckState(State):
    pass
