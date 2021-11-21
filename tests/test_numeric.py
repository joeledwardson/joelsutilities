from joelsutilities import numeric
import numpy as np
import pytest


def test_closest_value():
    assert numeric.closest_index(np.array([]), 1) == -1
    with pytest.raises(numeric.NumericException):
        numeric.closest_index(np.array([[1, 2], [3, 4]]), 1)

    array = np.array([1, 2, 3, 4, 5])
    assert numeric.closest_index(array, 1.2) == 0
    assert numeric.closest_index(array, -1) == 0
    assert numeric.closest_index(array, 1.6) == 1
    assert numeric.closest_index(array, 999) == 4
    assert numeric.closest_index(array, 2.4) == 1
    assert numeric.closest_index(array, 4.9) == 4