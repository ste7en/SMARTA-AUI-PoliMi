from smarta.state.state import State
from smarta.events.events import Event
from smarta.events.timer import TimerCheckState
from smarta.events.launch import LaunchCheckState
from smarta.utility.led import *


class IdleState(State):
    """
    The state which indicates the machine is ready and waiting
    for an input to start and pass to the next (working) state
    """
    def on_event(self, event):
        if event == Event.START_EV:
            return RunState(self.machine)
        return self


class ResetState(State):
    """
    Reset state, which restart the machine for a new run
    """
    __GREEN_LIGHT_TIME = 3  # Duration of time that time green light will be shown, at the start of a new turn

    def on_event(self, event=None):
        return RunState(self.machine)

    def execute(self):
        # Test

        # LED green light blinks
        green = GreenLightThread(self.__GREEN_LIGHT_TIME)
        green.start()
        time.sleep(0.5)
        self.machine.on_event(Event.RESET_EV)


class RunState(State):
    """
    The main state, which represents the main features
    of the application and its operations
    """

    __TURN_DURATION_TIME = 15  # Duration of a turn
    __YELLOW_LIGHT_TIME = 5  # Duration of time that yellow light will blink, before the end of the turn

    __launch_check_state = None
    __timer_check_state = None

    def __del__(self):
        print("Delete RunState")
        self.__timer_check_state.__del__()
        self.__launch_check_state.__del__()

    def on_event(self, event) -> State:
        return ResetState(self.machine) if event is Event.TIMER_EXP_EV or Event.LAUNCH_DET_EV else None

    def execute(self):
        # Threads to check gyro/mic/timer
        print("Executing RunState")
        self.__timer_check_state = TimerCheckState(self.machine, self.__TURN_DURATION_TIME, self.__YELLOW_LIGHT_TIME)
        self.__launch_check_state = LaunchCheckState(self.machine)


class MicCheckState(State):
    pass
