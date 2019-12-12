from smarta.state.state import State
from smarta.events.events import Event
from smarta.utility.launch_detector import LaunchDetector
from math import fabs
import threading


class LaunchCheckState(State):
    __threshold_value = 2

    def __init__(self, machine):
        super().__init__(machine)
        self.__launchDetector = LaunchDetector()
        self.__last_vsa_value = None
        self.__execute()

    def __del__(self):
        self.__launchDetector.stop()
        print("destructor of launchcheckstate")

    def __execute(self):
        self.__launchDetector.start()
        threading.Thread(target=self.__check)

    def __check(self):
        """

        """
        self.__last_vsa_value = self.__launchDetector.avg_acc_value()
        while self.__last_vsa_value is not None:
            vsa_value = self.__launchDetector.avg_acc_value()
            delta = fabs(vsa_value - self.__last_vsa_value)
            if delta > self.__threshold_value:
                print("Lancio")
                self.machine.on_event()