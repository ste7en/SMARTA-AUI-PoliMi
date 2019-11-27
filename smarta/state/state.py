class State(object):
    """
    A state object which will be useful to define some
    common functions for each individual state of the FSM.
    """
    def __init__(self, machine):
        self.machine = machine
        print('Processing state:', str(self.__class__.__name__))

    def on_event(self, event):
        pass

    def __execute(self):
        pass
