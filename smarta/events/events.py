from enum import Enum, unique
@unique
class Event(Enum):
    START_EV = "Start event registered"
    END_EV = "End event registered"
    RESET_EV = "Reset state reached"
    LAUNCH_DET_EV = "Gyroscope registered a launch event"
    VOICE_OVERLAP_DET_EV = "Microphone registered a voice overlap event"
    TIMER_EXP_EV = "Timeout event registered"
