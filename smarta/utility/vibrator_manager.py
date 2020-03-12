import RPi.GPIO as GPIO
import threading
import time


class VibratorManager(object):
    """
    Singleton class responsible of controlling the vibration motor through a GPIO PWM
    """
    __instance = None
    __pin = 8
    __dc = 50  # duty-cycle
    __frequency = 1  # frequency in Hz

    def __init__(self):
        if VibratorManager.__instance is None:
            VibratorManager.__instance = self
            self.__pwm = VibratorManager.__setVibratorPWM()
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
    def __setVibratorPWM():
        #  GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(VibratorManager.__pin, GPIO.OUT)
        return GPIO.PWM(VibratorManager.__pin, VibratorManager.__frequency)

    def __runner(self, timeout):
        """
        Vibrates with the specified values of duty-cycle and frequency,
        does the GPIO cleanup and then re-instantiate the PWM
        :param timeout: duration of the vibration in seconds
        :return: None
        """
        self.__pwm.ChangeFrequency(VibratorManager.__frequency)
        self.__pwm.start(VibratorManager.__dc)
        time.sleep(timeout)
        self.__pwm.stop()
        GPIO.cleanup()
        self.__pwm = VibratorManager.__setVibratorPWM()

    def vibrate(self, t):
        """
        calls self.__runner(t) in another thread
        :param t: duration of the vibration in seconds
        :return: None
        """
        threading.Thread(target=self.__runner, args=[t]).start()
