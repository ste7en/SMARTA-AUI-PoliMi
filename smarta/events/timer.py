from smarta.state.state import State
from smarta.events.events import Event
from threading import Timer


class TimerCheckState(State):

    __timer_duration_sec = 10.0

    def __init__(self, machine):
        super().__init__(machine)
        self.timer = Timer(self.__timer_duration_sec, self.__timeout_expired)
        self.timer.start()

    def __timeout_expired(self):
        print("Timeout expired")
        self.machine.on_event(Event.TIMER_EXP_EV)

    def __del__(self):
        self.timer.cancel()
        print("timer destructor")
