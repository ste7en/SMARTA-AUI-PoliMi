import RPi.GPIO as GPIO
import threading
import time


class VibratorManager(object):
    """
    Singleton class responsible of controlling the vibration motor through a GPIO PWM
    """
    __instance = None
    __pin = 8
    __dc_intermittent = 50.0  # duty-cycle
    __dc_continuous = 100.0
    __frequency = 1.0  # frequency in Hz

    def __init__(self):
        if VibratorManager.__instance is None:
            self.__pwm = VibratorManager.__getVibratorPWM()
            VibratorManager.__instance = self
        else:
            raise Exception("This class is a Singleton")

    @staticmethod
    def get_instance():
        """ Static access method.
        :rtype: VibratorManager
        """
        if VibratorManager.__instance is None:
            VibratorManager()
        return VibratorManager.__instance

    @staticmethod
    def __getVibratorPWM():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(VibratorManager.__pin, GPIO.OUT)
        return GPIO.PWM(VibratorManager.__pin, VibratorManager.__frequency)

    @staticmethod
    def __runner(timeout, intermittent):
        """
        Vibrates with the specified values of duty-cycle and frequency,
        does the GPIO cleanup and then re-instantiate the PWM
        :param timeout: duration of the vibration in seconds
        :return: None
        """
        VibratorManager.get_instance().__pwm.ChangeFrequency(VibratorManager.__frequency)
        dc = VibratorManager.__dc_intermittent if intermittent else VibratorManager.__dc_continuous
        VibratorManager.get_instance().__pwm.start(dc)
        time.sleep(timeout)
        VibratorManager.get_instance().__pwm.stop()

    def vibrate(self, t=0, intermittent=True):
        """
        if t = 0 starts the vibration motor until the stop() method isn't called
        otherwise calls self.__runner(t) in another thread
        :param t: duration of the vibration in seconds
        :param intermittent: boolean parameter to choose between an intermittent or a continuous vibration
        :return: None
        """
        if t != 0: threading.Thread(target=VibratorManager.__runner, args=[t, intermittent]).start()
        else:
            dc = VibratorManager.__dc_intermittent if intermittent else VibratorManager.__dc_continuous
            self.__pwm.ChangeFrequency(VibratorManager.__frequency)
            self.__pwm.start(dc)

    def stop(self):
        self.__pwm.stop()
