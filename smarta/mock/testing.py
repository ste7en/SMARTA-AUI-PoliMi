from smarta.data import DataManager
import logging


class Smarta(object):
    """
        The FSM that will handle the different states of the game.
        """

    turn_duration = 90

    def __init__(self):
        self.__state = None

    @classmethod
    def set_turn_duration(cls, turn_duration):
        cls.turn_duration = turn_duration

    @classmethod
    def get_turn_duration(cls):
        '''
        Returns the default number of seconds for each turn.
        :return: Integer > 0
        '''
        return cls.turn_duration

    def on_event(self, event = None) -> None:
        """
        This function calls the State.on_event() func to realize
        a transition function for every captured event
        :param event: an acceptable event, as described into events.py
        """
        logging.debug('Event: '+ str(event))
        pass

    def start(self):
        logging.debug('Application started.')
        DataManager.clear()
        self.on_event()

    def stop(self):
        logging.debug('Application stopped.')

    @staticmethod
    def get_summary():
        dm = DataManager.get_instance()
        return dm.get_avg_turn_duration(), dm.get_number_of_turns(), dm.get_number_of_overlaps()
