from smarta.state import IdleState, RunState
from smarta.data import DataManager
from smarta import Event
import logging
import threading


class Smarta(object):
    """
    The FSM that will handle the different states of the game.
    """

    def __init__(self):
        self.__state = IdleState(self)

    @staticmethod
    def set_turn_duration(turn_duration):
        RunState.set_turn_duration_time(turn_duration)

    @staticmethod
    def get_turn_duration():
        '''
        Returns the default number of seconds for each turn.
        :return: Integer > 0
        '''
        return RunState.get_turn_duration_time()

    def on_event(self, event: Event) -> None:
        """
        This function calls the State.on_event() func to realize
        a transition function for every captured event
        :param event: an acceptable event, as described into events.py
        """
        logging.info('FSM Event processed: ' + str(event))
        # Every state is responsible for its transition table
        next_state = self.__state.on_event(event)
        if next_state is not None:
            self.__state.exit()
            self.__state = next_state
            logging.info('Executing next state: ' + str(next_state.__class__.__name__))
            threading.Thread(target=self.__state.execute).start()

    def start(self):
        logging.debug('Application started.')
        DataManager.clear()
        self.__state.execute()
        self.on_event(Event.START_EV)

    def stop(self):
        self.__state.exit()
        self.__state = IdleState(self)
        logging.debug('Application stopped.')

    @staticmethod
    def get_summary():
        dm = DataManager.get_instance()
        return dm.get_avg_turn_duration(), dm.get_number_of_turns(), dm.get_number_of_overlaps()
