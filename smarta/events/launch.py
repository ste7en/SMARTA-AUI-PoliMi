from smarta.state import State
from smarta.events import Event
from smarta.utility import LaunchDetector
from math import fabs
import threading
import logging


class LaunchCheckState(State):
    __threshold_value_phase_one = 0.3
    __threshold_value_phase_two = 0.1

    def __init__(self, machine):
        super().__init__(machine)
        self.__launchDetector = LaunchDetector()
        self.__last_vsa_value = None
        self.__launch_phase_started = False
        self.__execute()

    def exit(self) -> None:
        self.__launchDetector.stop()
        logging.debug('LaunchCheckState - exiting')

    def __execute(self):
        logging.debug('LaunchCheckState - Starting the LaunchDetector...')
        self.__launchDetector.start()
        logging.debug('LaunchCheckState - Switching to another thread...')
        threading.Thread(target=self.__check).start()

    def __check(self):
        """

        """
        logging.debug('LaunchCheckState - OK.')
        self.__last_vsa_value = self.__launchDetector.avg_acc_value()
        while self.__last_vsa_value is not None:
            vsa_value = self.__launchDetector.avg_acc_value()
            if vsa_value is None:
                return
            delta = fabs(vsa_value - self.__last_vsa_value)
            # print('delta =', delta)
            if delta > self.__threshold_value_phase_one and self.__launch_phase_started is False:
                logging.debug('Launch detected, delta = ' + str(delta))
                self.__launch_phase_started = True
            if delta < self.__threshold_value_phase_two and self.__launch_phase_started:
                logging.debug('End of launch detected, delta = ' + str(delta))
                self.__launch_phase_started = False
                logging.info('The ball has been launched. Sending a Launch event to FSM...')
                self.machine.on_event(Event.LAUNCH_DET_EV)
            self.__last_vsa_value = vsa_value
