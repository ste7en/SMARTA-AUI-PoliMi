import time
from rpi_ws281x import Color, PixelStrip, ws
from threading import Thread
from threading import Timer
from enum import Enum


class LedColor(Enum):
    RED = Color(255, 0, 0)
    YELLOW = Color(255, 200, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    WHITE = Color(255, 255, 255)
    OFF = Color(0, 0, 0, 0)


class LedManager(object):
    # TODO: - Log and document this class

    # LED strip configuration:
    __LED_COUNT = 3         # Number of LED pixels.
    __LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM!).
    __LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    __LED_DMA = 10          # DMA channel to use for generating signal (try 10)
    __LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    __LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
    __LED_CHANNEL = 0
    __LED_STRIP = ws.WS2812_STRIP

    __instance = None

    def __init__(self):
        if LedManager.__instance is None:
            LedManager.__instance = self
            self.strip = PixelStrip(self.__LED_COUNT, self.__LED_PIN, self.__LED_FREQ_HZ, self.__LED_DMA,
                                    self.__LED_INVERT, self.__LED_BRIGHTNESS, self.__LED_CHANNEL, self.__LED_STRIP)
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

    # Define function that colors all LEDs of the given color.
    def color_wipe(self, led_color, wait_ms=50):
        for i in range(0, self.strip.numPixels()):
            self.strip.setPixelColor(i, led_color.value)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)


class LedThread(Thread):
    """
        Thread that will make the leds start showing the given color in a blinking or steady manner.
        The light will last a given amount of seconds.
        To stop ahead of time, you can also set "running" parameter of thread to False.
    """
    def __init__(self, color, duration_s, blinking_time_s=0):
        """
        :param color: a LedColor item, the desired color of the light
        :param duration_s: length of time the light must last
        :param blinking_time_s: blinking interval. If set to 0, the light will be steady.
        """
        super().__init__()
        self.led = LedManager.get_instance()
        self.running = True
        self.color = color
        self.duration_s = duration_s
        self.blinking_time_s = blinking_time_s

    def __timeout_expired(self):
        self.running = False

    def run(self):
        timer = Timer(self.duration_s, self.__timeout_expired)   # timer will stop the thread after duration_s seconds
        timer.start()                                            # (by setting "running" = False)

        if self.blinking_time_s:               # if the light is a blinking light,
            while self.running:                    # while the thread is running, it will:
                self.led.color_wipe(self.color)    # turn on leds for blinking_time_s seconds,
                time.sleep(self.blinking_time_s)
                self.led.color_wipe(LedColor.OFF)  # and turn off leds for blinking_time_s seconds
                time.sleep(self.blinking_time_s)

        else:                                  # otherwise, if the light is a steady light,
            self.led.color_wipe(self.color)    # it will turn on the leds of the desired color
            while self.running:                # while the thread is running.
                pass

        self.led.color_wipe(LedColor.OFF)     # once the thread is not running anymore, leds will be turned off.
