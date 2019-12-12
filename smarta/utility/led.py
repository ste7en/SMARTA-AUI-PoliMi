from smarta.utility.GPIOManager import GPIOManager
import time
from rpi_ws281x import Color, PixelStrip, ws
from threading import Timer

class LedManager():

    # LED strip configuration:
    __LED_COUNT = 3  # Number of LED pixels.
    __LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
    __LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    __LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    __LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    __LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    __LED_CHANNEL = 0
    __LED_STRIP = ws.WS2812_STRIP

    #__LED_STRIP = ws.SK6812W_STRIP

    # LED_STRIP = ws.SK6812W_STRIP

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

    def colorWipe(self, strip, color, wait_ms=50):

        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)

    def elenafunc(self):

        while True:

            self.colorWipe(self.strip, Color(255, 0, 0), 0)  # Red wipe
            time.sleep(1)
            self.colorWipe(self.strip, Color(0, 255, 0), 0)  # Green wipe
            time.sleep(1)
            self.colorWipe(self.strip, Color(0, 0, 255), 0)  # Blue wipe
            time.sleep(1)
            self.colorWipe(self.strip, Color(255, 255, 255), 0)  # Composite White wipe
            time.sleep(1)
            self.colorWipe(self.strip, Color(255, 255, 255, 255), 0)  # Composite White + White LED wipe
            time.sleep(1)

    # possibilmente implementare una versione più carina con un timer, invece di un for
    def red_blinking(self, wait_s):
        for i in range(wait_s):
            self.colorWipe(self.strip, Color(255, 0, 0), 0)  # Red wipe
            time.sleep(0.5)
            self.colorWipe(self.strip, Color(0, 0, 0, 0), 0)  # Off
            time.sleep(0.5)

    def stop(self):
        self.colorWipe(self.strip, Color(0, 0, 0, 0), 0)  # Off

    def yellow_blinking_slowly(self, wait_s):
        for i in range(wait_s):
            self.colorWipe(self.strip, Color(255, 200, 0), 0)  # Yellow wipe
            time.sleep(1)
            self.colorWipe(self.strip, Color(0, 0, 0, 0), 0)  # Off
            time.sleep(1)

    def green_new_turn(self):
        self.colorWipe(self.strip, Color(0, 255, 0), 0)  # Green wipe
        time.sleep(3)
        self.colorWipe(self.strip, Color(0, 0, 0, 0), 0)  # Off
