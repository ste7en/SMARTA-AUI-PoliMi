import smbus
import time
import RPi.GPIO as gpio

from abc import ABC, abstractmethod


class GPIOManager(ABC):

    def __init__(self, dev_address):
        self.__bus = smbus.SMBus(1)
        self.dev_address = dev_address
        super().__init__()

    def write_byte_data(self, bus_address, value):
        self.__bus.write_byte_data(self.dev_address, bus_address, value)

    def read_byte_data(self, bus_address):
        return self.__bus.read_byte_data(self.dev_address, bus_address)

    @staticmethod
    def gpio_sleep():
        time.sleep(0.005)

    @abstractmethod
    def read(self, bus_address):
        pass

    @abstractmethod
    def write(self, bus_address, value):
        pass
