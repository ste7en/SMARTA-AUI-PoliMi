from smarta.state.state import State
from smarta.events.events import Event
from smarta.events.timer import TimerCheckState


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
    def __init__(self, machine):
        super().__init__(machine)
        self.__execute()

    def on_event(self, event=None):
        return RunState(self.machine)

    def __execute(self):
        # Test
        self.on_event()

        # LED blink
        pass


class RunState(State):
    """
    The main state, which represents the main features
    of the application and its operations
    """
    def __init__(self, machine):
        super().__init__(machine)
        self.__execute()

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
        TimerCheckState(self.machine)


class GyroCheckState(State):
    pass


class MicCheckState(State):
    pass





