from math import sqrt
from statistics import mean
from smarta.utility.accellerometer_manager import AccelerometerManager as Accelerometer
import sched
import threading
import time


class LaunchDetector(threading.Thread):
    __queue_length = 15
    __acquisition_period_in_seconds = 0.1

    def __init__(self):
        super().__init__()
        self.__vsa_array = []
        self.__sched = sched.scheduler(time.time, time.sleep)
        self.__accelerometer = Accelerometer.get_instance()
        self.__stopped = False

    def _compute_vsa(self, x, y, z):
        """
        Computes the vector sum of acceleration data and puts it into a __queue_length queue
        :param x: x-acceleration
        :param y: y-acceleration
        :param z: z-acceleration
        """
        vsa = round(sqrt((x ** 2) + (y ** 2) + (z ** 2)), 5)

        if len(self.__vsa_array) == LaunchDetector.__queue_length:
            self.__vsa_array.pop()
        self.__vsa_array.insert(0, vsa)

        # TEST TODO: - Remove this print
        print('vsa_array = ', self.__vsa_array)
        # END TEST

    def start_detection(self):
        # TODO: - Log this operation
        self._enter_scheduler()
        self.__sched.run()

    def run(self):
        self.start_detection()

    def stop(self):
        self.__stopped = True
        self.__vsa_array = []

    def _sched_acquire_and_store_data(self):
        x = self.__accelerometer.get_accel_x()  # get_gyro_x()
        y = self.__accelerometer.get_accel_y()  # get_gyro_y()
        z = self.__accelerometer.get_accel_z()  # get_gyro_z()
        self._compute_vsa(x, y, z)
        if not self.__stopped:
            self._enter_scheduler()

    def _enter_scheduler(self):
        self.__sched.enter(self.__acquisition_period_in_seconds, 1, self._sched_acquire_and_store_data)

    def avg_acc_value(self):
        return mean(self.__vsa_array)
