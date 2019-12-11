from smarta.utility.GPIOManager import GPIOManager


class AccelerometerManager(GPIOManager):
    """
    Subclass of GPIOManager, responsible of managing data I/O with
    the MPU6050, in particular data coming from the accelerometer.
    """
    __PWR_M = 0x6B
    __DIV = 0x19
    __CONFIG = 0x1A
    __GYRO_CONFIG = 0x1B
    __ACC_CONFIG = 0x1C
    __INT_EN = 0x38

    __ACCEL_X = 0x3B
    __ACCEL_Y = 0x3D
    __ACCEL_Z = 0x3F

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
        """ Static access method. 
        :rtype: AccelerometerManager
        """
        if AccelerometerManager.__instance is None:
            AccelerometerManager()
        return AccelerometerManager.__instance

    def write(self, bus_address, value) -> None:
        """
        Write operation on 8b register
        :param bus_address: the address of the register
        :param value: 8-bit value to write
        :return: None
        """
        super().write_byte_data(bus_address, value)

    def read(self, bus_address):
        """
        Read operation on 2B registers
        :param bus_address: the high address of the register
        :return: 16-bit data stored in the registers
        """
        value = super().read_byte_data(bus_address) << 8 | super().read_byte_data(bus_address + 1)
        if value >= 0x8000:
            return -((65535 - value) + 1)
        else:
            return value

    def __init_mpu(self) -> None:
        """
        Initializes the MPU6050
        :return: None
        """
        self.write(self.__DIV, 7)
        self.write(self.__PWR_M, 1)
        self.write(self.__CONFIG, 0)
        self.write(self.__ACC_CONFIG, 8)  # Full Scale Range of ± 4g
        self.write(self.__INT_EN, 1)
        super().gpio_sleep()

    def get_accel_x(self) -> float:
        """
        :return: x-axis value of acceleration
        """
        return self.read(AccelerometerManager.__ACCEL_X)/8192.0  # Normalized to a Full Scale Range of ± 4g

    def get_accel_y(self) -> float:
        """
        :return: y-axis value of acceleration
        """
        return self.read(AccelerometerManager.__ACCEL_Y)/8192.0  # Normalized to a Full Scale Range of ± 4g

    def get_accel_z(self) -> float:
        """
        :return: z-axis value of acceleration
        """
        return self.read(AccelerometerManager.__ACCEL_Z)/8192.0  # Normalized to a Full Scale Range of ± 4g

    """
    These are the parameters to use in order to get data from the gyroscope:
    
    __GYRO_X = 0x43
    __GYRO_Y = 0x45
    __GYRO_Z = 0x47

    Put the following line in the __init__():
    self.write(self.__GYRO_CONFIG, 24)

    Helper methods:
    def get_gyro_x(self):
        return self.read(AccelerometerManager.__GYRO_X)

    def get_gyro_y(self):
        return self.read(AccelerometerManager.__GYRO_Y)

    def get_gyro_z(self):
        return self.read(AccelerometerManager.__GYRO_Z) 
    """
