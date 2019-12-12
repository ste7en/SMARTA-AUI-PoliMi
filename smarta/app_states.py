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

    def __init__(self, machine):
        super().__init__(machine)
        self.__execute()

    def on_event(self, event=None):
        return RunState(self.machine)

    def __execute(self):
        # Test

        # LED green light blinks
        green = GreenLightThread(self.__GREEN_LIGHT_TIME)
        green.start()
        self.machine.on_event(Event.RESET_EV)


class RunState(State):
    """
    The main state, which represents the main features
    of the application and its operations
    """

    __TURN_DURATION_TIME = 15  # Duration of a turn
    __YELLOW_LIGHT_TIME = 5  # Duration of time that yellow light will blink, before the end of the turn

    def __init__(self, machine):
        super().__init__(machine)
        self.__execute()

    def __del__(self):
        print("Delete RunState")

    def on_event(self, event):
        if event == Event.TIMER_EXP_EV:
            return ResetState(self.machine)
        if event == Event.LAUNCH_DET_EV:
            return ResetState(self.machine)
        if event == Event.VOICE_OVERLAP_DET_EV:
            pass

    def __execute(self):
        # Threads to check gyro/mic/timer
        print("Executing RunState")
        TimerCheckState(self.machine, self.__TURN_DURATION_TIME, self.__YELLOW_LIGHT_TIME)
        LaunchCheckState(self.machine)


class MicCheckState(State):
    pass
