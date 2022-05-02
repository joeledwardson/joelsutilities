from typing import Union

import numpy as np

from .exceptions import NumericException


def closest_index(array: np.ndarray, value: Union[float, int]) -> int:
    """
    get closest index in numpy array, or -1 if empty
    
    
    >>> closest_index([1,2,3,4,5], 1.2)
    0
    >>> closest_index([1,2,3,4,5], -1)
    0
    >>> closest_index([1,2,3,4,5], 1.6)
    1
    >>> closest_index([1,2,3,4,5], 999)
    4
    >>> closest_index([1,2,3,4,5], 2.4)
    1
    >>> closest_index([1,2,3,4,5], 4.9)
    4
    """

    if array.ndim != 1:
        raise NumericException(f"expected 1-dimensional array, got: {array.ndim}")

    if not array.shape[0]:
        return -1

    return int(abs(array - value).argmin())
