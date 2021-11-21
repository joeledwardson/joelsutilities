import numpy as np
from typing import Union
from .exceptions import NumericException


def closest_index(array: np.ndarray, value: Union[float, int]) -> int:
    """get closest index in numpy array, or -1 if empty"""

    if array.ndim != 1:
        raise NumericException(f'expected 1-dimensional array, got: {array.ndim}')

    if not array.shape[0]:
        return -1

    return int(abs(array - value).argmin())

