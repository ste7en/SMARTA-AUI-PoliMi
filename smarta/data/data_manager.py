from statistics import mean


class DataManager(object):
    """
    Data manager used by the application to show to the user useful information
    """

    __instance = None

    def __init__(self):
        if DataManager.__instance is None:
            DataManager.__instance = self
            self.__number_of_turns = 0
            self.__turn_durations = []
            self.__overlaps = 0
        else:
            raise Exception("This class is a Singleton")

    @staticmethod
    def get_instance():
        """ Static access method.
        :rtype: DataManager
        """
        if DataManager.__instance is None:
            DataManager()
        return DataManager.__instance

    @classmethod
    def clear(cls):
        """
        Deletes the DataManager instance of the singleton
        """
        cls.__instance = None

    def add_turn(self, t_time, new_turn=True) -> None:
        """
        Increments the number of turns played in the game
        and updates the list of turns' duration
        :param t_time: duration of the last turn
        :param new_turn: True if the turn duration belongs to a new turn
        """
        if not new_turn:
            t_time += self.__turn_durations.pop()
        else: self.__number_of_turns += 1
        self.__turn_durations.append(t_time)

    def add_overlap(self) -> None:
        self.__overlaps += 1

    def get_number_of_turns(self):
        return self.__number_of_turns

    def get_avg_turn_duration(self):
        return round(mean(self.__turn_durations), 2)

    def get_number_of_overlaps(self):
        return self.__overlaps
