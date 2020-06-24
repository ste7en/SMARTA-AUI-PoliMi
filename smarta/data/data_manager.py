from statistics import mean
from datetime import date
import logging
import json


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
            self.__archive = self._load_archive()
            self.__current_team_name = "NewTeam"
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

    def _load_archive(self):
        with open("data/archive.json") as data:
            logging.info("Data loading...")
            return json.load(data)

    def _dump_archive(self):
        logging.info("Saving data...")
        with open("data/archive.json", "w") as file:
            json.dump(self.__archive, file)
            logging.info("Data successfully saved.")

    def get_archived_teams(self):
        return list(self.__archive.keys())

    def get_team_history(self, team_name):
        return self.__archive.get(team_name)

    def set_team_name(self, name):
        self.__current_team_name = name

    def game_ended(self):
        s = {'date': date.today().strftime("%d/%m/%y"),
             'n_of_turns': self.get_number_of_turns(),
             'avg_turn_length': str(self.get_avg_turn_duration()),
             'overlaps_detected': self.get_number_of_overlaps()
             }
        if self.__archive.get(self.__current_team_name) is None:
            self.__archive[self.__current_team_name] = []
        self.__archive.get(self.__current_team_name).insert(0, s)

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
        return 0 if len(self.__turn_durations) == 0 else round(mean(self.__turn_durations), 2)

    def get_number_of_overlaps(self):
        return self.__overlaps
