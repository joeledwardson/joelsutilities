class EdgeDetector:
    """
    detect when a boolean value changes from True to False and vice-versa comparing to previous-state value
    
    >>> EdgeDetector(True).current_value
    True
    >>> detector.update(True)
    >>> detector.update(False)
    >>> detector.rising
    False
    >>> detector.falling
    True
    >>> detector.update(True)
    >>> detector.rising
    True
    >>> detector.falling
    False
    >>> detector.update(True)
    >>> detector.rising
    False
    >>> detector.current_value
    True    
    """

    def __init__(self, initial_value: bool):
        self._value: bool = initial_value
        self._previous: bool = initial_value
        self._rising: bool = False
        self._falling: bool = False

    def update(self, new_value: bool):
        """
        update current state boolean value
        
        .. _update:
        
        
        """
        self._previous = self._value
        self._value = new_value
        self._rising = self._value and not self._previous
        self._falling = self._previous and not self._value

    @property
    def current_value(self) -> bool:
        """most recent value set by :ref:`self.update <update>`"""
        return self._value

    @property
    def rising(self) -> bool:
        """returns `True` if latest value set by :ref:`self.update <update>` is `True` but preceeding value `False`    """
        return self._rising

    @property
    def falling(self) -> bool:
        """returns `True` if latest value set by :ref:`self.update <update>` is `False` but preceeding value `True`    """
        return self._falling



if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'detector': EdgeDetector()})