from smarta.utility.GPIOManager import GPIOManager
import time
from rpi_ws281x import Color, PixelStrip, ws

class LedManager():

    # LED strip configuration:
    __LED_COUNT = 30  # Number of LED pixels.
    __LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
    __LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    __LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    __LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    __LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    __LED_CHANNEL = 0
    # LED_STRIP = ws.SK6812_STRIP_RGBW
    __LED_STRIP = ws.SK6812W_STRIP
    __instance = None

    def __init__(self):
        if LedManager.__instance is None:
            LedManager.__instance = self

        else:
            raise Exception("This class is a Singleton")

    @staticmethod
    def get_instance():

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
        strip = PixelStrip(self.__LED_COUNT, self.__LED_PIN, self.__LED_FREQ_HZ, self.__LED_DMA, self.__LED_INVERT, self.__LED_BRIGHTNESS, self.__LED_CHANNEL, self.__LED_STRIP)
        strip.begin()
        while True:

            self.colorWipe(strip, Color(255, 0, 0), 0)  # Red wipe
            time.sleep(1)
            self.colorWipe(strip, Color(0, 255, 0), 0)  # Blue wipe
            time.sleep(1)
            self.colorWipe(strip, Color(0, 0, 255), 0)  # Green wipe
            time.sleep(1)
            self.colorWipe(strip, Color(0, 0, 0, 255), 0)  # White wipe
            time.sleep(1)
            self.colorWipe(strip, Color(255, 255, 255), 0)  # Composite White wipe
            time.sleep(1)
            self.colorWipe(strip, Color(255, 255, 255, 255), 0)  # Composite White + White LED wipe
            time.sleep(1)