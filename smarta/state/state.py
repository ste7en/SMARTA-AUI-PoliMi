from smarta.__main__ import Smarta


class State(object):
    """
    A state class that will be useful to define some
    common functions for each individual state of the FSM.
    It has to be subclassed to implement specific functionalities
    for each state.
    """
    def __init__(self, machine: Smarta):
        """
        State object initializer, called by subclasses
        :param machine: the FSM responsible of handling events and transitions
        """
        self.machine = machine
        print('Processing state:', str(self.__class__.__name__))

    def on_event(self, event):
        """
        Called by the machine which runs the state to get a specific transition
        :param event: an event that could happen during state's execution
        :return: a State subclass that the machine will run
        :rtype: State
        """
        pass

    def execute(self) -> None:
        """
        Code to be executed by the state when it's ran by the machine
        :return: None
        """
        pass
