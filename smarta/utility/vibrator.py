from gpiozero import InputDevice, OutputDevice, PWMOutputDevice

trig = OutputDevice(4)
echo = InputDevice(17)
motor = PWMOutputDevice(14)

sleep(2)
class vibratorManager():

    def __init__(self):
        if vibratorManager.__instance is None:
            vibratorManager.__instance = self

        else:
            raise Exception("This class is a Singleton")

    @staticmethod
    def get_instance():

        if vibratorManager.__instance is None:
            vibratorManager()
        return vibratorManager.__instance



    def get_pulse_time(self):
        trig.on()
        sleep(0.0001)
        trig.off()

        while echo.is_active == False:
            pulse_start = time()

        while echo.is_active == True:
            pulse_end = time()

        sleep(0.06)

        return pulse_end - pulse_start

    def calculate_distance(duration):
        speed = 343
        distance = speed * duration / 2
        return distance

    def calculate_vibration(distance):
        vibration = (((distance - 0.02) * -1) / (4 - 0.02)) + 1
        return vibration

    while True:
        duration = get_pulse_time()
        distance = calculate_distance(duration)
        vibration = calculate_vibration(distance)
        motor.value = vibration