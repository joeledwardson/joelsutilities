import logging
import queue
from enum import Enum
from typing import Dict, List, Union

from .exceptions import StateMachineException

active_logger = logging.getLogger(__name__)


class State:
    """Base state class used with :ref:`State.run <_staterun>`
    
    
    .. _state:
    
    """
    
    def enter(self, **inputs):
        """function called when transitioning from another state
        function not called on subsequent `run`s once state is entered
        """
        pass

    def run(self, **inputs) -> Union[Enum, bool, None, List[Enum]]:
        """execute state actions
        
        
        .. _staterun:
        

        :raises NotImplementedError: function must be defined
        :return: `Enum` for the next state, or `list` of `Enum`s for list of next states, `False` or `None` to remain in current state, `True` to continue to next state in list
        :rtype: Union[Enum, bool, None, List[Enum]]
        """        
        raise NotImplementedError



# TODO - this should be broken up into individual building blocks
class StateMachine:
    """Handle state execution, magenement and transition
    
    
    .. _statemachine:
    
    
    """
    def __init__(self, states: Dict[Enum, State], initial_state: Enum):
        """
        :param states: map of `Enum` to `State`
        :type states: Dict[Enum, State]
        :param initial_state: first key to use
        :type initial_state: Enum
        """
        self.states: Dict[Enum, State] = states
        self.current_state_key: Enum = initial_state
        self.previous_state_key: Enum = initial_state
        self.initial_state_key: Enum = initial_state
        self.is_state_change: bool = True
        self.state_queue = queue.Queue()


    def flush(self):
        """
        clear state queue
        """
        self.state_queue.queue.clear()

    def force_change(self, new_states: List[Enum]):
        """
        updating current state to first in queue and forcibly add a list of new states to queue
        """
        for state_key in new_states:
            self.state_queue.put(state_key)
        self.current_state_key = self.state_queue.get()
        self.is_state_change = True



    def run(self, **kwargs):
        """
        run state machine with `kwargs` dictionary repeatedly until no state change is detected
        """

        while True:

            if self.is_state_change:
                self.states[self.current_state_key].enter(**kwargs)

            self.previous_state_key = self.current_state_key

            ret = self.states[self.current_state_key].run(**kwargs)

            if isinstance(ret, list):
                # list returned, add all to queue
                for s in ret:
                    self.state_queue.put(s)
                self.current_state_key = self.state_queue.get()
            elif ret is None or ret is False or ret == self.current_state_key:
                # no value returned or same state returned, same state
                pass
            elif isinstance(ret, Enum):
                # True means go to next state, None means use existing, otherwise single state value has been
                # returned so add to queue
                self.state_queue.put(ret)
                self.current_state_key = self.state_queue.get()
            elif ret is True:
                # returned value implies state change (True, list of states, or single new state)
                if not self.state_queue.qsize():
                    # state has returned true when nothing in queue! (this shouldn't happen)
                    raise StateMachineException("state machine queue has no size")
                # get next state from queue
                self.current_state_key = self.state_queue.get()
            else:
                # unrecognized return type
                raise StateMachineException(
                    f'return value "{ret}" in state machine not recognised'
                )

            self.is_state_change = self.previous_state_key != self.current_state_key
            if self.is_state_change:
                # new state is different to current, process change and repeat loop
                self.process_state_change(
                    self.previous_state_key, self.current_state_key, **kwargs
                )
            else:
                # exit loop if no state change
                break

    def process_state_change(self, old_state, new_state, **kwargs):
        pass
