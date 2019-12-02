from smarta.utility.GPIOManager import GPIOManager


class AccelerometerManager(GPIOManager):
    __PWR_M = 0x6B
    __DIV = 0x19
    __CONFIG = 0x1A
    __GYRO_CONFIG = 0x1B
    __INT_EN = 0x38

    __ACCEL_X = 0x3B
    __ACCEL_Y = 0x3D
    __ACCEL_Z = 0x3F
    __GYRO_X = 0x43
    __GYRO_Y = 0x45
    __GYRO_Z = 0x47

    __DEV_ADDR = 0x68  # device address

    __instance = None

    def __init__(self):
        if AccelerometerManager.__instance is None:
            super().__init__(AccelerometerManager.__DEV_ADDR)
            AccelerometerManager.__instance = self
            self.__init_mpu()
        else:
            raise Exception("This class is a Singleton")

    @staticmethod
    def get_instance():
        """ Static access method. """
        if AccelerometerManager.__instance is None:
            AccelerometerManager()
        return AccelerometerManager.__instance

    def write(self, bus_address, value):
        super().write_byte_data(bus_address, value)

    def read(self, bus_address):
        return super().read_byte_data(bus_address)

    def __init_mpu(self):
        self.write(self.__DIV, 7)
        self.write(self.__PWR_M, 1)
        self.write(self.__CONFIG, 0)
        self.write(self.__GYRO_CONFIG, 24)
        self.write(self.__INT_EN, 1)
        super().gpio_sleep()

    def get_accel_x(self):
        return self.read(AccelerometerManager.__ACCEL_X)

    def get_accel_y(self):
        return self.read(AccelerometerManager.__ACCEL_Y)

    def get_accel_z(self):
        return self.read(AccelerometerManager.__ACCEL_Z)

    def get_gyro_x(self):
        return self.read(AccelerometerManager.__GYRO_X)

    def get_gyro_y(self):
        return self.read(AccelerometerManager.__GYRO_Y)

    def get_gyro_z(self):
        return self.read(AccelerometerManager.__GYRO_Z)
