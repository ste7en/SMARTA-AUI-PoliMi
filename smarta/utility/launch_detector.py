from smarta.utility import AccelerometerManager
from math import sqrt
from statistics import mean
from threading import Thread
import sched
import time
import copy
import logging


class LaunchDetector(Thread):
    # TODO: - Log and document this class
    __queue_length = 5
    __acquisition_period_in_seconds = 0.25

    def __init__(self):
        super().__init__()
        self.__vsa_array = []
        self.__sched = sched.scheduler(time.time, time.sleep)
        self.__accelerometer = AccelerometerManager.get_instance()
        self.__stopped = False

    def _compute_and_store_vsa(self, x, y, z) -> None:
        """
        Computes the vector sum of acceleration data and puts it into a __queue_length queue
        :param x: x-acceleration
        :param y: y-acceleration
        :param z: z-acceleration
        """
        vsa = round(sqrt((x ** 2) + (y ** 2) + (z ** 2)), 4)

        if len(self.__vsa_array) == LaunchDetector.__queue_length:
            self.__vsa_array.pop()
        self.__vsa_array.insert(0, vsa)

    def start_detection(self) -> None:
        self._enter_scheduler()
        self.__sched.run(blocking=True)
        logging.debug('LaunchDetector - OK.')

    def run(self):
        self.start_detection()

    def stop(self) -> None:
        """
        Stops the data acquisition and, consequently, the Thread
        :return: None
        """
        self.__stopped = True
        self.__vsa_array = []

    def _sched_acquire_and_store_data(self) -> None:
        """
        Acquire accelerometer data, computes the VSA and stores it in the queue
        :return: None
        """
        x = self.__accelerometer.get_accel_x()  # get_gyro_x()
        y = self.__accelerometer.get_accel_y()  # get_gyro_y()
        z = self.__accelerometer.get_accel_z()  # get_gyro_z()
        self._compute_and_store_vsa(x, y, z)
        if not self.__stopped:
            # time.sleep(0.05) changed by setting __acquisition_period_in_seconds from 0.2 to 0.25
            self._enter_scheduler()

    def _enter_scheduler(self) -> None:
        """
        Schedules the acquisition process after the specified '__acquisition_period_in_seconds' seconds
        :return: None
        """
        self.__sched.enter(self.__acquisition_period_in_seconds, 1, self._sched_acquire_and_store_data)

    def avg_acc_value(self) -> float:
        """
        Computes the average value of the VSA queue
        :return: average of the values stored in __vsa_array
        """
        return None if self.__stopped else 1 if len(self.__vsa_array) is 0 else mean(copy.copy(self.__vsa_array))
