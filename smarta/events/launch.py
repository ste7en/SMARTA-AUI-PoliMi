from smarta.state.state import State
from smarta.events.events import Event
from smarta.utility.launch_detector import LaunchDetector
from math import fabs
import threading


class LaunchCheckState(State):
    __threshold_value_phase_one = 0.3
    __threshold_value_phase_two = 0.1

    def __init__(self, machine):
        super().__init__(machine)
        self.__launchDetector = LaunchDetector()
        self.__last_vsa_value = None
        self.__launch_phase_started = False
        self.__execute()

    def __del__(self):
        self.__launchDetector.stop()
        print("destructor of launchcheckstate")

    def __execute(self):
        self.__launchDetector.start()
        threading.Thread(target=self.__check).start()

    def __check(self):
        """

        """
        self.__last_vsa_value = self.__launchDetector.avg_acc_value()
        while self.__last_vsa_value is not None:
            vsa_value = self.__launchDetector.avg_acc_value()
            if vsa_value is None:
                return
            delta = fabs(vsa_value - self.__last_vsa_value)
            # print('delta =', delta)
            if delta > self.__threshold_value_phase_one and self.__launch_phase_started is False:
                print("Lancio iniziato, delta = ", delta)
                self.__launch_phase_started = True
            if delta < self.__threshold_value_phase_two and self.__launch_phase_started:
                print("Lancio finito, delta = ", delta)
                self.__launch_phase_started = False
                self.machine.on_event(Event.LAUNCH_DET_EV)
            self.__last_vsa_value = vsa_value
