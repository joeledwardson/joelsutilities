import functools
import logging
import time
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Union


active_logger = logging.getLogger(__name__)


class TimingRegistrar:
    def __init__(self, timings: Optional[Dict[str, List[timedelta]]] = None):
        """_summary_

        :param timings: initial store of timings, defaults to None
        :type timings: Optional[Dict[str, List[timedelta]]], optional
        """
        self._function_timings: Dict[str, List[timedelta]] = timings or {}

    def log_result(self, elapsed_seconds: float, name: str) -> None:
        """manually add to list of timed functions

        :param elapsed_seconds: elapsed time value
        :type elapsed_seconds: float
        :param name: function name
        :type name: str
        """
        if name not in self._function_timings:
            self._function_timings[name] = []
        self._function_timings[name].append(timedelta(seconds=elapsed_seconds))

    def _call(self, f: Callable, key: str, *args, **kwargs) -> Any:
        start_time = time.perf_counter() # gets timestamp in seconds (with decimal places)
        val = f(*args, **kwargs)  # execute function and store output
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time  # compute time for function execution
        # use object name with method name for key
        if key not in self._function_timings:
            self._function_timings[key] = list()
        self._function_timings[key].append(timedelta(seconds=elapsed_time))
        return val

    def register_named_method(self, name_attr: str) -> Callable:
        """
        Register a function for execution times to be logged, using a custom named key
        """
        def outer(method: Callable):
            @functools.wraps(method)
            def inner(_self, *args, **kwargs):
                return self._call(method, name_attr, _self, *args, **kwargs)

            return inner

        return outer

    def register_method(self, func: Callable) -> Callable:
        """
        Register a function for for execution times to be logged using <class name>.<function name> as the key
        """
        @functools.wraps(func)
        def inner(_self, *args, **kwargs):
            key = _self.__class__.__name__ + "." + func.__name__
            return self._call(inner, key, _self, *args, **kwargs)

        return inner

    def register_function(self, func: Callable) -> Callable:
        """
        Register a function for execution times to be logged, using function name as the key
        """
        @functools.wraps(func)
        def inner(*args, **kwargs):
            return self._call(func, func.__name__, *args, **kwargs)

        return inner

    @property
    def timings(self):
        return self._function_timings



def ms_to_datetime(timestamp_ms: Union[int, float]) -> datetime:
    """convert millisecond timestamp to datetime in UTC

    :param timestamp_ms: milliseconds timestamp since epoch
    :type timestamp_ms: Union[int, float]
    :return: datetime object
    :rtype: datetime
    
    
    >>> ms_to_datetime(0) == datetime(1970, 1, 1) # epoch is 1st jan 1970
    True
    """
    return datetime.utcfromtimestamp(float(timestamp_ms) / 1000)
