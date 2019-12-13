import RPi.GPIO as GPIO
import time


class VibratorManager(object):
    """
    Singleton class responsible of controlling the vibration motor through a GPIO PWM
    """
    __instance = None

    def __init__(self):
        if VibratorManager.__instance is None:
            VibratorManager.__instance = self
            self.__pin = 8
            self.__dc = 75
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

    def setVibrator(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__pin, GPIO.OUT)
        pwm = GPIO.PWM(self.__pin, 50)

        pwm.start(50)
        pwm.ChangeDutyCycle(self.__dc)
        time.sleep(0.25)

        pwm.stop()
        GPIO.cleanup()


