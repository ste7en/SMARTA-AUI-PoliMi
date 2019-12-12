from smarta.utility.GPIOManager import GPIOManager
import time
from rpi_ws281x import Color, PixelStrip, ws
from threading import Thread
from threading import Timer


class LedManager():

    # LED blinking times configuration:
    __BLINKING_TIME_RED = 0.5
    __BLINKING_TIME_YELLOW = 1   # yellow light blinks more slowly

    # LED strip configuration:
    __LED_COUNT = 3  # Number of LED pixels.
    __LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
    __LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    __LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    __LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    __LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    __LED_CHANNEL = 0
    __LED_STRIP = ws.WS2812_STRIP

    __instance = None

    def __init__(self):
        if LedManager.__instance is None:
            LedManager.__instance = self
            self.strip = PixelStrip(self.__LED_COUNT, self.__LED_PIN, self.__LED_FREQ_HZ, self.__LED_DMA, self.__LED_INVERT,
                               self.__LED_BRIGHTNESS, self.__LED_CHANNEL, self.__LED_STRIP)
            self.strip.begin()

        else:
            raise Exception("This class is a Singleton")

    @staticmethod
    def get_instance():
        """

        :rtype: LedManager
        """
        if LedManager.__instance is None:
            LedManager()
        return LedManager.__instance


    # Define functions which animate LEDs in various ways.

    def __colorWipe(self, strip, color, wait_ms=50):

        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)

    def __elenafunc(self):
        """
        Function to test LEDs
        """
        while True:
            self.__colorWipe(self.strip, Color(255, 0, 0), 0)  # Red wipe
            time.sleep(1)
            self.__colorWipe(self.strip, Color(0, 255, 0), 0)  # Green wipe
            time.sleep(1)
            self.__colorWipe(self.strip, Color(0, 0, 255), 0)  # Blue wipe
            time.sleep(1)
            self.__colorWipe(self.strip, Color(255, 255, 255), 0)  # Composite White wipe
            time.sleep(1)
            self.__colorWipe(self.strip, Color(255, 255, 255, 255), 0)  # Composite White + White LED wipe
            time.sleep(1)

    def red_blinking(self):
        self.__colorWipe(self.strip, Color(255, 0, 0), 0)  # Red wipe
        time.sleep(self.__BLINKING_TIME_RED)
        self.__colorWipe(self.strip, Color(0, 0, 0, 0), 0)  # Off
        time.sleep(self.__BLINKING_TIME_RED)

    def turn_off(self):
        self.__colorWipe(self.strip, Color(0, 0, 0, 0), 0)  # Off

    def yellow_blinking_slowly(self):
        self.__colorWipe(self.strip, Color(255, 200, 0), 0)  # Yellow wipe
        time.sleep(self.__BLINKING_TIME_YELLOW)
        self.__colorWipe(self.strip, Color(0, 0, 0, 0), 0)  # Off
        time.sleep(self.__BLINKING_TIME_YELLOW)

    def green_steady(self):
        self.__colorWipe(self.strip, Color(0, 255, 0), 0)  # Green wipe


class RedLightThread(Thread):
    """
    Thread that will make the leds start blinking red light.
    To stop, set "running" parameter of thread to False.
    """
    def __init__(self):
        """
        """
        super().__init__()
        self.led = LedManager.get_instance()
        self.running = True

    def run(self):
        while self.running:
            self.led.red_blinking()
        self.led.turn_off()


class YellowLightThread(Thread):
    """
    Thread that will make the leds start blinking yellow light (slowly), for a determined amount of time.
    Specify amount of time as parameter "time_s" when creating thread.
    To stop, set "running" parameter of thread to False.
    """
    def __init__(self, time_s):
        """
        :param time_s: length of time (in seconds) the yellow light must blink
        """
        super().__init__()
        self.led = LedManager.get_instance()
        self.running = True
        self.time_s = time_s

    def __timeout_expired(self):
        self.running = False

    def run(self):

        timer = Timer(self.time_s, self.__timeout_expired)
        timer.start()
        while self.running:
            self.led.yellow_blinking_slowly()
        self.led.turn_off()


class GreenLightThread(Thread):
    """
    Thread that will make the leds start showing green light (steady, not blinking), for a determined amount of time.
    Specify amount of time as parameter "time_s" when creating thread.
    """

    def __init__(self, time_s):
        """
        :param time_s: length of time (in seconds) the green light must be shown
        """
        super().__init__()
        self.led = LedManager.get_instance()
        self.time_s = time_s

    def run(self):

        self.led.green_steady()
        time.sleep(self.time_s)
        self.led.turn_off()
