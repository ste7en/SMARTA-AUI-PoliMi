import RPi.GPIO as GPIO
import threading
import time


class VibratorManager(object):
    """
    Singleton class responsible of controlling the vibration motor through a GPIO PWM
    """
    __instance = None
    __pin = 8
    __dc_intermittent = 50  # duty-cycle
    __dc_continuous = 100
    __frequency = 1  # frequency in Hz

    def __init__(self):
        if VibratorManager.__instance is None:
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
        pwm = VibratorManager.__getVibratorPWM()
        # pwm.ChangeFrequency(VibratorManager.__frequency)
        dc = VibratorManager.__dc_intermittent if intermittent else VibratorManager.__dc_continuous
        pwm.start(dc)
        time.sleep(timeout)
        pwm.stop()
        GPIO.cleanup()

    @staticmethod
    def vibrate(t, intermittent=False):
        """
        calls self.__runner(t) in another thread
        :param t: duration of the vibration in seconds
        :param intermittent: boolean parameter to choose between an intermittent or a continuous vibration
        :return: None
        """
        threading.Thread(target=VibratorManager.__runner, args=[t, intermittent]).start()
