import RPi.GPIO as GPIO
import time

class VibratorManager():

     def __init__(self):
        VibratorManager.__instance = self

     @staticmethod
     def get_instance():

         if VibratorManager.__instance is None:
            VibratorManager()
         return VibratorManager.__instance

     def setVibrator(self):

        __pin = 8
        __dc = 75
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(__pin, GPIO.OUT)
        pwm = GPIO.PWM(__pin, 50)

        pwm.start(50)
        pwm.ChangeDutyCycle(__dc)
        time.sleep(0.25)

        pwm.stop()
        GPIO.cleanup()


