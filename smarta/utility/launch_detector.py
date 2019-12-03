from math import sqrt
from smarta.utility.accellerometer_manager import AccelerometerManager as Accelerometer
import sched
import time


class LaunchDetector:
    __instance = None
    __queue_length = 5
    __acquisition_period_in_seconds = 0.1

    def __init__(self):
        if LaunchDetector.__instance is None:
            LaunchDetector.__instance = self
            self.__vsa_array = [0.0, 0.0, 0.0, 0.0, 0.0]
            self.__sched = sched.scheduler(time.time, time.sleep)
            self.__accelerometer = Accelerometer.get_instance()
        else:
            raise Exception("This class is a Singleton")

    @staticmethod
    def get_instance():
        """ Static access method. 
        :rtype: LaunchDetector
        """
        if LaunchDetector.__instance is None:
            LaunchDetector()
        return LaunchDetector.__instance

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

    def start(self):
        # TODO: - Log this operation
        self.__sched.enter(self.__acquisition_period_in_seconds, 1, self._sched_acquire_and_store_data)
        self.__sched.run()

    def stop(self):
        self.__vsa_array = [0.0, 0.0, 0.0, 0.0, 0.0]

    def _sched_acquire_and_store_data(self):
        x = self.__accelerometer.get_accel_x() #get_gyro_x()
        y = self.__accelerometer.get_accel_y() #get_gyro_y()
        z = self.__accelerometer.get_accel_z() #get_gyro_z()
        self._compute_vsa(x, y, z)
        self.__sched.enter(self.__acquisition_period_in_seconds, 1, self._sched_acquire_and_store_data)
