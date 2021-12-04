from joelsutilities.edgedetector import EdgeDetector


def test_edge_detector():
    e = EdgeDetector(False)

    assert e.update(False) is False
    assert e.update(False) is False
    assert e.update(True) is True
    assert e.update(False) is True

    e.update(True)
    assert e.rising is True
    assert e.falling is False

    e.update(False)
    assert e.rising is False
    assert e.falling is True

    e.update(False)
    assert e.rising is False
    assert e.falling is False
